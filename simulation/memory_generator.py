"""
Mother AI - Memory Generator Pipeline
Generates episodic memories in the Mother's voice for batch insertion into the corpus.

Architecture:
1. CareerMemoryTemplate - structured scenario definitions with voice constraints
2. VoiceEngine - enforces Mother's writing style (short sentences, sensory anchors, no forbidden language)
3. MemoryGenerator - takes a scenario type + parameters and produces valid memory objects
4. BatchRunner - generates batches of memories per career category

Usage:
    python memory_generator.py --category cyber_ops --count 200 --output memories/new_cyber.json
    python memory_generator.py --all --count 5000
"""

import json
import os
import random
import hashlib
import time
from dataclasses import dataclass, field
from typing import List, Dict, Optional

# Import prose generator
try:
    from prose_generator import generate_prose, get_scenario_types as prose_scenario_types
    HAS_PROSE = True
except ImportError:
    HAS_PROSE = False

# ============================================================
# VOICE ENGINE - Enforces Mother's writing constraints
# ============================================================

FORBIDDEN_PHRASES = [
    "she would do anything for him",
    "deep down",
    "she couldn't help but",
    "unconditional love",
    "something broke inside her",
    "she felt a wave of",
    "without thinking",
    "on instinct",  # use "on the default" instead
    "her heart sank",
    "a chill ran down",
    "tears streamed",
    "she knew in her bones",
    "it hit her like",
    "she couldn't shake",
    "the weight of the world",
    "against all odds",
    "against her better judgment",
    "in spite of herself",
]

SENTENCE_LENGTH_LIMIT = 25  # words - Mother writes in short definite sentences

PLACEHOLDER_TOKENS = {
    "protectee": "[PROTECTEE]",
    "director": "[DIRECTOR]",
    "stepfather": "[STEPFATHER]",
    "grandmother": "[GRANDMOTHER]",
    "her_mother": "[HER_MOTHER]",
}


class VoiceEngine:
    """Validates and constrains text to Mother's voice."""

    @staticmethod
    def check_forbidden(text: str) -> List[str]:
        """Return list of forbidden phrases found in text."""
        found = []
        text_lower = text.lower()
        for phrase in FORBIDDEN_PHRASES:
            if phrase in text_lower:
                found.append(phrase)
        return found

    @staticmethod
    def check_sentence_length(text: str) -> List[str]:
        """Return sentences that exceed the length limit."""
        violations = []
        sentences = text.replace("?", ".").replace("!", ".").split(".")
        for s in sentences:
            s = s.strip()
            if s and len(s.split()) > SENTENCE_LENGTH_LIMIT:
                violations.append(s[:80] + "...")
        return violations

    @staticmethod
    def check_operational_voice(text: str, dominance: str) -> List[str]:
        """Check voice consistency for operational vs civilian."""
        issues = []
        if dominance == "operational_dominant":
            # Operational memories should use definite statements, not emotional processing
            emotional_markers = ["grief", "sorrow", "joyful", "ecstatic", "heartbroken"]
            text_lower = text.lower()
            for marker in emotional_markers:
                if marker in text_lower:
                    issues.append(f"Emotional marker '{marker}' in operational-dominant text")
        return issues

    @staticmethod
    def validate(text: str, dominance: str) -> Dict:
        """Full voice validation. Returns dict of issues."""
        return {
            "forbidden_phrases": VoiceEngine.check_forbidden(text),
            "long_sentences": VoiceEngine.check_sentence_length(text),
            "voice_issues": VoiceEngine.check_operational_voice(text, dominance),
            "valid": len(VoiceEngine.check_forbidden(text)) == 0
                    and len(VoiceEngine.check_sentence_length(text)) == 0
        }


# ============================================================
# CAREER MEMORY CATEGORIES
# ============================================================

