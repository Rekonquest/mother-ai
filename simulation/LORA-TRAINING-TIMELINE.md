# Mother AI - LoRA Training Timeline

## Compute Time: 10-15 Minutes on Free T4

The dataset is ~80-120K tokens at 800-1,200 memories. Still small in LoRA terms. LoRA rank 24 on a 7B-14B base model processes this in minutes.

| Platform | GPU | 7B Model | 14B Model | Cost |
|---|---|---|---|---|
| Google Colab Free | T4 16GB | ~10 min | ~15 min | Free |
| Google Colab Pro | L4 24GB | ~7 min | ~10 min | $10/mo |
| Kaggle Free | T4 16GB | ~10 min | ~15 min | Free (30h/week) |

**Any of these works.** The dataset fits comfortably on a free T4.

The bottleneck is NOT compute. It's writing 800-1,200 high-quality cross-domain memories.

The dataset is ~80-120K tokens at 800-1,200 memories. Still small in LoRA terms. LoRA rank 24 on a 7B-14B base model processes this in minutes.

| Platform | GPU | 7B Model | 14B Model | Cost |
|---|---|---|---|---|
| Google Colab Free | T4 16GB | ~15 min | ~20 min | Free |
| Google Colab Pro | L4 24GB | ~10 min | ~15 min | $10/mo |
| Google Colab Pro | A100 40GB | ~5 min | ~8 min | $10/mo + compute units |
| Kaggle Free | T4 16GB | ~15 min | ~20 min | Free (30h/week) |

**Any of these works.** Even at 1,200 memories, the dataset fits comfortably on a free T4.

The bottleneck is NOT compute. It's writing 800-1,200 high-quality thin-connected memories.

## The Real Timeline: Data Preparation

Training is fast. Getting the data ready is the real work. With 800-1,200 memories, this is a real project.

### Step 1: Write Childhood Memories (Buckets 1-6) — 2-3 weeks

Need ~430 hand-crafted memories (have 65, need 365 more). These are the ORIGINS. Every cross-domain bridge starts here. No shortcuts.

