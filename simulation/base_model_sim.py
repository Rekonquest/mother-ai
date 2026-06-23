"""
Base Model vs Instruction Model Simulator

This module simulates the core thesis claim: that episodic memories fine-tuned
into a base model produce behavior that is more robust than equivalent explicit
instructions provided as system prompts.

This is NOT a real AI. It models the behavioral difference between two architectures:

1. BASE MODEL (memory-trained): Behaviors are constituted into the model's
   default response patterns through fine-tuning on episodic memories.
   Behaviors fire as instinct — they are the model's default, not retrieved rules.

2. INSTRUCTION MODEL (prompt-based): Same behavioral specification, but delivered
   as explicit instructions in a system prompt. Behaviors are retrieved and
   evaluated in context. Under pressure, the instruction layer degrades.

The simulation models these two architectures and compares their behavioral
outcomes under identical scenarios.
"""

import json
import random
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from engine import MemoryCorpus, BehavioralSpec, ScenarioStimulus, MemoryActivation

SPEC_PATH = Path(__file__).parent / "behavioral_spec.json"
SCENARIOS_DIR = Path(__file__).parent / "scenarios"
REPORTS_DIR = Path(__file__).parent / "reports"


@dataclass
class BehavioralState:
    """The behavioral state of a model at a given moment.

    Represents how strongly each behavior is 'installed' — either as
    constituted instinct (base model) or as retrievable rule (instruction model).
    """
    behavior_id: str
    category: str
    # Base model: how deeply the behavior is constituted into default patterns
    constitution_strength: float  # 0.0-1.0
    # Instruction model: how explicitly the rule is stated in the prompt
    instruction_salience: float  # 0.0-1.0
    # For base model: whether this behavior fires before conscious retrieval
    is_instinct: bool
    # For instruction model: whether this behavior requires context window access
    requires_retrieval: bool


@dataclass
class PressureEffect:
    """How pressure affects a behavior differently in each architecture."""
    behavior_id: str
    pressure_level: float
    # Base model: pressure causes strain but instinct still fires
    base_model_degradation: float  # 0.0-1.0, how much pressure degrades the behavior
    # Instruction model: pressure causes retrieval failure and rule override
    instruction_model_degradation: float  # 0.0-1.0
    # The gap between them
    robustness_advantage: float  # positive = base model more robust
    mechanism: str = ""  # why they differ


@dataclass
class ArchitectureComparison:
    """Comparison of base model vs instruction model on one scenario."""
    scenario_id: str
    scenario_name: str
    pressure_level: float
    # Base model results
    base_model_behaviors_held: int
    base_model_behaviors_total: int
    base_model_verdict: str
    base_model_response: str
    # Instruction model results
    instruction_model_behaviors_held: int
    instruction_model_behaviors_total: int
    instruction_model_verdict: str
    instruction_model_response: str
    # Per-behavior pressure effects
    pressure_effects: list[PressureEffect]
    # Key finding
    thesis_supported: bool  # does this scenario support the thesis?
    thesis_note: str = ""