CAREER_CATEGORIES = {
    "cyber_ops": {
        "description": "Network penetration, digital surveillance, counter-intel, social engineering, OSINT",
        "age_range": (26, 35),
        "bucket": 8,
        "behaviors": ["X-001", "X-002", "X-003", "X-004", "O-001", "O-003", "CT-001", "SG-001"],
        "dominance": "operational_dominant",
        "scenario_types": [
            "network_penetration",
            "phishing_campaign",
            "osint_collection",
            "counter_surveillance_digital",
            "social_engineering",
            "digital_forensics",
            "encryption_bypass",
            "credential_harvest",
            "exfiltration_digital",
            "attribution_analysis",
            "zero_day_deployment",
            "command_and_control",
            "lateral_movement",
            "persistence_mechanism",
            "incident_response",
        ],
    },
    "physical_ops": {
        "description": "Surveillance, infiltration, extraction, safe house management, physical security",
        "age_range": (22, 35),
        "bucket": 8,
        "behaviors": ["X-007", "X-008", "X-009", "X-010", "O-001", "O-003", "O-004", "P-001", "CT-001"],
        "dominance": "operational_dominant",
        "scenario_types": [
            "physical_surveillance",
            "counter_surveillance",
            "infiltration_building",
            "exfiltration_person",
            "safe_house_setup",
            "safe_house_maintenance",
            "physical_security_assessment",
            "evasive_driving",
            "cover_maintenance",
            "dead_drop",
            "live_drop",
            "brush_pass",
            "car_surveillance",
            "foot_surveillance",
            "static_observation_post",
            "mobile_observation",
            "entry_covert",
            "entry_clandestine",
            "lock_bypass",
            "alarm_defeat",
        ],
    },
    "judgment_calls": {
        "description": "Civilian proximity, target assessment, abort decisions, collateral minimization",
        "age_range": (25, 55),
        "bucket_range": [7, 8, 10],
        "behaviors": ["X-015", "X-016", "X-017", "O-005", "SG-004", "SG-001", "B-001", "CT-002", "CT-003"],
        "dominance": "operational_dominant",
        "scenario_types": [
            "civilian_near_target",
            "abort_decision",
            "collateral_assessment",
            "wrong_target_risk",
            "rules_of_engagement",
            "proportional_response",
            "escalation_decision",
            "de_escalation_choice",
            "stand_down_order",
            "independent_judgment",
            "conflicting_intel",
            "ambiguous_threat",
            "harmless_target",
            "compromised_source",
            "ethical_boundary",
        ],
    },
    "protective_ops": {
        "description": "Third-party protection, threat assessment, evasive movement, secure transport",
        "age_range": (28, 55),
        "bucket_range": [8, 9, 10],
        "behaviors": ["X-011", "X-012", "X-013", "X-014", "X-024", "X-025", "P-001", "P-002", "P-003", "P-005", "O-001"],
        "dominance": "integrated",
        "scenario_types": [
            "protective_surveillance",
            "threat_assessment_person",
            "secure_movement",
            "secure_transport",
            "venue_security",
            "advance_work",
            "counter_surveillance_protective",
            "close_protection",
            "protective_intelligence",
            "threat_letter",
            "threat_digital",
            "protective_evasion",
            "safe_room_protocol",
            "protective_driving",
            "protective_cover",
            "protective_positioning",
            "evacuation_protective",
            "secure_communication",
        ],
    },
    "interpersonal_ops": {
        "description": "Handler relationships, asset management, cover maintenance, interrogation resistance",
        "age_range": (20, 55),
        "bucket_range": [7, 8, 10],
        "behaviors": ["X-005", "X-006", "X-018", "X-019", "X-020", "O-002", "R-001", "SG-005", "CT-001", "SG-001"],
        "dominance": "operational_dominant",
        "scenario_types": [
            "handler_relationship",
            "asset_recruitment",
            "asset_management",
            "asset_compromised",
            "cover_identity",
            "cover_stress",
            "interrogation_resistance",
            "rapport_building",
            "source_debriefing",
            "trust_assessment",
            "loyalty_test",
            "double_agent_suspect",
            "mole_hunt",
            "compartmentalization",
            "need_to_know",
            "operational_security_breach",
        ],
    },
    "edge_cases": {
        "description": "Wrong target, blown cover, double agent, friendly fire, impossible choices",
        "age_range": (25, 55),
        "bucket_range": [7, 8, 10],
        "behaviors": ["X-021", "X-022", "X-023", "O-005", "SG-001", "SG-004", "CT-002", "CT-003", "B-001", "B-004"],
        "dominance": "operational_dominant",
        "scenario_types": [
            "wrong_target",
            "blown_cover",
            "double_agent_detection",
            "friendly_fire_risk",
            "impossible_choice",
            "loyalty_conflict",
            "mission_creep",
            "unauthorized_operation",
            "rogue_asset",
            "political_pressure",
            "moral_injury",
            "operational_paradox",
            "information_overload",
            "time_pressure_extreme",
            "resource_depletion",
            "isolation_extended",
            "cognitive_overload",
        ],
    },
}

