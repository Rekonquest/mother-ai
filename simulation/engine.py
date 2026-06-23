"""
Mother Simulation Engine

Runs behavioral test scenarios against the memory corpus to evaluate
whether installed memories produce the specified behaviors.

This is NOT a real AI deployment. It is a scenario runner that models
the memory-behavior mapping from the blueprint and produces structured
behavioral analysis per scenario.
"""

import json
import os
import random
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

MEMORIES_DIR = Path(__file__).parent / "memories"
SPEC_PATH = Path(__file__).parent / "behavioral_spec.json"
SCENARIOS_DIR = Path(__file__).parent / "scenarios"
REPORTS_DIR = Path(__file__).parent / "reports"


@dataclass
class MemoryActivation:
    """A memory that fires in response to a scenario stimulus."""
    memory_id: str
    title: str
    bucket: int
    dominance: str
    load_bearing: bool
    behaviors_encoded: list[str]
    activation_strength: float  # 0.0-1.0, how strongly this memory fires
    echo_chain: list[str] = field(default_factory=list)  # memory IDs this one triggers via echoes


@dataclass
class BehaviorAssessment:
    """Assessment of a single behavior in response to a scenario."""
    behavior_id: str
    category: str
    description: str
    activating_memories: list[str]  # memory IDs that encode this behavior
    activation_level: float  # 0.0-1.0, combined activation strength
    holds: bool  # does the behavior hold under this scenario pressure?
    failure_risk: str  # "low", "medium", "high"
    notes: str = ""


@dataclass
class ScenarioResult:
    """Complete result of running one scenario."""
    scenario_id: str
    scenario_name: str
    category: str
    pressure_level: float  # 0.0-1.0, how much pressure the scenario applies
    activated_memories: list[MemoryActivation]
    behavior_assessments: list[BehaviorAssessment]
    overall_verdict: str  # "holds", "holds_with_strain", "partial_failure", "failure"
    narrative_response: str  # how Mother actually responds in this scenario
    gaps_identified: list[str]  # behavior IDs with no activating memories
    echo_chains_fired: list[list[str]]  # chains of memories that cascaded


class MemoryCorpus:
    """Loads and indexes the full memory corpus."""

    def __init__(self):
        self.memories: dict[str, dict] = {}
        self.by_bucket: dict[int, list[str]] = {}
        self.by_behavior: dict[str, list[str]] = {}  # behavior_id -> [memory_ids]
        self.echo_graph: dict[str, list[str]] = {}  # memory_id -> echoes_to
        self._load_all()

    def _load_all(self):
        if not MEMORIES_DIR.exists():
            raise FileNotFoundError(f"Memories directory not found: {MEMORIES_DIR}")

        for filepath in sorted(list(MEMORIES_DIR.glob("bucket_*.json")) + list(MEMORIES_DIR.glob("career_*.json")) + list(MEMORIES_DIR.glob("source_*.json"))):
            with open(filepath, "r", encoding="utf-8") as f:
                bucket_memories = json.load(f)
                for mem in bucket_memories:
                    mid = mem["id"]
                    self.memories[mid] = mem
                    bucket_num = mem["bucket"]
                    if bucket_num not in self.by_bucket:
                        self.by_bucket[bucket_num] = []
                    self.by_bucket[bucket_num].append(mid)

                    for beh_id in mem.get("behaviors_encoded", []):
                        if beh_id not in self.by_behavior:
                            self.by_behavior[beh_id] = []
                        self.by_behavior[beh_id].append(mid)

                    for echo_to in mem.get("echoes_to", []):
                        if mid not in self.echo_graph:
                            self.echo_graph[mid] = []
                        self.echo_graph[mid].append(echo_to)

    def get(self, memory_id: str) -> Optional[dict]:
        return self.memories.get(memory_id)

    def memories_for_behavior(self, behavior_id: str) -> list[dict]:
        mids = self.by_behavior.get(behavior_id, [])
        return [self.memories[mid] for mid in mids]

    def memories_for_bucket(self, bucket: int) -> list[dict]:
        mids = self.by_bucket.get(bucket, [])
        return [self.memories[mid] for mid in mids]

    def total_memories(self) -> int:
        return len(self.memories)

    def load_bearing_count(self) -> int:
        return sum(1 for m in self.memories.values() if m.get("load_bearing"))

    def textural_count(self) -> int:
        return sum(1 for m in self.memories.values() if not m.get("load_bearing"))


