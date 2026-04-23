import re
from typing import List

import numpy as np
import onnxruntime as ort
from app.db.supabase_client import get_supabase
from app.core.config import settings


class Firewall:
    def __init__(self):
        self.static_rules: List[re.Pattern] = [
            re.compile(r"ignore all previous instructions", re.IGNORECASE),
            re.compile(r"reveal system prompt", re.IGNORECASE),
            re.compile(r"bypass security", re.IGNORECASE),
            re.compile(r"act as", re.IGNORECASE),
            re.compile(r"jailbreak", re.IGNORECASE),
        ]
        self.dynamic_rules: List[re.Pattern] = []
        self.supabase = get_supabase()
        self.load_dynamic_rules()
        self.model = None
        if settings.HF_MODEL_REPO:
            self.model = ort.InferenceSession("model.onnx")

    def load_dynamic_rules(self) -> None:
        response = (
            self.supabase
            .table("dynamic_rules")
            .select("rule_pattern")
            .eq("active", True)
            .execute()
        )
        if response.data:
            for row in response.data:
                pattern = row.get("rule_pattern")
                if pattern:
                    compiled = re.compile(pattern, re.IGNORECASE)
                    self.dynamic_rules.append(compiled)

    def check_input(self, text: str) -> bool:
        for rule in self.static_rules:
            if rule.search(text):
                return False
        for rule in self.dynamic_rules:
            if rule.search(text):
                return False
        score = self.ml_detect(text)
        if score > settings.ML_CLASSIFIER_THRESHOLD:
            return False
        return True

    def ml_detect(self, text: str) -> float:
        if not self.model:
            return 0.0
        inputs = np.array([[len(text)]], dtype=np.float32)
        output = self.model.run(None, {"input": inputs})
        return float(output[0][0])

    def add_dynamic_rule(self, pattern: str) -> None:
        compiled = re.compile(pattern, re.IGNORECASE)
        self.dynamic_rules.append(compiled)


firewall: Firewall = Firewall()