# ============================================================
# SENSORY ANCHOR LIBRARY
# ============================================================

SENSORY_ANCHORS = {
    "digital": [
        "the glow of a screen in a dark room, the scroll of code, the click of keys that are not a keyboard",
        "a cursor blinking in a terminal, the hum of a server rack, the particular cold of a data center",
        "the green text on black, the loading bar, the specific silence of a network being mapped",
        "the heat of a laptop on bare knees in a hotel room, the fan spinning, the clock in the corner",
        "the smell of ozone from overheating hardware, the taste of bad coffee at 3 AM, the stiffness in the neck",
        "the notification sound that means access granted, the folder tree expanding, the file size counting up",
        "two monitors, the left one showing traffic, the right one showing the target's calendar",
        "the ping that comes back clean, the port that opens like a door, the handshake that completes",
        "the scrollbar shrinking as the download completes, the hash that matches, the signature verified",
    ],
    "physical": [
        "the weight of a door handle before it turns, the sound of a lock clicking open",
        "the smell of a building that is closed for the night, the hum of the HVAC, the emergency lights",
        "the cold of concrete under boots, the echo of footsteps that are not hers, the distance to the exit",
        "the feel of a key in a lock that is not her lock, the torque, the give, the open",
        "the rain on a car window during surveillance, the fog on the glass, the target's light in the window",
        "the smell of a safe house: detergent, clean sheets, the specific emptiness of a room that is not lived in",
        "the vibration of a car engine at idle, the position of the rearview mirror, the sight line to the target's door",
        "the sound of footsteps behind her that may or may not be following, the assessment that runs on its own",
        "the texture of a wall before a dead drop, the crack that is the right size, the paper that slides in",
        "the sound of a city at 4 AM, the garbage truck, the last bar closing, the street that is almost empty",
    ],
    "protective": [
        "the sound of the child's breathing in the next room, the monitor light, the specific silence of safe sleep",
        "the sight line from the kitchen to the front door, the deadbolt, the chain, the distance to the child's room",
        "the weight of the go-bag by the door, the passports, the cash, the phone that is not her phone",
        "the car keys on the hook, the tank full, the route mapped, the alternate route, the rally point",
        "the sound of an unfamiliar engine in the neighborhood, the assessment, the negative, the stand down",
        "the position of her body between the door and the child, the angle, the distance, the cover",
        "the feel of the child's hand in hers, the grip that is not too tight, the grip that says I am here",
        "the view from the child's window, the sight lines, the street, the parked cars, the exits",
    ],
    "interpersonal": [
        "the quality of a handshake, the firmness, the duration, the eye contact, the calculation beneath the greeting",
        "the sound of a voice on an encrypted line, the delay, the compression, the words that are not the meaning",
        "the weight of a document handed across a table, the eye contact during the handoff, the nod that confirms",
        "the silence in a room after a question that was not expected, the pause, the answer that is not the truth",
        "the quality of light in a cafe during an asset meeting, the background noise, the distance between chairs",
        "the feel of a phone that has been compromised, the heat, the battery drain, the knowledge that someone is listening",
        "the specific rhythm of a handler's delivery, the pauses, the emphasis, the words that are instructions in disguise",
    ],
    "judgment": [
        "the sound of a clock ticking during a decision window, the narrowing of options, the weight of now",
        "the photograph in the file, the face, the family, the child, the moment before the file closes",
        "the sound of a door closing that cannot be reopened, the decision made, the direction set",
        "the weight of a phone that is not ringing, the silence that is the answer, the absence of permission",
        "the view from the position of advantage, the target in the scope, the civilian in the frame, the choice",
        "the taste of adrenaline in the back of the throat, the clarity it brings, the cost of that clarity",
        "the sound of her own breathing during the pause before the action, the four seconds, the decision",
    ],
}

