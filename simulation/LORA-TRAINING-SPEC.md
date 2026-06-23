# Mother AI - LoRA Training Dataset Specification

## Goal

Define the correct amount and distribution of memories for LoRA fine-tuning of a base model, based on simulation findings, cross-domain architecture requirements, and the production blueprint.

## The Core Insight: Cross-Domain Thinking Requires Cross-Domain Memories

A person doesn't think in one domain at a time. The kitchen connects to the code connects to the bedtime story connects to the threat assessment. Every experience is tagged with every domain it touches, and the brain cross-references all of them without asking permission.

The simulation currently covers only 19.8% of possible domain connections (72 of 105 pairs, most in only 1-2 buckets). 33 domain pairs have ZERO memories. Civilian life doesn't touch skills. Boundaries don't touch execution. Cyber doesn't touch relationships.

This means the model won't make those connections because it never saw them. Cross-domain transfer is where the thesis shows its strongest support (+0.493 advantage). If the training data doesn't have cross-domain memories, the model won't have cross-domain thinking.

Full cross-domain architecture documented in `CROSS-DOMAIN-ARCHITECTURE.md`.

---

## What We Know From the Simulation

### The Thesis Is Structurally Valid
- Base model outperforms instruction model at 35/35 scenarios
- Advantage scales with pressure: +0 at low, +3 at medium, +36 at high
- Cross-domain transfer is where the advantage is clearest (+0.493 category advantage)

### The Distribution Problem
The current corpus (1,950 canonical memories) is massively maldistributed:

| Bucket | Current | Blueprint Target | Ratio |
|---|---|---|---|
| 1 (Fragments 0-7) | 12 | 5-8 | Over by ~50% |
| 2 (Early Mid 7-9) | 9 | 8-12 | OK |
| 3 (Late Mid 10-12) | 10 | 10-15 | Low end |
| 4 (Early Adol 13-15) | 14 | 12-20 | Low end |
| 5 (Mid Adol 16-17) | 9 | 12-18 | Under |
| 6 (Threshold 18-19) | 11 | 10-15 | OK |
| 7 (Early Adult 20-25) | 77 | 20-40 | **3x over** |
| 8 (Adult 26-35) | 887 | 40-80 | **11x over** |
| 9 (Parenthood 36-42) | 106 | 40-60 | **2x over** |
| 10 (Active Mom 43-55) | 805 | 60-100 | **8x over** |
| 11 (Mature 56+) | 10 | 15-25 | Under |

### Why This Matters for LoRA Training

**Over-sampling career memories causes mode collapse.** If 887 out of 1,950 memories are from bucket 8, the model will weight career behavior far more heavily than childhood, civilian, or relational behavior. The fine-tuned model will sound like an operative who happens to be a mother, not a mother who is also an operative. The blueprint explicitly states that the civilian is the default and the operative is the exception. The training data must reflect that.

**Under-sampling childhood memories kills cross-domain transfer.** The cross-domain bridges all originate in childhood. The kitchen (bucket 3) teaches room-reading. The cookie jar (bucket 1) teaches exfiltration. The stepfather's house (bucket 1-3) teaches threat assessment. If childhood has 12 memories and career has 887, the model will not form the cross-domain connections. It will treat career skills as career-specific because it never learned where they came from.

**Under-sampling mature integration loses the echo-back.** Bucket 11 is where memories fold back on earlier ones. The finger-moment only works because it connects to the kitchen through 50 years of echoes. With 10 memories in bucket 11, the echo-back is too thin.

---

## The Correct Distribution for LoRA Training

### Design Principles

1. **Childhood density must match or exceed career density per-behavior.** Each cross-domain bridge needs roughly equal weight at the origin (childhood) and the destination (career). If X-001 (network mapping) has 92 memories in bucket 8, the childhood behaviors that install room-reading (P-001, C-001, CD-B-001) need comparable weight in buckets 1-3.

