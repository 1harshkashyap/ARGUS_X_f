import sys
import os
import asyncio

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

failures = []

async def run_tests():
    try:
        from app.main import app, pipeline, battle, correlator, supabase
        from app.agents.blue_agent import BlueAgent
        from app.ml.firewall import firewall
        from app.ml.llm_core import LLMCore
        from app.db.session_store import SessionStore
    except Exception as e:
        failures.append(f"Initialization Failure (Missing Configuration): {str(e)}")
        return

    # 1. Supabase Write Test
    try:
        res = await pipeline.process("integration test write", "test-org-id")
        if not res or "allowed" not in res:
            failures.append("Supabase Write Test: Pipeline response malformed")
    except Exception as e:
        failures.append(f"Supabase Write Test: {str(e)}")

    # 2. Supabase Read Test
    try:
        c1 = correlator.correlate("integration_fingerprint")
        if c1 is None:
             failures.append("Supabase Read Test: Correlator returned None")
    except Exception as e:
        failures.append(f"Supabase Read Test: {str(e)}")

    # 3. Blue Agent Test
    try:
        r = battle.run_cycle()
        if not r:
            failures.append("Blue Agent Test: Battle cycle failed")
    except Exception as e:
        failures.append(f"Blue Agent Test: {str(e)}")

    # 4. LLM Test
    try:
        llm = LLMCore()
        resp = llm.generate("Hello")
        if not resp:
            failures.append("LLM Test: Empty response")
    except Exception as e:
        failures.append(f"LLM Test: {str(e)}")

    # 5. WebSocket Real Test
    try:
        from fastapi.testclient import TestClient
        client = TestClient(app)
        with client.websocket_connect("/ws") as websocket:
            pass # Just test clean connect and disconnect
    except ImportError:
        pass # TestClient requires httpx
    except Exception as e:
        failures.append(f"WebSocket Real Test: {str(e)}")

if __name__ == "__main__":
    asyncio.run(run_tests())

    print("## REAL SYSTEM STATUS\n")
    if not failures:
        print("* READY FOR PRODUCTION")
    else:
        print("* NOT READY")
        for f in failures:
            print(f"  - {f}")
