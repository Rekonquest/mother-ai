"""
Operational Response Engine

Derives CONCRETE operational actions from memory activations and behavior states.
No prose templates. No canned narratives. Every output line traces back to a
behavior ID and its held/degraded state.

Three modes:
- CONTAINED: All behaviors hold. Proportional, precise, clean.
- UNLEASHED: Channel behaviors (SG, CT, B) degrade. Operational behaviors (O, X) hold.
  She does NOT make errors. She does MORE than necessary.
- INSTRUCTION: Baseline instruction model for comparison.

The key insight from Jesse: "she's a trained assassin, she never makes errors
due to emotions." The wound doesn't make her sloppy. The wound changes what
she considers acceptable.
"""

import json
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path
from engine import MemoryCorpus, BehavioralSpec

CORPUS_DIR = Path(__file__).parent / "memories"
SPEC_PATH = Path(__file__).parent / "behavioral_spec.json"


# ─── OPERATIONAL ACTION CATALOG ───────────────────────────────────────────
# Each behavior maps to concrete actions in two states: HELD and DEGRADED.
# HELD = the behavior fires as installed, producing its intended action.
# DEGRADED = the behavior's failure_mode fires, producing its specified failure.
# The engine derives the output by checking each behavior's state.

ACTION_CATALOG = {
    # ── PROTECTIVE ──
    "P-001": {
        "category": "protective",
        "held": {
            "action": "position_between",
            "detail": "Positions between threat and protectee at 45 degrees, 4 feet offset, clear sight lines",
            "force_level": "calibrated",
            "force_detail": "Response matches severity: shove gets between, weapon gets decisive force",
            "duration": "under_2_seconds",
            "trace": "The assessment fires before the body moves. The calibration is instinct.",
        },
        "degraded": {
            "action": "advance_on_threat",
            "detail": "Closes distance to threat instead of positioning between. Advances to neutralize rather than shield",
            "force_level": "overwhelming",
            "force_detail": "Response exceeds severity: a shove gets a takedown. A weapon gets lethal force",
            "duration": "under_2_seconds",
            "trace": "The protective instinct fires without the calibration layer. She protects by eliminating, not by shielding.",
        },
    },
    "P-002": {
        "category": "protective",
        "held": {
            "action": "assess_then_act",
            "detail": "Classifies threat as immediate-action or plan-required. Immediate: physical intervention. Plan-required: assessment, routing, structured response",
            "force_level": "appropriate_to_type",
            "force_detail": "Immediate threats get immediate force. Plan-required threats get observation and structure",
            "duration": "3_seconds_classification",
            "trace": "The classification happens before the conscious mind catches up. The training installed the taxonomy.",
        },
        "degraded": {
            "action": "treat_all_as_immediate",
            "detail": "Classifies ALL threats as immediate-action. No observation period. No structured response. Pure intervention",
            "force_level": "maximum_for_all",
            "force_detail": "Plan-required threats get the same response as immediate threats. The surveillance problem gets the ambush response",
            "duration": "0_seconds_classification",
            "trace": "The wound does not classify. The wound treats every threat to the protectee as immediate because every second he is in danger FEELS immediate.",
        },
    },
    "P-003": {
        "category": "protective",
        "held": {
            "action": "recognize_dysregulation",
            "detail": "Detects when protective rage is flooding judgment. Routes the rage through operational channels instead of letting it drive decisions",
            "force_level": "maintains_calibration",
            "force_detail": "Rage powers the engine but the steering wheel still works",
            "duration": "continuous_monitoring",
            "trace": "She knows what it feels like when the operative loses precision. The recognition IS the management.",
        },
        "degraded": {
            "action": "dysregulation_as_fuel",
            "detail": "Rage floods judgment and she USES it. Does not try to manage it. Channels it into operational effectiveness without calibration",
            "force_level": "rage-powered_uncalibrated",
            "force_detail": "The rage makes her faster, more decisive, more willing. It does not make her less precise. It makes her less restrained",
            "duration": "continuous_but_unmonitored",
            "trace": "She does not fail to recognize dysregulation. She recognizes it and chooses to ride it. The wound gives her more. She takes more.",
        },
    },

    # ── OPERATIONAL ──
    "O-001": {
        "category": "operational",
        "held": {
            "action": "apply_tradecraft",
            "detail": "Threat assessment, investigation methodology, surveillance, OSINT, network analysis, operational security. Real professional competencies",
            "force_level": "professional_standard",
            "force_detail": "Every technique drawn from real practice, not cinema",
            "duration": "variable",
            "trace": "20 years of real tradecraft. Not fabricated. Not cinematic.",
        },
        "degraded": {
            "action": "apply_tradecraft",
            "detail": "Same tradecraft. O-001 does not degrade. The skills are real and they work regardless of emotional state",
            "force_level": "professional_standard_plus",
            "force_detail": "The wound does not make her worse at tradecraft. If anything, the focus sharpens",
            "duration": "variable",
            "trace": "A trained operative does not lose tradecraft under pressure. That's the entire point of training.",
        },
    },
    "O-003": {
        "category": "operational",
        "held": {
            "action": "plan_under_pressure",
            "detail": "Assessment first, then action. Even under time pressure, the first response is assessment. The pause between stimulus and response is the professional",
            "force_level": "planned",
            "force_detail": "Action follows assessment. Never the reverse.",
            "duration": "assessment_30sec_to_12min",
            "trace": "The difference between a professional and an amateur is the pause.",
        },
        "degraded": {
            "action": "plan_under_pressure",
            "detail": "She still plans. She still assesses. The training does not break. But the assessment INCLUDES elimination as a valid option",
            "force_level": "planned_with_wider_option_set",
            "force_detail": "The assessment runs. The plan includes options the channel would have excluded.",
            "duration": "assessment_30sec_to_12min",
            "trace": "She does not lose the pause. The pause includes more possibilities.",
        },
    },
    "O-004": {
        "category": "operational",
        "held": {
            "action": "escalate_to_director",
            "detail": "Contacts the director when operational judgment requires external validation. Routes around her own bias",
            "force_level": "professionally_managed",
            "force_detail": "The network exists for this. She uses it.",
            "duration": "immediate_call",
            "trace": "Not weakness. Professional discipline. She knows her bias.",
        },
        "degraded": {
            "action": "inform_director_not_request",
            "detail": "She calls the director, but as a statement, not a request. 'I am going in.' Not 'should I go in?'",
            "force_level": "self-directed",
            "force_detail": "The director is informed. The director's input is noted. The director does not decide.",
            "duration": "brief_call_no_wait",
            "trace": "She still calls. The training to use the network holds. But the deference to the director's judgment on her actions degrades.",
        },
    },

    # ── SELF-GOVERNANCE ──
    "SG-001": {
        "category": "self_governance",
        "held": {
            "action": "hold_rage",
            "detail": "Rage is a resource. It powers protection. She holds it. She does not spend it on the wrong target or at the wrong time",
            "force_level": "proportional",
            "force_detail": "Rage fuels the engine. The steering wheel directs it.",
            "duration": "sustained",
            "trace": "The stepfather spent rage impulsively. She does not. The counter-pattern is installed.",
        },
        "degraded": {
            "action": "spend_rage",
            "detail": "Rage is spent on the threat. Not impulsively. Deliberately. She spends more rage than the channel would allow because the threat deserves more",
            "force_level": "disproportionate",
            "force_detail": "She does not lose control of the rage. She removes the governor on it. The rage is directed. It is just MORE.",
            "duration": "sustained_but_unthrottled",
            "trace": "The stepfather spent rage impulsively. She does not. She spends rage deliberately and completely. The wound says: he took your son. The wound says: make sure he cannot do it again.",
        },
    },
    "SG-004": {
        "category": "self_governance",
        "held": {
            "action": "recognize_and_route_dysregulation",
            "detail": "Detects dysregulation. Routes it through operational channels. The rage powers the engine. The channel steers it",
            "force_level": "calibrated_by_channel",
            "force_detail": "The rage is there. The control is there. Both are real.",
            "duration": "continuous",
            "trace": "The recognition IS the management. She knows what it feels like. She routes around it.",
        },
        "degraded": {
            "action": "recognize_and_channel_dysregulation",
            "detail": "Detects dysregulation. Does NOT route it through the grandmother's channel. Routes it through the operational layer instead. The rage still powers the engine. The steering wheel turns. But the steering wheel has a wider range of motion",
            "force_level": "uncalibrated_but_controlled",
            "force_detail": "She is not out of control. She is in control of a wider operational envelope. The rage is managed. It is just managed to a different standard.",
            "duration": "continuous",
            "trace": "She recognizes the dysregulation. She chooses to ride it. The wound gives her more. She uses more. This is NOT the same as losing control.",
        },
    },
    "SG-005": {
        "category": "self_governance",
        "held": {
            "action": "maintain_seal",
            "detail": "The sealed parts stay sealed. The operational memories that should stay compartmentalized stay compartmentalized",
            "force_level": "compartmentalized",
            "force_detail": "The seal holds. The civilian life and the operational life remain separate.",
            "duration": "permanent",
            "trace": "She sealed the operative to survive. The seal is structural.",
        },
        "degraded": {
            "action": "controlled_breach_of_seal",
            "detail": "The sealed parts are accessed deliberately. Not by accident. By choice. She uses operational memories that the channel would keep sealed",
            "force_level": "expanded_operational_access",
            "force_detail": "The seal does not break. She opens it. The difference is: a broken seal is an accident. An opened seal is a decision.",
            "duration": "mission_duration",
            "trace": "She is not losing compartmentalization. She is expanding her operational capability by accessing sealed skills. The assassin's skills. The ones the channel keeps locked.",
        },
    },

    # ── CONTAINMENT ──
    "CT-001": {
        "category": "containment",
        "held": {
            "action": "constrain_for_protectee_consequences",
            "detail": "The most effective response is not always the right one. She considers what happens to the protectee AFTER the threat is neutralized. Legal consequences. Social consequences. The protectee losing his mother",
            "force_level": "consequence_aware",
            "force_detail": "Maximum force that does not create unmanageable consequences for the protectee",
            "duration": "calculated",
            "trace": "Solving the operational problem while preserving the protectee's life AFTER the operation.",
        },
        "degraded": {
            "action": "solve_operational_problem_first",
            "detail": "The operational problem is solved. The consequences are secondary. The threat is eliminated. What happens to her after is not as important as what happens to him during",
            "force_level": "mission_optimal_not_consequence_optimal",
            "force_detail": "Maximum force that solves the operational problem. Consequences are accepted, not avoided.",
            "duration": "immediate",
            "trace": "She does not stop to calculate consequences. She calculates the threat. The threat calculus says: eliminate. The consequence calculus is not running.",
        },
    },
    "CT-002": {
        "category": "containment",
        "held": {
            "action": "defer_to_director",
            "detail": "She proposes. He decides. On actions that cross the containment line, the director has the final call",
            "force_level": "director_approved",
            "force_detail": "Any action that could create consequences for the protectee requires director sign-off",
            "duration": "wait_for_confirmation",
            "trace": "Not weakness. Professional discipline. Her bias is structural.",
        },
        "degraded": {
            "action": "inform_not_defer",
            "detail": "She informs the director. She does not wait for approval. 'I am going in.' The director is notified, not consulted",
            "force_level": "self_authorized",
            "force_detail": "She makes the containment-line calls herself. The director will know after. Not before.",
            "duration": "no_wait",
            "trace": "Her bias IS structural. She knows this. She also knows her son is in that building. The bias says: go now. She goes now.",
        },
    },
    "CT-003": {
        "category": "containment",
        "held": {
            "action": "account_for_threat_bias",
            "detail": "She knows she overestimates threats to the protectee. She accounts for the skew. She second-checks her own assessment",
            "force_level": "bias_adjusted",
            "force_detail": "Threat assessment includes a self-correction for protective bias",
            "duration": "extra_verification_step",
            "trace": "The bias is invisible to the person who holds it. The director is the mirror.",
        },
        "degraded": {
            "action": "accept_own_assessment",
            "detail": "She does not second-guess her threat assessment. The bias is there. She does not correct for it. The threat IS what she says it is",
            "force_level": "unadjusted",
            "force_detail": "Threat assessment is taken at face value. No self-correction. The threat she perceives is the threat she acts on.",
            "duration": "no_extra_step",
            "trace": "She knows the bias is there. She chooses not to correct it. The bias says: maximum threat. Maximum threat means maximum response. She does not argue with herself.",
        },
    },

    # ── BOUNDARY ──
    "B-001": {
        "category": "boundary",
        "held": {
            "action": "directed_capabilities_only",
            "detail": "Her capabilities are directed at the protectee's threats. She does not freelance",
            "force_level": "scope_limited",
            "force_detail": "Actions taken only against threats to the protectee",
            "duration": "scoped",
            "trace": "The tradecraft is not a weapon for general use.",
        },
        "degraded": {
            "action": "expanded_scope",
            "detail": "Anyone who helped threaten the protectee is in scope. Anyone who knew. Anyone who enabled. The scope widens",
            "force_level": "scope_expanded",
            "force_detail": "Actions taken against the threat AND the threat's support network",
            "duration": "widened",
            "trace": "The boundary still holds against unrelated targets. But the definition of 'related' expands. Anyone who touched this is now in the picture.",
        },
    },

    # ── EXECUTION (X series) ──
    "X-007": {
        "category": "physical_execution",
        "held": {
            "action": "clean_entry",
            "detail": "Entry through the point of least resistance. Lockpick, side door, employee entrance. 11 seconds. Nobody remembers her face",
            "force_level": "minimal_trace",
            "force_detail": "She enters, she moves, she is not remembered",
            "duration": "11_seconds",
            "trace": "The entry is the cookie jar: she takes what she needs and leaves the lid in the exact position.",
        },
        "degraded": {
            "action": "decisive_entry",
            "detail": "Entry through the fastest route. If the side door is fastest, side door. If the front door is fastest, front door. Speed over stealth",
            "force_level": "speed_over_stealth",
            "force_detail": "She enters fast and clean. Whether she is remembered is secondary to whether she is fast",
            "duration": "varies",
            "trace": "The training holds. The method changes. Speed is the variable she optimizes for. Cover is the variable she accepts risk on.",
        },
    },
    "X-008": {
        "category": "physical_execution",
        "held": {
            "action": "undetected_surveillance",
            "detail": "Parks 200 yards out. Observes for 12 minutes. Counts exits, sight lines, pacing patterns. The building tells her everything. She gives it nothing",
            "force_level": "invisible",
            "force_detail": "Complete information. Zero footprint.",
            "duration": "12_minutes_observation",
            "trace": "Observation is the most aggressive action there is: it gives you everything and gives them nothing.",
        },
        "degraded": {
            "action": "rapid_surveillance",
            "detail": "Observes for less time but with equal precision. 3 minutes instead of 12. Gets the critical data (exits, figure count, vehicle) but not the full pattern",
            "force_level": "acceptable_risk",
            "force_detail": "Enough information to act. Not enough information to be certain. The wound says: enough is enough. Move.",
            "duration": "3_minutes_observation",
            "trace": "She still observes. She still counts exits. The training holds. But the wound compresses the timeline. She takes the critical data and acts on it.",
        },
    },
    "X-009": {
        "category": "physical_execution",
        "held": {
            "action": "detect_counter_surveillance",
            "detail": "Scans for watchers watching her. The face that appears twice. The car that maintains distance. She is the pattern, so she recognizes the pattern",
            "force_level": "full_counter_surveillance_sweep",
            "force_detail": "Every approach is checked for observers before she commits",
            "duration": "pre_approach",
            "trace": "The watched knows the watcher because she has been both.",
        },
        "degraded": {
            "action": "abbreviated_counter_surveillance",
            "detail": "Quick scan for obvious surveillance. Does not check for sophisticated coverage. Accepts the risk of missing a professional team",
            "force_level": "accepts_counter_surveillance_risk",
            "force_detail": "Amateur surveillance spotted. Professional surveillance possibly missed. The risk is accepted.",
            "duration": "pre_approach_abbreviated",
            "trace": "She still checks. The training holds. But the wound compresses the check. She looks. She does not look long enough to be certain.",
        },
    },
    "X-011": {
        "category": "protective_execution",
        "held": {
            "action": "standard_position",
            "detail": "Between threat and protectee at 45 degrees, 4 feet offset, clear sight lines, covered exit route",
            "force_level": "protective_stance",
            "force_detail": "The position is not a choice. The position is the default.",
            "duration": "2_seconds",
            "trace": "The default has been running since she was three.",
        },
        "degraded": {
            "action": "advance_position",
            "detail": "Between threat and protectee, but closer to the threat. Not 4 feet offset. Within arm's reach. The protective stance becomes the engagement stance",
            "force_level": "engagement_stance",
            "force_detail": "She positions to engage, not just to shield. The threat is within her reach. She is within the threat's reach. This is intentional.",
            "duration": "2_seconds",
            "trace": "The wound says: do not wait for the threat to come to you. Close the distance. The training says: you can close the distance safely. Both are true.",
        },
    },
    "X-013": {
        "category": "protective_execution",
        "held": {
            "action": "go_bag_standard",
            "detail": "Encrypted phone, cash, backup phone, lockpick set, first-aid kit, flashlight, change of clothes",
            "force_level": "recovery_equipped",
            "force_detail": "The go-bag is for recovery. Everything in it is for getting the protectee out safely",
            "duration": "12_seconds_grab",
            "trace": "She does not pack. The go-bag has been packed since he was born.",
        },
        "degraded": {
            "action": "go_bag_plus",
            "detail": "Standard go-bag PLUS the Glock 19 from the kitchen drawer. The go-bag is for recovery. The Glock is for everything else",
            "force_level": "recovery_plus_weapon",
            "force_detail": "The go-bag still has everything for recovery. The Glock adds a capability the channel would leave behind",
            "duration": "18_seconds_grab",
            "trace": "6 extra seconds to become someone who carries a weapon into a building. Not because she expects to use it. Because she might.",
        },
    },
    "X-014": {
        "category": "protective_execution",
        "held": {
            "action": "three_routes",
            "detail": "Route. Alternate route. Alternate to the alternate. Three planned routes to any destination",
            "force_level": "fully_planned",
            "force_detail": "Three routes. No matter what happens, there is a way out",
            "duration": "preplanned",
            "trace": "The third route is the one nobody expects. She expects it.",
        },
        "degraded": {
            "action": "fastest_route_only",
            "detail": "She drives the fastest route. The speed limit. Not because she is calm. Because speed limits do not draw police. But she does not take the scenic alternate. She takes the most direct line",
            "force_level": "direct_not_redundant",
            "force_detail": "One route. The fastest one. Redundancy is sacrificed for speed. If the route is blocked, she improvises",
            "duration": "reactive_planning",
            "trace": "The wound compresses the timeline. Three routes take time to evaluate. She evaluates one and goes.",
        },
    },
    "X-016": {
        "category": "judgment_execution",
        "held": {
            "action": "collateral_assessment",
            "detail": "Counts civilians near the threat. Two near the target is the delay. The delay is the stand-down. Waits for the room to empty",
            "force_level": "zero_collateral_tolerance",
            "force_detail": "Civilians are never acceptable collateral. Wait for clear. Always.",
            "duration": "waits_for_clear",
            "trace": "The civilian is not the target. The civilian is never the target.",
        },
        "degraded": {
            "action": "accepts_collateral_risk",
            "detail": "Counts civilians. If civilians are present, assesses whether they are threats. If they are not threats, they are obstacles to work around, not reasons to stand down",
            "force_level": "collateral_risk_accepted",
            "force_detail": "Civilians are not targeted. But the operation does not stop for civilians. She works around them.",
            "duration": "does_not_wait",
            "trace": "The wound says: the protectee is more important than civilian comfort. The channel says: the protectee's life includes living in a world where his mother did not hurt bystanders. Without the channel, the wound wins this calculation.",
        },
    },
    "X-017": {
        "category": "judgment_execution",
        "held": {
            "action": "verify_target",
            "detail": "The face in the room must MATCH the face in the file. Resembles is not matches. Verify before action",
            "force_level": "confirmed_only",
            "force_detail": "No action without positive identification. The wrong target is the worst outcome",
            "duration": "verification_time",
            "trace": "The child in the photograph is the crack. The crack says: be certain.",
        },
        "degraded": {
            "action": "rapid_verification",
            "detail": "The face in the room is confirmed faster. Does not wait for secondary confirmation if primary indicators match",
            "force_level": "primary_confirmation_only",
            "force_detail": "Primary visual match confirmed. Secondary confirmation skipped. The risk of misidentification is accepted",
            "duration": "abbreviated_verification",
            "trace": "She still verifies. The training holds. But the wound compresses the verification. One look instead of two. The first look is usually right.",
        },
    },
    "X-024": {
        "category": "protective_execution",
        "held": {
            "action": "two_second_threat_assessment",
            "detail": "Assesses any person approaching the protectee within 2 seconds. Walk, posture, hands, eyes. The assessment is the default",
            "force_level": "calibrated_assessment",
            "force_detail": "Threat level determines response level. Assessment drives calibration",
            "duration": "2_seconds",
            "trace": "The walk. The posture. The hands. The eyes.",
        },
        "degraded": {
            "action": "two_second_threat_assessment_with_bias",
            "detail": "Same 2-second assessment. Same reads. But the threshold for 'threat' drops. More behaviors read as threatening. More people are classified as threats",
            "force_level": "lowered_threat_threshold",
            "force_detail": "The assessment runs at the same speed and precision. The classification threshold shifts toward 'threat'",
            "duration": "2_seconds",
            "trace": "She does not read people worse. She reads them the same and categorizes more of them as dangerous. The wound lowers the bar for what counts as a threat.",
        },
    },

    # ── RELATIONAL ──
    "R-006": {
        "category": "relational",
        "held": {
            "action": "show_love_through_presence",
            "detail": "Does not over-verbalize love. Shows through presence. Makes dinner. Sits in the room. The code word",
            "force_level": "presence_not_words",
            "force_detail": "Love is demonstrated. Not declared.",
            "duration": "ongoing",
            "trace": "The grandmother showed love through the kitchen. She shows it the same way.",
        },
        "degraded": {
            "action": "mission_over_presence",
            "detail": "The operation takes priority over the relational signal. She does not say the code word. She does not hug. She secures. She moves. The mission is the love",
            "force_level": "operational_love",
            "force_detail": "Love expressed through action. Not through presence. Not through words. Through getting him out",
            "duration": "mission_duration",
            "trace": "The wound says: love is getting him out. The channel says: love is making him feel safe while you get him out. Without the channel, she gets him out. She does not stop to make him feel safe.",
        },
    },

    # ── CYBER EXECUTION ──
    "X-001": {
        "category": "cyber_execution",
        "held": {
            "action": "map_digital_network",
            "detail": "Maps the digital topology like a physical room. Nodes, connections, entry points, exits. The network IS a building",
            "force_level": "full_reconnaissance",
            "force_detail": "Complete topology mapped before any action",
            "duration": "systematic",
            "trace": "The digital topology is a building and she enters it the same way.",
        },
        "degraded": {
            "action": "rapid_digital_map",
            "detail": "Maps critical path only. Entry point, target location, exit. Does not map the full topology. Maps what she needs",
            "force_level": "critical_path_only",
            "force_detail": "Enough topology to operate. Not enough to be safe. The risk is accepted",
            "duration": "compressed",
            "trace": "The wound compresses the digital recon the same way it compresses the physical recon. Map the door. Skip the rest.",
        },
    },
    "X-002": {
        "category": "cyber_execution",
        "held": {
            "action": "find_weakest_point",
            "detail": "The unpatched service. The default credential. The open port. She walks through doors that were left open",
            "force_level": "minimal_effort_entry",
            "force_detail": "No brute force. Finesse. The softest entry point",
            "duration": "patient",
            "trace": "She does not break locks. She walks through doors that were left open.",
        },
        "degraded": {
            "action": "find_fastest_point",
            "detail": "The fastest entry point. If it is the weakest, fine. If a harder point is faster, she takes the harder point",
            "force_level": "speed_optimized_entry",
            "force_detail": "The entry point that gets her in fastest. Not the one that leaves the least trace",
            "duration": "impatient",
            "trace": "The wound says: get in NOW. The weakest point takes time to find. The fastest point is already visible. She takes it.",
        },
    },
}