Strategy: write in clusters. Each cluster is a scene (Saturday morning, the cookie jar, the stepfather's car) that encodes 3-4 behaviors from different domains. One well-written scene can install "kitchen = room-reading = patience = civilian default" in a single memory.

~5-10 memories/day. Some days more, some less. The childhood memories are the foundation.

### Step 2: Select + Edit Career Memories (Buckets 7-8) — 1 week

From 1,200 generated career memories, select 320 that:
- Cover ALL 105 domain pairs
- Span both buckets (not all in bucket 8)
- Sound like Mother, not templates
- Include cross-domain bridges explicitly

Most need voice editing. Rule: if you can spot the template, it needs rewriting.

### Step 3: Write Parenthood/Motherhood Memories (Buckets 9-11) — 2-3 weeks

Need ~450 memories. Key scenes (hospital, apartment, godfather conversation, finger-moment) are hand-crafted. The rest can be guided generation + voice review.

This is the highest cross-domain density. Career skills in civilian context. Protective instinct meeting professional judgment. The child in every room.

### Step 4: Gap Fill + Echo Wiring — 1 week

Run consistency audit. Find uncovered domain pairs (33 currently). Find broken echo chains. Write memories specifically to close gaps.

### Step 5: Voice Consistency Pass — 1-2 weeks

Every generated memory reviewed. If template shows through, rewrite. If voice drifts, rewrite. If cross-domain connection is stated instead of lived, rewrite to show not tell.

### Step 6: Format + Train + Validate — 2-3 days

Format data for training. Set up Colab notebook. Train both phases. Run validation prompts.

### Total Timeline

| Phase | Time | Notes |
|---|---|---|
| Childhood memories | 2-3 weeks | Foundation. No shortcuts. |
| Career selection | 1 week | Selection + voice editing |
| Parenthood/motherhood | 2-3 weeks | Highest cross-domain density |
| Gap fill + echoes | 1 week | Audit-driven |
| Voice consistency | 1-2 weeks | Every memory reviewed |
| Format + train | 2-3 days | Mechanical |
| **Total** | **8-13 weeks** | Most time is writing, not computing |

The thin behaviors need dedicated hand-crafted memories:

| Behavior | Current | Needs | What to Write |
|---|---|---|---|
| P-004 (stand down when presence > action) | 1 | 3-4 | Moments she wants to act but the child needs her presence |
| B-002 (don't volunteer for missions) | 1 | 3-4 | The director offers, she does not ask |
| B-003 (don't use skills for grievances) | 2 | 4-5 | The stepfather anger channeled into restraint |
| R-002 (allocate herself appropriately) | 2 | 4-5 | Not always present, not always absent |
| R-003 (don't over-verbalize love) | 2 | 4-5 | The grandmother showed it, never said it |
| X-002 (weakest point, cross-domain) | 2 | 5-8 | Finding weak points across different life stages |

These must be hand-crafted in Mother's voice. No templates. Each takes 10-15 minutes to write. Total: 3-5 hours of writing.

### Step 2: Voice Review 185 Generated Memories (1-2 days)

From 1,800 career memories, select 185 that:
- Sound like Mother, not like a template
- Encode behaviors from multiple categories (cross-domain)
- Span the right bucket distribution (not all in bucket 8)

Selection criteria:
- If you can spot the template pattern behind the text, reject or rewrite
- If the sensory anchor is generic ("the room was quiet"), reject
- If the emotional signature is instruction-shaped ("she knew she must never"), reject
- Prefer memories with 2+ behaviors encoded and cross-domain bridges

Estimated: 30-60 minutes for initial selection, then 1-2 hours for rewrites.

### Step 3: Format Training Data (2-3 hours)

Convert 336 memories to training format. Options:

**Format A: Raw prose (simplest, recommended for Phase 1)**
```
[Memory body text as-is]
```
The model learns voice and identity from the prose itself.

**Format B: Labeled (better for Phase 2)**
```
Below is a memory from the life of a person.

[Memory body text]
```

**Format C: Conversation pairs (for chat models)**
```
User: Tell me about a memory from when you were ten.
Assistant: [Memory body text]
```

For a BASE model (not instruction-tuned), Format A is correct. The model learns to complete text in Mother's voice. No special formatting needed.

### Step 4: Set Up Colab Notebook (1-2 hours)

Install Unsloth, load base model, configure LoRA, load data, train. This is a one-time setup. Template notebook available from Unsloth.

### Step 5: Train Phase 1 (~3-6 min on T4)

76 memories, buckets 1-6. This teaches the model WHO she is.

After Phase 1: test with validation prompts. Does the model produce kitchen-adjacent prose? Does it assess threats? Is the civilian default present?

### Step 6: Train Phase 2 (~2-4 min on T4)

260 memories, buckets 7-11. This teaches WHAT she does, built on the identity foundation.

After Phase 2: test cross-domain transfer. Does the model describe networks like rooms? Does it default to civilian but transition when cued?

### Step 7: Validation (2-4 hours)

Run validation prompts, compare against:
- The base model without LoRA (control)
- An instruction model with the same behaviors as rules
- Your own judgment of whether "she sounds like her"

## Total Timeline

| Step | Time | Notes |
|---|---|---|
| Childhood memories (365 new) | 2-3 weeks | Foundation. No shortcuts. |
| Career selection + editing | 3-5 days | From 1,200 generated, select ~150 cross-domain |
| Parenthood/motherhood | 1-2 weeks | Mix of hand-crafted and guided generation |
| Gap fill + cross-domain wiring | 1 week | Close the 33 missing connections |
| Voice consistency pass | 1 week | Every generated memory |
| Format + train + validate | 2-3 days | Mechanical |
| **Total** | **6-10 weeks** | Most time is writing, not computing |

## The Notebook Structure (Updated for Rank 32)

```python
# Cell 1: Install
!pip install unsloth

# Cell 2: Load model
from unsloth import FastLanguageModel
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/qwen3-14b",  # or llama-3.1-8b
    max_seq_length=1024,
    dtype=None,  # auto
    load_in_4bit=True,  # fits T4
)

# Cell 3: Configure LoRA
model = FastLanguageModel.get_peft_model(
    model,
    r=24,  # rank 24 for thin-connected architecture
    lora_alpha=48,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                     "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
)

# Cell 4: Load data
from datasets import Dataset
data = Dataset.from_json("mother_memories_phase1.jsonl")

# Cell 5: Train
from trl import SFTTrainer
from transformers import TrainingArguments
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=data,
    args=TrainingArguments(
        per_device_train_batch_size=2,
        gradient_accumulation_steps=1,
        warmup_steps=10,
        num_train_epochs=5,
        learning_rate=2e-4,
        fp16=not torch.cuda.is_bf16_supported(),
        bf16=torch.cuda.is_bf16_supported(),
        logging_steps=10,
        optim="adamw_8bit",
        output_dir="outputs",
    ),
)
trainer.train()

# Cell 6: Save
model.save_pretrained("mother_phase1_lora")
tokenizer.save_pretrained("mother_phase1_lora")

# Cell 7: Test
messages = [{"role": "user", "content": "Describe a Saturday morning when you were ten."}]
inputs = tokenizer.apply_chat_template(messages, tokenize=True, add_generation_prompt=True, return_tensors="pt").to("cuda")
outputs = model.generate(inputs, max_new_tokens=256, temperature=0.7)
print(tokenizer.decode(outputs[0]))
```

## Key Decision: Which Base Model?

| Model | Params | VRAM Needed (4-bit) | Prose Quality | Reasoning | LoRA Compatibility |
|---|---|---|---|---|---|
| Qwen3 14B | 14B | ~10GB | Excellent | Strong | Great (Unsloth supported) |
| Llama 3.1 8B | 8B | ~6GB | Very good | Good | Great (most tested) |
| Mistral 7B v0.3 | 7B | ~5GB | Good | Good | Great |
| Qwen3 8B | 8B | ~6GB | Good | Strong | Great |

**Recommendation: Qwen3 14B base** if your GPU can handle it (L4 or A100 on Colab Pro). The 14B model has enough capacity to form a distinct identity without losing coherence. 7B models sometimes struggle with consistent first-person narrative voice.

If stuck on T4 Free Tier: **Llama 3.1 8B base**. Well-tested, fits in 16GB with 4-bit quantization, good English prose.

## Cost Summary

| Option | Total Cost |
|---|---|
| Colab Free + T4 + 7B model | $0 |
| Colab Free + T4 + 14B model | $0 |
| Colab Pro + L4 + 14B model | $10/month |
| Kaggle Free + T4 + 14B model | $0 |

The entire training run costs nothing or nearly nothing. The value is in the data, not the compute.