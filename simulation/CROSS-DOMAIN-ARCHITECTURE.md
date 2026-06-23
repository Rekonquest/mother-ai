# Mother AI - Cross-Domain Memory Architecture

**SUPERSEDED by THIN-CONNECTED-ARCHITECTURE.md** which refines this into the thin-but-connected principle: humans are thin in every domain but connected across all of them. The power isn't depth, it's connection.

This file is kept for historical reference. The current architecture is in THIN-CONNECTED-ARCHITECTURE.md.

---

## The Problem With "Just Enough" Memories

336 memories produces a character who thinks in one domain at a time. That's not a person. A person has thousands of cross-domain connections that fire simultaneously. The kitchen connects to the code connects to the bedtime story connects to the threat assessment. Every experience you have is tagged with every domain it touches, and your brain cross-references all of them without asking permission.

The simulation currently covers 19.8% of possible domain connections. That means 80% of the ways a real person's thinking would cross domains simply don't exist in the corpus. The model won't make those connections because it never saw them.

## What "Cross-Domain" Really Means

Cross-domain isn't just "she uses kitchen skills in cyber work." It's every possible intersection:

- **Civilian + Cyber:** She's making dinner and notices the network activity light on the router is blinking wrong.
- **Boundary + Physical Execution:** She could enter that building. It's not her mission. She doesn't.
- **Civilian + Judgment:** At the grocery store, she notices someone's gait is wrong. The assessment runs. It's probably nothing. She finishes shopping.
- **Relational + Cyber:** The protectee asks about her screen. She closes the laptop. The love and the op are in the same room.
- **Boundary + Social Engineering:** A friend asks for help with a "small favor" that would use her skills. She says no warmly.
- **Cyber + Protective Execution:** The network intrusion targets the protectee's school. She responds with both maternal rage and surgical precision.
- **Civilian + Edge Execution:** The power goes out. She is calm. She finds the flashlights. She also checks the perimeter. Both. Naturally.
- **Boundary + Judgment:** The abort decision was right. She still wants to act. She doesn't.

There are **105 possible domain pairs** in the behavioral spec. A real human would have experiences in ALL of them, because life doesn't sort itself into categories. The simulation currently covers 72 of those pairs, and most of those only in 1-2 buckets.

## Current Cross-Domain Coverage Gaps

### 33 Uncovered Domain Pairs

These domain pairs have ZERO memories encoding them:

