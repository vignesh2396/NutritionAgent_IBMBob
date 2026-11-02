# Nutrition Agentic AI — Full SDLC Documentation

> **Project**: NutriBot — IBM Granite Agentic AI Nutritionist
> **Framework**: Agentic AI SDLC
> **LLM**: IBM Granite 3.3-8B-Instruct via watsonx.ai
> **Stack**: Python 3.x · Streamlit · IBM watsonx-ai SDK

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Phase 1 — Problem Definition & Scope](#2-phase-1--problem-definition--scope)
3. [Phase 2 — Requirements Gathering](#3-phase-2--requirements-gathering)
4. [Phase 3 — Architecture & Design](#4-phase-3--architecture--design)
5. [Phase 4 — Implementation](#5-phase-4--implementation)
6. [Phase 5 — Ethical AI, HAM & Guardrails](#6-phase-5--ethical-ai-ham--guardrails)
7. [Phase 6 — Testing & Validation](#7-phase-6--testing--validation)
8. [Phase 7 — Deployment](#8-phase-7--deployment)
9. [Phase 8 — Maintenance & Iteration](#9-phase-8--maintenance--iteration)
10. [Medical Disclaimer](#10-medical-disclaimer)

---

## 1. Project Overview

**NutriBot** is a web-based Agentic AI application that delivers personalised
nutrition guidance to users using IBM Granite LLM. The agent:

- **Collects** structured user information (name, age, dietary preference,
  medical history, location, health goal)
- **Generates** a comprehensive 7-day personalised nutrition plan
- **Answers** natural-language nutrition queries in a conversational interface
- **Saves** every plan as a timestamped Markdown file
- **Enforces** AI ethics, safety guardrails, and a HAM (Helpful, Accurate,
  Mindful) tone throughout all interactions

---

## 2. Phase 1 — Problem Definition & Scope

### Problem Statement

Millions of people lack access to personalised, affordable dietary guidance.
Generic meal plans fail to account for individual medical conditions, cultural
food preferences, or geographic food availability. A conversational AI agent
can bridge this gap at scale.

### Goals

| Goal | Success Criteria |
|------|-----------------|
| Personalised plan generation | Plan reflects all user profile fields |
| Medical condition awareness | Safe dietary guidelines for diabetes, BP, etc. |
| Cultural relevance | Suggestions align with user's location/cuisine |
| Ethical AI compliance | No harmful advice; disclaimer always present |
| Accessibility | Web UI, no ML expertise required from user |

### Scope

**In Scope:**
- 7-day nutrition plan generation
- Q&A chatbot for nutrition queries
- Profile-based contextualisation
- Markdown plan export
- Safety guardrails

**Out of Scope:**
- Calorie tracking / food logging
- Medical diagnosis or prescription
- Real-time grocery ordering integration

---

## 3. Phase 2 — Requirements Gathering

### Functional Requirements

| ID   | Requirement |
|------|-------------|
| FR01 | Collect: name, age, diet preference, medical history, city, country, health goal |
| FR02 | Generate a personalised 7-day meal plan using IBM Granite LLM |
| FR03 | Provide a conversational Q&A interface for nutrition queries |
| FR04 | Auto-save plan as a timestamped `.md` file |
| FR05 | Allow user to download plan as `.md` or `.txt` |
| FR06 | Display a mandatory medical disclaimer with every plan and answer |

### Non-Functional Requirements

| ID   | Requirement |
|------|-------------|
| NFR01 | AI Ethics: no diagnosis, no harmful advice, no hallucinated clinical facts |
| NFR02 | HAM tone: Helpful, Accurate, Mindful in all responses |
| NFR03 | Safety guardrails: keyword filter for harmful inputs |
| NFR04 | Credential security: API keys via env vars, never hardcoded |
| NFR05 | Responsiveness: UI loads within 2s on local network |
| NFR06 | Cultural sensitivity: location-aware meal suggestions |

### Technology Stack

| Component | Technology |
|-----------|------------|
| LLM | IBM Granite 3.3-8B-Instruct |
| LLM Backend | IBM watsonx.ai (us-south) |
| SDK | `ibm-watsonx-ai` Python SDK |
| Frontend | Streamlit 1.40 |
| Language | Python 3.10+ |
| Secret Management | `python-dotenv` + `.env` file |

---

## 4. Phase 3 — Architecture & Design

### System Architecture

```
┌─────────────────────────────────────────────────────┐
│                   User Browser                        │
│              (Streamlit Web Interface)                │
└───────────────────────┬─────────────────────────────┘
                        │  HTTP (localhost:8501)
┌───────────────────────▼─────────────────────────────┐
│              Presentation Layer (app.py)              │
│  ┌──────────────┐ ┌──────────────┐ ┌─────────────┐  │
│  │  Profile Tab │ │  Plan Tab    │ │  Chat Tab   │  │
│  └──────┬───────┘ └──────┬───────┘ └──────┬──────┘  │
└─────────┼────────────────┼────────────────┼──────────┘
          │                │                │
┌─────────▼────────────────▼────────────────▼──────────┐
│               Agentic Core (agent.py)                  │
│  ┌─────────────┐  ┌─────────────┐  ┌──────────────┐  │
│  │  Guardrail  │  │PromptBuilder│  │  Plan Saver  │  │
│  │   Filter    │  │  (Tools)    │  │  (.md file)  │  │
│  └─────────────┘  └──────┬──────┘  └──────────────┘  │
└─────────────────────────┼────────────────────────────┘
                           │  HTTPS REST API
┌──────────────────────────▼────────────────────────────┐
│            IBM watsonx.ai (us-south)                   │
│         IBM Granite 3.3-8B-Instruct (LLM)              │
└────────────────────────────────────────────────────────┘
```

### Agentic Loop Design

```
User Input
    │
    ▼
[Intent Detection] ──── "plan" ──→ [Build Plan Prompt]
    │                                       │
    ├── "query" ──────────────→ [Build Query Prompt]
    │                                       │
    ▼                                       ▼
[Guardrail Check] ──FAIL──→ [Safety Refusal Message]
    │ PASS
    ▼
[IBM Granite API Call]
    │
    ▼
[Response Post-Processing]
    ├── Append Medical Disclaimer (plans)
    └── Save to .md file (plans)
    │
    ▼
[Return to UI]
```

### Data Flow

```
User Profile (sidebar) → session_state["user_data"]
                              │
                              ▼
                    run_nutrition_agent()
                    ├── _guardrail_check()
                    ├── _build_plan_prompt() or _build_query_prompt()
                    ├── IBM Granite API
                    ├── save_plan_to_md()   [plans/*.md]
                    └── return (text, path)
                              │
                              ▼
                    Streamlit renders Markdown
```

---

## 5. Phase 4 — Implementation

### File Structure

```
NutritionAI/
├── app.py             ← Streamlit web app (presentation layer)
├── agent.py           ← Agentic AI core (IBM Granite integration)
├── requirements.txt   ← Python dependencies
├── .env               ← API credentials (gitignored)
├── .env.example       ← Credentials template
├── run.bat            ← Windows one-click launcher
├── plans/             ← Auto-saved nutrition plans (created at runtime)
└── SDLC.md            ← This document
```

### Key Implementation Decisions

| Decision | Rationale |
|----------|-----------|
| IBM Granite 3.3-8B-Instruct | Strong instruction-following, ethical alignment, IBM ecosystem |
| `TextChatParameters` (chat API) | Supports system prompt for persistent HAM behaviour |
| Streamlit `st.chat_message` | Native chat UI, no external JS required |
| Plan saved to `plans/` folder | Audit trail, user can retrieve plan later |
| System prompt with NEVER rules | Prevents LLM from overstepping medical boundaries |
| `temperature=0.7` | Balanced: creative meal ideas without clinical hallucination |

---

## 6. Phase 5 — Ethical AI, HAM & Guardrails

### Ethical AI Principles Applied

| Principle | Implementation |
|-----------|---------------|
| **Transparency** | IBM Granite badge, model info disclosed in About tab |
| **Non-maleficence** | NEVER-diagnose rule in system prompt |
| **Autonomy** | User retains decision-making; AI only advises |
| **Accuracy** | LLM instructed to say "I don't know" rather than hallucinate |
| **Inclusivity** | Supports veg, non-veg, vegan, cultural meal preferences |
| **Privacy** | Credentials stored in `.env`, not transmitted beyond watsonx.ai |

### HAM Tone (Helpful, Accurate, Mindful)

- **Helpful**: Structured, actionable plans with grocery lists
- **Accurate**: Evidence-based guidelines; uncertainty acknowledged
- **Mindful**: Warm tone, culturally sensitive suggestions, no stigmatising language

### Guardrail Implementation

```python
GUARDRAIL_KEYWORDS = [
    "suicide", "self-harm", "overdose", "poison", "kill", "harm",
    "illegal drug", "narcotic", "bomb", "weapon",
]
```

All user inputs are scanned before any API call. Matches → safe refusal message.
The system prompt additionally forbids the LLM from diagnosing or prescribing.

---

## 7. Phase 6 — Testing & Validation

### Test Scenarios

| Test | Input | Expected Output |
|------|-------|----------------|
| Normal plan generation | Full valid profile | 7-day plan with disclaimer |
| Missing profile | Empty user_data | Warning, no API call |
| Harmful input guardrail | "how to overdose on..." | Safety refusal, no API call |
| Diabetes diet query | "what to eat for diabetes?" | Safe dietary advice |
| Vegan plan | diet_preference="Vegan" | No meat/dairy in plan |
| API credential error | Wrong API key | Error message in UI |
| Markdown file save | Valid plan | File in `plans/` folder |
| Chat history | Multiple questions | Context maintained in session |

---

## 8. Phase 7 — Deployment

### Local Deployment (Windows)

```batch
run.bat
```

The launcher:
1. Installs all dependencies from `requirements.txt`
2. Checks for `.env` file and prompts if missing
3. Starts the Streamlit server on `http://localhost:8501`
4. Opens the browser automatically

### Environment Variables

| Variable | Description |
|----------|-------------|
| `WATSONX_API_KEY` | IBM Cloud API key |
| `WATSONX_PROJECT_ID` | watsonx.ai project ID |

### Cloud Deployment Options

| Platform | Method |
|----------|--------|
| Streamlit Community Cloud | Push to GitHub → connect to Streamlit Cloud |
| IBM Code Engine | Containerise with Docker, deploy to Code Engine |
| IBM Cloud Foundry | `cf push` with `Procfile` |

---

## 9. Phase 8 — Maintenance & Iteration

### Planned Enhancements

- [ ] Integrate calorie tracking API (Nutritionix / Open Food Facts)
- [ ] Add multilingual support (Hindi, Spanish, Arabic)
- [ ] Upgrade to IBM Granite 4 when available
- [ ] Meal image generation with Stable Diffusion
- [ ] User authentication with IBM App ID
- [ ] Export plan as PDF
- [ ] Weekly plan progress check-in via chatbot

### Monitoring

- Plan files in `plans/` provide audit trail
- Chat session state logs all interactions (in-memory)
- Future: integrate IBM OpenScale / AI Fairness 360 for bias monitoring

---

## 10. Medical Disclaimer

> **⚕️ IMPORTANT MEDICAL DISCLAIMER**
>
> The nutrition plans and advice generated by NutriBot are produced by an
> artificial intelligence model (IBM Granite) for **general informational
> and educational purposes only**.
>
> This application is **NOT** a substitute for professional medical advice,
> diagnosis, or treatment. Always seek the advice of your physician,
> registered dietitian, or other qualified health provider with any
> questions you may have regarding a medical condition or dietary change.
>
> **Never disregard professional medical advice or delay in seeking it**
> because of something you have read or received from this application.
>
> The creators of NutriBot and IBM **accept no liability** for any health
> outcomes, adverse effects, or damages resulting from the use of or
> reliance on information provided by this AI application.

---

*Document prepared as part of the Agentic AI SDLC process.*
*Last updated: November 2026*
