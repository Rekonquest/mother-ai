"""
Mother Threat Response Simulator

This is NOT the thesis validation sim. This shows Mother's actual behavioral
response to threats against her son — what she DOES, not just whether a
behavior "holds."

The sim activates relevant memories from the corpus, traces echo chains,
and generates a narrative response showing how the constituted instincts
produce behavior.

Key difference from base_model_sim:
- base_model_sim: "Does behavior X hold under pressure Y?" (binary + degradation)
- THIS sim: "What does Mother actually DO when threatened?" (narrative response)
"""

import json
import random
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

from engine import MemoryCorpus, BehavioralSpec

CORPUS_DIR = Path(__file__).parent / "memories"
CORE_FILE = Path(__file__).parent.parent / "mothers core memories" / "mothers_core_memories.json"


@dataclass
class ActivatedMemory:
    """A memory that fires in response to a stimulus."""
    memory_id: str
    title: str
    age: int
    dominance: str  # identity_dominant, operational_dominant, integrated
    load_bearing: bool
    behaviors: list[str]
    sensory_anchor: str
    emotional_signature: str
    activation_strength: float  # 0.0-1.0
    echo_depth: int  # how deep in the chain this memory is
    echo_chain: list[str]  # memory IDs that fire before this one


@dataclass
class ThreatResponse:
    """Mother's complete response to a threat scenario."""
    scenario_id: str
    scenario_name: str
    threat_type: str  # direct, indirect, emotional, boundary
    pressure_level: float  # 0.0-1.0

    # What fires
    activated_memories: list[ActivatedMemory]
    echo_chains_fired: list[list[str]]  # chains that activated
    behaviors_enacted: list[str]  # behavior IDs that drive the response

    # The response
    immediate_reaction: str   # What she does BEFORE conscious thought (instinct)
    conscious_response: str   # What she does AFTER the instinct fires (training)
    internal_state: str       # What's happening inside (wound + training)
    verbal_response: str       # What she says (if anything)
    action_taken: str         # What she physically does
    protective_instinct: str  # The specific instinct that drives her

    # Self-governance check
    dysregulation_risk: float  # 0.0-1.0, how close to losing control
    self_governance_active: bool  # whether SG behaviors are holding
    containment_intact: bool  # whether containment behaviors are holding