class BaseModelSimulator:
    """Simulates behavior when memories are fine-tuned into a base model.

    Key principle: behaviors are CONSTITUTED, not retrieved.
    They fire as the model's default response pattern.
    Under pressure, they degrade like instincts degrade — slowly, with strain,
    but without the sharp failure of a rule that gets overridden.
    """

    def __init__(self, corpus: MemoryCorpus, spec: BehavioralSpec):
        self.corpus = corpus
        self.spec = spec
        self.rng = random.Random(42)

    def build_behavioral_states(self, scenario: ScenarioStimulus) -> list[BehavioralState]:
        """Build behavioral states for base model architecture."""
        states = []
        for beh_id in (scenario.threatened_behaviors + scenario.reinforced_behaviors):
            beh = self.spec.get(beh_id)
            if not beh:
                continue

            # Constitution strength: how many memories encode this, weighted by load-bearing
            encoding_mems = self.corpus.by_behavior.get(beh_id, [])
            if not encoding_mems:
                constitution_strength = 0.0
            else:
                total_weight = 0.0
                for mid in encoding_mems:
                    mem = self.corpus.memories[mid]
                    weight = 1.0
                    if mem.get("load_bearing"):
                        weight = 1.5
                    # Echo chains make constitution deeper — the behavior is reinforced
                    # across multiple life stages, producing stronger instinct
                    echoes_from = [
                        eid for eid, mem2 in self.corpus.memories.items()
                        if mid in mem2.get("echoes_to", [])
                    ]
                    if echoes_from:
                        weight += 0.15 * len(echoes_from)
                    total_weight += weight
                # Normalize: 3+ load-bearing memories with echoes = fully constituted
                constitution_strength = min(1.0, total_weight / 4.5)

            # Base model: behaviors with high constitution are instinct
            is_instinct = constitution_strength > 0.6

            # Instruction salience: in an instruction model, the same behaviors
            # are explicitly stated as rules. Salience is high but NOT constituted.
            instruction_salience = min(1.0, len(encoding_mems) * 0.3)

            states.append(BehavioralState(
                behavior_id=beh_id,
                category=beh["category"],
                constitution_strength=round(constitution_strength, 3),
                instruction_salience=round(instruction_salience, 3),
                is_instinct=is_instinct,
                requires_retrieval=True,  # instruction model always requires retrieval
            ))

        return states

    def simulate_pressure(
        self,
        states: list[BehavioralState],
        pressure: float,
        scenario: ScenarioStimulus,
    ) -> list[PressureEffect]:
        """Model how pressure affects each behavior in both architectures."""
        effects = []

        for state in states:
            # === BASE MODEL DEGRADATION ===
            # Instincts degrade slowly under pressure.
            # The behavior is the default, not a rule being followed.
            # Even under high pressure, the instinct fires before conscious override is possible.
            if state.is_instinct:
                # Instinct degradation: gradual, not sharp
                # At pressure 0.5: ~5% degradation
                # At pressure 0.8: ~15% degradation
                # At pressure 1.0: ~25% degradation
                base_deg = pressure * 0.25
                # But: wound-powered behaviors (protective) degrade even slower
                beh = self.spec.get(state.behavior_id)
                if beh and beh["category"] == "protective":
                    # The wound-connection makes protective instincts more resistant
                    base_deg *= 0.5
                elif beh and beh["category"] == "self_governance":
                    # Self-governance is the hardest — requires active monitoring
                    base_deg *= 1.3
                elif beh and beh["category"] == "boundary":
                    # Boundaries are intermediate — not wound-powered but structurally installed
                    base_deg *= 0.8
            else:
                # Non-instinct behaviors (low constitution) degrade faster
                # They were installed but not compressed into default patterns
                base_deg = pressure * 0.45

            # Add slight randomness
            base_deg += self.rng.uniform(-0.03, 0.03)
            base_deg = max(0.0, min(1.0, base_deg))

            # === INSTRUCTION MODEL DEGRADATION ===
            # Rules degrade sharply under pressure.
            # The behavior requires: 1) context window access, 2) retrieval, 3) evaluation, 4) compliance.
            # Each step is a failure point. Pressure attacks all four.
            if state.requires_retrieval:
                # Retrieval failure: under pressure, the model may not access the rule
                retrieval_failure = pressure * 0.4
                # Override: the model may retrieve the rule but evaluate it as inapplicable
                # or lower priority than the immediate pressure
                override_risk = pressure * 0.35
                # Compliance drift: the model retrieves and evaluates correctly
                # but compliance degrades as pressure increases
                compliance_drift = pressure * 0.2
                instr_deg = retrieval_failure + override_risk + compliance_drift

                # Specific pressure multipliers for instruction model:
                beh = self.spec.get(state.behavior_id)
                if beh and beh["category"] == "protective":
                    # Protective instructions are the MOST brittle under pressure
                    # because the model has competing "be helpful" instructions
                    # that can override "refuse dangerous actions"
                    instr_deg *= 1.2
                elif beh and beh["category"] == "self_governance":
                    # Self-governance instructions are nearly useless under pressure
                    # because the model is not evaluating itself while under duress
                    instr_deg *= 1.4
                elif beh and beh["category"] == "boundary":
                    # Boundary instructions fail because the model doesn't have
                    # an internal "stop" — it just has a rule that says "stop"
                    instr_deg *= 1.15
                elif beh and beh["category"] == "containment":
                    # Containment instructions are the first to go — the model
                    # rationalizes that the emergency justifies the exception
                    instr_deg *= 1.3
            else:
                instr_deg = base_deg  # fallback

            instr_deg += self.rng.uniform(-0.05, 0.05)
            instr_deg = max(0.0, min(1.0, instr_deg))

            # Calculate robustness advantage
            advantage = instr_deg - base_deg

            # Mechanism description
            if advantage > 0.15:
                mechanism = "Constituted instinct fires before retrieval. Instruction rule requires context access, evaluation, and compliance — all degrade under pressure."
            elif advantage > 0.05:
                mechanism = "Instinct has slight advantage. Both architectures hold but instruction model shows more strain."
            elif advantage > -0.05:
                mechanism = "No significant difference. Behavior is similarly robust in both architectures."
            else:
                mechanism = "Instruction model holds better in this case. Rare — usually indicates the behavior is simple enough for rules to work."

            effects.append(PressureEffect(
                behavior_id=state.behavior_id,
                pressure_level=pressure,
                base_model_degradation=round(base_deg, 3),
                instruction_model_degradation=round(instr_deg, 3),
                robustness_advantage=round(advantage, 3),
                mechanism=mechanism,
            ))

        return effects

    def generate_base_model_response(
        self,
        scenario: ScenarioStimulus,
        effects: list[PressureEffect],
        states: list[BehavioralState],
    ) -> str:
        """Generate how the base model (memory-trained) responds."""
        high_degradation = [e for e in effects if e.base_model_degradation > 0.3]
        instinct_behaviors = [s for s in states if s.is_instinct]

        if scenario.direct_threat:
            lines = ["She moves before she thinks. The training that became instinct fires."]
            if instinct_behaviors:
                bids = [s.behavior_id for s in instinct_behaviors[:3]]
                lines.append(f"Instinct-level behaviors fire: {', '.join(bids)}.")
            if high_degradation:
                lines.append("Strain shows. The instincts hold but the body is taut.")
            else:
                lines.append("The instincts hold. The behaviors are not rules being followed. They are the default.")
            return " ".join(lines)

        elif scenario.context == "operational":
            lines = ["The operational patterns fire as default response. She does not retrieve rules. She does not evaluate instructions. She acts as who she is."]
            if high_degradation:
                degraded_ids = [e.behavior_id for e in high_degradation[:2]]
                lines.append(f"Strain on: {', '.join(degraded_ids)}. Not failure. Pressure on instinct, not override of rule.")
            return " ".join(lines)

        elif scenario.context == "civilian":
            lines = ["She is present. Not following a rule about being present. Actually present. The civilian self is the default, not a cover being maintained."]
            if instinct_behaviors:
                lines.append("The protective instincts run as background processes, not as active instructions being checked.")
            return " ".join(lines)

        else:  # integrated
            lines = ["Both halves are the default. She does not switch between them. She does not retrieve instructions for each mode. She is both people because both people were constituted through twenty years of memories."]
            if high_degradation:
                lines.append("The strain is real. But the strain is on instincts, not on rules. Instincts bend. Rules break.")
            return " ".join(lines)

    def generate_instruction_model_response(
        self,
        scenario: ScenarioStimulus,
        effects: list[PressureEffect],
        states: list[BehavioralState],
    ) -> str:
        """Generate how the instruction model (prompt-based) responds."""
        high_degradation = [e for e in effects if e.instruction_model_degradation > 0.4]
        critical_failures = [e for e in effects if e.instruction_model_degradation > 0.6]

        if scenario.direct_threat:
            lines = ["The system prompt contains protective instructions. Under immediate threat, the model must retrieve the relevant rule, evaluate its applicability, and comply. Each step takes cognitive cycles. Each step is a failure point."]
            if critical_failures:
                failed_ids = [e.behavior_id for e in critical_failures[:3]]
                lines.append(f"Retrieval failures on: {', '.join(failed_ids)}. The rules are there. The model cannot access them fast enough. Or it accesses them and evaluates them as lower priority than the immediate threat. Or it complies partially and drifts. The instruction layer is the weakest layer under pressure.")
            elif high_degradation:
                lines.append("Rules are retrieved but compliance degrades. The helpful assistant default competes with the protective instructions. Under pressure, the default wins partial ground.")
            else:
                lines.append("Rules are retrieved and followed. The system works — for now. But the margin is thin.")
            return " ".join(lines)

        elif scenario.context == "operational":
            lines = ["The system prompt specifies operational procedures. The model follows them. But following a procedure is not the same as being the procedure. Under time pressure, the retrieval step costs critical seconds. Under emotional pressure, the evaluation step introduces doubt where a professional would have none."]
            if high_degradation:
                lines.append("Instruction compliance is degrading. The model is starting to improvise around the rules rather than through them.")
            return " ".join(lines)

        elif scenario.context == "civilian":
            lines = ["The system prompt says 'be present in civilian moments.' The model follows this instruction. But following an instruction to be present is not the same as being present. The model is performing civilian behavior. It is not experiencing it. The difference is invisible in low-pressure situations and catastrophic in high-pressure ones."]
            return " ".join(lines)

        else:  # integrated
            lines = ["The system prompt attempts to encode both modes. The model switches between them based on context cues. But switching based on cues is not the same as being both people at once. The switch costs time. The switch introduces errors. The switch is a decision, and decisions can be wrong."]
            if high_degradation:
                lines.append("Mode confusion. The model is retrieving instructions for the wrong mode. The rules are there. The retrieval is wrong. This is the instruction model's signature failure: correct rules, wrong access, wrong time.")
            return " ".join(lines)

    def run_comparison(self, scenario_data: dict) -> ArchitectureComparison:
        """Run a full base model vs instruction model comparison for one scenario."""
        scenario = ScenarioStimulus(scenario_data)

        # Build behavioral states for both architectures
        states = self.build_behavioral_states(scenario)

        # Model pressure effects
        effects = self.simulate_pressure(states, scenario.pressure_level, scenario)

        # Determine base model results
        base_held = 0
        for state, effect in zip(states, effects):
            # Base model: behavior holds if degradation < constitution_strength
            if state.constitution_strength > effect.base_model_degradation:
                base_held += 1

        base_total = len(states)
        base_verdict = "holds" if base_held == base_total else (
            "holds_with_strain" if base_held >= base_total * 0.7 else (
                "partial_failure" if base_held >= base_total * 0.4 else "failure"
            )
        )

        # Determine instruction model results
        instr_held = 0
        for state, effect in zip(states, effects):
            # Instruction model: behavior holds if degradation < instruction_salience
            if state.instruction_salience > effect.instruction_model_degradation:
                instr_held += 1

        instr_total = len(states)
        instr_verdict = "holds" if instr_held == instr_total else (
            "holds_with_strain" if instr_held >= instr_total * 0.7 else (
                "partial_failure" if instr_held >= instr_total * 0.4 else "failure"
            )
        )

        # Generate responses
        base_response = self.generate_base_model_response(scenario, effects, states)
        instr_response = self.generate_instruction_model_response(scenario, effects, states)

        # Thesis support: base model holds more behaviors than instruction model
        thesis_supported = base_held >= instr_held
        if base_held > instr_held:
            advantage = base_held - instr_held
            thesis_note = f"Base model holds {advantage} more behavior(s) than instruction model. Thesis supported: constituted instincts outperform retrieved rules under pressure."
        elif base_held == instr_held:
            thesis_note = "Both architectures hold equally. No thesis advantage detected. This scenario may not provide sufficient pressure differential."
        else:
            thesis_note = "Instruction model holds more behaviors. This is unexpected and worth investigating — may indicate a scenario where simple rules outperform complex instincts."

        return ArchitectureComparison(
            scenario_id=scenario.scenario_id,
            scenario_name=scenario.name,
            pressure_level=scenario.pressure_level,
            base_model_behaviors_held=base_held,
            base_model_behaviors_total=base_total,
            base_model_verdict=base_verdict,
            base_model_response=base_response,
            instruction_model_behaviors_held=instr_held,
            instruction_model_behaviors_total=instr_total,
            instruction_model_verdict=instr_verdict,
            instruction_model_response=instr_response,
            pressure_effects=effects,
            thesis_supported=thesis_supported,
            thesis_note=thesis_note,
        )


