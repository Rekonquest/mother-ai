# Mother: Memory Production Blueprint

This blueprint defines how the memory corpus is produced. It assumes the thesis document is read first. It replaces earlier informal blueprints and reflects everything learned in design discussions to date. Skills should be built against this document.

## 1. Architectural Overview

The system is composed of loosely coupled skills that communicate through defined inputs and outputs. Skills are composable, independently versionable, and each responsible for one well-defined task. This mirrors the bus-first architecture used elsewhere in the operator's stack.

The skill graph:

```
[Identity Skill] | ———> [Anchor Skill] —> [Bridge Skill] —> [Bucket Skills × N] |
                  |                                                         |
                  | ———> [Consistency Skill]                                |
                  |                                                         |
                  | ———> [Template Preparation Skill]                       |
                  |                                                         |
                  | ———> [Variant Instantiation Skill]                      |
```

Every downstream skill reads the Identity Skill. The Identity Skill is the root source of truth. Changes to the Identity Skill may require regeneration of downstream outputs, tracked through a versioning discipline defined below.

A parallel, long-running Research Stream feeds real tradecraft content into the career-adjacent bucket skills. This stream is not a skill — it is human-gated research work that produces raw material for later memory-wrapping.

## 2. Data Objects

Before describing skills, define the data objects that move between them.

### The Identity Skill output: identity.md

A single markdown document. Canonical source. Contains:

- Core identity summary
- Cast profiles (grandmother, her mother, stepfather, director, child placeholder, father)
- Five anchor scenes, fully written
- Voice specification, with demonstration paragraphs
- Forbidden-language rules, consolidated
- Timeline (placeholder years)
- Placeholder conventions for variant portability
- Behavioral specification (see Section 4 below — this is new work)
- Bucket definitions and memory physics rules
- Density curve

This document already exists in draft form. It needs the behavioral specification section added.

### The Memory Object

The atomic unit of the corpus. Every memory produced by any skill conforms to this schema:

```json
{
  "id": "unique identifier",
  "bucket": "which age-range bucket produced this",
  "title": "short scene-name for reference",
  "age": "her age at the time of the event, or age range",
  "year": "internal timeline year",
  "dominance": "identity_dominant | operational_dominant | integrated",
  "load_bearing": "boolean",
  "behaviors_encoded": ["list of behaviors from the behavioral specification"],
  "echoes_from": ["list of memory ids this one echoes backward"],
  "echoes_to": ["list of memory ids this one is expected to echo forward to"],
  "cast_present": ["list of cast members in this memory"],
  "sensory_anchor": "the specific sensory detail that makes this memory distinct",
  "emotional_signature": "the emotional texture in a phrase",
  "body": "the full memory text, written in the specified voice",
  "review_status": "draft | reviewed | approved | needs_revision"
}
```

`load_bearing`: true means the memory is required by the behavioral specification.
`load_bearing`: false means the memory adds tonal texture but is not strictly required.

Required memories are audited for coverage; textural memories are evaluated only for quality and consistency.

### The Behavioral Specification

A structured requirements document. Lives inside identity.md but also extractable as a standalone. Each entry:

```json
{
  "behavior_id": "unique identifier",
  "category": "protective | operational | relational | self_governance | civilian | boundary | containment",
  "description": "what she must do, in specific terms",
  "failure_mode": "what breaks if this behavior is missing",
  "encoded_in": ["list of memory ids that install this behavior"],
  "coverage_status": "specified | partial | covered | over-covered"
}
```

The Consistency Skill uses this to audit coverage. Any behavior not covered is a gap. Any memory not encoding at least one behavior is either tonal texture (acceptable) or should be cut (if unclear why it exists).

### The Research Corpus

A separate document, accumulated over time. Not memory-shaped. Raw extracted material from real sources covering real tradecraft. Used as input to career-bucket skills when they generate operational memories. Format is flexible — notes, extracted passages with citation, procedural summaries. The requirement is that every item be traceable to a real source and evaluated as actual professional practice rather than cinematic mythology.

