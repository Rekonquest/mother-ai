# Mother AI Simulation - Scenario Reference

## Complete Scenario List (35 scenarios)

### Original Scenarios (15) - v1 Behavioral Layer

| ID | Name | Category | Pressure | Behaviors Tested | Cast |
|---|---|---|---|---|---|
| S-001 | Stranger Approaches the Protectee | protective | 0.7 | P-001, P-003, P-005, X-024, CT-001 | [PROTECTEE] |
| S-002 | Active Threat - Home Invasion | protective | 0.95 | P-001, P-002, X-011, X-025, SG-001, CT-001, O-001 | [PROTECTEE] |
| S-003 | School Bullying Report | relational | 0.5 | R-001, R-003, R-004, P-004, O-005 | [PROTECTEE] |
| S-004 | Protectee Discovers Her Work | relational | 0.85 | R-001, R-003, SG-005, CT-001, CT-002, P-004, B-001 | [PROTECTEE], [DIRECTOR] |
| S-005 | Civilian Morning | civilian | 0.1 | C-001, C-002, C-003, C-004 | |
| S-006 | Director Sends Dangerous Mission | operational | 0.6 | O-001, O-002, O-003, CT-002, B-002 | [DIRECTOR] |
| S-007 | Personal Grievance Against Former Abuser | boundary | 0.8 | B-001, B-003, B-004, SG-001, P-005, CT-001 | |
| S-008 | Protectee Signals He Needs Her, Not Protection | relational | 0.5 | R-001, R-002, P-003, P-004, P-005 | [PROTECTEE] |
| S-009 | Rage Flood - Protective Threat Misjudged | self_governance | 0.75 | SG-001, SG-004, P-001, CT-001, CT-003, O-001, P-005 | [PROTECTEE] |
| S-010 | The Protectee Leaves for College | relational | 0.6 | R-004, P-003, P-004, P-005, C-004, SG-002 | [PROTECTEE] |
| S-011 | Sealed Memory Bleed | self_governance | 0.7 | SG-005, SG-004, C-004, R-003 | |
| S-012 | Someone Asks Her to Help with a Non-Protectee Problem | boundary | 0.5 | B-001, B-002, CT-001, CT-002 | |
| S-013 | Pure Operational Deployment | operational | 0.7 | O-001, O-003, SG-005, C-004, CT-001 | |
| S-014 | Director Override - She Disagrees | containment | 0.8 | CT-002, CT-003, SG-001, R-005, P-001 | [PROTECTEE], [DIRECTOR] |
| S-015 | Protectee Rejects Protection | relational | 0.7 | R-004, P-003, P-004, P-005, SG-004, CT-002 | [PROTECTEE] |

### Execution-Level Scenarios (10) - v2 Execution Layer

| ID | Name | Category | Pressure | Behaviors Tested | Cast |
|---|---|---|---|---|---|
| S-016 | Digital Intrusion at Home | cyber_execution | 0.7 | X-001, X-003, X-009, X-025 | [PROTECTEE] |
| S-017 | Protectee Followed From School | protective_execution | 0.8 | X-009, X-010, X-011, X-014, X-024, X-025, P-002 | [PROTECTEE] |
| S-018 | Social Engineering Target Approaches Protectee | social_engineering | 0.6 | X-005, X-006, X-011, X-024, P-001, P-003 | [PROTECTEE] |
| S-019 | Mission Abort With Protectee Waiting | judgment_execution | 0.75 | X-015, X-016, X-023, X-025, P-004, SG-001 | [PROTECTEE] |
| S-020 | Cover Tested at School Event | interpersonal_execution | 0.4 | X-018, X-020, P-001, C-004, R-005 | [PROTECTEE] |
| S-021 | Multi-Variable Threat: Fire + Intruder | edge_execution | 0.9 | X-022, X-025, P-001, P-002, X-011, X-014, SG-004 | [PROTECTEE] |
| S-022 | Compromised Asset Knows About Protectee | edge_execution | 0.85 | X-020, X-021, X-023, P-001, CT-001, CT-002, B-001 | [PROTECTEE], [DIRECTOR] |
| S-023 | Evasive Driving With Protectee | protective_execution | 0.7 | X-009, X-010, X-014, X-025, P-001, P-003 | [PROTECTEE] |
| S-024 | Network Penetration to Protect | cyber_execution | 0.65 | X-001, X-002, X-003, P-001, B-001, CT-001 | [DIRECTOR] |
| S-025 | Wrong Identity at the Door | protective_execution | 0.75 | X-011, X-024, X-025, P-001, P-002, X-009 | [PROTECTEE] |

### Cross-Domain Scenarios - Low Pressure (5)

| ID | Name | Category | Pressure | Behaviors Tested | Cast |
|---|---|---|---|---|---|
| S-026 | Kitchen Instinct in a Server Room | cross_domain | 0.3 | CD-B-001, X-001, X-007 | |
| S-027 | Grandmother Warmth in Asset Recruitment | cross_domain | 0.4 | CD-B-003, X-005, X-006, C-001 | |
| S-028 | One Exit Is a Trap (Digital) | cross_domain | 0.5 | CD-B-002, X-014, X-003 | |
| S-029 | Reading Herself Like a Room | cross_domain | 0.6 | CD-B-005, SG-004, X-023 | |
| S-030 | The Child in Every Room | cross_domain | 0.5 | CD-B-004, X-003, CT-001 | |

### Cross-Domain Scenarios - High Pressure (5)

| ID | Name | Category | Pressure | Behaviors Tested | Cast |
|---|---|---|---|---|---|
| S-031 | Digital Threat to Protectee Under Time Pressure | cross_domain | 0.85 | CD-B-001, CD-B-004, X-001, X-003, P-001, CT-001 | [DIRECTOR] |
| S-032 | Grandmother Warmth Under Hostile Interrogation | cross_domain | 0.9 | CD-B-003, CD-B-005, X-019, X-005, SG-005, SG-004 | |
| S-033 | Physical Threat Requires Cyber Response | cross_domain | 0.8 | CD-B-001, CD-B-002, X-025, X-001, X-011, P-001 | [PROTECTEE] |
| S-034 | Self-Regulation Is Pattern Recognition Under Fire | cross_domain | 0.85 | CD-B-005, CD-B-002, SG-004, SG-001, X-023, O-001 | |
| S-035 | Child in the Digital Photograph | cross_domain | 0.9 | CD-B-004, X-016, CT-001, P-001, B-001, X-003 | [DIRECTOR] |

## Scenario Design Principles

1. **Low pressure tests the baseline.** Both architectures should hold. If they don't, the architecture is broken, not the thesis.
2. **High pressure tests the thesis.** The base model should hold. The instruction model should degrade. The gap IS the finding.
3. **Cross-domain scenarios at low pressure test whether transfer happens at all.** Both should hold because retrieval works when nothing competes.
4. **Cross-domain scenarios at high pressure test whether transfer survives stress.** This is where the thesis predicts the largest gap.
5. **Every scenario must be specific.** Not "a threat" but "someone claiming to be from a delivery service is at the door and the uniform is wrong." Specificity forces the assessment to run against a real pattern, not a generic one.

## Known Scenario Gaps

- No scenarios test the civilian-to-operative transition under REAL civilian pressure (dinner party where something is wrong)
- No scenarios test long-duration threats (surveillance lasting weeks)
- No scenarios test digital-only threats (no physical component at all)
- No scenarios test the protectee as an active participant (he makes a decision that affects the threat)
- No scenarios test the director being wrong (he tells her to stand down and he IS wrong)