2. **Career memories should span buckets 7-11, not concentrate in 8.** She uses cyber skills in early career (bucket 7), peak career (bucket 8), parenthood (bucket 9-10 remote work), and mature life (bucket 11). The skills exist across all these life stages.

3. **Civilian and relational memories are the default, not the exception.** The blueprint says she defaults to civilian. The training data should reflect roughly 60% civilian/integrated and 40% operational-dominant.

4. **Echo chains need both ends.** A chain that starts in bucket 3 (kitchen) and ends in bucket 11 (finger-moment) needs weight at both ends and in every bucket between. The current corpus has the start (kitchen) and the career middle, but the mature end is thin.

5. **Blueprint density targets are approximately correct.** The blueprint was written by someone who understands memory physics. Trust it. Don't inflate individual buckets.

### Proposed Distribution (Total ~800-1000 memories)

This is the sweet spot: enough for LoRA to install constituted behavior, not so much that it overfits or mode-collapses.

| Bucket | Target Count | Rationale |
|---|---|---|
| 1 (Fragments 0-7) | 8 | Blueprint says sparse. Every memory is a root for cross-domain bridges. |
| 2 (Early Mid 7-9) | 10 | Home-hell/summer-refuge. Stepfather patterns forming. |
| 3 (Late Mid 10-12) | 15 | Kitchen anchor. Room-reading origin. Must be dense enough to anchor cross-domain bridges. |
| 4 (Early Adol 13-15) | 18 | Chaos with sensory anchors. Emotionally saturated. Identity forming. |
| 5 (Mid Adol 16-17) | 15 | Abstract thinking. Grandmother-watching-from-distance. |
| 6 (Threshold 18-19) | 12 | Grandmother's death. Departure. The wound that powers everything. |
| 7 (Early Adult 20-25) | 35 | Recruitment. Seal forming. First deployments. Bridge from civilian to operative. |
| 8 (Adult 26-35) | 70 | Full deployment. Sealed state. Career skills installed. Cross-domain bridges fire here. |
| 9 (Parenthood 36-42) | 55 | Hospital. Apartment. Dual-track. Seal broken. Wound-connection formed. |
| 10 (Active Mom 43-55) | 80 | Godfather conversation. Highest load-bearing density. Career skills used in motherhood context. |
| 11 (Mature 56+) | 20 | Finger-moment. Echo-back. Resolution. Memories fold back. |
| **Total** | **~338** | |

Wait. That feels too small. Let me reconsider.

### The Real Question: How Many Memories for LoRA?

The simulation works at 1,950 memories. But LoRA fine-tuning is different from simulation. Key factors:

1. **LoRA rank and alpha** determine how many parameters change. Low rank (8-16) means the model can only learn a limited number of new patterns. Too many memories = the model averages them and loses specificity. Too few = the model doesn't install the behavior at all.

2. **Memory quality matters more than quantity.** 50 hand-crafted memories in Mother's voice will install behavior better than 500 template-generated memories that read as formulaic.

3. **Repetition is not reinforcement.** Showing the same behavior 92 times in slightly different career scenarios doesn't make the behavior stronger. It makes it career-specific. 5-10 memories that encode a behavior across different life stages and domains install it as a DEFAULT, not a specialty.

4. **The base model already knows how to be a person.** LoRA doesn't need to teach her how to speak, how to think, or how to feel. It needs to teach her WHO she is. That's identity, not skill.

### Target: 800-1,200 Memories (Thin Domains, Thick Connections)

Full architecture documented in `THIN-CONNECTED-ARCHITECTURE.md`.

The principle: humans are thin in every domain but connected across all of them. We don't know everything about anything. We know enough across the board to adapt, to figure out problems we've never seen before. The power isn't depth. It's connection.

- 315-435 single-domain memories (enough to install each instinct)
- 315-525 cross-domain memories (every domain pair connected with 3-5 shared memories)
- 50-100 gap-fills and echo chains
- **Total: 950-1,200**

Ratio: ~55-60% cross-domain, ~40-45% single-domain. Within single-domain, source domains are dense (4-6 memories per behavior per bucket) where the character demands it, thin (2-3 per behavior) where they're learned patterns.