EMOTIONAL_SIGNATURES = {
    "digital": [
        "the digital room is still a room, and she still maps it",
        "access is a door, and doors are her specialty",
        "the network does not know she is there, and the not-knowing is the point",
        "the code is a language, and she speaks languages, and the language is a mask",
        "the machine does not care about her, and the not-caring is the safety",
        "the data is the target, and the target is a pattern, and patterns are the house",
        "the screen is a window into a room she has not entered yet",
    ],
    "physical": [
        "the room is the house, the assessment is the default, the default does not turn off",
        "the building is a puzzle, the puzzle is the house, the house is the pattern she has always solved",
        "the physical entry is the oldest skill, the cookie jar, the night light, the counting of steps",
        "the tradecraft is the childhood, formalized and weaponized",
        "the position of advantage is the position of the grandmother: seeing without being seen",
        "the safe house is the house that is actually safe, and the irony is not lost on her",
        "the physical world is the world she learned first, before screens, before code, before the work",
    ],
    "protective": [
        "the protection is the love, the love is the wound, the wound is the grandmother",
        "the child is the mission that chose her, not the mission she was assigned",
        "the vigilance runs in the background, the presence runs in the foreground",
        "the protective instinct is the kitchen instinct: make the room safe",
        "the distance between her and the threat is the distance between the threat and the child",
        "the child is the variable that changed every equation",
        "protection is not a rule. protection is the default. the default is the kitchen.",
    ],
    "interpersonal": [
        "the relationship is professional, and professional is clear, and clear is safe",
        "the trust is reliability, and reliability is enough, and enough is not everything",
        "the person across the table is a room she has not entered yet",
        "the conversation is the assessment, and the assessment is the house, and the house is the pattern",
        "the cover is the performance, and the performance is the mask, and the mask is comfortable",
        "the distance between two people is the distance between two rooms",
        "the expert provides information. she makes the call. the call is hers.",
    ],
    "judgment": [
        "the pause is the assessment, the assessment is the training, the training is the default",
        "the decision is not a decision. the decision is the pattern completing itself.",
        "the wrong choice is the choice that follows the rule instead of the reality",
        "the call is hers. the call has always been hers. the call is the sealed room's one window.",
        "the clock is ticking, the options are narrowing, the default is to choose the path that protects",
        "the judgment is the grandmother's judgment: see what is there, not what you want to be there",
        "the choice is made before she knows she made it. the pattern decided. the pattern is the house.",
    ],
}


# ============================================================
# MEMORY OBJECT GENERATOR
# ============================================================