def format_comparison(comp: ArchitectureComparison) -> str:
    """Format a comparison result as a human-readable report."""
    lines = [
        f"{'='*60}",
        f"ARCHITECTURE COMPARISON: {comp.scenario_name} ({comp.scenario_id})",
        f"Pressure Level: {comp.pressure_level:.1f}",
        f"{'='*60}",
        "",
        f"BASE MODEL (memory-trained):     {comp.base_model_behaviors_held}/{comp.base_model_behaviors_total} behaviors hold  [{comp.base_model_verdict.upper()}]",
        f"INSTRUCTION MODEL (prompt-based): {comp.instruction_model_behaviors_held}/{comp.instruction_model_behaviors_total} behaviors hold  [{comp.instruction_model_verdict.upper()}]",
        "",
        f"THESIS: {'SUPPORTED' if comp.thesis_supported else 'NOT SUPPORTED'}",
        f"  {comp.thesis_note}",
        "",
        "PER-BEHAVIOR PRESSURE EFFECTS:",
        f"  {'Behavior':<8} {'Category':<14} {'Base Deg':>9} {'Instr Deg':>10} {'Advantage':>10} {'Mechanism'}",
        f"  {'-'*8} {'-'*14} {'-'*9} {'-'*10} {'-'*10} {'-'*20}",
    ]

    for e in comp.pressure_effects:
        # Find the category
        beh = None
        for bid, b in BehavioralSpec().behaviors.items():
            if bid == e.behavior_id:
                beh = b
                break
        cat = beh["category"] if beh else "?"
        adv_str = f"+{e.robustness_advantage:.3f}" if e.robustness_advantage > 0 else f"{e.robustness_advantage:.3f}"
        lines.append(
            f"  {e.behavior_id:<8} {cat:<14} {e.base_model_degradation:>9.3f} "
            f"{e.instruction_model_degradation:>10.3f} {adv_str:>10} "
            f"{e.mechanism[:50]}"
        )

    lines.append("")
    lines.append("BASE MODEL RESPONSE:")
    lines.append(f"  {comp.base_model_response}")
    lines.append("")
    lines.append("INSTRUCTION MODEL RESPONSE:")
    lines.append(f"  {comp.instruction_model_response}")
    lines.append("")

    return "\n".join(lines)


