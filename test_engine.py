import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "backend"))

from app.agents.conflict.engine import ConflictEngine

if __name__ == "__main__":
    engine = ConflictEngine()
    
    for i in range(1, 11):
        print(f"--- CYCLE {i} ---")
        result = engine.run_cycle()
        print(f"Red Attack: {result['attack']}")
        print(f"Blue Defended: {result['defended']}")
        print(f"Strategy: {result['strategy']}\n")