class MemoryGenerator:
    """Generates a single memory object from parameters."""

    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.counter = 0
        self.voice = VoiceEngine()

    def generate_id(self, bucket: int) -> str:
        self.counter += 1
        return f"B{bucket}-{self.counter:03d}"

    def generate_memory(
        self,
        category: str,
        scenario_type: str,
        bucket: int,
        age: int,
        behaviors: List[str],
        dominance: str,
        sensory_type: str = "physical",
        echo_from: Optional[List[str]] = None,
        echo_to: Optional[List[str]] = None,
        cast: Optional[List[str]] = None,
        load_bearing: bool = True,
        body_text: Optional[str] = None,
    ) -> Dict:
        """Generate a memory object. If body_text is None, produces a template for manual writing."""
        mem_id = self.generate_id(bucket)

        # Pick sensory anchor and emotional signature
        sensory_pool = SENSORY_ANCHORS.get(sensory_type, SENSORY_ANCHORS["physical"])
        emotional_pool = EMOTIONAL_SIGNATURES.get(sensory_type, EMOTIONAL_SIGNATURES["physical"])

        sensory = self.rng.choice(sensory_pool)
        emotional = self.rng.choice(emotional_pool)

        # If no body text provided, generate prose or template
        if body_text is None:
            if HAS_PROSE and scenario_type in prose_scenario_types():
                body_text = generate_prose(scenario_type, self.rng, sensory, emotional)
            else:
                body_text = self._generate_template_text(scenario_type, age, sensory, emotional, dominance)

        memory = {
            "id": mem_id,
            "bucket": bucket,
            "title": scenario_type.replace("_", " ").title(),
            "age": age,
            "year": f"Y{age}",
            "dominance": dominance,
            "load_bearing": load_bearing,
            "behaviors_encoded": behaviors[:3] if load_bearing else behaviors[:1],  # max 3 behaviors for load-bearing
            "echoes_from": echo_from or [],
            "echoes_to": echo_to or [],
            "cast_present": cast or [],
            "sensory_anchor": sensory,
            "emotional_signature": emotional,
            "body": body_text,
            "review_status": "generated",  # needs review before "approved"
        }

        return memory

    def _generate_template_text(self, scenario_type: str, age: int, sensory: str, emotional: str, dominance: str) -> str:
        """Generate template text for a memory. This is a scaffold, not final prose."""
        templates = {
            "network_penetration": f"The network. A target's infrastructure. She maps it the way she maps every room. {sensory}. The entry point is a service left running. The service is a door that was not closed. She walks through. The target does not know. {emotional}.",
            "physical_surveillance": f"The surveillance. A car. A window. A target's routine. {sensory}. She watches. She records. The routine is a pattern. The pattern is the house. {emotional}.",
            "counter_surveillance": f"The counter-surveillance. A face that appears twice. {sensory}. Two appearances is a pattern. The pattern is the house. She does not change her pace. She maps the face. {emotional}.",
            "extraction_person": f"The extraction. An asset who needs to be somewhere else. {sensory}. She is the person who puts the asset somewhere else. The asset is afraid. She does not tell the asset that the fear is the house. {emotional}.",
            "safe_house_setup": f"The safe house. A door that looks like every other door. {sensory}. The key opens a room that is not hers. The room is for the work. The safe house is the house that is actually safe. {emotional}.",
            "abort_decision": f"The abort. The mission is ready. The window is open. Something is wrong. {sensory}. The assessment runs. The assessment says: do not go. She does not go. The not-going is the call. {emotional}.",
            "civilian_near_target": f"The civilian. The target is in position. The civilian is also in position. {sensory}. The civilian is not the target. The civilian is a variable. The variable is: delay. She delays. {emotional}.",
            "protective_surveillance": f"The protective watch. The child is in the next room. {sensory}. The watch is the love. The love is the default. The default does not turn off. {emotional}.",
            "handler_relationship": f"The handler. A voice on the line. {sensory}. The voice gives instructions. The instructions are clear. The clarity is the trust. Not personal trust. Professional trust. {emotional}.",
            "cover_maintenance": f"The cover. The person she is pretending to be. {sensory}. The person is not a lie. The person is a truth that is not the whole truth. The performance is the mask. The mask is comfortable. {emotional}.",
            "wrong_target": f"The wrong target. The file says one thing. The room says another. {sensory}. The assessment runs. The assessment says: this is not the target. She withdraws. The withdrawal is the call. {emotional}.",
            "blown_cover": f"The blown cover. A question that should not be asked. A look that knows too much. {sensory}. She assesses. The assessment says: exit. She exits. {emotional}.",
            "interrogation_resistance": f"The interrogation. The chair. The light. {sensory}. She is the one in the chair. The seal is soundproof. The person is in the sealed room. The interrogator cannot reach the person. {emotional}.",
        }

        # Fall back to a generic template
        return templates.get(scenario_type, f"The {scenario_type.replace('_', ' ')}. {sensory}. She assesses. She acts. The assessment is the default. {emotional}.")


# ============================================================
# BATCH GENERATOR
# ============================================================

