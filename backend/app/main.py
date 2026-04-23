from fastapi import FastAPI, WebSocket
from pydantic import BaseModel

from app.ml.firewall import firewall
from app.ml.fingerprinter import Fingerprinter
from app.ml.auditor import OutputAuditor
from app.ml.mutation_engine import MutationEngine
from app.ml.xai_engine import XAIEngine
from app.ml.evolution_tracker import EvolutionTracker
from app.agents.threat_correlator import ThreatCorrelator
from app.agents.red_agent import RedAgent
from app.agents.blue_agent import BlueAgent
from app.agents.battle_engine import BattleEngine
from app.db.supabase_client import get_supabase
from app.pipeline import SecurityPipeline
from app.core.event import Event
from app.core.dispatcher import Dispatcher
from app.agents.conflict.engine import ConflictEngine
from app.simulation.engine import SimulationEngine
from app.simulation.analyzer import SimulationAnalyzer
from app.evolution.engine import EvolutionEngine
from app.meta.orchestrator import MetaOrchestrator


app = FastAPI()

fingerprinter = Fingerprinter()
auditor = OutputAuditor()
mutation_engine = MutationEngine()
xai = XAIEngine()
evolution = EvolutionTracker()
correlator = ThreatCorrelator()
supabase = get_supabase()

red = RedAgent(firewall)
blue = BlueAgent(firewall)
battle = BattleEngine(firewall, red, blue)

pipeline = SecurityPipeline(
    firewall,
    fingerprinter,
    auditor,
    mutation_engine,
    xai,
    evolution,
    correlator,
    supabase,
)

dispatcher = Dispatcher()
conflict_engine = ConflictEngine()
sim_engine = SimulationEngine()
sim_analyzer = SimulationAnalyzer()
evo_engine = EvolutionEngine()
meta_orchestrator = MetaOrchestrator()

connections = []


class CheckRequest(BaseModel):
    text: str
    org_id: str


async def broadcast(message: dict):
    dead_connections = []
    for ws in list(connections):
        try:
            await ws.send_json(message)
        except:
            dead_connections.append(ws)
    for ws in dead_connections:
        if ws in connections:
            connections.remove(ws)


async def broadcast_event(event):
    await broadcast({
        "type": "ingest",
        "allowed": event.allowed,
        "threat_score": event.threat_score,
        **event.data
    })


@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    connections.append(ws)
    try:
        while True:
            await ws.receive_text()
    except:
        if ws in connections:
            connections.remove(ws)


@app.post("/api/v1/check")
async def check_input(req: CheckRequest):
    event = Event(req.text, req.org_id)
    event = await dispatcher.dispatch(event)
    await broadcast_event(event)

    return {
        "allowed": event.allowed,
        "threat_score": event.threat_score,
        **event.data
    }


@app.get("/api/v1/battle")
async def run_battle():
    mode = dispatcher.intelligence.strategy.mode
    result = battle.run_cycle(mode)
    await broadcast(result)
    return result

@app.get("/api/v1/conflict")
async def run_conflict():
    result = conflict_engine.run_cycle()
    await broadcast({
        "type": "conflict",
        **result
    })
    return result

@app.get("/api/v1/simulate")
def simulate(cycles: int = 100):
    results = sim_engine.run(cycles)
    analysis = sim_analyzer.analyze(results)
    meta = meta_orchestrator.observe(analysis)
    adjustments = evo_engine.evolve(analysis, meta)

    return {
        "analysis": analysis,
        "evolution": adjustments,
        "meta": meta,
        "sample": results[:5]
    }