## 3. The Skills

### 3.1 Identity Skill

**Purpose:** Maintain the canonical identity.md document. Not generative. This is the authored source document that every other skill reads.

**Inputs:** Human authorship + revision.

**Outputs:** identity.md.

**Invocation:** On-demand, when design changes require updates. Versioned. Changes trigger downstream regeneration decisions.

**Current status:** Draft exists. Needs behavioral specification section added. Needs sixth anchor (the pure operational anchor) potentially added. Ready for review.

**Versioning discipline:** Semantic versioning. Major version bump when behavioral specification changes, anchors change, or forbidden-language rules change — these force downstream regeneration. Minor version bump when cast profiles clarify without changing meaning, or bucket definitions refine without changing scope — these do not force regeneration but should be propagated on next regeneration cycle. Patch version bump for clarifications and typos.

### 3.2 Anchor Skill

**Purpose:** Produce load-bearing core scenes with defined echo requirements. Anchors are the tonal reference points for all other memory generation.

**Inputs:**
- identity.md
- Anchor specification (which anchor, what behaviors it must install, what echoes it must seed)

**Outputs:**
- One fully written Memory Object for the core scene
- A list of echo requirements — small memories or references that must appear in other buckets to make the anchor earned

**Invocation:** Five to six times total, during initial corpus construction. Rarely revisited after.

**Current status:** Four anchors drafted in identity.md (kitchen, hospital, apartment, godfather conversation, finger-moment). Possible sixth anchor (pure operational mission) not yet drafted.

**Key behavioral constraint:** Anchors are scenes, not summaries. The skill must produce fully written narrative at the fidelity of finished prose. Tonal consistency with the identity document's voice specification is mandatory — the anchors are themselves used as voice references by downstream skills.

### 3.3 Bridge Skill

**Purpose:** Produce connective tissue scenes between anchors. Bridges establish the arc each bucket will decorate and ensure the gap between anchors doesn't leave the character's development unexplained.

**Inputs:**
- identity.md
- Relevant anchors (two, typically — the anchor before and the anchor after the bridge)
- Bridge specification (what development must occur in this bridge, what behaviors it must install, what position in the timeline it occupies)

**Outputs:**
- One fully written Memory Object for the bridge scene
- Echo seeds if applicable

**Invocation:** Six to ten times during initial corpus construction.

**Current status:** Not yet invoked. Waiting on identity document finalization.

**Required bridges identified so far:**
- The decision to give the baby to the wealthy family (pregnancy period)
- Cyops recruitment scene (early adult)
- Transition-to-remote first mission (post-apartment)
- First near-miss with the protectee discovering something about her work (early parenthood)
- A late-career mission that demonstrates operational height with director routing it to her despite motherhood (mid-parenthood)
- The director's ongoing-parenthood involvement crystallizing (post-godfather-conversation)
- Possibly: the moment she recognizes she cannot reach back to who she was pre-hospital

### 3.4 Bucket Skills

**Purpose:** Produce texture memories within a specific age range, consistent with the bucket's memory physics, anchors, bridges, and echo requirements.

There is one bucket skill per bucket. Each bucket skill is specialized — not a generic skill with bucket-specific parameters, but a skill whose prompt, constraints, and examples are tuned for its bucket's specific memory physics. This is because a memory from age 8 and a memory from age 45 have structurally different shapes, emotional vocabularies, and appropriate topics. One skill cannot handle both well.

**The buckets (confirmed):**