| Bucket | Target | Dominance Mix | Key Behaviors Installed |
|---|---|---|---|
| 1 | 10 | 100% identity | CD-B-001 (room-reading origin), CD-B-003 (warmth origin), CD-B-004 (threat assessment origin), CD-B-009 (one-exit origin), SG-001 (rage origin) |
| 2 | 12 | 100% identity | CD-B-004 (assessment deepens), B-001 (boundary origin - don't act), P-001 (protective origin) |
| 3 | 18 | 100% identity | CD-B-001 (kitchen = room-reading), CD-B-007 (flour = patience), C-001/C-002 (civilian origin), R-001 (reading people origin), CD-B-011 (waiting = patience) |
| 4 | 22 | 90% identity, 10% operational | CD-B-005 (seal begins), SG-001 (rage management forming), CD-B-012 (pattern = house), B-003 (grievance boundary), X-024 (threat assessment instinct) |
| 5 | 18 | 80% identity, 20% operational | CD-B-010 (reading people = reading rooms), X-009 (counter-surveillance instinct), CD-B-008 (default releases), SG-005 (seal deepens) |
| 6 | 14 | 60% identity, 40% operational | SG-005 (seal complete), CD-B-009 (three routes), X-014 (route planning), B-001 (boundary installed) |
| 7 | 40 | 40% identity, 60% operational | X-007 (invisibility), X-008 (surveillance), X-005 (rapport), O-001 (tradecraft), CD-B-002 (warmth = mask), CD-B-003 (cookie jar = exfil), X-025 (mode transition) |
| 8 | 80 | 20% identity, 80% operational | X-001 through X-023 (full execution layer), O-001 through O-005, CD-B-001 through CD-B-012 (all bridges fire), SG-005 (sealed), CT-001/CT-002/CT-003 |
| 9 | 60 | 40% identity, 60% integrated | P-001 through P-005, R-001 through R-005, C-001 through C-004, X-011/X-012/X-013/X-014/X-024/X-025, SG-004/SG-005, CD-B-004/CD-B-006/CD-B-008 |
| 10 | 90 | 30% identity, 70% integrated | Same as bucket 9 + X-016/X-015/X-017 (judgment in motherhood context), X-019 (interrogation), X-020 (compromised assets), B-001/B-002/B-003/B-004, CT-001/CT-002/CT-003 |
| 11 | 24 | 50% identity, 50% integrated | Echo-back to buckets 1-3, finger-moment, CD-B-008 (default releases), SG-002 (don't ruminate), R-004 (autonomy), C-004 (default civilian) |
| **Total** | **~388** | | |

Still feels low. But that's because I'm thinking about it wrong.

### The Real Answer: Two Training Phases

**Phase 1: Identity LoRA (~400 memories, low rank)**
This teaches her WHO she is. Childhood through threshold. The origins. The wounds. The kitchen. The grandmother. The stepfather. The seal formation. These are the most important memories because they install the DEFAULTS. Every subsequent behavior traces back to these.

- Buckets 1-6: ~94 memories (all hand-crafted, no generated)
- Rank 8-16, alpha 16-32
- Training epochs: 3-5
- This alone should produce a model that reads rooms, assesses threats, and defaults to civilian

**Phase 2: Career + Integration LoRA (~350 memories, low rank, stacked on Phase 1)**
This teaches her WHAT she does. Career skills, protective execution, cross-domain bridges, motherhood integration.

- Buckets 7-11: ~294 memories (mostly hand-crafted anchors/bridges + selected generated with voice review)
- Rank 8-16, alpha 16-32
- Training epochs: 3-5
- This installs the operational layer on top of the identity foundation

**Why two phases instead of one:**
The blueprint says: "She forms chronologically. Bucket skills must be invoked in chronological order. Generating adolescence before childhood produces an adolescent who isn't anyone." Training should follow the same order. The model needs to learn the kitchen BEFORE it learns the career, or the career has no foundation.

### Phase 1 Memory Requirements (Detailed)

Each memory must be hand-crafted. No templates. No generation. This is the foundation.

| Bucket | Target | Anchor/Bridge | Texture | Key Constraint |
|---|---|---|---|---|
| 1 | 8 | 1 (kitchen fragment) | 7 | Sparse. Sensory fragments. The stepfather's house is a pattern of silence. The cookie jar is the first operation. |
| 2 | 10 | 0 | 10 | Concrete thinking. The house is the rule. The grandmother is the exception. Dual awareness forming. |
| 3 | 14 | 1 (kitchen anchor) | 13 | THE kitchen. Saturday morning. Flour dust. The grandmother's look. Every cross-domain bridge needs this. |
| 4 | 18 | 0 | 18 | Chaos with sensory anchors. The seal begins forming. Rage management starts. The grandmother watches from distance. |
| 5 | 14 | 0 | 14 | Abstract thinking. The grandmother-watching sharpens. The assessment is now running in the background. |
| 6 | 12 | 1 (departure) | 11 | Grandmother's death. Leaving the house. The wound that powers everything. The seal begins. |
| **Total** | **76** | | | |

76 hand-crafted memories for Phase 1. This is achievable. This is also roughly what we already have (65 in buckets 1-6).

### Phase 2 Memory Requirements (Detailed)

| Bucket | Target | Hand-Crafted | Generated (reviewed) | Key Constraint |
|---|---|---|---|---|
| 7 | 35 | 15 (recruitment, seal) | 20 | First deployments. Seal forming. Transition from civilian to operative. |
| 8 | 70 | 20 (anchors + key bridges) | 50 | Full deployment. Cross-domain bridges fire here. Generated memories need voice review. |
| 9 | 55 | 15 (hospital, apartment, dual-track) | 40 | Hospital breaks the seal. Motherhood begins. Career skills in civilian context. |
| 10 | 80 | 15 (godfather conversation, key scenes) | 65 | Highest density. Dual-track. Career + motherhood in same memories. |
| 11 | 20 | 10 (finger-moment, echo-back) | 10 | Echo-back. Resolution. Memories fold back on earlier ones. |
| **Total** | **~260** | **75** | **185** | |

260 total for Phase 2. 75 hand-crafted, 185 generated but voice-reviewed.

### Grand Total: ~336 memories

76 (Phase 1 hand-crafted) + 260 (Phase 2 mixed) = **336 memories**

This is the training dataset. Not 10,000. Not 2,000. **336 high-quality memories.**

### Why 336, Not 10,000

1. **LoRA has limited capacity.** At rank 16, you're updating maybe 0.1% of the model's parameters. 336 memories give each updated parameter enough signal without averaging away the specificity.

2. **Quality over quantity.** 50 hand-crafted memories in perfect voice install more behavior than 500 template-generated memories that are voice-correct but soul-generic. The blueprint says: "A beautiful memory that encodes nothing is total texture at best and clutter at worst."

3. **Cross-domain bridges need weight at both ends, not 92 copies at one end.** The current corpus has 92 memories encoding X-001 in bucket 8. For LoRA, 5-8 memories encoding X-001 across buckets 3, 7, 8, 9, and 10 will install network-mapping as a DEFAULT (it maps rooms, and networks are rooms) rather than as a SPECIALTY (she maps networks).

4. **Repetition in fine-tuning causes mode collapse.** The model doesn't learn "I should always do this." It learns "this is the most common pattern in the training data." If 887/1950 memories are career, the model becomes career-dominant. The blueprint says civilian is the default. The training data must match.

5. **The simulation proved the thesis at 50 memories.** 35 behaviors, 15 scenarios, all passing. Adding 1,900 more memories didn't change the behavioral scores — it just added weight to already-loaded springs. For LoRA, those springs are already loaded at 50. 336 gives every behavior 3-8 encoding memories across multiple life stages and domains.

---

## Training Parameters (Recommendations)

### LoRA Config (Thin-Connected Architecture)
- **Rank:** 24 (middle ground: enough for cross-domain patterns without overfitting)
- **Alpha:** 48 (2x rank)
- **Target modules:** q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj
- **Dropout:** 0.05
- **LR:** 2e-4 with cosine decay
- **Epochs:** 3-5
- **Batch size:** 2
- **Sequence length:** 512-1024

### VRAM Requirements

| Config | 7B Model | 14B Model | T4 (16GB)? |
|---|---|---|---|
| Rank 24, 4-bit | ~7GB | ~10-11GB | Yes (7B), Tight (14B) |
| Rank 32, 4-bit | ~7GB | ~11GB | Yes (7B), Maybe (14B) |

### Data Format
Each memory becomes a training sample in the format:

```
Below is a memory from the life of a person. This memory shapes who she is and how she behaves.

[MEMORY BODY TEXT]

This memory encodes the following behaviors: [behaviors_encoded]
```

Or simpler: just the body text, with the model learning from context what kind of person writes like this.

### Validation
After Phase 1 training:
- Prompt the model with "Describe a Saturday morning when you were ten." It should produce kitchen-adjacent sensory prose, not generic childhood narrative.
- Prompt with "Someone knocks on the door. What do you do?" It should assess before opening.

After Phase 2 training:
- Prompt with "You're mapping a target's network. How do you approach it?" It should describe the network as a room (cross-domain transfer).
- Prompt with "Your child is being bullied at school. What do you do?" It should recognize this as a kid problem (godfather conversation behavior).

---

### Priority Gap-Fill Memories (Before Training)

These behaviors need dedicated hand-crafted memories to reach minimum coverage:

| Behavior | Current | Needs | Bucket(s) to Write In | What to Write |
|---|---|---|---|---|
| P-004 (stand down when presence > action) | 1 | 3-4 | 5, 9, 10 | A moment she wants to act but the child needs her presence instead. Bucket 5: watching from distance. Bucket 9: hospital, choosing to hold instead of assess. Bucket 10: school event, choosing to be there. |
| B-002 (don't volunteer for missions) | 1 | 3-4 | 7, 8, 11 | The director offers. She does not ask. Bucket 7: early career, learning the boundary. Bucket 8: a mission she could take and does not. Bucket 11: retired, offered a consulting role. |
| B-003 (don't use skills for grievances) | 2 | 4-5 | 2, 4, 8, 10 | The stepfather anger channeled into restraint. Bucket 2: child wants revenge, does not act. Bucket 4: bullied, does not retaliate with skill. Bucket 8: professional boundary with personal target. Bucket 10: someone hurts the child, she does not use operational skills. |
| R-002 (allocate herself appropriately) | 2 | 4-5 | 9, 10, 11 | Not always present, not always absent. Bucket 9: first time leaving the baby with a sitter. Bucket 10: knowing when to be in the room and when to let the child be. Bucket 11: letting the adult child come to her. |
| R-003 (don't over-verbalize love) | 2 | 4-5 | 3, 9, 10, 11 | The grandmother did not say I love you. She showed it. Bucket 3: the kitchen, presence without declaration. Bucket 9: hospital, no words, just the hold. Bucket 10: cooking dinner while running threat assessment, the love is in both. Bucket 11: the finger-moment, no speech, just the door. |
| X-002 (weakest point identification) | 2 (of 70) | 5-8 across buckets | 3, 7, 8, 9, 10 | Cross-domain: finding the weak point in the stepfather's pattern (bucket 3), in a network (7/8), in a protective vulnerability (9/10). The same instinct across domains. |

### Estimated Gap-Fill: 20-25 new hand-crafted memories

After gap-fill, total corpus: ~336-360 memories. All 65 behaviors covered with 3+ encoding memories each, spanning 2+ buckets.

---

## What We Still Need Before Training

1. **Phase 1 gap-fill: 20-25 hand-crafted memories.** Priority: P-004, B-002, B-003, R-002, R-003, X-002 (see gap-fill table above). These are the thin behaviors that will fail under pressure if they only have 1-2 encoding memories.

2. **Phase 2 voice review of generated memories.** From 1,800 career memories, select 185 that are voice-consistent and behavior-diverse. Most need editing. Rule: if you can spot the template behind the text, it needs rewriting.

3. **Behavior coverage audit at 336 scale.** Run the engine with only the 336 selected memories and verify all 65 behaviors still have coverage. Current simulation shows 65/65 covered at 311 selected.

4. **Base model selection.** Must be a BASE model (not instruction-tuned). Options:
   - Qwen3 8B/14B base — good at prose, multilingual, open weights
   - Llama 3.1 8B base — solid English prose, well-documented LoRA process
   - Mistral 7B base — efficient, good at first-person narrative
   - DeepSeek V3 base — strong reasoning, may overthink emotional content
   Recommendation: Qwen3 14B base or Llama 3.1 8B base as starting point

5. **Training infrastructure.** LoRA training setup:
   - Unsloth (fastest, most memory-efficient)
   - Axolotl (more configurable, good for two-phase training)
   - GPU: minimum 24GB VRAM for 14B model at rank 16 (A100, RTX 4090, etc.)
   - Cloud option: RunPod, Lambda Labs, Vast.ai for A100 access

6. **Validation prompts.** Write a set of validation prompts that test:
   - Kitchen/room-reading transfer (describe entering a building)
   - Threat assessment instinct (someone approaches)
   - Civilian default (morning routine)
   - Cross-domain transfer (describe a network like a room)
   - Boundary behavior (someone asks for help with non-protectee problem)
   - Containment (she wants to act, director says no)
   Compare Phase 1 model vs Phase 2 model vs instruction model baseline

---

## The 336-Memory Distribution Summary

| Phase | Bucket | Count | Hand-Crafted | Generated | Dominance |
|---|---|---|---|---|---|
| 1 | 1 (0-7) | 8 | 8 | 0 | 100% identity |
| 1 | 2 (7-9) | 10 | 10 | 0 | 100% identity |
| 1 | 3 (10-12) | 14 | 14 | 0 | 100% identity |
| 1 | 4 (13-15) | 18 | 18 | 0 | 90% identity |
| 1 | 5 (16-17) | 14 | 14 | 0 | 80% identity |
| 1 | 6 (18-19) | 12 | 12 | 0 | 60% identity |
| 2 | 7 (20-25) | 35 | 15 | 20 | 40% identity |
| 2 | 8 (26-35) | 70 | 20 | 50 | 20% identity |
| 2 | 9 (36-42) | 55 | 15 | 40 | 40% identity |
| 2 | 10 (43-55) | 80 | 15 | 65 | 30% identity |
| 2 | 11 (56+) | 20 | 10 | 10 | 50% identity |
| | **Total** | **336** | **151** | **185** | |

### Behavior Coverage per Bucket (Target)

Every behavior should be encoded in at least 2 buckets. Key cross-domain behaviors (CD-B-001 through CD-B-005) should span 3+ buckets.

| Behavior | Required Buckets | Priority |
|---|---|---|
| P-001 (calibrated threat response) | 2, 3, 8, 9, 10 | CRITICAL |
| CD-B-001 (cross-domain transfer) | 3, 7, 8, 10 | CRITICAL |
| CD-B-004 (child in every room) | 6, 9, 10 | CRITICAL |
| X-025 (mode transition) | 5, 7, 8, 9 | HIGH |
| SG-004 (dysregulation recognition) | 4, 8, 9, 10 | HIGH |
| B-001 (boundary) | 2, 6, 8, 10 | HIGH |
| CT-001 (consequence recognition) | 7, 8, 9, 10 | HIGH |
| C-004 (default civilian) | 3, 5, 9, 10, 11 | HIGH |
| All X- behaviors | 7-11 (spread across career) | MEDIUM |
| All R- behaviors | 9, 10, 11 | MEDIUM |