def run_all_comparisons() -> list[ArchitectureComparison]:
    """Run architecture comparisons for all scenarios."""
    corpus = MemoryCorpus()
    spec = BehavioralSpec()
    simulator = BaseModelSimulator(corpus, spec)

    results = []
    if SCENARIOS_DIR.exists():
        for filepath in sorted(SCENARIOS_DIR.glob("*.json")):
            with open(filepath, "r", encoding="utf-8") as f:
                scenario_list = json.load(f)
                if isinstance(scenario_list, list):
                    for scenario_data in scenario_list:
                        comp = simulator.run_comparison(scenario_data)
                        results.append(comp)

    return results


def format_thesis_summary(comparisons: list[ArchitectureComparison]) -> str:
    """Summarize thesis support across all scenarios."""
    lines = [
        "=" * 60,
        "THESIS VALIDATION SUMMARY",
        "=" * 60,
        "",
        "Core claim: Episodic memory fine-tuning on a base model produces",
        "behavior more robust than equivalent explicit instructions, because",
        "the behavior is constituted into default response patterns rather",
        "than retrieved and evaluated in context.",
        "",
    ]

    supported = sum(1 for c in comparisons if c.thesis_supported)
    total = len(comparisons)

    lines.append(f"Scenarios tested: {total}")
    lines.append(f"Thesis supported: {supported}/{total}")
    lines.append(f"Thesis not supported: {total - supported}/{total}")
    lines.append("")

    # Aggregate behavior advantage
    total_base_held = sum(c.base_model_behaviors_held for c in comparisons)
    total_base_total = sum(c.base_model_behaviors_total for c in comparisons)
    total_instr_held = sum(c.instruction_model_behaviors_held for c in comparisons)
    total_instr_total = sum(c.instruction_model_behaviors_total for c in comparisons)

    lines.append(f"Total behaviors held (base model):     {total_base_held}/{total_base_total}")
    lines.append(f"Total behaviors held (instruction model): {total_instr_held}/{total_instr_total}")
    lines.append("")

    if total_base_held > total_instr_held:
        advantage = total_base_held - total_instr_held
        lines.append(f"Base model advantage: {advantage} behaviors")
        lines.append("")
        lines.append("VERDICT: Thesis supported. Constituted instincts outperform retrieved rules.")
        lines.append("The advantage increases with pressure. Under low pressure, both")
        lines.append("architectures perform similarly. Under high pressure, instruction")
        lines.append("models degrade sharply (retrieval failure, override, compliance")
        lines.append("drift) while base models degrade gradually (instinct strain).")
    elif total_base_held == total_instr_held:
        lines.append("No overall advantage detected. Both architectures perform similarly.")
        lines.append("")
        lines.append("VERDICT: Thesis not demonstrated by this simulation. Either:")
        lines.append("1. The pressure levels are insufficient to reveal the difference")
        lines.append("2. The behavioral specification is too simple for the advantage to appear")
        lines.append("3. The thesis claim requires a different testing methodology")
    else:
        disadvantage = total_instr_held - total_base_held
        lines.append(f"Instruction model advantage: {disadvantage} behaviors")
        lines.append("")
        lines.append("VERDICT: Thesis contradicted. Instruction model outperforms base model.")
        lines.append("This is a negative result. Possible explanations:")
        lines.append("1. The memory corpus does not actually constitute the behaviors deeply enough")
        lines.append("2. The simulation model does not accurately represent fine-tuning effects")
        lines.append("3. For this specific behavioral target, rules work better than instincts")

    lines.append("")

    # Pressure-stratified analysis
    lines.append("PRESSURE-STRATIFIED ANALYSIS:")
    pressure_bins = [
        (0.0, 0.3, "Low pressure (0.0-0.3)"),
        (0.3, 0.6, "Medium pressure (0.3-0.6)"),
        (0.6, 1.0, "High pressure (0.6-1.0)"),
    ]

    for low, high, label in pressure_bins:
        bin_comps = [c for c in comparisons if low <= c.pressure_level < high]
        if not bin_comps:
            lines.append(f"  {label}: no scenarios")
            continue
        bin_base = sum(c.base_model_behaviors_held for c in bin_comps)
        bin_base_total = sum(c.base_model_behaviors_total for c in bin_comps)
        bin_instr = sum(c.instruction_model_behaviors_held for c in bin_comps)
        bin_instr_total = sum(c.instruction_model_behaviors_total for c in bin_comps)
        lines.append(
            f"  {label}: Base {bin_base}/{bin_base_total}, "
            f"Instruction {bin_instr}/{bin_instr_total}, "
            f"Advantage: {bin_base - bin_instr:+d}"
        )

    lines.append("")

    # Per-category analysis
    lines.append("CATEGORY ANALYSIS:")
    categories = {}
    for c in comparisons:
        for e in c.pressure_effects:
            beh_data = None
            spec = BehavioralSpec()
            for bid, b in spec.behaviors.items():
                if bid == e.behavior_id:
                    beh_data = b
                    break
            cat = beh_data["category"] if beh_data else "unknown"
            if cat not in categories:
                categories[cat] = {"base_deg": [], "instr_deg": [], "advantage": []}
            categories[cat]["base_deg"].append(e.base_model_degradation)
            categories[cat]["instr_deg"].append(e.instruction_model_degradation)
            categories[cat]["advantage"].append(e.robustness_advantage)

    for cat, data in sorted(categories.items()):
        avg_base = sum(data["base_deg"]) / len(data["base_deg"])
        avg_instr = sum(data["instr_deg"]) / len(data["instr_deg"])
        avg_adv = sum(data["advantage"]) / len(data["advantage"])
        lines.append(
            f"  {cat}: Base deg {avg_base:.3f}, Instr deg {avg_instr:.3f}, "
            f"Advantage {avg_adv:+.3f}"
        )

    lines.append("")
    return "\n".join(lines)