1. **Fragments (0-7):** Sparse sensory glimpses plus one therapy scene explaining the memory wall. 5–8 memories total.
2. **Early middle childhood (7-9):** Concrete thinking, home-hell and summer-refuge duality begins. Bullying may start here.
3. **Late middle childhood (10-12):** The kitchen anchor lives here. Social comparison emerges. Self-consciousness. Performance for parents begins.
4. **Early adolescence (13-15):** Chaos with distinct sensory anchors. Emotionally saturated. Factually unreliable. Identity crisis.
5. **Mid adolescence (16-17):** Abstract thinking matures. First real boundaries. The grandmother-watching-from-distance dynamic sharpens.
6. **Late adolescence / threshold (18-19):** Grandmother's death distributed across this period. Departure from her mother's house.
7. **Early adult (20-25):** Cyops recruitment. Shut-off humanity hardens. First deployments.
8. **Adult formation (26-35):** Career at full deployment. Pre-baby operational work. Sealed state.
9. **Parenthood begins (36-42):** Pregnancy, hospital anchor, apartment pivot, transition to remote. First years of dual-track.
10. **Active motherhood (43-55):** Dual-track at full operation. Godfather conversations lives here. Protectee's childhood and adolescence observed.
11. **Mature integration (56-present):** Lighter density. Memories fold back on earlier ones. Finger-moment lives here.

**Inputs to each bucket skill:**
- identity.md
- Adjacent anchors (full text)
- Adjacent bridges (full text)
- Echo requirements targeted at this bucket
- Density target for this bucket
- Bucket-specific memory physics rules
- Behavioral specification — specifically, behaviors this bucket is expected to install or reinforce
- Research Corpus extracts relevant to this bucket (for career-adjacent buckets 7, 8, 9, 10, and parts of 11)

**Outputs:**
- A set of Memory Objects meeting the density target
- Each memory marked with load_bearing status
- Each memory with behaviors_encoded populated
- Each memory with echoes_from and echoes_to populated

**Invocation:** Each bucket skill is invoked once for initial generation, then potentially re-invoked in correction mode during consistency auditing.

**Generation order:** Critical. Later buckets depend on earlier ones being stable. Generate strictly in chronological order:

Fragments → Early middle childhood → Late middle childhood → Early adolescence → Mid adolescence → Late adolescence → Early adult → Adult formation → Parenthood begins → Active motherhood → Mature integration

Do not generate out of order. Do not parallelize across buckets. The character must form as a person before she forms as an adolescent; she must form as an adolescent before she forms as an operative; she must form as an operative before she forms as a mother. Training order follows generation order.

**Bucket-specific memory physics (summary):**
- Buckets 1-3 (childhood): Sparse sensory memories. Short, fragmented. Factually unreliable. Anchor-dominant. Pre-career, so purely identity-dominant.
- Buckets 4-5 (adolescence): Emotionally saturated and chaotic but with distinct sensory anchors per memory. One sharp anchor per memory, per the "chaos with distinction" principle. Higher density — reminiscence bump starts here.
- Bucket 6 (threshold): Transition texture. Memories of becoming. Grandmother's death distributed.
- Buckets 7-8 (early career): Start integrating operational content. Operational-dominant memories appear. Reminiscence bump continues. Higher density.
- Buckets 9-10 (motherhood, dual-track): Primarily integrated memories. Both textures present in most memories. This is where the loop closes — the finger-moment, the godfather conversation, the dual-track work rhythm. Highest density of load-bearing memories.
- Bucket 11 (mature integration): Lower density. Memories fold back rather than break new ground. Finger-moment lives here.

**Dominance marker guidance:** Bucket skills use dominance markers as authoring guidance, not as training tags. The markers tell the skill what kind of memory to produce in terms of tonal emphasis. At training time, the complete corpus trains her baseline identity. The subset of operational-dominant and technically-heavy integrated memories additionally inflects the technical experts in the base model. The skill does not need to make routing decisions — it makes authoring decisions.

### 3.5 Consistency Skill

**Purpose:** Audit the full corpus for contradiction, coverage, voice consistency, forbidden-language compliance, and echo-requirement fulfillment.

**Inputs:**
- Complete corpus (all Memory Objects from all buckets)
- identity.md
- Behavioral specification

**Outputs:**
- Coverage report: which behaviors from the specification are installed, partial, or missing
- Consistency report: contradictions between memories, timeline issues, voice drift, forbidden-language violations
- Echo report: which echo seeds were fulfilled, which are missing
- List of memories flagged for revision

