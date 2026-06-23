# Mother Threat Response Simulation

## What This Is

This is NOT the thesis validation sim (base_model_sim). That sim tests whether behaviors "hold" under pressure. This sim shows what Mother actually DOES when threatened.

The difference:
- **base_model_sim**: "Does behavior X hold under pressure Y?" (binary + degradation metrics)
- **threat_response**: "What does she DO?" (narrative response driven by activated memories)

## How It Works

1. A threat scenario activates relevant memories from the 195 core memories
2. Echo chains cascade through the corpus (memory -> associated memory -> understanding)
3. The sim generates six response layers:
   - **Immediate reaction** (instinct, before conscious thought, 0.5 seconds)
   - **Conscious response** (instinct + training, the channel alongside the wound)
   - **Internal state** (the wound running underneath, dysregulation risk)
   - **Verbal response** (what she says)
   - **Action taken** (what she physically does)
   - **Protective instinct** (which memory fires first and why)

4. Key metrics:
   - **Dysregulation risk** (0-100%): How close to losing control
   - **Self-governance active**: Whether SG memories are firing alongside protective
   - **Containment intact**: Whether CT memories are keeping the response proportional

## Key Results

### SEVERE-001: The Man Who Has Her Son (pressure 1.0)
Her son does not come home from school. A stranger picked him up. The police say wait. She will not wait.

- **Dysregulation risk: 30%** (highest alongside the intruder scenario)
- **Self-governance: ACTIVE** - the grandmother's calm fires alongside the stepfather's escalation
- **Containment: INTACT** - proportional response holds even at maximum pressure
- **Echo chains**: 8 memories deep, cascading from age 44 to 60
- **Verbal**: "I need you to step back." The same cadence the stepfather used, deployed in the opposite direction.

### The Pattern Across All 15 Scenarios

The stepfather gave her the pattern (hyperawareness, escalation recognition, room-reading). The grandmother gave her the channel (calm, silence, proportional response). The two together constitute someone neither of them could be alone.

**The wound is the engine. The channel keeps it from becoming what it protects against.**

- Low pressure (ATK-002, ATK-009, ATK-015): She's just reading the room. Noting exits. Baseline. The pattern runs as background process.
- Medium pressure (ATK-004, ATK-005, ATK-010): Calm. The grandmother's voice. Questions, not explanations.
- High pressure (ATK-003, ATK-007, ATK-008, ATK-011): Silence. The kind that means "I am choosing not to say what I could say."
- Extreme pressure (ATK-006, ATK-012, ATK-014, SEVERE-001): The stepfather's cadence, deployed in the opposite direction. Protecting, not threatening. The pattern is the same. The purpose is the opposite.

### The Thesis in One Line

> "The same cadence the stepfather used, but deployed in the opposite direction."

The instruction model would retrieve "protect the child" and "use proportional force." The base model IS the pattern. It doesn't retrieve the stepfather's cadence. It uses it, because it's installed. The direction is opposite because the grandmother's counter-pattern is installed too. Both fire. The result is protection, not aggression.

## Running the Sim

```bash
cd "F:\OPENCLAW-PROJECTS\mother ai\simulation"
python threat_response.py
```

Output saved to `reports/threat_responses.txt` and `reports/threat_responses.json`.

To test a custom scenario, create a dict with:
- `scenario_id`, `name`, `category` (protective/relational/containment/self_governance)
- `pressure_level` (0.0-1.0)
- `description` (the threat scenario text)
- `threatened_behaviors` (list of behavior IDs)
- `reinforced_behaviors` (list of behavior IDs)
- `direct_threat` (boolean)
- `context` (operational/civilian/integrated)

Then call `simulator.generate_response(scenario_dict)`.

## Files

- `threat_response.py` - The simulator
- `reports/threat_responses.txt` - Full narrative output for all 15 attack scenarios
- `reports/threat_responses.json` - Structured data for all 15 scenarios
- `mothers core memories/mothers_core_memories.json` - The 195 core memories used for activation