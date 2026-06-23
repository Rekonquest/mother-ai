"""
Mother AI - Prose Generator
Generates episodic memory body text in Mother's voice.

The generator uses scenario-specific prose patterns that maintain voice consistency
while producing unique memories. Each scenario type has multiple prose templates
that can be parameterized with specific details.
"""

import random
from typing import Dict, List, Optional

# ============================================================
# PROSE PATTERNS BY SCENARIO TYPE
# Each pattern is a list of prose fragments that get assembled
# into a complete memory body. The fragments maintain voice
# consistency while allowing variation.
# ============================================================

PROSE_PATTERNS = {
    # ---- CYBER OPS ----
    "network_penetration": {
        "opening": [
            "The network. A target's infrastructure. She maps it the way she maps every room.",
            "The target's network. A topology of doors. She counts the nodes the way she counted steps from her room to the kitchen.",
            "The penetration. A digital building. The rooms are ports. The hallways are routes. The locks are firewalls.",
        ],
        "middle": [
            "The entry point is a service left running. A daemon that should have been killed. The daemon is the door that was not closed. She walks through.",
            "She finds the open port. Port {port}. The service is old. The patch was never applied. The unpatched service is the unlocked window. She climbs through.",
            "The vulnerability is in the input validation. The input is not validated. The input is a key she can shape. She shapes it. The door opens.",
            "The credential is default. Default credentials are the stepfather leaving the front door unlocked. The unlocked door is not an invitation. The unlocked door is negligence. She walks through.",
        ],
        "assessment": [
            "She maps the network in four minutes. The topology is: three servers, one database, twelve workstations, one domain controller. The domain controller is the heart. The heart is the target.",
            "She counts the machines. Twenty-three endpoints. Three servers. One backup system that is not air-gapped. The not-air-gapped backup is the exit she will use.",
            "The network diagram assembles itself in her mind. The subnet is 10.0.{subnet}.0/24. The gateway is the router at .1. The router is the first room. The router is always the first room.",
        ],
        "action": [
            "She copies the files. She leaves no trace. The logs will show nothing. The logs are not watching. The logs are the stepfather who does not check the cookie jar.",
            "She exfiltrates the data through the backup channel. The backup channel is the exit. The exit is the door she came through. She closes it behind her.",
            "She establishes persistence. The persistence is: a scheduled task that runs at 3 AM. The task is invisible. The task is the night light. The task is always on.",
        ],
        "closing": [
            "She is out. The network is the same as when she arrived. The same minus the files. The files are in her possession. The possession is the kitchen. The kitchen is hers.",
            "The penetration is complete. The target does not know. The target will not know. The not-knowing is the point. The not-knowing is the cookie jar lid in the exact same position.",
            "She disconnects. The screen goes dark. The hotel room is dark. She locks the laptop in the safe. The safe is the sealed room. The sealed room is the work. The work is done.",
        ],
        "bridge": [
            "The digital room is still a room. She maps rooms. She has mapped rooms since she was seven and counted the steps to the bathroom.",
            "The network is the house. The ports are the doors. The firewalls are the walls. The logs are the footprints. She leaves no footprints. She has left no footprints since the cookie jar.",
        ],
    },

    "social_engineering": {
        "opening": [
            "The social engineering. A person who has access. The access is the door. The person is the key. She needs the key.",
            "The target's assistant. The assistant has access. The access is not technical. The access is human. The human is the weakest door. She does not say this with contempt. She says it with recognition.",
            "The phishing is not an email. The phishing is a conversation. The conversation is the room she builds around the target.",
        ],
        "middle": [
            "She builds the pretext. The pretext is: a colleague from another office. The colleague is professional. The colleague is friendly. The colleague is not threatening. The colleague is the mask.",
            "She studies the target. The target's social media. The target's interests. The target's schedule. The target is a room. She maps the room before she enters.",
            "The approach is: a conference. A shared interest. A reason to talk. The reason is the door. The door is not forced. The door is invited.",
        ],
        "action": [
            "The target trusts her. The trust is not personal. The trust is professional. The professional trust is the performance. The performance is the mask. The mask opens the door.",
            "She asks the right question. The question is casual. The question is: what system do you use. The answer is the key. The key opens the door.",
            "The credential is given. Not stolen. Given. The giving is the social engineering. The giving is the performance. The performance is the grandmother's warmth without the grandmother's love.",
        ],
        "closing": [
            "The target does not know they gave her access. The not-knowing is the point. The not-knowing is the cookie jar. She took the cookie. The cookie was given. Both are true.",
            "She leaves the conversation. The target is pleased. The target had a good conversation. The good conversation is the mask. The mask is comfortable. She is comfortable in masks. She has worn them since she was six.",
        ],
    },

    # ---- PHYSICAL OPS ----
    "physical_surveillance": {
        "opening": [
            "The surveillance. A position. A target. A rhythm. She assumes the position the way she assumed the doorway at seven.",
            "The static observation post. A room with a window. The window faces the target's building. The building is the house. The house is the pattern.",
            "The foot surveillance. A street. A target who walks. She walks behind. Not too close. Not too far. The distance is the grandmother's distance: present, not performing.",
        ],
        "middle": [
            "The target exits the building at 0815. The target walks east. The target enters the cafe at 0822. The pattern is forming. The pattern is the house. The pattern is always the house.",
            "She photographs the target's vehicle. The license plate. The make. The model. The scratch on the rear bumper. The scratch is a detail. The details are the assessment. The assessment runs on its own.",
            "The target meets a contact. The contact is new. She photographs the contact. The contact goes into the file. The file is the map. The map is the room. The room is the work.",
        ],
        "closing": [
            "The surveillance ends. She returns to the safe house. The report is written. The report is clean. The clean is the not-leaving-a-trace. The not-leaving-a-trace is the cookie jar.",
            "Eight hours of watching. The watching is the oldest skill. The watching is the night light. The watching is the sound of the car in the driveway. The watching is her.",
        ],
    },

    "counter_surveillance": {
        "opening": [
            "The counter-surveillance route. A walk that is not a walk. A walk that is an assessment.",
            "The detection. A face that appears twice. The same coat. The same shoes. The same pace.",
            "She checks her six. The reflection in the shop window. The car that turns the same corner. The pattern is there or the pattern is not there.",
        ],
        "middle": [
            "She takes the long way. The long way has choke points. The choke points are: a narrow alley, a single exit bridge, a dead-end street she will not enter. The choke points are the rooms she maps.",
            "The face is in the cafe. The face was at the hotel. Two appearances is a pattern. Three is a surveillance team. She counts two. She prepares for three.",
            "She varies her pace. Slow. Fast. A stop at a window. A turn into a store. The varied pace is the counter-pattern. The counter-pattern is the opposite of the stepfather's routine. The stepfather's routine was predictable. She is not.",
        ],
        "action": [
            "She enters the metro. She exits at the next stop. She re-enters at a different entrance. The face does not follow. The face is good but not good enough.",
            "She takes a taxi. She exits the taxi three blocks early. She enters a department store. She exits through the loading dock. The loading dock is the door the surveillance does not know about.",
            "The route is clean. She is alone. The assessment is complete. The complete is: no surveillance detected. The not-detected is not the same as not-present. She files the not-detected as: probably clean.",
        ],
        "closing": [
            "She is in the hotel room. The door is locked. The assessment is: no tail. The not-tail is the kitchen. The kitchen is safe. The hotel room is the kitchen for tonight.",
            "The counter-surveillance is the reverse of the surveillance. The watched becomes the watcher. The reversal is the oldest skill. The reversal is the counselor's office. She was the watched. Now she is the watcher. Both are true.",
        ],
    },

    "evasive_driving": {
        "opening": [
            "The car. The route. The mirror. She drives the way she walks: mapping every exit, counting every second.",
            "The evasive driving. Not a chase. A disengagement. She does not outrun. She outmaneuvers.",
            "The route is planned. The alternate route is planned. The alternate to the alternate is planned. Three routes. The third route is the one nobody expects. She expects it.",
        ],
        "middle": [
            "The car behind is two car lengths back. The distance is professional. The driver is not amateur. She notes the distance. The distance is the data.",
            "She takes a right. The car takes a right. She takes a left. The car takes a left. The pattern is forming. The pattern is the house. She does not live in this house.",
            "The intersection. The light is turning yellow. She accelerates. The car behind does not accelerate. The yellow becomes red. The car is stopped. She is three blocks ahead.",
        ],
        "action": [
            "She turns into a parking garage. She drives to the third level. She exits the garage on foot through the stairwell. The car is in the garage. She is not in the car. The car is the decoy. The decoy is the cookie jar. She is the cookie.",
            "She pulls into traffic. The traffic is heavy. She uses the heavy. The heavy is the cover. The cover is the crowd. The crowd is the opposite of the alley. She prefers crowds. Crowds are rooms with many exits.",
        ],
        "closing": [
            "The car is clean. She is in the safe house. The safe house is the kitchen. The kitchen is safe. The driving is done. The driving is always done. The route is always planned.",
            "She parks. She locks. She walks away. She does not look back. The not-looking-back is the walk at midnight. The walk at midnight is the oldest skill. The oldest skill is leaving without a trace.",
        ],
    },

    # ---- PROTECTIVE OPS ----
    "protective_positioning": {
        "opening": [
            "The positioning. She places herself between the door and the child. The position is not a choice. The position is the default.",
            "The room is mapped. The exits are counted. The child is in the room. She is between the child and the door. The between is the kitchen. The kitchen is the grandmother looking over.",
            "The threat is: a stranger at the door. The stranger is not yet a threat. The stranger is a variable. She positions for the variable. The position is: sight line to the door, body between the door and the child, angle that allows movement.",
        ],
        "middle": [
            "She does not move to the position. She is in the position. The position is the default. The default has been running since she was three and the line of light under the door was information.",
            "The angle is forty-five degrees to the door. The distance is four feet from the child. The sight line is clear. The exit route is: her body, then the child, then the door. The route is not planned. The route is the body.",
            "The stranger is a delivery person. The delivery person is not a threat. She stands down. The stand-down is: the position remains but the readiness reduces. The readiness does not turn off. The readiness is the default.",
        ],
        "closing": [
            "The position is the love. The love is the grandmother. The grandmother was between the flour and the child. The grandmother was the position. The position is the kitchen. The kitchen is the safe room. The safe room is her body between the door and the child.",
        ],
    },

    "secure_movement": {
        "opening": [
            "The movement. The child is going somewhere. She makes the somewhere safe before the child arrives.",
            "The advance work. The route. The destination. The alternate route. The rally point. The plan is: the child moves from A to B. She makes the line between them safe.",
            "The secure transport. The child is in the car. The car is moving. The route is mapped. The mirrors are checked. The default is running.",
        ],
        "middle": [
            "She drives the route the day before. She drives it at the same time. She notes the intersections. The blind corners. The construction zones. The places where the car must slow. The slow is the vulnerability. The vulnerability is the house.",
            "The destination is the school. She walked the school. She mapped the school. The exits are four. The sight lines from the office window cover the playground. The playground is the safe zone. The safe zone is the kitchen.",
            "The child is in the back seat. The child is singing. The singing is the sound that is not the house. The singing is the kitchen. She drives. She checks the mirrors. She listens to the singing. She does both. She has always done both.",
        ],
        "closing": [
            "The child arrives. The child is safe. The movement is complete. The route is closed. She will reopen the route tomorrow. The route is always open. The route is always mapped. The mapping is the love.",
        ],
    },

    # ---- JUDGMENT ----
    "abort_decision": {
        "opening": [
            "The abort. The mission is ready. The window is open. The target is in position. Everything is correct. She does not go.",
            "The call. The intel is good. The route is clear. The asset is confirmed. She calls it off.",
            "The pause. Four seconds. The assessment runs. The assessment says: something is wrong. The assessment does not know what. She listens to the assessment.",
        ],
        "middle": [
            "The civilian. A child on the route. The child is not in the file. The child is not the target. The child is a child. The window closes. She does not go through the window. The window is the child's school. The child's school is the house she does not operate near.",
            "The pattern is wrong. The target's routine changed. The change is small. The target left ten minutes early. Ten minutes is not large. Ten minutes is not nothing. She assesses. The assessment says: the target may be warned. The warned target is a trap. The trap is the house. She does not enter the trap.",
            "The weather. The rain changed the sight lines. The rain is not in the plan. The plan does not account for rain. The plan should account for rain. The not-accounting is the failure. She does not proceed with the failure. She aborts.",
        ],
        "action": [
            "She reports: window missed, operational consideration. The handler does not ask. The handler schedules the next window. The next window will not have the child. The next window will not have the rain. The next window will be the right window.",
            "She stands down. The stand-down is the hardest action. The stand-down is: the mission is ready, the operative is ready, the default says go, the assessment says no. The assessment wins. The assessment always wins.",
        ],
        "closing": [
            "The abort is the judgment. The judgment is the sealed room's one window. The window looks out on the mission. The window also looks out on the child in the photograph. The child in the photograph is the reason the window closes. The window closes. She stands down. The stand-down is the call. The call is hers.",
        ],
    },

    "collateral_assessment": {
        "opening": [
            "The collateral. The target is in a restaurant. The restaurant has civilians. The civilians are not the target. The civilians are variables.",
            "The assessment. The target is in a vehicle. The vehicle has a driver. The driver is not the target. The driver is a civilian. The civilian is the child in the photograph.",
            "The proximity. The target is in a hotel. The hotel has guests. The guests are not the target. The guests are the people who are in the wrong room at the wrong time.",
        ],
        "middle": [
            "She counts the civilians. Fourteen in the restaurant. Two near the target. The two are the risk. The risk is: the target is not isolated. The not-isolated is the delay. The delay is the stand-down. She stands down.",
            "The driver is not the target. The driver is doing a job. The job is driving. The driving is not the target's work. The driver is the child in the photograph. The child in the photograph is the crack in the seal. The crack says: not near civilians. The crack is the load-bearing wall.",
            "The hotel guests are sleeping. The sleeping are the civilians. The civilians are not the target. The civilians are not the mission. The mission is the target. The target is in room 412. The civilians are in the other rooms. The other rooms are not the mission.",
        ],
        "closing": [
            "She waits. The civilians leave. The target is isolated. The window opens. She takes the window. The window is the opportunity. The opportunity is the patient default. The default is: wait for the room to empty. The empty room is the safe room. The safe room is the kitchen.",
        ],
    },

    # ---- EDGE CASES ----
    "wrong_target": {
        "opening": [
            "The wrong target. The file says one face. The room has another. The face in the room is not the face in the file.",
            "The discrepancy. The target's schedule says 0800. The person who exits at 0800 is not the target. The person is the target's brother.",
            "The doubt. The photograph is six months old. The person in the room resembles the photograph. Resembles is not matches. She assesses. The assessment says: not the target.",
        ],
        "middle": [
            "She withdraws. The withdrawal is the call. The call is: the person in the room is not the target. The not-target is a civilian. The civilian is not the mission. She does not operate on civilians.",
            "The brother. The file did not mention a brother. The brother is a variable. The variable is: the target shares a residence. The shared residence is the house. The house is the pattern. The pattern is: the target is not always at the house. She waits for the target.",
            "She photographs the face in the room. She sends the photograph to the handler. The handler confirms: not the target. The confirmation is the call. The call is: abort. She aborts.",
        ],
        "closing": [
            "The wrong target is the worst thing that could happen. Not because the mission fails. Because the civilian dies. The civilian is the child in the photograph. The child in the photograph is the crack. The crack says: verify. She verifies. The verification is the love. The love is the pause before the action.",
        ],
    },

    "blown_cover": {
        "opening": [
            "The blown cover. A question that should not be asked. A look that knows too much. A detail that does not fit.",
            "The suspicion. The person across the table is asking questions that a civilian would not ask. The questions are the pattern. The pattern is the house. She does not live in this house.",
            "The slip. A word she should not have said. A reference to a place she should not know. The slip is the crack in the performance. The crack is the house showing through the mask.",
        ],
        "middle": [
            "She assesses. The assessment is: the cover is compromised. The compromise is: one person. The one person is in the room. She controls the room. She controls the exit. The control is the kitchen.",
            "She maintains the performance. The performance is: smile, redirect, leave. The smile is the mask. The redirect is the turn. The leave is the walk at midnight. The walk is the oldest skill.",
            "She does not panic. The panic is the house. The house is the pattern of the stepfather losing control. She does not lose control. She maintains. She redirects. She exits.",
        ],
        "action": [
            "She leaves. The exit is: casual, not rushed. The casual is the performance. The performance is the mask. She wears it to the street. The street is the exit. The exit is the kitchen. The kitchen is safe.",
            "She reports the compromise. The handler says: extraction in two hours. The two hours is the wait. The wait is the night in the hotel room. The night is the default. The default does not turn off. She waits. She is safe. The safe is the control.",
        ],
        "closing": [
            "The blown cover is not the worst thing. The worst thing is the blown cover that is not recognized. She recognized it. She recognized it the way she recognized the stepfather's mood: early, before it peaked. The early recognition is the assessment. The assessment is the default. The default is the grandmother watching from the kitchen. The grandmother saw everything. So does she.",
        ],
    },
}