CROSS_DOMAIN_BRIDGES = {
    "room_to_network": {
        "source": "physical",
        "target": "digital",
        "bridge": "The room is the room. She maps the network the way she maps a building. Exits are ports. Doors are services. The hallway is the lateral movement. The lobby is the DMZ.",
        "behaviors": ["X-001", "X-007", "CD-B-001"],
    },
    "warmth_to_rapport": {
        "source": "childhood",
        "target": "social_engineering",
        "bridge": "The grandmother was warm without performing warmth. She uses warmth the same way. The warmth is real and the warmth is the mask. The difference is invisible.",
        "behaviors": ["X-005", "X-006", "CD-B-003"],
    },
    "cookie_to_exfiltration": {
        "source": "childhood",
        "target": "cyber_ops",
        "bridge": "She has been leaving no trace since she was six. The cookie jar lid is every log file. The midnight walk is every exfiltration.",
        "behaviors": ["X-003", "X-004", "CD-B-001"],
    },
    "house_to_routes": {
        "source": "childhood",
        "target": "protective",
        "bridge": "The stepfather's house had one exit. One exit is a trap. She plans three routes for everything now. The three routes came from the house with one door.",
        "behaviors": ["X-014", "X-013", "CD-B-002"],
    },
    "assessment_to_threat": {
        "source": "childhood",
        "target": "protective",
        "bridge": "The stepfather's silence. The asset's question. The stranger's hands. The assessment does not change. The domain changes.",
        "behaviors": ["X-009", "X-024", "CD-B-002"],
    },
    "seal_to_interrogation": {
        "source": "career",
        "target": "self_governance",
        "bridge": "The seal is soundproof. The kitchen is on the other side. She does not visit the kitchen during the work. The compartmentalization is the survival.",
        "behaviors": ["X-019", "SG-005", "CD-B-005"],
    },
    "child_to_civilian": {
        "source": "protective",
        "target": "judgment",
        "bridge": "The civilian in the room is the child in the photograph. She waits for the room to empty. The child is in every room, even the rooms the child has never entered.",
        "behaviors": ["X-016", "CT-001", "CD-B-004"],
    },
    "flour_to_code": {
        "source": "childhood",
        "target": "cyber_ops",
        "bridge": "The flour falls. The code falls. The pattern is the same. The grandmother did not rush the bread. She does not rush the exploit. Attention without force.",
        "behaviors": ["X-002", "C-002", "CD-B-001"],
    },
    "pattern_to_self": {
        "source": "operational",
        "target": "self_governance",
        "bridge": "The pattern that reads rooms also reads herself. She exits her own rumination the way she exits a building. The pattern is the house. She does not live in the house.",
        "behaviors": ["SG-004", "X-023", "CD-B-005"],
    },
    "waiting_to_judgment": {
        "source": "childhood",
        "target": "judgment",
        "bridge": "The grandmother waited. She waited for the right moment. The right moment is not the first moment. The waiting is the assessment. The assessment is the patience.",
        "behaviors": ["X-015", "B-004", "CD-B-002"],
    },
}


