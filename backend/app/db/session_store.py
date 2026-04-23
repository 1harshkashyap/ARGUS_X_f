import time
from typing import Optional, Dict, Any

import redis
from app.core.config import settings


class InMemoryStore:
    def __init__(self):
        self.store: Dict[str, Dict[str, Any]] = {}

    def set(self, key: str, value: Any) -> None:
        self.store[key] = {"value": value, "timestamp": time.time()}

    def get(self, key: str) -> Optional[Any]:
        entry = self.store.get(key)
        if entry is None:
            return None
        if time.time() - entry["timestamp"] > 3600:
            del self.store[key]
            return None
        return entry["value"]


class SessionStore:
    def __init__(self):
        if settings.REDIS_URL:
            self.client = redis.Redis.from_url(settings.REDIS_URL)
            self.use_redis = True
        else:
            self.store = InMemoryStore()
            self.use_redis = False

    def set_session(self, org_id: str, session_id: str, data: Dict[str, Any]) -> None:
        key = f"{org_id}:{session_id}"
        if self.use_redis:
            self.client.set(key, str(data), ex=3600)
        else:
            self.store.set(key, data)

    def get_session(self, org_id: str, session_id: str) -> Optional[Dict[str, Any]]:
        key = f"{org_id}:{session_id}"
        if self.use_redis:
            data = self.client.get(key)
            return eval(data) if data else None
        else:
            return self.store.get(key)