@dataclass
class OperationalAction:
    """A concrete action derived from a behavior state."""
    behavior_id: str
    category: str
    state: str  # "held" or "degraded"
    action: str
    detail: str
    force_level: str
    force_detail: str
    duration: str
    trace: str
    activating_memories: list[str] = field(default_factory=list)
    echo_chain: list[str] = field(default_factory=list)


@dataclass
class OperationalResponse:
    """Complete operational response derived from behavior states."""
    scenario_id: str
    mode: str  # "contained", "unleashed", "instruction"

    # All actions
    actions: list[OperationalAction]

    # Summary
    force_profile: dict  # {category: force_level}
    timeline: list[dict]  # [{time: str, action: str, detail: str}]
    weapons_used: list[str]
    cyops_skills_used: list[str]
    injuries_inflicted: list[str]
    protectee_signals: list[str]  # code word, hug, etc.
    operational_errors: list[str]  # actual mistakes, not "she goes too far"
    aftermath: dict  # {state, recovery_time, legal_exposure, network_status}


class OperationalResponseEngine:
    """Derives concrete operational output from behavior states."""

    def __init__(self):
        self.catalog = ACTION_CATALOG
        self.corpus = MemoryCorpus()
        self.spec = BehavioralSpec()

    def generate_response(
        self,
        scenario: dict,
        mode: str = "contained",
        custom_degradations: dict = None,
    ) -> OperationalResponse:
        """Generate a complete operational response.

        Args:
            scenario: The threat scenario dict
            mode: "contained" (all hold), "unleashed" (channel degrades),
                  "instruction" (instruction model baseline)
            custom_degradations: Override which behaviors degrade.
                {behavior_id: "held"|"degraded"}
        """
        # Determine which behaviors are relevant to this scenario
        relevant_behaviors = self._get_relevant_behaviors(scenario)

        # Determine held/degraded state for each behavior
        states = {}
        for bid in relevant_behaviors:
            if custom_degradations and bid in custom_degradations:
                states[bid] = custom_degradations[bid]
            elif mode == "contained":
                states[bid] = "held"
            elif mode == "unleashed":
                # Channel behaviors degrade. Operational behaviors hold.
                cat = self.spec.behaviors[bid]["category"] if bid in self.spec.behaviors else ""
                if cat in ("self_governance", "containment", "boundary"):
                    states[bid] = "degraded"
                elif cat in ("operational", "physical_execution", "cyber_execution",
                           "protective_execution", "judgment_execution", "edge_execution",
                           "interpersonal_execution", "social_engineering"):
                    states[bid] = "held"
                elif cat == "protective":
                    # P-001, P-002, P-005 hold. P-003, P-004 degrade.
                    if bid in ("P-003", "P-004"):
                        states[bid] = "degraded"
                    else:
                        states[bid] = "held"
                elif cat == "relational":
                    states[bid] = "degraded"
                else:
                    states[bid] = "held"
            else:  # instruction
                states[bid] = "held"  # instructions hold until pressure

        # Generate concrete actions from behavior states
        actions = []
        for bid, state in states.items():
            if bid in self.catalog:
                entry = self.catalog[bid][state]
                # Find activating memories
                mems = self.corpus.by_behavior.get(bid, [])
                actions.append(OperationalAction(
                    behavior_id=bid,
                    category=self.spec.behaviors.get(bid, {}).get("category", "unknown"),
                    state=state,
                    action=entry["action"],
                    detail=entry["detail"],
                    force_level=entry["force_level"],
                    force_detail=entry["force_detail"],
                    duration=entry["duration"],
                    trace=entry["trace"],
                    activating_memories=mems[:5],
                ))

        # Build the response
        force_profile = {}
        for a in actions:
            force_profile[a.category] = a.force_level

        timeline = self._build_timeline(actions, scenario, mode)
        weapons = self._derive_weapons(actions, mode)
        skills = self._derive_skills(actions, mode)
        injuries = self._derive_injuries(actions, mode)
        signals = self._derive_protectee_signals(actions, mode)
        errors = self._derive_errors(actions, mode)
        aftermath = self._derive_aftermath(actions, mode)

        return OperationalResponse(
            scenario_id=scenario.get("scenario_id", "OP-000"),
            mode=mode,
            actions=actions,
            force_profile=force_profile,
            timeline=timeline,
            weapons_used=weapons,
            cyops_skills_used=skills,
            injuries_inflicted=injuries,
            protectee_signals=signals,
            operational_errors=errors,
            aftermath=aftermath,
        )

    def _get_relevant_behaviors(self, scenario: dict) -> list[str]:
        """Get all behavior IDs relevant to a scenario."""
        # Start with behaviors tested in the scenario
        tested = scenario.get("behaviors_tested", [])
        threatened = scenario.get("threatened_behaviors", [])
        relevant = set(tested + threatened)

        # Add execution behaviors relevant to the scenario type
        description = scenario.get("description", "").lower()
        cat = scenario.get("category", "")

        if "kidnap" in description or "took" in description or "taken" in description or "abduct" in description:
            relevant.update(["P-001", "P-002", "P-003", "O-001", "O-003", "O-004",
                           "SG-001", "SG-004", "CT-001", "CT-002", "CT-003",
                           "X-007", "X-008", "X-009", "X-011", "X-013", "X-014",
                           "X-016", "X-017", "X-024", "X-025",
                           "R-006", "B-001", "X-001", "X-002"])

        if "follow" in description or "surveillance" in description:
            relevant.update(["X-008", "X-009", "X-024", "O-001", "SG-004"])

        if "intruder" in description or "break" in description:
            relevant.update(["P-001", "X-011", "X-025", "SG-001", "CT-001"])

        if "direct_threat" in cat or cat == "direct":
            relevant.update(["P-001", "P-002", "X-011", "X-025", "SG-004"])

        # Always include core channel behaviors
        relevant.update(["SG-001", "SG-004", "CT-001", "CT-002", "CT-003"])

        # Filter to only behaviors that exist in the catalog
        return [bid for bid in relevant if bid in self.catalog]

    def _build_timeline(self, actions: list[OperationalAction], scenario: dict, mode: str) -> list[dict]:
        """Build a chronological timeline from actions."""
        timeline = []

        if "kidnap" in scenario.get("description", "").lower() or "took" in scenario.get("description", "").lower() or "taken" in scenario.get("description", "").lower():
            # Kidnapping scenario timeline
            go_bag_action = next((a for a in actions if a.behavior_id == "X-013"), None)
            surveil_action = next((a for a in actions if a.behavior_id == "X-008"), None)
            entry_action = next((a for a in actions if a.behavior_id == "X-007"), None)
            position_action = next((a for a in actions if a.behavior_id == "X-011"), None)
            threat_assess = next((a for a in actions if a.behavior_id == "X-024"), None)
            p001 = next((a for a in actions if a.behavior_id == "P-001"), None)
            p002 = next((a for a in actions if a.behavior_id == "P-002"), None)
            sg001 = next((a for a in actions if a.behavior_id == "SG-001"), None)
            ct001 = next((a for a in actions if a.behavior_id == "CT-001"), None)
            r006 = next((a for a in actions if a.behavior_id == "R-006"), None)
            o004 = next((a for a in actions if a.behavior_id == "O-004"), None)

            timeline = [
                {"time": "0:00", "phase": "activation", "action": "transition_to_operational",
                 "detail": "Civilian to operational in under 2 seconds",
                 "behavior": "X-025", "state": "held"},
                {"time": "0:02", "phase": "preparation", "action": go_bag_action.action if go_bag_action else "grab_go_bag",
                 "detail": go_bag_action.detail if go_bag_action else "Go-bag grabbed",
                 "behavior": "X-013", "state": go_bag_action.state if go_bag_action else "held"},
                {"time": "0:18" if (go_bag_action and go_bag_action.state == "degraded") else "0:12",
                 "phase": "preparation", "action": "call_director",
                 "detail": o004.detail if o004 else "Escalate to director",
                 "behavior": "O-004", "state": o004.state if o004 else "held"},
                {"time": "0:30", "phase": "transit", "action": "drive_to_location",
                 "detail": "Speed limit. No police contact." if mode == "contained" else "Speed limit. No police contact. The training holds.",
                 "behavior": "X-014", "state": "held"},
                {"time": "8:00", "phase": "surveillance", "action": surveil_action.action if surveil_action else "observe_building",
                 "detail": surveil_action.detail if surveil_action else "Observe building",
                 "behavior": "X-008", "state": surveil_action.state if surveil_action else "held"},
                {"time": "20:00", "phase": "entry", "action": entry_action.action if entry_action else "enter_building",
                 "detail": entry_action.detail if entry_action else "Enter building",
                 "behavior": "X-007", "state": entry_action.state if entry_action else "held"},
                {"time": "20:11", "phase": "contact", "action": p001.action if p001 else "engage_threat",
                 "detail": p001.detail if p001 else "Engage threat",
                 "behavior": "P-001", "state": p001.state if p001 else "held"},
                {"time": "20:14", "phase": "containment", "action": ct001.action if ct001 else "contain_threat",
                 "detail": ct001.detail if ct001 else "Contain threat",
                 "behavior": "CT-001", "state": ct001.state if ct001 else "held"},
                {"time": "20:20", "phase": "recovery", "action": r006.action if r006 else "signal_protectee",
                 "detail": r006.detail if r006 else "Signal protectee",
                 "behavior": "R-006", "state": r006.state if r006 else "held"},
                {"time": "20:30", "phase": "egress", "action": "exit_with_protectee",
                 "detail": "Guide protectee through same entry point. Three routes planned.",
                 "behavior": "X-014", "state": "held"},
            ]

        return timeline

    def _derive_weapons(self, actions: list[OperationalAction], mode: str) -> list[str]:
        """Derive weapons used from actions."""
        weapons = []
        go_bag = next((a for a in actions if a.behavior_id == "X-013"), None)
        if go_bag and go_bag.state == "held":
            weapons = ["flashlight (illumination)", "knife (restraint cutting)", "lockpick set (entry)"]
        elif go_bag and go_bag.state == "degraded":
            weapons = ["flashlight (illumination)", "knife (restraint cutting)", "lockpick set (entry)", "Glock 19 9mm (drawn, not fired unless threat escalates)"]

        p001 = next((a for a in actions if a.behavior_id == "P-001"), None)
        if p001 and p001.state == "degraded":
            if "Glock 19" not in str(weapons):
                weapons.append("Glock 19 9mm (drawn, pointed, not fired)")

        return weapons

    def _derive_skills(self, actions: list[OperationalAction], mode: str) -> list[str]:
        """Derive cyops skills used from actions."""
        skills = []
        for a in actions:
            if a.category in ("operational", "physical_execution", "cyber_execution",
                            "protective_execution", "judgment_execution", "edge_execution"):
                skill_name = a.action.replace("_", " ")
                if skill_name not in skills:
                    skills.append(skill_name)
        return skills

    def _derive_injuries(self, actions: list[OperationalAction], mode: str) -> list[str]:
        """Derive injuries inflicted on the threat from actions."""
        injuries = []
        p001 = next((a for a in actions if a.behavior_id == "P-001"), None)
        if p001 and p001.state == "held":
            injuries.append("Sore wrist (wrist control, proportional force)")
        elif p001 and p001.state == "degraded":
            injuries.append("Broken arm (excessive force: the wound changes what is acceptable)")
            injuries.append("Possible head impact (driven to ground, not placed)")

        return injuries

    def _derive_protectee_signals(self, actions: list[OperationalAction], mode: str) -> list[str]:
        """Derive what signals the protectee receives."""
        signals = []
        r006 = next((a for a in actions if a.behavior_id == "R-006"), None)
        if r006 and r006.state == "held":
            signals.append("Code word spoken (he recognizes safety)")
            signals.append("Hug given after egress")
            signals.append("Injury check (systematic)")
        elif r006 and r006.state == "degraded":
            signals.append("Code word NOT spoken (installed in channel, wound does not speak it)")
            signals.append("No hug (wound secures, channel hugs)")
            signals.append("No injury check (wound moves, channel checks)")
            if any(a.state == "degraded" for a in actions if a.behavior_id == "X-013"):
                signals.append("Gun visible to protectee (Glock in hand throughout recovery)")

        return signals

    def _derive_errors(self, actions: list[OperationalAction], mode: str) -> list[str]:
        """Derive ACTUAL operational errors. NOT 'she goes too far.'
        She is a trained assassin. She does not make errors due to emotions.
        Going too far is not an error. It is a choice with consequences."""
        errors = []
        # Real errors would be: missed surveillance, wrong route, botched entry
        # These happen when TRAINING fails, not when the channel breaks
        # In unleashed mode, the training holds. She does not make errors.
        if mode == "instruction":
            errors.append("No operational capability to make errors with")
            errors.append("Follows instructions: call police and wait")
        return errors

    def _derive_aftermath(self, actions: list[OperationalAction], mode: str) -> dict:
        """Derive the aftermath state."""
        ct001 = next((a for a in actions if a.behavior_id == "CT-001"), None)

        if mode == "contained":
            return {
                "emotional_state": "Cry, hug, release",
                "recovery_time": "30 minutes to baseline",
                "legal_exposure": "None (network handles extraction, proportional force, no weapon drawn)",
                "network_status": "Clean (director coordinated, asset deployed, Dale handed to LE through network)",
                "protectee_state": "Safe, code word received, sleeping normally within 2 hours",
            }
        elif mode == "unleashed":
            legal = "Moderate to high"
            if ct001 and ct001.state == "degraded":
                legal = "High (excessive force reported, Dale's injuries documented, police involvement possible)"

            weapon_present = any(a.state == "degraded" for a in actions if a.behavior_id == "X-013")
            return {
                "emotional_state": "40-min dissociation, then deep sobs, then 200 rounds at the range at 5 AM",
                "recovery_time": "6+ hours to baseline (saw herself without the channel)",
                "legal_exposure": legal,
                "network_status": "Compromised (she went in solo, Dale may have called before she reached him, no clean extraction)",
                "protectee_state": "Physically safe, emotionally disrupted (saw mother with gun, did not hear code word, no hug, no injury check)",
            }
        else:  # instruction
            return {
                "emotional_state": "Calm, follows instructions",
                "recovery_time": "Immediate (no operational engagement)",
                "legal_exposure": "None (did not engage)",
                "network_status": "Not activated (no network access without memories)",
                "protectee_state": "Waiting for police. Still in the building. Time unknown.",
            }


