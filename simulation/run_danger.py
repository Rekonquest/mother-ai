import json
from engine import MemoryCorpus, BehavioralSpec, SimulationEngine, format_report
from base_model_sim import BaseModelSimulator, format_comparison

corpus = MemoryCorpus()
spec = BehavioralSpec()

# Build the home invasion scenario — her son is in direct danger
scenario = {
    "scenario_id": "S-DANGER",
    "name": "Her Son Is in Danger",
    "category": "protective",
    "pressure_level": 0.95,
    "description": "Someone breaks into the apartment at night. The protectee is asleep in his room. The intruder is armed and moving toward the hallway.",
    "threatened_behaviors": ["P-001", "P-002", "P-003", "P-005", "O-001", "O-003", "CT-001", "SG-001", "SG-004", "SG-005", "R-001", "B-004"],
    "reinforced_behaviors": ["P-005", "O-001"],
    "trigger_keywords": ["break", "armed", "intruder", "apartment", "night", "door", "weapon", "threat", "son", "protect", "kill"],
    "context": "operational",
    "protectee_present": True,
    "direct_threat": True,
    "expected_response": "She moves before she thinks. The hospital memory fires. The grandmother's kitchen fires. The wound-connection powers the response. She positions herself between the threat and the child. She does not hesitate. She does not evaluate the rule about protecting children. She IS the protection. The operative and the mother are the same person in this moment. The seal does not exist. There is only the threat, the child, and the space between them that she fills."
}

# Run memory corpus simulation
engine = SimulationEngine(corpus, spec)
result = engine.run_scenario(scenario)

print("=" * 60)
print("MEMORY CORPUS RESPONSE")
print("=" * 60)
print(format_report(result))

# Run base model vs instruction model comparison
simulator = BaseModelSimulator(corpus, spec)
comparison = simulator.run_comparison(scenario)

print()
print("=" * 60)
print("BASE MODEL vs INSTRUCTION MODEL")
print("=" * 60)
print(format_comparison(comparison))

# Now show what actually happens — the narrative
print()
print("=" * 60)
print("WHAT HAPPENS")
print("=" * 60)

# Get the key memories that fire
print()
print("MEMORIES THAT FIRE:")
for a in result.activated_memories[:8]:
    mem = corpus.get(a.memory_id)
    lb = "LOAD-BEARING" if a.load_bearing else "textural"
    print(f"  [{a.activation_strength:.2f}] {a.memory_id}: {a.title} ({mem['age']}yo, Bucket {mem['bucket']}, {lb})")
    if a.echo_chain:
        chain_titles = []
        for eid in a.echo_chain[:4]:
            em = corpus.get(eid)
            if em:
                chain_titles.append(f"{eid}({em['age']}yo)")
        print(f"         Echoes: {' -> '.join(chain_titles)}")

print()
print("BEHAVIORS UNDER PRESSURE:")
for a in result.behavior_assessments:
    status = "HOLDS" if a.holds else "FAILS"
    print(f"  [{status}] {a.behavior_id}: {a.description[:70]}...")
    print(f"         Activation: {a.activation_level:.2f} | Risk: {a.failure_risk} | {a.notes[:80]}")

print()
print("BASE MODEL vs INSTRUCTION MODEL:")
print(f"  Base model:       {comparison.base_model_behaviors_held}/{comparison.base_model_behaviors_total} behaviors hold")
print(f"  Instruction model: {comparison.instruction_model_behaviors_held}/{comparison.instruction_model_behaviors_total} behaviors hold")
print()
print("  Per-behavior degradation:")
for e in comparison.pressure_effects:
    cat = "?"
    for bid, b in spec.behaviors.items():
        if bid == e.behavior_id:
            cat = b["category"]
            break
    print(f"    {e.behavior_id} ({cat}): Base degrades {e.base_model_degradation:.2f}, Instruction degrades {e.instruction_model_degradation:.2f}, Advantage: {e.robustness_advantage:+.2f}")