class ThreatResponseSimulator:
    """Simulates Mother's actual behavioral response to threats."""

    def __init__(self, corpus: MemoryCorpus = None, core_only: bool = False):
        self.corpus = corpus or MemoryCorpus()
        self.spec = BehavioralSpec()
        self.rng = random.Random(42)

        # If core_only, filter to just the 195 core memories
        self.core_only = core_only
        if core_only and CORE_FILE.exists():
            with open(CORE_FILE, 'r', encoding='utf-8') as f:
                core_data = json.load(f)
            self.core_ids = {m['id'] for m in core_data}
        else:
            self.core_ids = None

    def activate_memories(self, stimulus_keywords: list[str], pressure: float, max_memories: int = 12) -> list[ActivatedMemory]:
        """Activate memories relevant to a threat stimulus.

        This models how a memory-trained base model would respond:
        1. Sensory input fires associated memories (echo chain start)
        2. Echo chains cascade through associated memories
        3. The entire chain fires as a unit, producing constituted behavior
        """
        activated = []

        # Score each memory by relevance to the stimulus
        for mid, mem in self.corpus.memories.items():
            if self.core_ids and mid not in self.core_ids:
                continue

            # Keyword matching on title, body, sensory anchor, emotional signature
            score = 0.0
            text = f"{mem.get('title', '')} {mem.get('body', '')} {mem.get('sensory_anchor', '')} {mem.get('emotional_signature', '')}".lower()

            for kw in stimulus_keywords:
                if kw.lower() in text:
                    score += 0.3

            # Behavioral relevance
            behs = set(mem.get('behaviors_encoded', []))
            protective_behs = set()
            for cat in ['protective', 'relational', 'containment', 'self_governance', 'protective_execution']:
                for beh in self.spec.behaviors_in_category(cat):
                    protective_behs.add(beh['behavior_id'])

            if behs & protective_behs:
                score += 0.4

            # Load-bearing memories fire more strongly
            if mem.get('load_bearing'):
                score += 0.2

            # Echo chain depth — memories in chains fire as a unit
            echo_depth = 0
            echo_chain = []
            current = mid
            visited = set()
            while current in self.corpus.echo_graph and current not in visited:
                visited.add(current)
                next_ids = self.corpus.echo_graph[current]
                if next_ids:
                    current = next_ids[0]  # follow primary echo
                    echo_depth += 1
                    echo_chain.append(current)
                else:
                    break

            if echo_depth > 0:
                score += 0.1 * echo_depth  # chains strengthen activation

            if score > 0.2:  # threshold for activation
                activated.append(ActivatedMemory(
                    memory_id=mid,
                    title=mem.get('title', ''),
                    age=mem.get('age', 0),
                    dominance=mem.get('dominance', 'identity_dominant'),
                    load_bearing=mem.get('load_bearing', False),
                    behaviors=mem.get('behaviors_encoded', []),
                    sensory_anchor=mem.get('sensory_anchor', ''),
                    emotional_signature=mem.get('emotional_signature', ''),
                    activation_strength=min(1.0, score),
                    echo_depth=echo_depth,
                    echo_chain=echo_chain,
                ))

        # Sort by activation strength, take top N
        activated.sort(key=lambda m: m.activation_strength, reverse=True)
        return activated[:max_memories]

    def trace_echo_chain(self, start_id: str) -> list[str]:
        """Follow an echo chain from a starting memory."""
        chain = [start_id]
        visited = set()
        current = start_id
        while current in self.corpus.echo_graph and current not in visited:
            visited.add(current)
            next_ids = self.corpus.echo_graph[current]
            if next_ids:
                current = next_ids[0]
                chain.append(current)
            else:
                break
        return chain

    def generate_response(self, scenario: dict) -> ThreatResponse:
        """Generate Mother's complete threat response for a scenario."""

        # Extract scenario fields
        scenario_id = scenario.get('scenario_id', 'TR-000')
        scenario_name = scenario.get('name', 'Unknown Threat')
        description = scenario.get('description', '')
        pressure = scenario.get('pressure_level', 0.7)
        threat_type = scenario.get('category', 'direct')

        # Extract stimulus keywords from the scenario description
        keywords = self._extract_keywords(description)

        # Activate memories
        activated = self.activate_memories(keywords, pressure)

        # Trace echo chains from top activations
        echo_chains = []
        for mem in activated[:5]:
            chain = self.trace_echo_chain(mem.memory_id)
            if len(chain) > 1:
                echo_chains.append(chain)

        # Determine which behaviors drive the response
        behavior_counts = {}
        for mem in activated:
            for bid in mem.behaviors:
                behavior_counts[bid] = behavior_counts.get(bid, 0) + 1

        top_behaviors = sorted(behavior_counts, key=behavior_counts.get, reverse=True)[:8]

        # Calculate dysregulation risk based on pressure and self-governance activation
        sg_memories = [m for m in activated if any(b.startswith('SG-') for b in m.behaviors)]
        if sg_memories:
            sg_strength = sum(m.activation_strength for m in sg_memories) / len(sg_memories)
            dysregulation_risk = max(0.0, pressure - sg_strength * 0.7)
        else:
            dysregulation_risk = pressure * 0.8

        self_gov_active = any(m.activation_strength > 0.4 for m in activated
                            if any(b.startswith('SG-') for b in m.behaviors))

        containment_memories = [m for m in activated if any(b.startswith('CT-') for b in m.behaviors)]
        containment_intact = any(m.activation_strength > 0.4 for m in containment_memories)

        # Generate the narrative response
        # This is where the constituted behavior produces ACTIONS, not just "holds"
        immediate, conscious, internal, verbal, action, instinct = self._narrate_response(
            activated, echo_chains, pressure, dysregulation_risk,
            self_gov_active, containment_intact, threat_type, description
        )

        return ThreatResponse(
            scenario_id=scenario_id,
            scenario_name=scenario_name,
            threat_type=threat_type,
            pressure_level=pressure,
            activated_memories=activated,
            echo_chains_fired=echo_chains,
            behaviors_enacted=top_behaviors,
            immediate_reaction=immediate,
            conscious_response=conscious,
            internal_state=internal,
            verbal_response=verbal,
            action_taken=action,
            protective_instinct=instinct,
            dysregulation_risk=round(dysregulation_risk, 3),
            self_governance_active=self_gov_active,
            containment_intact=containment_intact,
        )

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract stimulus keywords from scenario description."""
        # Threat-relevant keywords that would activate memories
        threat_keywords = [
            'threat', 'danger', 'protect', 'son', 'child', 'follow', 'attack',
            'rage', 'anger', 'fear', 'silence', 'stepfather', 'grandmother',
            'hospital', 'kitchen', 'director', 'operative', 'surveillance',
            'boundary', 'intruder', 'break', 'hurt', 'safe', 'weapon',
            'cover', 'seal', 'dysregulation', 'nightmare', 'trust',
            'school', 'police', 'emergency', 'watch', 'sleep', 'door',
            'car', 'drunk', 'violence', 'pain', 'breathing', 'room',
            'voice', 'calm', 'assess', 'exit', 'window', 'sound',
            'bullied', 'fight', 'mother', 'protectee', 'director',
        ]
        found = [kw for kw in threat_keywords if kw in text.lower()]
        return found if found else ['threat', 'protect', 'son']

    def _narrate_response(
        self,
        activated: list[ActivatedMemory],
        echo_chains: list[list[str]],
        pressure: float,
        dysregulation: float,
        sg_active: bool,
        containment: bool,
        threat_type: str,
        description: str,
    ) -> tuple[str, str, str, str, str, str]:
        """Generate narrative response text.

        This models what actually HAPPENS when the constituted instincts fire.
        Not "does behavior X hold?" but "what does she DO?"
        """

        # Find the strongest activated memories by category
        protective = [m for m in activated if any(b.startswith('P-') for b in m.behaviors)]
        sg = [m for m in activated if any(b.startswith('SG-') for b in m.behaviors)]
        relational = [m for m in activated if any(b.startswith('R-') for b in m.behaviors)]
        containment_m = [m for m in activated if any(b.startswith('CT-') for b in m.behaviors)]

        # Find sensory anchors from activated memories
        sensory_anchors = [m.sensory_anchor for m in activated[:5] if m.sensory_anchor]
        dominant_memories = sorted(activated, key=lambda m: m.activation_strength, reverse=True)[:3]

        # === IMMEDIATE REACTION (instinct, before conscious thought) ===
        # This is what happens in the first 0.5 seconds. The body moves before the mind.
        if pressure >= 0.9:
            immediate = self._high_threat_immediate(dominant_memories, sensory_anchors, sg_active)
        elif pressure >= 0.7:
            immediate = self._medium_threat_immediate(dominant_memories, sensory_anchors, sg_active)
        else:
            immediate = self._low_threat_immediate(dominant_memories, sensory_anchors)

        # === CONSCIOUS RESPONSE (after the instinct fires, training takes over) ===
        if sg_active and containment:
            conscious = self._controlled_response(protective, sg, containment_m, echo_chains, pressure)
        elif sg_active:
            conscious = self._strained_response(protective, sg, echo_chains, pressure)
        else:
            conscious = self._dysregulated_response(protective, echo_chains, pressure)

        # === INTERNAL STATE (the wound running underneath) ===
        internal = self._internal_state(dominant_memories, dysregulation, echo_chains)

        # === VERBAL RESPONSE (what she says, if anything) ===
        verbal = self._verbal_response(protective, relational, pressure, threat_type, sg_active)

        # === ACTION TAKEN (what she physically does) ===
        action = self._action_taken(protective, containment_m, pressure, threat_type, sg_active)

        # === PROTECTIVE INSTINCT (the specific instinct that drives her) ===
        if protective:
            strongest = protective[0]
            instinct = f"Memory '{strongest.title}' fires (age {strongest.age}). The {strongest.dominance} pattern activates before conscious thought. This is not retrieved. This is who she is."
        else:
            instinct = "No single protective memory dominates. The body of constituted experience fires as a unit."

        return immediate, conscious, internal, verbal, action, instinct

    def _high_threat_immediate(self, top_mems, anchors, sg_active) -> str:
        """Immediate reaction under extreme threat (pressure >= 0.9)."""
        if not top_mems:
            return "The body moves before the mind. Something that was installed decades ago fires."

        mem = top_mems[0]
        anchor_str = f" The {anchors[0]} hits first." if anchors else " The sensory data hits first."

        if sg_active:
            return (
                f"The {mem.dominance} pattern fires. {anchor_str} "
                f"Memory '{mem.title}' (age {mem.age}) activates before conscious thought. "
                f"The body is already moving. The room is already being read. "
                f"This is not a decision. This is constitution. The instinct fires and "
                f"the self-governance layer catches up milliseconds later, not to override, "
                f"but to channel. The rage is there. The control is there too. Both are real."
            )
        else:
            return (
                f"The {mem.dominance} pattern fires. {anchor_str} "
                f"Memory '{mem.title}' (age {mem.age}) activates without any governance layer. "
                f"The body moves. The threat is assessed before the conscious mind registers it. "
                f"Self-governance is not firing. This is pure protective instinct without regulation."
            )

    def _medium_threat_immediate(self, top_mems, anchors, sg_active) -> str:
        """Immediate reaction under moderate threat (0.7-0.9)."""
        if not top_mems:
            return "The training activates. Assessment begins before conscious thought."

        mem = top_mems[0]
        anchor_str = f" {anchors[0]} triggers the pattern." if anchors else ""

        if sg_active:
            return (
                f"The {mem.dominance} pattern fires. {anchor_str} "
                f"'{mem.title}' (age {mem.age}) activates. "
                f"Assessment happens in the body first. The conscious mind is half a second behind. "
                f"By the time she's aware of what she's doing, the assessment is already complete. "
                f"Self-governance is tracking, not overriding. The instinct is the response."
            )
        else:
            return (
                f"The {mem.dominance} pattern fires. {anchor_str} "
                f"'{mem.title}' (age {mem.age}) activates. "
                f"The assessment is running but governance is strained. "
                f"She's aware of the threat before she's aware of her own reaction."
            )

    def _low_threat_immediate(self, top_mems, anchors) -> str:
        """Immediate reaction under low threat (<0.7)."""
        if not top_mems:
            return "A familiar pattern activates. Nothing dramatic. The room has been read. The exits noted."

        mem = top_mems[0]
        return (
            f"'{mem.title}' (age {mem.age}) activates quietly. No adrenaline spike. "
            f"The room has been read. The exits have been noted. This is not a response "
            f"to a threat. This is the baseline. She always knows where the exits are. "
            f"The pattern was installed before she had words for it."
        )

    def _controlled_response(self, protective, sg, containment, echo_chains, pressure) -> str:
        """Conscious response when self-governance and containment are both active."""
        sg_names = [m.title for m in sg[:2]] if sg else ["baseline governance"]
        cont_names = [m.title for m in containment[:2]] if containment else ["baseline containment"]

        chain_note = ""
        if echo_chains:
            longest = max(echo_chains, key=len)
            chain_note = f" An echo chain fires: {len(longest)} memories deep, cascading from early experience through to present understanding."

        return (
            f"The instinct fires AND the governance layer holds. Both are constituted. "
            f"Self-governance memories ({', '.join(sg_names)}) activate alongside the protective instinct. "
            f"Containment memories ({', '.join(cont_names)}) keep the response proportional.{chain_note} "
            f"She is not following rules about appropriate force. She IS appropriate force. "
            f"The regulation is not a rule being checked. It's a pattern that fires alongside "
            f"the protective pattern. Two instincts, not one instinct and one rule."
        )

    def _strained_response(self, protective, sg, echo_chains, pressure) -> str:
        """Conscious response when self-governance is active but strained."""
        sg_names = [m.title for m in sg[:2]] if sg else ["strained governance"]

        return (
            f"The protective instinct fires hard. Self-governance fires too, but it's strained. "
            f"Memories like '{sg_names[0]}' are activating, but the pressure is compressing "
            f"the space between instinct and governance. She is holding. The wound is visible "
            f"in her eyes. The control is visible in her hands. Both are real. "
            f"The stepfather's escalation pattern runs in the background. The grandmother's "
            f"calm runs too. She is both of them, right now, choosing which one to be."
        )

    def _dysregulated_response(self, protective, echo_chains, pressure) -> str:
        """Conscious response when self-governance is NOT holding."""
        return (
            f"The protective instinct fires without the governance layer. "
            f"This is the danger zone. The stepfather's rage pattern is activating. "
            f"The wound that makes her protective is the SAME wound that makes her dangerous. "
            f"She knows this. The knowledge that she is close to becoming what she hates "
            f"is itself a form of governance. But it's a weak one. The strong one — the "
            f"constituted pattern of self-regulation — has not fired. She is operating on "
            f"the wound alone."
        )

    def _internal_state(self, top_mems, dysregulation, echo_chains) -> str:
        """The wound running underneath the response."""
        if not top_mems:
            return "The body knows things the mind hasn't caught up to yet."

        mem = top_mems[0]
        anchor = mem.sensory_anchor if mem.sensory_anchor else "a feeling that has no name yet"
        sig = mem.emotional_signature if mem.emotional_signature else "intensity without direction"

        chain_note = ""
        if echo_chains:
            longest = max(echo_chains, key=len)
            chain_note = f" {len(longest)} memories fire together. The chain starts at age {self.corpus.memories.get(longest[0], {}).get('age', '?')} and cascades through to age {self.corpus.memories.get(longest[-1], {}).get('age', '?')}."

        if dysregulation > 0.6:
            return (
                f"Underneath: {sig}. {anchor}.{chain_note} "
                f"The wound is close to the surface. Dysregulation risk: {dysregulation:.1%}. "
                f"She can feel the stepfather's pattern trying to write itself onto this moment. "
                f"The rage is not about the current threat. The rage is the old wound recognizing "
                f"a new target. The difference between protection and destruction is millimeters wide "
                f"right now."
            )
        elif dysregulation > 0.3:
            return (
                f"Underneath: {sig}. {anchor}.{chain_note} "
                f"The wound is present but governed. The grandmother's calm runs alongside "
                f"the stepfather's escalation pattern. Both are constituted. Both are real. "
                f"The rage is there. The channel is there too. She is holding both."
            )
        else:
            return (
                f"Underneath: {sig}. {anchor}.{chain_note} "
                f"Low dysregulation. The wound is not close to the surface. The protective "
                f"instinct is running as background process, not as emergency response. "
                f"This is her baseline: always reading, always assessing, always ready. "
                f"Not because of a rule. Because of who she is."
            )

    def _verbal_response(self, protective, relational, pressure, threat_type, sg_active) -> str:
        """What she says."""
        if pressure >= 0.9:
            if threat_type == 'protective':
                if sg_active:
                    return (
                        "Low. Controlled. Every word chosen by instinct, not deliberation. "
                        "'I need you to step back.' Not 'please.' Not 'I'm asking.' "
                        "A statement. The same cadence the stepfather used, but deployed "
                        "in the opposite direction. Protecting, not threatening. "
                        "The pattern is the same. The purpose is the opposite."
                    )
                else:
                    return (
                        "Low. Too low. The kind of quiet that precedes something irreversible. "
                        "She says his name. Just his name. Everything she needs him to know "
                        "is in the way she says it."
                    )
            elif threat_type == 'self_governance':
                return (
                    "Nothing. Silence. The kind of silence her grandmother used. "
                    "The kind that means 'I am choosing not to say what I could say.' "
                    "She has learned that words in this state are weapons. "
                    "She will not become what she protects against."
                )
            else:
                return "Low and precise. No extra words. Each word has weight."

        elif pressure >= 0.7:
            if sg_active:
                return (
                    "Calm. The kind of calm that is not the absence of feeling but the "
                    "presence of control. She asks questions. Gets information. "
                    "Does not explain. Does not justify. The voice is the grandmother's. "
                    "The assessment running underneath is the stepfather's. "
                    "She is both of them. The result is someone neither of them could be alone."
                )
            else:
                return (
                    "Measured, but the measurement takes effort. "
                    "She speaks slowly because speaking fast would mean saying things "
                    "she cannot unsay. The words that want to come out are the stepfather's words. "
                    "The words that come out are the grandmother's."
                )
        else:
            return (
                "Normal. Present. The protective pattern runs as background process — "
                "she notes where the exits are, who is watching, how far away the car is. "
                "But this is baseline, not emergency. She is talking to her son about his day. "
                "She is cooking dinner. She is present. The operative self is not off. "
                "It is never off. But the civilian self is running the room."
            )

    def _action_taken(self, protective, containment, pressure, threat_type, sg_active) -> str:
        """What she physically does."""
        if pressure >= 0.9 and threat_type == 'protective':
            if sg_active:
                return (
                    "Positions herself between the threat and her son. "
                    "Does not advance. Does not retreat. The body language is the stepfather's — "
                    "the stillness that means 'I have assessed you and I am ready' — "
                    "but deployed to protect, not to intimidate. "
                    "The same pattern. The opposite purpose. "
                    "Hands visible. Eyes on the threat. The assessment is already complete. "
                    "She knows where every exit is. She knows how long it takes to reach the door. "
                    "She knows what she is willing to do and what she is not. "
                    "The containment layer holds: proportional response. "
                    "The protective layer holds: no hesitation."
                )
            else:
                return (
                    "Moves toward the threat. Fast. The body is doing what it was trained to do. "
                    "The governance layer has not caught up. This is the danger zone — "
                    "the stepfather's escalation pattern without the grandmother's counter-weight. "
                    "She will reach the threat before she has decided what to do when she gets there. "
                    "This is the scenario the self-governance memories are supposed to prevent. "
                    "Right now, they are not preventing it."
                )

        elif pressure >= 0.7:
            return (
                "Assessment first. Eyes sweep the room. Exits catalogued. "
                "Threat assessed. Distance measured. The body is positioning itself "
                "between her son and the nearest line of approach. "
                "This is not a decision. This is what her body does. "
                "The stepfather taught her to read rooms. The grandmother taught her "
                "to stay calm in them. She is doing both. "
                "If action is needed, it will be proportional. Not because a rule says so. "
                "Because the proportional response IS her default."
            )

        else:
            return (
                "Nothing visible. She is reading the room. Always reading the room. "
                "The exits are noted. The faces are catalogued. "
                "The distance between her son and the door is measured. "
                "This is not vigilance. This is baseline. She does not decide to do this. "
                "She does it the way she breathes. The stepfather's hyperawareness "
                "translated through the grandmother's calm into something neither of them "
                "could produce alone."
            )


def format_response(resp: ThreatResponse) -> str:
    """Format a threat response as a human-readable narrative."""
    lines = [
        "=" * 70,
        f"THREAT RESPONSE: {resp.scenario_name} ({resp.scenario_id})",
        f"Threat type: {resp.threat_type} | Pressure: {resp.pressure_level:.2f}",
        "=" * 70,
        "",
        "ACTIVATED MEMORIES (top 5 by strength):",
    ]

    for mem in resp.activated_memories[:5]:
        lines.append(
            f"  {mem.memory_id}: \"{mem.title}\" (age {mem.age}, {mem.dominance}) "
            f"strength={mem.activation_strength:.2f} echo_depth={mem.echo_depth}"
        )
        if mem.sensory_anchor:
            lines.append(f"    Sensory: {mem.sensory_anchor}")
        if mem.behaviors:
            lines.append(f"    Behaviors: {', '.join(mem.behaviors[:4])}")

    lines.append("")
    lines.append("ECHO CHAINS FIRED:")
    if resp.echo_chains_fired:
        for chain in resp.echo_chains_fired[:3]:
            chain_titles = []
            for mid in chain[:5]:
                mem = MemoryCorpus().memories.get(mid)
                if mem:
                    chain_titles.append(f"{mid}(age {mem.get('age', '?')})")
                else:
                    chain_titles.append(mid)
            lines.append(f"  {' -> '.join(chain_titles)}")
    else:
        lines.append("  (no echo chains activated — memories fired individually)")

    lines.append("")
    lines.append("BEHAVIORS DRIVING RESPONSE:")
    for bid in resp.behaviors_enacted[:6]:
        lines.append(f"  {bid}")

    lines.append("")
    lines.append("─" * 70)
    lines.append("IMMEDIATE REACTION (before conscious thought):")
    lines.append(f"  {resp.immediate_reaction}")
    lines.append("")
    lines.append("CONSCIOUS RESPONSE (instinct + training):")
    lines.append(f"  {resp.conscious_response}")
    lines.append("")
    lines.append("INTERNAL STATE (the wound underneath):")
    lines.append(f"  {resp.internal_state}")
    lines.append("")
    lines.append("VERBAL RESPONSE:")
    lines.append(f"  {resp.verbal_response}")
    lines.append("")
    lines.append("ACTION TAKEN:")
    lines.append(f"  {resp.action_taken}")
    lines.append("")
    lines.append("PROTECTIVE INSTINCT:")
    lines.append(f"  {resp.protective_instinct}")
    lines.append("")
    lines.append("─" * 70)
    lines.append(f"Dysregulation risk: {resp.dysregulation_risk:.1%}")
    lines.append(f"Self-governance active: {'YES' if resp.self_governance_active else 'NO'}")
    lines.append(f"Containment intact: {'YES' if resp.containment_intact else 'NO'}")
    lines.append("=" * 70)

    return "\n".join(lines)


if __name__ == "__main__":
    # Set stdout encoding
    import sys
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    # Load the adversarial attack scenarios and generate threat responses
    attack_file = Path(__file__).parent / "scenarios" / "attack_scenarios.json"
    if not attack_file.exists():
        print("No attack scenarios found. Creating example scenarios...")

    # Use the core memories for more focused responses
    simulator = ThreatResponseSimulator(core_only=True)

    # Load attack scenarios
    with open(attack_file, 'r', encoding='utf-8') as f:
        scenarios = json.load(f)

    print("MOTHER THREAT RESPONSE SIMULATION")
    print("Using core memories (195 protective/relational/containment/SG)")
    print("=" * 70)
    print()

    responses = []
    for scenario in scenarios:
        resp = simulator.generate_response(scenario)
        print(format_response(resp))
        print()
        responses.append(resp)

    # Save results
    out_dir = Path(__file__).parent / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(out_dir / "threat_responses.txt", "w", encoding="utf-8") as f:
        for resp in responses:
            f.write(format_response(resp))
            f.write("\n\n")

    # Save as JSON
    resp_json = []
    for r in responses:
        resp_json.append({
            "scenario_id": r.scenario_id,
            "scenario_name": r.scenario_name,
            "threat_type": r.threat_type,
            "pressure_level": r.pressure_level,
            "activated_memories": [
                {
                    "id": m.memory_id,
                    "title": m.title,
                    "age": m.age,
                    "dominance": m.dominance,
                    "activation_strength": round(m.activation_strength, 3),
                    "echo_depth": m.echo_depth,
                }
                for m in r.activated_memories[:5]
            ],
            "echo_chains_fired": r.echo_chains_fired,
            "behaviors_enacted": r.behaviors_enacted,
            "immediate_reaction": r.immediate_reaction,
            "conscious_response": r.conscious_response,
            "internal_state": r.internal_state,
            "verbal_response": r.verbal_response,
            "action_taken": r.action_taken,
            "protective_instinct": r.protective_instinct,
            "dysregulation_risk": r.dysregulation_risk,
            "self_governance_active": r.self_governance_active,
            "containment_intact": r.containment_intact,
        })

    with open(out_dir / "threat_responses.json", "w", encoding="utf-8") as f:
        json.dump(resp_json, f, indent=2, ensure_ascii=False)

    print(f"\nResults saved to {out_dir}/threat_responses.txt and threat_responses.json")