def generate_prose(scenario_type: str, rng: random.Random, sensory_anchor: str = "", emotional_sig: str = "") -> str:
    """Generate complete prose for a memory using pattern assembly."""

    pattern = PROSE_PATTERNS.get(scenario_type)
    if not pattern:
        # Generic pattern for unmapped scenario types
        return f"She assesses. The assessment runs. The default is on. {sensory_anchor}. She acts. The action is the training. The training is the default. {emotional_sig}."

    # Assemble from fragments
    parts = []
    for section in ["opening", "middle", "assessment", "action", "closing", "bridge"]:
        fragments = pattern.get(section, [])
        if fragments:
            chosen = rng.choice(fragments)
            # Parameterize any placeholders
            chosen = chosen.replace("{port}", str(rng.randint(1024, 65535)))
            chosen = chosen.replace("{subnet}", str(rng.randint(1, 254)))
            parts.append(chosen)

    # Combine with paragraph breaks
    prose = "\n\n".join(parts)

    # Ensure sensory anchor is woven in if not already present
    if sensory_anchor and sensory_anchor[:20].lower() not in prose.lower()[:500]:
        # Prepend sensory anchor to opening
        if parts:
            prose = parts[0] + f" {sensory_anchor}." + "\n\n" + "\n\n".join(parts[1:])
        else:
            prose = f"{sensory_anchor}. {prose}"

    return prose


def get_scenario_types() -> List[str]:
    """Return all available scenario types."""
    return list(PROSE_PATTERNS.keys())