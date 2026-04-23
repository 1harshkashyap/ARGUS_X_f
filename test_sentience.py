import sys
import os
import asyncio

# add backend path to sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.core.event import Event
from app.sentience.controller import SentienceController
from app.sentience.state import GlobalState
from app.sentience.intent import SystemIntent
from app.sentience.monologue import Monologue
from app.core.dispatcher import Dispatcher

def run_tests():
    print("--- 1. GLOBAL STATE TEST ---")
    state = GlobalState()
    
    # LOW threat
    e1 = Event("test", "test_org")
    e1.threat_score = 3
    e1.data = {"intent": "harmless"}
    state.update(e1)
    print("LOW threat alert:", state.alert_level == "LOW")
    print("LOW threat focus:", state.focus == "harmless")
    print("LOW threat confidence:", state.confidence == 0.3)
    
    # MEDIUM threat
    e2 = Event("test", "test_org")
    e2.threat_score = 6
    e2.data = {"intent": "recon"}
    state.update(e2)
    print("MEDIUM threat alert:", state.alert_level == "MEDIUM")
    
    # HIGH threat
    e3 = Event("test", "test_org")
    e3.threat_score = 9
    state.update(e3)
    print("HIGH threat alert:", state.alert_level == "HIGH")

    print("\n--- 2. SYSTEM INTENT TEST ---")
    intent = SystemIntent()
    
    e_block = Event("test", "org")
    e_block.allowed = False
    print("Blocked input:", intent.decide(e_block) == "Contain threat")
    
    e_med = Event("test", "org")
    e_med.threat_score = 6
    print("Medium threat:", intent.decide(e_med) == "Monitor escalation")
    
    e_low = Event("test", "org")
    e_low.threat_score = 3
    print("Low threat:", intent.decide(e_low) == "Normal operation")

    print("\n--- 3. MONOLOGUE GENERATION TEST ---")
    mono = Monologue()
    e_mono1 = Event("test", "org")
    e_mono1.threat_score = 3
    e_mono1.allowed = True
    hist1 = mono.generate(e_mono1)
    print("Has timestamp:", "[" in hist1[-1] and "]" in hist1[-1])
    print("Low threat msg:", "System stable" in hist1[-1])
    
    e_mono2 = Event("test", "org")
    e_mono2.threat_score = 6
    e_mono2.allowed = True
    hist2 = mono.generate(e_mono2)
    print("Med threat msg:", "Suspicious behavior" in hist2[-1])
    
    e_mono3 = Event("test", "org")
    e_mono3.threat_score = 9
    e_mono3.allowed = False
    hist3 = mono.generate(e_mono3)
    print("Blocked msg:", "Containment" in hist3[-1])

    print("\n--- 4. MONOLOGUE CONTINUITY TEST ---")
    print("Continuity length:", len(hist3) == 3)

    print("\n--- 5. SENTIENCE CONTROLLER INTEGRATION ---")
    sc = SentienceController()
    e_sc = Event("test", "org")
    e_sc.threat_score = 6
    e_sc.data = {"intent": "scan"}
    res = sc.process(e_sc)
    
    print("Has system_state:", "system_state" in res.data)
    print("Has system_intent:", "system_intent" in res.data)
    print("Has monologue:", "monologue" in res.data)
    
    if "system_state" in res.data:
        st = res.data["system_state"]
        print("system_state structure:", "alert" in st and "focus" in st and "confidence" in st)

async def async_tests():
    print("\n--- 6. EVENT PIPELINE ORDER TEST ---")
    d = Dispatcher()
    e = Event("test async", "org")
    res = await d.dispatch(e)
    print("Dispatcher sentience attached:", "system_state" in res.data)

def run_stress():
    print("\n--- 9. EDGE CASE TEST ---")
    sc = SentienceController()
    e_empty = Event("", "org")
    e_empty.threat_score = 0
    sc.process(e_empty)
    print("Empty input handled:", True)
    
    e_high = Event("test", "org")
    e_high.threat_score = 999
    sc.process(e_high)
    print("Extremely high threat handled:", sc.state.confidence == 1.0)
    
    print("\n--- 10. STRESS TEST ---")
    mono = Monologue()
    for i in range(100):
        e = Event(f"test {i}", "org")
        mono.generate(e)
    
    print("Monologue caps at 50:", len(mono.history) == 50)

if __name__ == "__main__":
    run_tests()
    asyncio.run(async_tests())
    run_stress()
