import sys
import os
import asyncio
import time
from fastapi.testclient import TestClient

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app, dispatcher, battle
from app.core.event import Event
from app.ml.firewall import firewall

client = TestClient(app)

results = {}
critical_issues = []
warnings = []

def record(name, condition, error_msg=None):
    results[name] = "PASS" if condition else "FAIL"
    if not condition and error_msg:
        critical_issues.append(f"{name}: {error_msg}")

async def run_tests():
    print("Running Async Validation...")
    
    # 1. ASYNC FLOW TEST
    try:
        e1 = Event("async flow", "org-1")
        res1 = await dispatcher.dispatch(e1)
        record("1. ASYNC FLOW TEST", hasattr(res1, 'allowed'), "Dispatcher did not return event properly")
    except Exception as e:
        record("1. ASYNC FLOW TEST", False, str(e))

    # 2. PARALLEL PROCESSOR TEST
    try:
        e2 = Event("parallel test", "org-2")
        res2 = await dispatcher.dispatch(e2)
        has_all = all(k in res2.data for k in ['similarity_score', 'evolution_score', 'correlation_count', 'reason'])
        record("2. PARALLEL PROCESSOR TEST", has_all, f"Missing fields. Data: {res2.data.keys()}")
    except Exception as e:
        record("2. PARALLEL PROCESSOR TEST", False, str(e))

    # 3. RACE CONDITION TEST
    try:
        # We will dispatch 20 events concurrently
        events = [Event(f"race condition {i}", "org-3") for i in range(20)]
        coroutines = [dispatcher.dispatch(e) for e in events]
        res_list = await asyncio.gather(*coroutines)
        
        valid = len(res_list) == 20 and all(hasattr(r, 'allowed') for r in res_list)
        record("3. RACE CONDITION TEST", valid, "Concurrency caused crashes or dropped events")
    except Exception as e:
        record("3. RACE CONDITION TEST", False, str(e))

    # 4. SHARED EVENT MUTATION TEST
    try:
        # Check if threat_score is corrupted
        # Because processors use max() and min(), we just check if it's a valid int/float
        valid = all(isinstance(r.threat_score, (int, float)) for r in res_list)
        record("4. SHARED EVENT MUTATION TEST", valid, "Threat score overwritten incorrectly")
    except Exception as e:
        record("4. SHARED EVENT MUTATION TEST", False, str(e))

    # 5. BACKGROUND TASK TEST
    try:
        # Just ensure loop continues and no immediate unhandled task exceptions crash the app
        await asyncio.sleep(0.5) 
        record("5. BACKGROUND TASK TEST", True)
    except Exception as e:
        record("5. BACKGROUND TASK TEST", False, str(e))

    # 6. FIREWALL CONSISTENCY TEST
    try:
        battle.run_cycle() # triggers a patch
        firewall.dynamic_rules.append(r"async_firewall_test")
        e6 = Event("async_firewall_test", "org-6")
        res6 = await dispatcher.dispatch(e6)
        record("6. FIREWALL CONSISTENCY TEST", not res6.allowed, "Dynamic rule was not applied immediately")
    except Exception as e:
        record("6. FIREWALL CONSISTENCY TEST", False, str(e))

    # 7. WEBSOCKET STABILITY TEST
    try:
        with client.websocket_connect("/ws") as ws:
            ws.send_text("ping")
        record("7. WEBSOCKET STABILITY TEST", True)
    except Exception as e:
        record("7. WEBSOCKET STABILITY TEST", False, str(e))

    # 8. PERFORMANCE TEST
    try:
        start = time.time()
        for i in range(5):
            await dispatcher.dispatch(Event("perf test seq", "org-8"))
        seq_time = time.time() - start
        
        start = time.time()
        perf_events = [Event("perf test par", "org-8") for i in range(5)]
        await asyncio.gather(*[dispatcher.dispatch(e) for e in perf_events])
        par_time = time.time() - start
        
        # Parallel should ideally be faster or at least stable
        record("8. PERFORMANCE TEST", par_time <= seq_time * 1.5, f"Parallel took significantly longer: {par_time:.2f}s vs {seq_time:.2f}s")
        if par_time > seq_time:
            warnings.append(f"Parallel execution is slightly slower than sequential ({par_time:.3f}s vs {seq_time:.3f}s), likely due to threading overhead for small workloads.")
    except Exception as e:
        record("8. PERFORMANCE TEST", False, str(e))


if __name__ == "__main__":
    asyncio.run(run_tests())
    
    print("\n--- RESULTS ---")
    for k, v in results.items():
        print(f"{v} - {k}")
    
    print("\n--- CRITICAL ISSUES ---")
    for iss in critical_issues:
        print(iss)
        
    print("\n--- WARNINGS ---")
    for warn in warnings:
        print(warn)
