from typing import Dict, Any
import uuid
import time

class Event:
    def __init__(self, text: str, org_id: str):
        self.id = str(uuid.uuid4())
        self.timestamp = time.time()
        
        self.text = text
        self.org_id = org_id
        
        self.data: Dict[str, Any] = {}
        
        self.allowed = True
        self.threat_score = 0