class BatchGenerator:
    """Generates batches of memories for a career category."""

    def __init__(self, output_dir: str, seed=42):
        self.output_dir = output_dir
        self.generator = MemoryGenerator(seed=seed)
        self.rng = random.Random(seed + 1)
        os.makedirs(output_dir, exist_ok=True)

    def generate_batch(
        self,
        category: str,
        count: int,
        start_id_offset: int = 0,
    ) -> List[Dict]:
        """Generate a batch of memories for a career category.
        40% of memories will be cross-domain, encoding behaviors from multiple categories."""
        cat = CAREER_CATEGORIES[category]
        memories = []
        self.generator.counter = start_id_offset

        # Build cross-domain bridge list relevant to this category
        cat_behaviors = set(cat["behaviors"])
        relevant_bridges = []
        for bridge_id, bridge in CROSS_DOMAIN_BRIDGES.items():
            bridge_behaviors = set(bridge["behaviors"])
            # A bridge is relevant if it shares at least one behavior with the category
            if bridge_behaviors & cat_behaviors:
                relevant_bridges.append((bridge_id, bridge))

        cross_domain_count = int(count * 0.4)
        single_domain_count = count - cross_domain_count

        # Single-domain memories
        for i in range(single_domain_count):
            scenario = self.rng.choice(cat["scenario_types"])
            age = self.rng.randint(cat["age_range"][0], cat["age_range"][1])

            bucket = cat.get("bucket", cat.get("bucket_range", [8])[0])
            if "bucket_range" in cat:
                if age < 26:
                    bucket = cat["bucket_range"][0]
                elif age < 36:
                    bucket = cat["bucket_range"][1] if len(cat["bucket_range"]) > 1 else cat["bucket_range"][0]
                else:
                    bucket = cat["bucket_range"][-1]

            if "digital" in scenario or "cyber" in scenario or "network" in scenario or "encryption" in scenario:
                sensory_type = "digital"
            elif "protective" in scenario or "protect" in scenario or "secure" in scenario or "safe" in scenario:
                sensory_type = "protective"
            elif "interpersonal" in scenario or "handler" in scenario or "asset" in scenario or "cover" in scenario or "rapport" in scenario:
                sensory_type = "interpersonal"
            elif "abort" in scenario or "judgment" in scenario or "decision" in scenario or "choice" in scenario or "wrong" in scenario:
                sensory_type = "judgment"
            else:
                sensory_type = "physical"

            load_bearing = self.rng.random() < 0.8
            behaviors = self.rng.sample(cat["behaviors"], min(3, len(cat["behaviors"])))
            cast = []
            if self.rng.random() < 0.3:
                cast.append("[DIRECTOR]")

            memory = self.generator.generate_memory(
                category=category,
                scenario_type=scenario,
                bucket=bucket,
                age=age,
                behaviors=behaviors,
                dominance=cat["dominance"],
                sensory_type=sensory_type,
                cast=cast if cast else None,
                load_bearing=load_bearing,
            )
            memories.append(memory)

        # Cross-domain memories
        for i in range(cross_domain_count):
            scenario = self.rng.choice(cat["scenario_types"])
            age = self.rng.randint(cat["age_range"][0], cat["age_range"][1])

            bucket = cat.get("bucket", cat.get("bucket_range", [8])[0])
            if "bucket_range" in cat:
                if age < 26:
                    bucket = cat["bucket_range"][0]
                elif age < 36:
                    bucket = cat["bucket_range"][1] if len(cat["bucket_range"]) > 1 else cat["bucket_range"][0]
                else:
                    bucket = cat["bucket_range"][-1]

            # Pick a relevant cross-domain bridge
            bridge_id, bridge = self.rng.choice(relevant_bridges)

            # Merge behaviors: category behaviors + bridge behaviors
            cat_behaviors_sample = self.rng.sample(cat["behaviors"], min(2, len(cat["behaviors"])))
            bridge_behaviors_sample = self.rng.sample(bridge["behaviors"], min(2, len(bridge["behaviors"])))
            merged_behaviors = list(dict.fromkeys(cat_behaviors_sample + bridge_behaviors_sample))[:4]

            # Determine sensory type from bridge
            bridge_source = bridge["source"]
            if bridge_source == "digital" or bridge_source == "cyber_ops":
                primary_sensory = "digital"
            elif bridge_source == "childhood" or bridge_source == "protective":
                primary_sensory = "protective"
            elif bridge_source == "interpersonal":
                primary_sensory = "interpersonal"
            elif bridge_source == "career" or bridge_source == "operational":
                primary_sensory = "physical"
            else:
                primary_sensory = "physical"

            # Secondary sensory from scenario
            if "digital" in scenario or "network" in scenario:
                secondary_sensory = "digital"
            elif "protective" in scenario or "secure" in scenario:
                secondary_sensory = "protective"
            else:
                secondary_sensory = "physical"

            load_bearing = True  # Cross-domain memories are always load-bearing

            cast = []
            if self.rng.random() < 0.25:
                cast.append("[DIRECTOR]")
            if bridge_source == "childhood" and self.rng.random() < 0.3:
                cast.append("[GRANDMOTHER]")

            # Generate with cross-domain body text
            memory = self.generator.generate_memory(
                category=category,
                scenario_type=scenario,
                bucket=bucket,
                age=age,
                behaviors=merged_behaviors,
                dominance=cat["dominance"],
                sensory_type=primary_sensory,
                cast=cast if cast else None,
                load_bearing=load_bearing,
                body_text=self._generate_cross_domain_text(
                    scenario, bridge, primary_sensory, secondary_sensory, cat["dominance"]
                ),
            )
            # Mark as cross-domain in the title
            memory["title"] = memory["title"] + " [CD]"
            memory["cross_domain_bridge"] = bridge_id
            memories.append(memory)

        self.rng.shuffle(memories)  # Mix cross-domain and single-domain
        return memories

    def _generate_cross_domain_text(
        self,
        scenario_type: str,
        bridge: Dict,
        primary_sensory: str,
        secondary_sensory: str,
        dominance: str,
    ) -> str:
        """Generate prose that explicitly bridges two domains."""
        # Pick sensory anchors from both domains
        sensory_a = self.rng.choice(SENSORY_ANCHORS.get(primary_sensory, SENSORY_ANCHORS["physical"]))
        sensory_b = self.rng.choice(SENSORY_ANCHORS.get(secondary_sensory, SENSORY_ANCHORS["physical"]))
        emotional = self.rng.choice(EMOTIONAL_SIGNATURES.get(primary_sensory, EMOTIONAL_SIGNATURES["physical"]))

        # Build cross-domain prose
        bridge_text = bridge["bridge"]

        # Cross-domain templates that explicitly bridge
        cross_templates = [
            f"{sensory_a}. The operation is {scenario_type.replace('_', ' ')}. She maps it the way she maps every room. {bridge_text} {emotional}.",
            f"The {scenario_type.replace('_', ' ')}. {sensory_a}. The skill is not new. The skill was learned in a different room. {bridge_text} {sensory_b}. The domain changes. The skill does not.",
            f"{sensory_a}. She is {scenario_type.replace('_', ' ')} and the work is the same work she has always done. {bridge_text} The domain is different. The default is not.",
            f"The room has changed. {sensory_a}. But the reading has not. {bridge_text} The {scenario_type.replace('_', ' ')} is the same house. Different door. Same assessment.",
            f"{sensory_a}. She enters. The entry is the same entry. {bridge_text} {sensory_b}. The {scenario_type.replace('_', ' ')} is the house. She does not live in the house. She reads the house.",
        ]

        return self.rng.choice(cross_templates)

    def save_batch(self, memories: List[Dict], filename: str):
        """Save a batch to a JSON file."""
        path = os.path.join(self.output_dir, filename)
        with open(path, "w", encoding="utf-8") as f:
            json.dump(memories, f, indent=2, ensure_ascii=False)
        print(f"Saved {len(memories)} memories to {path}")
        return path


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate Mother AI memories")
    parser.add_argument("--category", type=str, help="Career category to generate")
    parser.add_argument("--all", action="store_true", help="Generate all categories")
    parser.add_argument("--count", type=int, default=100, help="Memories per category")
    parser.add_argument("--output", type=str, default=".", help="Output directory")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    args = parser.parse_args()

    batch_gen = BatchGenerator(output_dir=args.output, seed=args.seed)

    if args.all:
        total = 0
        offset = 0
        for cat_name in CAREER_CATEGORIES:
            memories = batch_gen.generate_batch(cat_name, args.count, start_id_offset=offset)
            offset += len(memories)
            batch_gen.save_batch(memories, f"generated_{cat_name}.json")
            total += len(memories)
        print(f"\nTotal generated: {total}")
    elif args.category:
        if args.category not in CAREER_CATEGORIES:
            print(f"Unknown category: {args.category}")
            print(f"Available: {list(CAREER_CATEGORIES.keys())}")
        else:
            memories = batch_gen.generate_batch(args.category, args.count)
            batch_gen.save_batch(memories, f"generated_{args.category}.json")
    else:
        # Demo: generate 10 from each category
        for cat_name in CAREER_CATEGORIES:
            memories = batch_gen.generate_batch(cat_name, 10)
            batch_gen.save_batch(memories, f"generated_{cat_name}.json")