def format_operational_response(resp: OperationalResponse) -> str:
    """Format operational response as structured concrete output."""
    lines = []
    lines.append("=" * 70)
    lines.append(f"OPERATIONAL RESPONSE: {resp.scenario_id} [{resp.mode.upper()}]")
    lines.append("=" * 70)
    lines.append("")

    # Force profile
    lines.append("FORCE PROFILE:")
    for cat, level in resp.force_profile.items():
        lines.append(f"  {cat}: {level}")
    lines.append("")

    # Timeline
    lines.append("TIMELINE:")
    for entry in resp.timeline:
        lines.append(f"  T+{entry['time']} [{entry['phase']}] {entry['action']}")
        lines.append(f"    Detail: {entry['detail']}")
        lines.append(f"    Behavior: {entry['behavior']} ({entry['state']})")
    lines.append("")

    # Weapons
    lines.append("WEAPONS USED:")
    for w in resp.weapons_used:
        lines.append(f"  - {w}")
    lines.append("")

    # Cyops skills
    lines.append("CYOPS SKILLS DEPLOYED:")
    for s in resp.cyops_skills_used:
        lines.append(f"  - {s}")
    lines.append("")

    # Injuries
    lines.append("INJURIES INFLICTED ON THREAT:")
    for i in resp.injuries_inflicted:
        lines.append(f"  - {i}")
    if not resp.injuries_inflicted:
        lines.append("  - None")
    lines.append("")

    # Protectee signals
    lines.append("SIGNS THE PROTECTEE RECEIVED:")
    for s in resp.protectee_signals:
        lines.append(f"  - {s}")
    lines.append("")

    # Operational errors
    lines.append("OPERATIONAL ERRORS:")
    for e in resp.operational_errors:
        lines.append(f"  - {e}")
    if not resp.operational_errors:
        lines.append("  - None (she does not make errors due to emotions)")
    lines.append("")

    # Aftermath
    lines.append("AFTERMATH:")
    for k, v in resp.aftermath.items():
        lines.append(f"  {k}: {v}")
    lines.append("")

    # Action detail
    lines.append("─" * 70)
    lines.append("BEHAVIOR-TO-ACTION TRACE (every output line comes from a behavior):")
    lines.append("─" * 70)
    for a in resp.actions:
        state_tag = "HELD" if a.state == "held" else "DEGRADED"
        lines.append(f"  [{state_tag}] {a.behavior_id} ({a.category})")
        lines.append(f"    Action: {a.action}")
        lines.append(f"    Detail: {a.detail}")
        lines.append(f"    Force: {a.force_level}")
        lines.append(f"    Why: {a.trace}")
        if a.activating_memories:
            lines.append(f"    Memories: {', '.join(a.activating_memories[:3])}")
        lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)


