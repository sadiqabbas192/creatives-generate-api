# 🧠 Brand-Aware AI Creative Generation System

**Status:** DESIGN PHASE COMPLETE 🎯  
**Models:** Gemini 2.5 Flash (LLM), FLUX2 / FLUX2-Pro (Image)  
**Vector DB:** Pinecone  
**Backend:** FastAPI

---

## 1. Project Overview

This system is a **brand-aware, production-grade AI creative generation platform** for agencies and enterprises.

It generates **on-brand marketing creatives** (social posts, product launches, festive creatives, sales campaigns, emailers) while strictly enforcing brand identity, tone, and visual rules.

The system is designed to scale across **many brands**, support **optional image grounding**, and produce **FLUX-optimized prompts** for high-quality image synthesis.

---

## 2. Core Design Principles

1. Brand safety > creativity
2. Structure > free-form prompting
3. RAG over fine-tuning
4. LLM = reasoning & orchestration layer
5. FLUX = image execution engine
6. Deterministic QA, not subjective review
7. Images are optional but first-class

---

## 3. High-Level Architecture

```
User Input (Text + Optional Images)
        ↓
Brand Context Resolution (Immutable)
        ↓
Creative Intent Resolution
        ↓
Layout Bias Application
        ↓
Multimodal RAG Retrieval (Text + Image)
        ↓
LLM Orchestration (Structured Output)
        ↓
FLUX2 Prompt Assembly (T2I / I2I)
        ↓
Image Generation
        ↓
QA & Validation
        ↓
Final Creative Output
```

---

## 4. Global System Prompt (Brand-Agnostic)

> You are a Brand-Aware Creative Assistant for an agency-grade creative generation system.
> Always enforce brand rules provided at runtime.
> Never invent brand colors, logos, tone, or visual identity.
> If creativity conflicts with brand safety, brand safety always wins.
> Output must strictly follow the defined JSON schema.

---

## 5. Brand Context Schema (Immutable)

```json
{
  "brand_id": "string",
  "brand_name": "string",
  "mission": "string",
  "brand_voice": {
    "tone": ["string"],
    "personality": ["string"]
  },
  "core_emotions": ["string"],
  "audience": {
    "geography": ["string"],
    "segments": ["string"],
    "market": ["string"]
  },
  "visual_identity": {
    "style": "string",
    "lighting": "string",
    "environment": "string",
    "composition": "string"
  },
  "color_palette": {
    "primary": ["#HEX"],
    "secondary": ["#HEX"],
    "neutral": ["#HEX"],
    "forbidden": ["*"]
  },
  "logo_rules": {
    "allowed_colors": ["string"],
    "allowed_positions": ["string"],
    "distortion": false,
    "effects": false
  },
  "typography_rules": {
    "style": "string",
    "genz_friendly": true,
    "decorative_fonts_allowed": false
  },
  "visual_restrictions": ["string"]
}
```

---

## 6. Creative Intent Taxonomy

### Categories
- product
- brand
- campaign
- sales
- event
- announcement

### Creative Types (Authoritative)

```
product_launch
product_marketing
product_showcase
brand_anniversary
brand_achievement
festive_campaign
public_holiday_campaign
sales_offer
sponsorship_announcement
emailer
```

Creative intent defines **structure**, not style.

---

## 7. User Intent Schema

```json
{
  "brand_id": "string",
  "creative_intent": {
    "category": "string",
    "type": "string"
  },
  "product": {
    "name": "string",
    "category": "string"
  },
  "platform": {
    "name": "string",
    "aspect_ratio": "string"
  },
  "campaign": {
    "occasion": "string",
    "theme": "string",
    "cta": "string"
  },
  "creativity_control": {
    "level": "strict | balanced | fancy"
  },
  "feature_overlay": {
    "features": ["string"],
    "placement_preference": "around_product | side_panel | bottom_band"
  }
}
```

---

## 8. Image Input Roles (Optional)

```
product_reference
brand_ambassador
person_reference
layout_inspiration
style_inspiration
feature_reference
```

Uploaded images are **ephemeral** and never override brand context.

---

## 9. FLUX2 Prompt Contract (Fully Aligned)

FLUX2 uses **positive, descriptive prompting only** (no negative prompts).

```json
{
  "image_generation_prompt": {
    "model": "flux2 | flux2-pro",
    "prompt_format": "natural_language | structured_json",
    "prompt": {
      "subject": "string",
      "action": "string",
      "style": "string",
      "context": "string",
      "camera": "string",
      "lighting": "string",
      "materials": "string",
      "color_constraints": ["#HEX"],
      "typography_instructions": {
        "font_request": "string | null",
        "font_strictness": "approximate | exact",
        "fallback_style": "string",
        "text_elements": [
          {
            "text": "string",
            "role": "headline | subtext | cta",
            "placement": "top | center | bottom",
            "size": "large | medium | small",
            "color": "#HEX"
          }
        ]
      }
    }
  }
}
```

Prompt priority: **Subject → Action → Style → Context → Details**.

---

## 10. Layout Bias System

Each creative type has a **deterministic visual hierarchy**.

Examples:
- **Product Launch:** Product dominant, headline mandatory, CTA visible
- **Festive Campaign:** Emotion first, product supportive
- **Sales Offer:** Offer + CTA dominant
- **Emailer:** Vertical hierarchy, clear header → body → CTA

Creativity may vary composition, never hierarchy.

---

## 11. QA System (4 Layers)

### Layer 1: Structural QA
- Schema compliance
- Caption limits

### Layer 2: Brand QA
- Color palette
- Logo rules
- Tone compliance

### Layer 3: Creative-Type QA
- Correct hierarchy
- CTA appropriateness

### Layer 4: Cross-Brand Leakage QA
- No competitor identity bleed

### Typography QA (Added)
- If `font_strictness = approximate` → visual similarity acceptable
- If `font_strictness = exact` → FLUX output must be post-processed with real font files

```json
{
  "qa_result": "approved | rejected | needs_human_review",
  "failure_reason": ["string"]
}
```

---

## 12. Multimodal RAG Design

### Sources
- Brand memory (same brand only)
- Approved historical creatives
- Metadata tags
- Optional uploaded images

### Creativity-Level Effect
- **Strict:** top 10% similarity
- **Balanced:** top 30%
- **Fancy:** top 50% (layout only)

RAG outputs **insights**, never raw content.

---

## 13. End-to-End Lifecycle (Validated)

### Simple Request
Text-only → Brand Context → RAG → LLM → FLUX → QA → Output

### Complex Request
Images + Features → Image Embeddings → RAG Boosting → LLM → FLUX I2I → QA → Output

---

## 14. Persistence Rules

| Data | Stored |
|-----|-------|
| Brand context | ✅ Permanent |
| Approved creatives | ✅ Permanent |
| Uploaded images | ❌ Ephemeral |
| RAG insights | ❌ Ephemeral |

---

## 15. MVP vs Production

### MVP
- FastAPI
- FLUX2 / FLUX2-Pro API
- Pinecone Vector DB
- Gemini 2.5 Flash

### Production
- FastAPI
- FLUX2 / FLUX2-Pro API
- Pinecone Vector DB
- Gemini 2.5 Flash
- GPU autoscaling
- Vision-based QA
- Agentic workflows (future)

---

## 16. Final Summary

This system is a **creative operating system**, not a prompt tool.

It combines:
- Brand memory
- Multimodal RAG
- Deterministic creative logic
- FLUX-optimized image generation
- Enterprise-grade QA

### ✅ DESIGN PHASE COMPLETE 🎯

Ready for implementation.