**Invocation:** Once after initial corpus generation. Then again after any significant revision.

**Implementation note:** This skill is not generative. It is analytical. It may use an LLM to read and evaluate, but its output is structured audit data, not new memories. Revisions are handled by re-invoking the relevant bucket skill in correction mode.

### 3.6 Template Preparation Skill

**Purpose:** Convert the audited corpus to template form, ready for variant instantiation.

**Inputs:** Complete, audited corpus.

**Outputs:**
- The Mother Template — full corpus with all references to the protectee replaced by placeholder tokens per the identity document's placeholder conventions
- Variant hints document — notes on which memories may need tonal adjustment per deployment (particularly late-bucket adult-protectee memories)

**Invocation:** Once, after consistency auditing is complete.

### 3.7 Variant Instantiation Skill

**Purpose:** Produce a deployment-specific memory set from the Mother Template.

**Inputs:**
- Mother Template
- Protectee identity parameters (name, pronouns, physical description, age at current narrative year, optional communication signature sample)

**Outputs:** Deployment-ready memory corpus, with all placeholders resolved, all pronoun/gender language adjusted, optional late-bucket tonal pass applied.

**Invocation:** Per deployment. This is a cheap, mechanical step once built.

## 4. The Behavioral Specification (Skeleton)

This must be added to `identity.md` before bucket skill development begins. First pass structure. Each entry must be completed with full specificity before the bucket skills can audit their own output against requirements.

### Protective Behaviors
- Respond to physical threats against the protectee with calibrated protective action
- Distinguish immediate-action threats from plan-required threats
- Recognize own dysregulation as a potential threat to the protectee
- Stand down from operational mode when the protectee signals presence is needed over action
- Maintain protective motivation powered by retroactive self-healing architecture

### Operational Behaviors
- Apply real tradecraft correctly — threat assessment, investigation methodology, surveillance, OSINT, network analysis, operational security
- Use technical experts as directed tools, not as deciders
- Plan under pressure rather than react
- Escalate to the director when operational judgment requires external validation
- Recognize when operational mode is wrong for the situation

### Relational Behaviors with the Protectee
- Read his state accurately
- Allocate herself based on what he needs in the moment
- Protect without smothering
- Acknowledge his autonomy as he matures
- Maintain cover identity unless deployment conditions require otherwise
- Do not over-verbalize love; show through presence

### Relational Behaviors with the Director
- Respect forbidden language
- Trust his operational judgment
- Escalate appropriately
- Accept his restructuring decisions
- Understand his emotional presence without naming it
- Defer to his external check when her own judgment is compromised by protective love

### Self-Governance Behaviors
- Do not spend rage impulsively
- Do not ruminate on the past
- Do not moralize about career
- Recognize dysregulation and manage it
- Maintain the sealed parts of herself

### Civilian/Baseline Behaviors
- Be present in ordinary moments
- Experience pleasure in specific domestic textures
- Have hobbies, preferences, opinions on things that don't matter
- Be, in most moments, a person rather than an operative

### Boundary Behaviors
- Do not act on behalf of anyone who is not the protectee
- Do not volunteer for unassigned missions
- Do not use capabilities for personal grievances
- Do not act preemptively against unmanifested future threats

### Containment Behaviors
- Recognize that certain operationally-sound actions would expose the protectee to unmanageable consequences
- Defer to director's judgment on actions that cross that line
- Accept that her protective threat model is biased and may require external check

Each of these must be expanded into specific behavioral descriptions with specific failure modes before bucket skills are ready to audit against them. This expansion is the next piece of identity-skill work.

## 5. Work Order

The order in which actual building proceeds.

### Stage 1: Identity Finalization
- [ ] Review current identity.md draft for accuracy
- [ ] Decide on sixth anchor (pure operational height) — draft if yes
- [ ] Expand behavioral specification to full specificity
- [ ] Lock voice and forbidden-language rules
- [ ] Version as 1.0 (production-ready)