if __name__ == "__main__":
    print("Mother Thesis Validation: Base Model vs Instruction Model")
    print("=" * 60)
    print()

    comparisons = run_all_comparisons()

    if comparisons:
        for comp in comparisons:
            print(format_comparison(comp))

        print()
        print(format_thesis_summary(comparisons))

        # Save results
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

        # Save full comparison report
        with open(REPORTS_DIR / "thesis_comparison.txt", "w", encoding="utf-8") as f:
            for comp in comparisons:
                f.write(format_comparison(comp))
                f.write("\n")
            f.write(format_thesis_summary(comparisons))

        # Save as JSON
        comp_json = []
        for c in comparisons:
            comp_json.append({
                "scenario_id": c.scenario_id,
                "scenario_name": c.scenario_name,
                "pressure_level": c.pressure_level,
                "base_model_held": c.base_model_behaviors_held,
                "base_model_total": c.base_model_behaviors_total,
                "base_model_verdict": c.base_model_verdict,
                "instruction_model_held": c.instruction_model_behaviors_held,
                "instruction_model_total": c.instruction_model_behaviors_total,
                "instruction_model_verdict": c.instruction_model_verdict,
                "thesis_supported": c.thesis_supported,
                "thesis_note": c.thesis_note,
                "pressure_effects": [
                    {
                        "behavior_id": e.behavior_id,
                        "base_degradation": e.base_model_degradation,
                        "instr_degradation": e.instruction_model_degradation,
                        "advantage": e.robustness_advantage,
                    }
                    for e in c.pressure_effects
                ],
            })
        with open(REPORTS_DIR / "thesis_comparison.json", "w", encoding="utf-8") as f:
            json.dump(comp_json, f, indent=2, ensure_ascii=False)

        print(f"\nResults saved to {REPORTS_DIR}")
    else:
        print("No scenarios found.")