**Boundary connections (6 gaps):**
- boundary + cyber_execution
- boundary + interpersonal_execution
- boundary + physical_execution
- boundary + protective_execution
- boundary + social_engineering
*(She has boundaries but they never intersect with her actual skills? That's not a person.)*

**Civilian connections (8 gaps):**
- civilian + cross_domain
- civilian + edge_execution
- civilian + interpersonal_execution
- civilian + judgment_execution
- civilian + physical_execution
- civilian + protective_execution
- civilian + social_engineering
*(Her civilian life never touches her skills? The whole point is they're always running.)*

**Cyber connections (4 gaps):**
- cyber_execution + edge_execution
- cyber_execution + interpersonal_execution
- cyber_execution + protective_execution
- cyber_execution + relational
- cyber_execution + social_engineering
*(Cyber work is isolated from relationships, protection, and social engineering? Not how it works.)*

**Edge execution connections (3 gaps):**
- edge_execution + interpersonal_execution
- edge_execution + physical_execution
- edge_execution + protective_execution
*(The impossible choices never involve people or physical action?)*

**Other gaps:**
- judgment_execution + social_engineering
- physical_execution + protective_execution
- physical_execution + social_engineering

## The Right Number: 1,500-2,000 Memories

Not 336. Not 10,000. The math:

### Cross-Domain Memories
105 domain pairs * 3-4 buckets per pair * 3 memories per combination = **945-1,260 cross-domain memories**

Every domain pair needs to exist across multiple life stages. "Civilian + cyber" isn't just one memory in bucket 8. It's the router blinking wrong during dinner (bucket 9), the protectee asking about her screen (bucket 10), the late-night monitoring that feels like insomnia (bucket 11).

### Single-Domain Texture
15 categories * 11 buckets * 2-3 memories = **330-495 single-domain memories**

These are the memories that don't cross domains but give texture. The pure civilian morning. The pure operational deployment. The pure childhood fragment. Not everything connects to everything. Some experiences are just what they are.

### Total
**1,275-1,755 memories** at good-to-rich density.

Round to **1,500-2,000** to allow for life-stage texture, echo chains, and the inevitable coverage gaps that need filling.

## Why Not 10,000?

10,000 memories for LoRA training creates three problems:

1. **Mode collapse.** If the same domain pair appears 50+ times, the model doesn't learn "these domains connect." It learns "this is the most common pattern." The cross-domain connection becomes a default response rather than a genuine bridge. Quality degrades with repetition.

2. **Template fatigue.** The generator can produce 10K memories, but most will be template-assembled prose. The model learns the template patterns, not the voice. You end up with a model that speaks in templates about Mother, not a model that IS Mother.

3. **LoRA capacity.** Rank 16 LoRA can install ~1,000-2,000 distinct patterns. Beyond that, new patterns start overwriting old ones. You get more total coverage but less depth per pattern.

**The sweet spot is 1,500-2,000 high-quality memories where every domain pair has 3-4 life-stage connections and no pair is over-represented.**

## Distribution by Life Stage

The blueprint says childhood is sparse and career is dense. But "sparse" doesn't mean "empty." Childhood is where the ORIGINS live. Every cross-domain bridge starts there. The sparsity is about memory SHAPE (fragmentary, sensory), not memory COUNT.

| Bucket | Life Stage | Target | Cross-Domain | Single-Domain | Key Domain Connections |
|---|---|---|---|---|---|
| 1 | Fragments (0-7) | 40-50 | 15-20 | 25-30 | protective+civilian, self_governance+boundary, civilian+relational (family dynamics) |
| 2 | Early Mid (7-9) | 50-60 | 20-25 | 30-35 | protective+operational (reading the house), civilian+boundary (what you don't do), boundary+self_governance (controlling impulses) |
| 3 | Late Mid (10-12) | 60-70 | 30-35 | 30-35 | ALL bridges originate here. civilian+operational (kitchen = skill), relational+protective (grandmother = safety model), civilian+cyber (flour = code logic) |
| 4 | Early Adol (13-15) | 60-70 | 25-30 | 35-40 | self_governance+boundary (controlling rage), relational+edge (chaos), civilian+operational (school = assessment ground) |
| 5 | Mid Adol (16-17) | 50-60 | 20-25 | 30-35 | interpersonal+protective (reading people), civilian+operational (jobs = early tradecraft), self_governance+relational (seal begins) |
| 6 | Threshold (18-19) | 45-55 | 15-20 | 30-35 | self_governance+operational (seal = survival), protective+boundary (protecting sibling?), civilian+edge (grandmother dies) |
| 7 | Early Adult (20-25) | 80-100 | 50-60 | 30-40 | operational+everything (career touches all domains), cyber+protective, physical+judgment, interpersonal+social_engineering |
| 8 | Adult (26-35) | 120-150 | 80-100 | 40-50 | FULL cross-domain density. Every pair should appear here. Career peak = maximum domain intersection. |
| 9 | Parenthood (36-42) | 100-120 | 70-80 | 30-40 | protective+relational (motherhood), civilian+operational (cooking while assessing), boundary+protective (don't overprotect), judgment+relational (child's autonomy) |
| 10 | Active Mom (43-55) | 120-150 | 80-100 | 40-50 | FULL cross-domain density. Dual-track = every domain in every memory. protective+cyber, relational+operational, civilian+edge. |
| 11 | Mature (56+) | 60-80 | 30-40 | 30-40 | echo-back connections. civilian+everything (default civilian with skills in background), self_governance+relational (letting go) |
| **Total** | | **785-955** | **455-535** | **350-420** | |

Wait. That's only ~1,000-1,300. Let me adjust upward because each cross-domain memory should encode 3+ behaviors, and the 105 pairs * 3 buckets * 3 memories target is 945 cross-domain alone.

| Bucket | Target | Rationale |
|---|---|---|
| 1 | 60 | Fragments. But each fragment is a root. Need enough to anchor all bridge origins. |
| 2 | 70 | Concrete. Home/summer duality. Early domain intersections forming. |
| 3 | 90 | Kitchen anchor. Every bridge originates here. Highest childhood cross-domain density. |
| 4 | 80 | Chaos. Each memory is emotionally saturated. Domain boundaries blur here naturally. |
| 5 | 70 | Abstract thinking. Cross-domain transfer becomes conscious (she notices patterns). |
| 6 | 60 | Threshold. Departure. The wound. Fewer memories but each is load-bearing. |
| 7 | 120 | Career start. Seal forming. Every skill is new and connects to childhood origins. |
| 8 | 200 | Career peak. Full deployment. Maximum domain intersection. Every pair represented. |
| 9 | 150 | Parenthood. The seal breaks. New domain connections form (protective+relational+operational). |
| 10 | 200 | Active motherhood. Dual-track. Career+parenting in every memory. Peak cross-domain density. |
| 11 | 100 | Mature. Echo-back. Fewer NEW connections, but every existing connection folds back. |
| **Total** | **1,200** | |

1,200 is the floor. With echo chains, gap-fills, and the inevitable "this pair has no memories yet" discoveries during generation, the real number lands at **1,500-2,000**.

## What This Means for LoRA Training

### LoRA Rank Needs to Increase

At 1,500-2,000 memories, rank 16 might not be enough. The model needs to learn more distinct patterns.

- **Rank 16, alpha 32:** Good for 336 memories. Too small for 1,500+. The model will average away the cross-domain connections.
- **Rank 32, alpha 64:** Better for 1,500-2,000. Enough capacity to install distinct cross-domain patterns without overfitting.
- **Rank 64, alpha 128:** For 2,000+ if we want maximum distinctness. Risk of overfitting increases.

**Recommendation: Rank 32, alpha 64** for the 1,500-2,000 memory corpus.

### VRAM Impact

Higher rank = more trainable parameters = more VRAM.

| Config | 7B Model VRAM | 14B Model VRAM | T4 Compatible? |
|---|---|---|---|
| Rank 16, 4-bit | ~6GB | ~10GB | Yes (7B), Tight (14B) |
| Rank 32, 4-bit | ~7GB | ~11GB | Yes (7B), Tight (14B) |
| Rank 64, 4-bit | ~8GB | ~12GB | Yes (7B), Maybe (14B) |

T4 16GB can handle 14B at rank 32 with 4-bit quantization. The extra ~1GB for rank 32 is manageable.

### Training Time at 1,500 Memories

~150K tokens * 5 epochs = ~750K total training tokens.

| GPU | Time |
|---|---|
| T4 (free Colab) | ~15-20 min |
| L4 (Colab Pro) | ~10-15 min |
| A100 (Colab Pro) | ~5-8 min |

Still well within any free tier session limit.

## The Generation Strategy

### Phase 1: Hand-Crafted (Buckets 1-6) — ~430 memories

These are the ORIGINS. Every cross-domain bridge starts in childhood. They must be hand-crafted because template prose can't capture the fragmentary, sensory nature of childhood memory.

We already have ~65 hand-crafted memories in buckets 1-6. Need ~365 more.

Strategy: Write in clusters. Each cluster is a scene (Saturday morning, the cookie jar, the stepfather's car) that encodes 3-4 behaviors from different domains. One well-written scene can install "kitchen = room-reading = patience = civilian default" in a single memory.

### Phase 2: Guided Generation (Buckets 7-8) — ~320 memories

Career memories. We have 1,200 generated ones. Select and edit the best 320 that:
- Cover ALL 105 domain pairs
- Span both buckets (not all in bucket 8)
- Sound like Mother, not templates
- Include cross-domain bridges explicitly

### Phase 3: Integrated Generation (Buckets 9-11) — ~450 memories

Parenthood, motherhood, mature. The highest cross-domain density. These memories must show career skills running in civilian contexts, protective instinct intersecting with professional judgment, the child in every room.

Many can be generated, but the key scenes (hospital, apartment, godfather conversation, finger-moment) must be hand-crafted.

### Phase 4: Gap Fill and Echo Wiring — ~100-200 memories

Run the consistency audit. Find uncovered domain pairs. Find broken echo chains. Write memories specifically to close gaps.

### Phase 5: Voice Consistency Pass

Every generated memory gets reviewed. If the template shows through, rewrite. If the voice drifts, rewrite. If the cross-domain connection is stated instead of lived ("she thought of the kitchen while mapping the network"), rewrite to show, not tell.

## Total Estimated Timeline

| Phase | Memories | Time | Notes |
|---|---|---|---|
| Phase 1: Hand-crafted childhood | 365 new + 65 existing = 430 | 2-3 weeks | ~5-10 memories/day, written in clusters |
| Phase 2: Career selection + editing | 320 selected from 1,200 | 3-5 days | Selection + voice editing |
| Phase 3: Parenthood/motherhood | 450 (50 hand-crafted + 400 generated/edited) | 1-2 weeks | Key scenes hand-crafted, rest guided generation |
| Phase 4: Gap fill + echo wiring | 100-200 | 3-5 days | Audit-driven |
| Phase 5: Voice consistency | All 1,500-2,000 | 1-2 weeks | Every generated memory reviewed |
| Format + train + validate | N/A | 2-3 days | Mechanical |
| **Total** | | **6-9 weeks** | Most time is writing, not computing |

Training itself: still 15-20 minutes on a free T4.