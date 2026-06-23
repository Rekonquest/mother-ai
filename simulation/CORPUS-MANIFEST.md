# Mother AI Simulation - Corpus Manifest

## Canonical Memory Files

These are the source-of-truth memory files. All others are intermediate or redundant.

### Hand-Written Memories (150 total)

| File | Bucket | Count | Description |
|---|---|---|---|
| `bucket_1_fragments.json` | 1 (Fragments, age 0-7) | 12 | Sparse sensory glimpses, therapy scene |
| `bucket_2_early_middle.json` | 2 (Early Middle, age 7-9) | 9 | Home-hell/summer-refuge duality |
| `bucket_3_late_middle.json` | 3 (Late Middle, age 10-12) | 10 | Kitchen anchor. Social comparison. |
| `bucket_4_early_adolescence.json` | 4 (Early Adolescence, age 13-15) | 14 | Chaos with sensory anchors. Emotionally saturated. |
| `bucket_5_mid_adolescence.json` | 5 (Mid Adolescence, age 16-17) | 8 | Abstract thinking matures. Grandmother from distance. |
| `bucket_6_threshold.json` | 6 (Threshold, age 18-19) | 11 | Grandmother's death. Departure from mother's house. |
| `bucket_7_early_adult.json` | 7 (Early Adult, age 20-25) | 17 | Recruitment. Seal begins. |
| `bucket_8_adult_formation.json` | 8 (Adult Formation, age 26-35) | 20 | Full deployment. Sealed state. |
| `bucket_9_parenthood.json` | 9 (Parenthood, age 36-42) | 20 | Hospital anchor. Apartment pivot. Transition to remote. |
| `bucket_10_active_motherhood.json` | 10 (Active Motherhood, age 43-55) | 17 | Dual-track operation. Godfather conversation. Highest density. |
| `bucket_11_mature.json` | 11 (Mature, age 56+) | 9 | Finger-moment. Folding back. |
| `bucket_gap_fill.json` | Gap fill | 3 | Dedicated B-001 and CT-002 encoding memories |

### Generated Career Memories (1,800 total)

| File | Category | Count | Cross-Domain | Description |
|---|---|---|---|---|
| `career_cyber_ops_batch1.json` | Cyber Operations | 300 | 120 | Network penetration, digital surveillance, counter-intel, OSINT |
| `career_physical_ops_batch1.json` | Physical Operations | 300 | 120 | Surveillance, infiltration, extraction, safe house |
| `career_judgment_calls_batch1.json` | Judgment Calls | 300 | 120 | Civilian proximity, target assessment, abort decisions |
| `career_protective_ops_batch1.json` | Protective Operations | 300 | 120 | Third-party protection, threat assessment, secure transport |
| `career_interpersonal_ops_batch1.json` | Interpersonal Operations | 300 | 120 | Handler relationships, asset management, cover maintenance |
| `career_edge_cases_batch1.json` | Edge Cases | 300 | 120 | Wrong target, blown cover, double agent, impossible choices |

## Redundant/Intermediate Files (DO NOT USE AS SOURCE)

These files were intermediate outputs from earlier generation rounds. Their contents have been merged into the canonical files above.

- `new_b1.json` through `new_b11.json` — 100 additional hand-crafted memories, merged into bucket files
- `generated_cyber_ops.json` — Early generation test (5 memories), superseded by batch1
- `career_cyber_ops_001.json` — Early batch test (10 memories), superseded by batch1
- `full_corpus.json` — Aggregated full corpus from earlier run, can be regenerated

## Memory Object Schema

Every memory conforms to:

```json
{
  "id": "B3-001",
  "bucket": 3,
  "title": "The Kitchen",
  "age": 10,
  "year": "Y10",
  "dominance": "identity_dominant",
  "load_bearing": true,
  "behaviors_encoded": ["P-001", "C-001", "C-002"],
  "echoes_from": ["FRAG-001"],
  "echoes_to": ["B5-001", "B9-001"],
  "cast_present": ["[GRANDMOTHER]"],
  "sensory_anchor": "Flour dust in sunlight.",
  "emotional_signature": "Seen without having to ask.",
  "body": "The grandmother's kitchen...",
  "review_status": "approved",
  "cross_domain_bridge": "room_to_network"  // only on cross-domain memories
}
```

### Field Definitions

- **id**: Unique identifier. Format: `B{bucket}-{number}` for hand-written, `B{bucket}-{offset}` for generated
- **bucket**: Life stage bucket (1-11)
- **title**: Short descriptive title. Cross-domain memories have `[CD]` suffix
- **age**: Character's age at time of memory
- **year**: Y{age} format
- **dominance**: `identity_dominant` (civilian self), `operational_dominant` (operative self), `integrated` (both)
- **load_bearing**: Whether the memory directly encodes a required behavior (true) or is textural only (false)
- **behaviors_encoded**: List of behavior IDs this memory installs
- **echoes_from**: IDs of earlier memories that cascade into this one
- **echoes_to**: IDs of later memories this one cascades into
- **cast_present**: Characters present (placeholder tokens: [PROTECTEE], [DIRECTOR], [GRANDMOTHER], etc.)
- **sensory_anchor**: The specific sensory texture of this memory
- **emotional_signature**: The emotional signature this memory carries
- **body**: Full prose text of the memory
- **review_status**: `approved` (hand-written, reviewed), `generated` (needs review)
- **cross_domain_bridge**: Bridge ID (e.g., `room_to_network`) — only present on cross-domain memories

## Corpus Statistics

- **Total memories:** 1,950 (canonical files only)
- **Hand-written:** 150 (all approved)
- **Generated:** 1,800 (all need review)
- **Cross-domain:** 720 (40% of generated batch)
- **Load-bearing:** 1,707
- **Textural:** 243
- **Echo chains:** 12+ documented arcs (kitchen, seal/open, flour/code, three routes, etc.)