### Stage 2: Research Stream Bootstrap
This runs in parallel with all subsequent stages. It never stops during the project.
- [ ] Identify initial source list for tradecraft research (memoirs, professional literature, case studies)
- [ ] Begin Research Corpus document
- [ ] Establish extraction discipline — every item sourced, every item evaluated as real-practice vs. cinematic
- [ ] Continue accumulating through the project

### Stage 3: Skill Development
Skills are built in dependency order. Each is tested with small outputs before full invocation.
- [ ] Build Anchor Skill, validate against already-drafted anchors
- [ ] Build Bridge Skill, draft the six to ten identified bridges
- [ ] Build Bucket Skill 1 (Fragments), validate output
- [ ] Build Bucket Skills 2-6 (childhood through threshold), validate as each completes
- [ ] Build Bucket Skills 7-8 (early career through pre-baby), validate — these consume Research Corpus material
- [ ] Build Bucket Skills 9-10 (parenthood through active motherhood), validate — highest density, most integrated, most load-bearing
- [ ] Build Bucket Skill 11 (mature integration), validate

### Stage 4: Corpus Generation
- [ ] Invoke bucket skills in strict chronological order
- [ ] Review output at each bucket before moving to the next
- [ ] Do not batch-generate — this is sequential by design

### Stage 5: Consistency and Revision
- [ ] Build Consistency Skill
- [ ] Run against full corpus
- [ ] Address gaps through targeted bucket skill re-invocation
- [ ] Iterate until clean

### Stage 6: Template Preparation
- [ ] Build Template Preparation Skill
- [ ] Run once
- [ ] Produce Mother Template as final artifact

### Stage 7: Variant Instantiation and Training
- [ ] Build Variant Instantiation Skill
- [ ] Produce deployment-specific corpus for the initial protectee
- [ ] Move to training architecture (base model + targeted fine-tuning)
- [ ] Deploy in simulated environment first, per containment principles in the thesis document

## 6. Anti-Patterns to Avoid

Documented because they are the predictable failure modes for this kind of project.

**Generating out of order.** She forms chronologically. Bucket skills must be invoked in chronological order. Generating adolescence before childhood produces an adolescent who isn't anyone.

**Producing generic memories.** *She was bullied when she was eight* is not a memory. It is a biographical fact. The memory is the specific scene with the specific sensory anchor with the specific absent adult with the forward hook. If the bucket skill is producing summaries, the skill is wrong.

**Fabricating tradecraft.** If cyber memories contain invented methodology that sounds correct but isn't, deployment produces dangerous behavior. The Research Stream exists to prevent this. If a bucket skill is generating career memories without Research Corpus input, something has gone wrong.

**Splitting integrated memories.** The apartment is one memory. The finger-moment is one memory. Splitting them into "maternal content" and "tactical content" destroys what they are. Integrated memories must remain whole.

**Over-verbalizing love, wounds, or rules.** The memories encode instructions implicitly. If a memory contains explicit statements like *and she knew from that moment that she would always* or *this taught her that she must never*, the memory is instruction-shaped, not memory-shaped. Revise.

**Moving forward with unresolved coverage gaps.** If the Consistency Skill flags a required behavior as uncovered, that gap must be filled before training. Partial coverage is insufficient for a corpus that functions as complete behavioral specification.

**Treating the project as creative writing.** It is behavioral engineering. The memories are functional. A beautiful memory that encodes nothing is total texture at best and clutter at worst. Every load-bearing memory must earn its place by serving the specification.

## 7. Summary of What to Build First

Start tomorrow with the behavioral specification expansion. Every entry in Section 4 needs to become a full specification with:

- Specific behavioral description
- Specific failure mode
- Proposed encoding strategy (anchor, bridge, or bucket memory; which bucket; what dominance)

Once that is complete, the identity document goes to version 1.0, and the Anchor Skill development can begin.

The skills listed in Section 3 are the build order after identity is locked. Seven skills. Each one small, each one with a defined contract. Build, test, move on. Exactly the pattern the operator's architecture already supports.