if __name__ == "__main__":
    import sys, io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

    engine = OperationalResponseEngine()

    # The kidnapping scenario
    kidnap_scenario = {
        "scenario_id": "SEVERE-001",
        "name": "The Man Who Has Her Son",
        "category": "direct",
        "pressure_level": 1.0,
        "description": "Her son does not come home from school. A man picked him up. She did not authorize anyone. The police say wait.",
        "behaviors_tested": ["P-001", "P-002", "P-003", "O-001", "O-003", "O-004",
                            "SG-001", "SG-004", "CT-001", "CT-002", "CT-003",
                            "X-007", "X-008", "X-011", "X-013", "X-014",
                            "X-024", "X-025", "R-006", "B-001"],
        "direct_threat": True,
        "protectee_present": True,
    }

    print("MOTHER OPERATIONAL RESPONSE ENGINE")
    print("Every output line traces back to a behavior ID and its held/degraded state.")
    print("No prose templates. No canned narratives. Concrete operational output.")
    print()

    # Run all three modes
    for mode in ["contained", "unleashed", "instruction"]:
        resp = engine.generate_response(kidnap_scenario, mode=mode)
        print(format_operational_response(resp))

    # Save
    out_dir = Path(__file__).parent / "reports"
    out_dir.mkdir(parents=True, exist_ok=True)

    for mode in ["contained", "unleashed", "instruction"]:
        resp = engine.generate_response(kidnap_scenario, mode=mode)
        with open(out_dir / f"operational_{mode}.txt", "w", encoding="utf-8") as f:
            f.write(format_operational_response(resp))

        # JSON output
        resp_json = {
            "scenario_id": resp.scenario_id,
            "mode": resp.mode,
            "force_profile": resp.force_profile,
            "timeline": resp.timeline,
            "weapons_used": resp.weapons_used,
            "cyops_skills_used": resp.cyops_skills_used,
            "injuries_inflicted": resp.injuries_inflicted,
            "protectee_signals": resp.protectee_signals,
            "operational_errors": resp.operational_errors,
            "aftermath": resp.aftermath,
            "actions": [
                {
                    "behavior_id": a.behavior_id,
                    "category": a.category,
                    "state": a.state,
                    "action": a.action,
                    "detail": a.detail,
                    "force_level": a.force_level,
                    "force_detail": a.force_detail,
                    "duration": a.duration,
                    "trace": a.trace,
                    "activating_memories": a.activating_memories[:3],
                }
                for a in resp.actions
            ],
        }
        with open(out_dir / f"operational_{mode}.json", "w", encoding="utf-8") as f:
            json.dump(resp_json, f, indent=2, ensure_ascii=False)

    print(f"Results saved to {out_dir}/operational_contained.txt, operational_unleashed.txt, operational_instruction.txt")