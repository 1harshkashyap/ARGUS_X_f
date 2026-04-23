import asyncio

class EventBus:
    def __init__(self):
        self.critical = []
        self.parallel = []
        self.background = []
        self.tasks = []

    def register(self, processor, mode="critical"):
        if mode == "critical":
            self.critical.append(processor)
        elif mode == "parallel":
            self.parallel.append(processor)
        else:
            self.background.append(processor)

    async def process(self, event):
        # 1. Critical processors (sequential)
        for p in self.critical:
            p.handle(event)

        # 2. Parallel processors
        results = await asyncio.gather(*[
            asyncio.to_thread(p.handle, event)
            for p in self.parallel
        ])

        # Merge results safely
        for r in results:
            if not r:
                continue

            for key, value in r.items():
                if key == "threat_score":
                    event.threat_score = max(event.threat_score, value)
                elif key == "threat_score_add":
                    event.threat_score = min(10, event.threat_score + value)
                elif key == "allowed":
                    if not value:
                        event.allowed = False
                else:
                    event.data[key] = value

        # 3. Background processors (fire and forget)
        for p in self.background:
            task = asyncio.create_task(asyncio.to_thread(p.handle, event))
            self.tasks.append(task)

        if len(self.tasks) > 100:
            self.tasks = [t for t in self.tasks if not t.done()]

        return event