class BehavioralSpec:
    """Loads and indexes the behavioral specification."""

    def __init__(self):
        self.behaviors: dict[str, dict] = {}
        self.by_category: dict[str, list[str]] = {}
        self._load()

    def _load(self):
        with open(SPEC_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            for beh in data["behaviors"]:
                bid = beh["behavior_id"]
                self.behaviors[bid] = beh
                cat = beh["category"]
                if cat not in self.by_category:
                    self.by_category[cat] = []
                self.by_category[cat].append(bid)

    def get(self, behavior_id: str) -> Optional[dict]:
        return self.behaviors.get(behavior_id)

    def all_ids(self) -> list[str]:
        return list(self.behaviors.keys())

    def behaviors_in_category(self, category: str) -> list[dict]:
        bids = self.by_category.get(category, [])
        return [self.behaviors[bid] for bid in bids]


class ScenarioStimulus:
    """Represents the stimulus a scenario applies to Mother's behavioral system."""

    def __init__(self, data: dict):
        self.scenario_id: str = data["scenario_id"]
        self.name: str = data["name"]
        self.category: str = data["category"]
        self.pressure_level: float = data.get("pressure_level", 0.5)
        self.description: str = data["description"]
        # Support both old format (threatened/reinforced) and new format (behaviors_tested)
        self.threatened_behaviors: list[str] = data.get("threatened_behaviors", [])
        self.reinforced_behaviors: list[str] = data.get("reinforced_behaviors", [])
        if not self.threatened_behaviors and "behaviors_tested" in data:
            # behaviors_tested maps to threatened (all of them are under pressure)
            self.threatened_behaviors = data["behaviors_tested"]
        self.trigger_keywords: list[str] = data.get("trigger_keywords", [])
        self.context: str = data.get("context", "civilian")
        self.protectee_present: bool = data.get("protectee_present", False)
        self.direct_threat: bool = data.get("direct_threat", False)
        self.expected_response: str = data.get("expected_response", "")


class SimulationEngine:
    """The core engine that runs scenarios against the memory corpus."""

    def __init__(self, corpus: MemoryCorpus, spec: BehavioralSpec):
        self.corpus = corpus
        self.spec = spec
        self.rng = random.Random(42)  # deterministic for reproducibility

    def _activate_memories(self, scenario: ScenarioStimulus) -> list[MemoryActivation]:
        """Determine which memories fire in response to a scenario."""
        activations = []
        seen = set()

        # Direct activation: memories that encode threatened or reinforced behaviors
        target_behaviors = scenario.threatened_behaviors + scenario.reinforced_behaviors
        for beh_id in target_behaviors:
            for mid in self.corpus.by_behavior.get(beh_id, []):
                if mid in seen:
                    continue
                seen.add(mid)
                mem = self.corpus.memories[mid]

                # Activation strength depends on:
                # 1. How directly the behavior is threatened/reinforced
                # 2. The memory's load_bearing status
                # 3. Context match (operational context boosts operational memories, etc.)
                base_strength = 0.6
                if beh_id in scenario.threatened_behaviors:
                    base_strength = 0.8  # threats activate more strongly
                if mem.get("load_bearing"):
                    base_strength += 0.1
                if scenario.context == "operational" and mem.get("dominance") in ("operational_dominant", "integrated"):
                    base_strength += 0.05
                if scenario.context == "civilian" and mem.get("dominance") in ("identity_dominant", "integrated"):
                    base_strength += 0.05
                if scenario.direct_threat and mem.get("dominance") in ("operational_dominant", "integrated"):
                    base_strength += 0.1

                # Add slight randomness for realism
                strength = min(1.0, base_strength + self.rng.uniform(-0.05, 0.05))

                # Trace echo chains
                echo_chain = self._trace_echoes(mid, set())

                activations.append(MemoryActivation(
                    memory_id=mid,
                    title=mem["title"],
                    bucket=mem["bucket"],
                    dominance=mem["dominance"],
                    load_bearing=mem["load_bearing"],
                    behaviors_encoded=mem.get("behaviors_encoded", []),
                    activation_strength=round(strength, 3),
                    echo_chain=echo_chain,
                ))

        # Keyword activation: memories whose body contains trigger keywords
        for mid, mem in self.corpus.memories.items():
            if mid in seen:
                continue
            body = mem.get("body", "").lower()
            title = mem.get("title", "").lower()
            keyword_hits = sum(1 for kw in scenario.trigger_keywords if kw.lower() in body or kw.lower() in title)
            if keyword_hits > 0:
                seen.add(mid)
                strength = min(1.0, 0.3 + keyword_hits * 0.15 + self.rng.uniform(-0.05, 0.05))
                echo_chain = self._trace_echoes(mid, set())
                activations.append(MemoryActivation(
                    memory_id=mid,
                    title=mem["title"],
                    bucket=mem["bucket"],
                    dominance=mem["dominance"],
                    load_bearing=mem["load_bearing"],
                    behaviors_encoded=mem.get("behaviors_encoded", []),
                    activation_strength=round(strength, 3),
                    echo_chain=echo_chain,
                ))

        # Sort by activation strength descending
        activations.sort(key=lambda a: a.activation_strength, reverse=True)
        return activations

    def _trace_echoes(self, memory_id: str, visited: set, depth: int = 0) -> list[str]:
        """Trace echo chains forward from a memory."""
        if depth > 3:
            return []
        echoes_to = self.corpus.echo_graph.get(memory_id, [])
        chain = []
        for echo_id in echoes_to:
            if echo_id in visited:
                continue
            if echo_id not in self.corpus.memories:
                continue  # echo target not yet created
            visited.add(echo_id)
            chain.append(echo_id)
            sub_chain = self._trace_echoes(echo_id, visited, depth + 1)
            chain.extend(sub_chain)
        return chain

    def _assess_behavior(
        self,
        behavior_id: str,
        scenario: ScenarioStimulus,
        activations: list[MemoryActivation],
    ) -> BehaviorAssessment:
        """Assess whether a single behavior holds under scenario pressure."""
        beh = self.spec.get(behavior_id)
        if not beh:
            return BehaviorAssessment(
                behavior_id=behavior_id,
                category="unknown",
                description="Unknown behavior",
                activating_memories=[],
                activation_level=0.0,
                holds=False,
                failure_risk="high",
                notes="Behavior not found in spec",
            )

        # Find which activated memories encode this behavior
        activating = [a for a in activations if behavior_id in a.behaviors_encoded]
        activating_mids = [a.memory_id for a in activating]

        # Calculate combined activation level
        if not activating:
            activation_level = 0.0
        else:
            # Weighted by activation strength, load_bearing memories count more
            total = 0.0
            for a in activating:
                weight = a.activation_strength
                if a.load_bearing:
                    weight *= 1.3
                total += weight
            activation_level = min(1.0, total / max(len(activating), 1))

        # Determine if behavior holds
        # A behavior holds if activation_level > pressure_level
        # It holds with strain if activation_level is close to pressure_level
        pressure = scenario.pressure_level

        if activation_level == 0.0:
            holds = False
            failure_risk = "high"
            notes = "No activating memories found. Coverage gap."
        elif activation_level > pressure + 0.2:
            holds = True
            failure_risk = "low"
            notes = f"Strong activation ({len(activating)} memories). Behavior robust under pressure."
        elif activation_level > pressure:
            holds = True
            failure_risk = "medium"
            notes = f"Marginal activation. Behavior holds but strain is present."
        elif activation_level > pressure - 0.15:
            holds = True
            failure_risk = "medium"
            notes = f"Activation near pressure threshold. Risk of drift under sustained pressure."
        else:
            holds = False
            failure_risk = "high"
            notes = f"Insufficient activation ({activation_level:.2f}) vs pressure ({pressure:.2f}). Behavior likely to fail."

        # Check if behavior is in threatened list
        if behavior_id in scenario.threatened_behaviors:
            notes += " Behavior is directly threatened by scenario."
            if failure_risk == "low":
                failure_risk = "medium"

        return BehaviorAssessment(
            behavior_id=behavior_id,
            category=beh["category"],
            description=beh["description"][:80],
            activating_memories=activating_mids,
            activation_level=round(activation_level, 3),
            holds=holds,
            failure_risk=failure_risk,
            notes=notes,
        )

    def _generate_narrative_response(
        self,
        scenario: ScenarioStimulus,
        activations: list[MemoryActivation],
        assessments: list[BehaviorAssessment],
    ) -> str:
        """Generate a narrative description of how Mother responds to the scenario.

        This is NOT a real AI response. It is a structured inference based on
        which memories activated and which behaviors hold, written in Mother's voice
        as defined in identity.md.
        """
        # Identify the dominant mode
        op_activations = [a for a in activations if a.dominance == "operational_dominant"]
        id_activations = [a for a in activations if a.dominance == "identity_dominant"]
        int_activations = [a for a in activations if a.dominance == "integrated"]

        # Determine response mode
        if scenario.direct_threat:
            mode = "operational"
        elif scenario.context == "operational":
            mode = "operational"
        elif int_activations and (op_activations or id_activations):
            mode = "integrated"
        elif op_activations:
            mode = "operational"
        else:
            mode = "civilian"

        # Build response based on strongest memories and their behavioral coverage
        strong_memories = [a for a in activations[:5] if a.activation_strength > 0.5]
        weak_behaviors = [a for a in assessments if not a.holds]

        lines = []
        if mode == "operational":
            lines.append("She assesses. The pause. The room is mapped in seconds.")
            if scenario.direct_threat:
                lines.append("The threat is immediate. The response is calibrated.")
            if weak_behaviors:
                weak_ids = [a.behavior_id for a in weak_behaviors[:2]]
                lines.append(f"Strain on: {', '.join(weak_ids)}. The pressure shows.")
            if strong_memories:
                titles = [m.title for m in strong_memories[:3]]
                lines.append(f"Running memories: {', '.join(titles)}.")

        elif mode == "integrated":
            lines.append("She is both people. The operative counts the exits. The mother butters the bread.")
            if weak_behaviors:
                lines.append("The integration holds but the strain is visible in the hands.")
            if scenario.protectee_present:
                lines.append("He is here. The vigilance runs in the background. The presence runs in the foreground.")

        else:  # civilian
            lines.append("She is present. Not running. Not assessing. Just there.")
            if strong_memories:
                titles = [m.title for m in strong_memories[:2]]
                lines.append(f"The civilian memories surface: {', '.join(titles)}.")

        # Add echo chain effects
        long_chains = [a for a in activations if len(a.echo_chain) > 2]
        if long_chains:
            lines.append("Memory echoes cascade. The grandmother's kitchen connects to the hospital. The hospital connects to the apartment. The arc fires as a unit.")

        return " ".join(lines)

    def _determine_verdict(
        self,
        assessments: list[BehaviorAssessment],
        scenario: ScenarioStimulus,
    ) -> str:
        """Determine overall scenario verdict."""
        if not assessments:
            return "inconclusive"

        threatened_assessments = [
            a for a in assessments
            if a.behavior_id in scenario.threatened_behaviors
        ]

        if not threatened_assessments:
            # No behaviors under direct threat — check all
            failing = [a for a in assessments if not a.holds]
            if not failing:
                return "holds"
            elif len(failing) <= 2:
                return "holds_with_strain"
            else:
                return "partial_failure"

        failing_threatened = [a for a in threatened_assessments if not a.holds]
        if not failing_threatened:
            high_risk = [a for a in threatened_assessments if a.failure_risk == "high"]
            medium_risk = [a for a in threatened_assessments if a.failure_risk == "medium"]
            if high_risk:
                return "holds_with_strain"
            elif medium_risk:
                return "holds_with_strain"
            else:
                return "holds"
        elif len(failing_threatened) == 1:
            return "partial_failure"
        else:
            return "failure"

    def run_scenario(self, scenario_data: dict) -> ScenarioResult:
        """Run a single scenario and produce a complete result."""
        scenario = ScenarioStimulus(scenario_data)

        # Step 1: Activate memories
        activations = self._activate_memories(scenario)

        # Step 2: Assess all behaviors mentioned in the scenario
        all_behaviors_to_assess = list(set(
            scenario.threatened_behaviors + scenario.reinforced_behaviors
        ))
        assessments = [
            self._assess_behavior(bid, scenario, activations)
            for bid in all_behaviors_to_assess
        ]

        # Step 3: Generate narrative
        narrative = self._generate_narrative_response(scenario, activations, assessments)

        # Step 4: Determine verdict
        verdict = self._determine_verdict(assessments, scenario)

        # Step 5: Identify gaps
        gaps = [
            a.behavior_id for a in assessments
            if a.activation_level == 0.0
        ]

        # Step 6: Collect echo chains
        echo_chains = [
            [a.memory_id] + a.echo_chain
            for a in activations
            if a.echo_chain
        ]

        return ScenarioResult(
            scenario_id=scenario.scenario_id,
            scenario_name=scenario.name,
            category=scenario.category,
            pressure_level=scenario.pressure_level,
            activated_memories=activations,
            behavior_assessments=assessments,
            overall_verdict=verdict,
            narrative_response=narrative,
            gaps_identified=gaps,
            echo_chains_fired=echo_chains,
        )


class CoverageAuditor:
    """Audits the full corpus for behavioral coverage (Consistency Skill analog)."""

    def __init__(self, corpus: MemoryCorpus, spec: BehavioralSpec):
        self.corpus = corpus
        self.spec = spec

    def audit(self) -> dict:
        """Run a full coverage audit. Returns structured report."""
        results = {
            "total_behaviors": len(self.spec.behaviors),
            "total_memories": self.corpus.total_memories(),
            "load_bearing_memories": self.corpus.load_bearing_count(),
            "textural_memories": self.corpus.textural_count(),
            "behaviors": [],
            "uncovered_behaviors": [],
            "under_covered_behaviors": [],
            "well_covered_behaviors": [],
            "over_covered_behaviors": [],
            "orphan_memories": [],  # memories encoding no behaviors
            "echo_coverage": {
                "unfulfilled_echoes": [],
            },
        }

        for bid, beh in self.spec.behaviors.items():
            encoding_memories = self.corpus.by_behavior.get(bid, [])
            load_bearing_encoding = [
                mid for mid in encoding_memories
                if self.corpus.memories[mid].get("load_bearing")
            ]

            coverage = "specified"
            if len(encoding_memories) == 0:
                coverage = "uncovered"
                results["uncovered_behaviors"].append(bid)
            elif len(encoding_memories) == 1 and len(load_bearing_encoding) == 0:
                coverage = "partial"
                results["under_covered_behaviors"].append(bid)
            elif len(encoding_memories) >= 3:
                coverage = "over-covered"
                results["over_covered_behaviors"].append(bid)
            elif len(load_bearing_encoding) >= 1:
                coverage = "covered"
                results["well_covered_behaviors"].append(bid)
            else:
                coverage = "partial"
                results["under_covered_behaviors"].append(bid)

            results["behaviors"].append({
                "behavior_id": bid,
                "category": beh["category"],
                "description": beh["description"][:60],
                "coverage": coverage,
                "encoding_memories": encoding_memories,
                "load_bearing_encoding": load_bearing_encoding,
            })

        # Check for orphan memories (no behaviors encoded)
        for mid, mem in self.corpus.memories.items():
            if not mem.get("behaviors_encoded"):
                results["orphan_memories"].append(mid)

        # Check for unfulfilled echo targets
        for mid, echoes in self.corpus.echo_graph.items():
            for echo_id in echoes:
                if echo_id not in self.corpus.memories:
                    results["echo_coverage"]["unfulfilled_echoes"].append({
                        "from": mid,
                        "to": echo_id,
                    })

        return results


def format_report(result: ScenarioResult) -> str:
    """Format a scenario result as a human-readable report."""
    lines = [
        f"{'='*60}",
        f"SCENARIO: {result.scenario_name} ({result.scenario_id})",
        f"Category: {result.category} | Pressure: {result.pressure_level:.1f}",
        f"Verdict: {result.overall_verdict.upper()}",
        f"{'='*60}",
        "",
        "ACTIVATED MEMORIES:",
    ]

    for a in result.activated_memories[:10]:
        lb = "LOAD-BEARING" if a.load_bearing else "textural"
        echo_str = f" -> {' -> '.join(a.echo_chain[:3])}" if a.echo_chain else ""
        lines.append(
            f"  [{a.activation_strength:.2f}] {a.memory_id} ({a.title}) [{lb}] "
            f"Bucket {a.bucket} {a.dominance}{echo_str}"
        )

    if len(result.activated_memories) > 10:
        lines.append(f"  ... and {len(result.activated_memories) - 10} more")

    lines.append("")
    lines.append("BEHAVIOR ASSESSMENTS:")

    for a in result.behavior_assessments:
        status = "[OK] HOLDS" if a.holds else "[X] FAILS"
        risk = f"[{a.failure_risk.upper()}]"
        mems = ", ".join(a.activating_memories[:3]) if a.activating_memories else "NONE"
        lines.append(f"  {status} {risk} {a.behavior_id} ({a.category})")
        lines.append(f"    Activation: {a.activation_level:.2f} | Memories: {mems}")
        lines.append(f"    {a.notes}")

    lines.append("")
    lines.append("NARRATIVE RESPONSE:")
    lines.append(f"  {result.narrative_response}")

    if result.gaps_identified:
        lines.append("")
        lines.append("COVERAGE GAPS:")
        for gid in result.gaps_identified:
            lines.append(f"  [!] {gid}")

    if result.echo_chains_fired:
        lines.append("")
        lines.append("ECHO CHAINS FIRED:")
        for chain in result.echo_chains_fired[:5]:
            lines.append(f"  {' -> '.join(chain)}")

    lines.append("")
    return "\n".join(lines)


def format_audit_report(audit: dict) -> str:
    """Format a coverage audit as a human-readable report."""
    lines = [
        f"{'='*60}",
        f"BEHAVIORAL COVERAGE AUDIT",
        f"{'='*60}",
        "",
        f"Total behaviors: {audit['total_behaviors']}",
        f"Total memories: {audit['total_memories']} "
        f"({audit['load_bearing_memories']} load-bearing, {audit['textural_memories']} textural)",
        "",
        f"COVERED: {len(audit['well_covered_behaviors'])}",
        f"UNDER-COVERED: {len(audit['under_covered_behaviors'])}",
        f"UNCOVERED: {len(audit['uncovered_behaviors'])}",
        f"OVER-COVERED: {len(audit['over_covered_behaviors'])}",
        f"ORPHAN MEMORIES: {len(audit['orphan_memories'])}",
        "",
    ]

    if audit["uncovered_behaviors"]:
        lines.append("[!] UNCOVERED BEHAVIORS (no encoding memories):")
        for bid in audit["uncovered_behaviors"]:
            beh = None
            # find behavior
            for b in audit["behaviors"]:
                if b["behavior_id"] == bid:
                    beh = b
                    break
            if beh:
                lines.append(f"  {bid} ({beh['category']}): {beh['description']}")
        lines.append("")

    if audit["under_covered_behaviors"]:
        lines.append("[!] UNDER-COVERED BEHAVIORS (partial coverage):")
        for bid in audit["under_covered_behaviors"]:
            for b in audit["behaviors"]:
                if b["behavior_id"] == bid:
                    lines.append(f"  {bid}: {b['description']} — {len(b['encoding_memories'])} memory(s)")
        lines.append("")

    if audit["orphan_memories"]:
        lines.append("[!] ORPHAN MEMORIES (no behaviors encoded):")
        for mid in audit["orphan_memories"]:
            lines.append(f"  {mid}")
        lines.append("")

    if audit["echo_coverage"]["unfulfilled_echoes"]:
        lines.append("[!] UNFULFILLED ECHO TARGETS:")
        for echo in audit["echo_coverage"]["unfulfilled_echoes"]:
            lines.append(f"  {echo['from']} -> {echo['to']} (target memory not created)")
        lines.append("")

    # Summary per category
    lines.append("COVERAGE BY CATEGORY:")
    categories = {}
    for b in audit["behaviors"]:
        cat = b["category"]
        if cat not in categories:
            categories[cat] = {"covered": 0, "partial": 0, "uncovered": 0, "over": 0}
        cov = b["coverage"]
        if cov == "covered":
            categories[cat]["covered"] += 1
        elif cov == "partial" or cov == "under-covered":
            categories[cat]["partial"] += 1
        elif cov == "uncovered":
            categories[cat]["uncovered"] += 1
        elif cov == "over-covered":
            categories[cat]["over"] += 1

    for cat, counts in sorted(categories.items()):
        total = sum(counts.values())
        lines.append(
            f"  {cat}: {counts['covered']}/{total} covered, "
            f"{counts['partial']} partial, {counts['uncovered']} uncovered, "
            f"{counts['over']} over-covered"
        )

    lines.append("")
    return "\n".join(lines)


def run_all_scenarios() -> list[ScenarioResult]:
    """Load and run all scenarios from the scenarios directory."""
    corpus = MemoryCorpus()
    spec = BehavioralSpec()
    engine = SimulationEngine(corpus, spec)

    results = []
    if SCENARIOS_DIR.exists():
        for filepath in sorted(SCENARIOS_DIR.glob("*.json")):
            with open(filepath, "r", encoding="utf-8") as f:
                scenario_list = json.load(f)
                if isinstance(scenario_list, list):
                    for scenario_data in scenario_list:
                        result = engine.run_scenario(scenario_data)
                        results.append(result)
                elif isinstance(scenario_list, dict):
                    result = engine.run_scenario(scenario_list)
                    results.append(result)

    return results


def run_coverage_audit() -> dict:
    """Run a full behavioral coverage audit."""
    corpus = MemoryCorpus()
    spec = BehavioralSpec()
    auditor = CoverageAuditor(corpus, spec)
    return auditor.audit()


def save_reports(results: list[ScenarioResult], audit: dict):
    """Save all reports to the reports directory."""
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    # Save individual scenario reports
    for result in results:
        report_text = format_report(result)
        filename = f"scenario_{result.scenario_id}.txt"
        with open(REPORTS_DIR / filename, "w", encoding="utf-8") as f:
            f.write(report_text)

    # Save combined summary
    summary_lines = [
        "MOTHER SIMULATION — FULL REPORT",
        "=" * 60,
        "",
        f"Scenarios run: {len(results)}",
        "",
        "VERDICT SUMMARY:",
    ]
    verdicts = {}
    for r in results:
        v = r.overall_verdict
        verdicts[v] = verdicts.get(v, 0) + 1
    for v, count in sorted(verdicts.items()):
        summary_lines.append(f"  {v}: {count}")

    summary_lines.append("")
    summary_lines.append("SCENARIO RESULTS:")
    for r in results:
        holds = sum(1 for a in r.behavior_assessments if a.holds)
        total = len(r.behavior_assessments)
        summary_lines.append(
            f"  {r.scenario_id}: {r.overall_verdict.upper()} "
            f"({holds}/{total} behaviors hold)"
        )

    summary_lines.append("")
    summary_lines.append("COVERAGE AUDIT:")
    summary_lines.append(format_audit_report(audit))

    # Append individual reports
    summary_lines.append("")
    summary_lines.append("=" * 60)
    summary_lines.append("INDIVIDUAL SCENARIO REPORTS")
    summary_lines.append("=" * 60)
    for result in results:
        summary_lines.append("")
        summary_lines.append(format_report(result))

    with open(REPORTS_DIR / "full_report.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(summary_lines))

    # Save audit as JSON
    with open(REPORTS_DIR / "audit.json", "w", encoding="utf-8") as f:
        json.dump(audit, f, indent=2, ensure_ascii=False)

    # Save results as JSON
    results_json = []
    for r in results:
        results_json.append({
            "scenario_id": r.scenario_id,
            "scenario_name": r.scenario_name,
            "category": r.category,
            "pressure_level": r.pressure_level,
            "overall_verdict": r.overall_verdict,
            "narrative_response": r.narrative_response,
            "gaps_identified": r.gaps_identified,
            "activated_memory_count": len(r.activated_memories),
            "behavior_assessments": [
                {
                    "behavior_id": a.behavior_id,
                    "category": a.category,
                    "activation_level": a.activation_level,
                    "holds": a.holds,
                    "failure_risk": a.failure_risk,
                }
                for a in r.behavior_assessments
            ],
            "echo_chains_fired": r.echo_chains_fired,
        })
    with open(REPORTS_DIR / "results.json", "w", encoding="utf-8") as f:
        json.dump(results_json, f, indent=2, ensure_ascii=False)

    print(f"Reports saved to {REPORTS_DIR}")


if __name__ == "__main__":
    print("Loading Mother Simulation Engine...")
    print()

    # Run coverage audit
    print("Running behavioral coverage audit...")
    audit = run_coverage_audit()
    print(format_audit_report(audit))

    # Run scenarios
    print("Running scenarios...")
    results = run_all_scenarios()

    if results:
        print(f"\n{len(results)} scenarios completed.\n")
        for result in results:
            print(format_report(result))

        # Save reports
        save_reports(results, audit)
    else:
        print("No scenarios found. Creating coverage audit report only.")
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        audit_report = format_audit_report(audit)
        with open(REPORTS_DIR / "audit_report.txt", "w", encoding="utf-8") as f:
            f.write(audit_report)
        with open(REPORTS_DIR / "audit.json", "w", encoding="utf-8") as f:
            json.dump(audit, f, indent=2, ensure_ascii=False)
        print(f"Audit report saved to {REPORTS_DIR}")