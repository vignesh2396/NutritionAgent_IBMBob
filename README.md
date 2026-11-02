# 🥗 NutriBot — Agentic AI Nutritionist

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/Streamlit-1.35%2B-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" />
  <img src="https://img.shields.io/badge/Google%20Gemini-2.0%20Flash-4285F4?style=for-the-badge&logo=google&logoColor=white" />
  <img src="https://img.shields.io/badge/IBM%20Bob-Agentic%20AI-052FAD?style=for-the-badge&logo=ibm&logoColor=white" />
</p>

> **A personalised nutrition planning AI agent** built with Google Gemini (gemini-2.0-flash), IBM Granite-style guardrails, and Streamlit — developed as part of the **IBM SkillsBuild 2026 — Gartner Program**.

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Tech Stack](#-tech-stack)
- [Quick Start](#-quick-start)
- [Configuration](#-configuration)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [Safety & Guardrails](#-safety--guardrails)
- [SDLC Phases](#-sdlc-phases)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🧠 **Agentic AI Core** | Intent detection (plan vs query), tool-like sub-routines, retry logic |
| 📅 **7-Day Meal Plans** | Personalised plans with macros, meals, grocery lists, and lifestyle tips |
| 💬 **AI Chat** | Free-form Q&A nutrition assistant with user profile context |
| 🛡️ **Safety Guardrails** | IBM Granite-style HAM (Helpful, Accurate, Mindful) tone + content filters |
| 📥 **Export Plans** | Download generated plans as Markdown or plain text |
| 🎨 **Themed UI** | Custom Streamlit green-health theme, responsive tabs layout |
| 💾 **Auto-Save** | Plans saved locally to `plans/` as timestamped Markdown files |
| ⚕️ **Medical Disclaimer** | Automatically injected on every generated plan |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              Streamlit Frontend (app.py)         │
│  ┌──────────┐ ┌──────────┐ ┌────────┐ ┌──────┐  │
│  │ Profile  │ │  Plan    │ │  Chat  │ │About │  │
│  │  Tab     │ │  Tab     │ │  Tab   │ │ Tab  │  │
│  └──────────┘ └──────────┘ └────────┘ └──────┘  │
└─────────────────────┬───────────────────────────┘
                      │ run_nutrition_agent()
┌─────────────────────▼───────────────────────────┐
│           Agentic Core (agent.py)                │
│  ┌─────────────┐  ┌──────────────┐               │
│  │  Guardrail  │  │ Intent Det.  │               │
│  │   Check     │  │ plan/query   │               │
│  └─────────────┘  └──────┬───────┘               │
│                          │                       │
│  ┌───────────────────────▼───────────────────┐   │
│  │        Prompt Builders (Tool Sub-routines) │   │
│  │  build_plan_prompt()  build_query_prompt() │   │
│  └───────────────────────┬───────────────────┘   │
│                          │                       │
│  ┌───────────────────────▼───────────────────┐   │
│  │     Google Gemini API (gemini-2.0-flash)   │   │
│  │       with HAM System Prompt               │   │
│  └───────────────────────┬───────────────────┘   │
│                          │                       │
│  ┌───────────────────────▼───────────────────┐   │
│  │     save_plan_to_md()  →  plans/*.md       │   │
│  └───────────────────────────────────────────┘   │
└─────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | [Streamlit](https://streamlit.io/) ≥ 1.35 |
| **AI Model** | [Google Gemini](https://ai.google.dev/) (gemini-2.0-flash) |
| **Agentic Framework** | Custom agentic loop with IBM Granite-style prompting |
| **Environment** | python-dotenv |
| **HTTP** | requests |
| **Language** | Python 3.10+ |

---

## 🚀 Quick Start

### Prerequisites

- Python **3.10+** installed ([download](https://www.python.org/downloads/))
- A free **Google Gemini API key** ([get one here](https://aistudio.google.com/app/apikey))
- Git ([download](https://git-scm.com/))

### 1. Clone the Repository

```bash
git clone https://github.com/vignesh2396/NutritionAgent_IBMBob.git
cd NutritionAgent_IBMBob
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Your API Key

```bash
# Copy the example env file
cp .env.example .env
```

Edit `.env` and add your Gemini API key:

```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
```

### 4. Run the App

```bash
streamlit run app.py
```

The app will open at **http://localhost:8501** 🎉

> **Windows users:** Double-click `run.bat` to auto-install dependencies and launch the app.

---

## ⚙️ Configuration

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `GEMINI_API_KEY` | ✅ Yes | Your Google Gemini API key |

> **Note:** You can also enter your API key directly in the app sidebar — no `.env` file required for quick testing.

### Streamlit Theme

The app uses a custom green-health theme configured in [`.streamlit/config.toml`](.streamlit/config.toml):

```toml
[theme]
base                     = "light"
primaryColor             = "#40916c"
backgroundColor          = "#eaf4ec"
secondaryBackgroundColor = "#ffffff"
textColor                = "#1a2e1a"
font                     = "sans serif"
```

---

## 📁 Project Structure

```
NutritionAgent_IBMBob/
│
├── app.py                  # Streamlit frontend — UI tabs & session state
├── agent.py                # Agentic AI core — Gemini integration & prompts
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows one-click launcher
├── .env.example            # Environment variable template (safe to commit)
├── .env                    # Your actual credentials (⚠️ NEVER commit this)
├── SDLC.md                 # Software Development Lifecycle documentation
│
├── .streamlit/
│   └── config.toml         # Streamlit theme configuration
│
└── plans/                  # Auto-generated nutrition plans (Markdown)
    └── nutrition_plan_<name>_<timestamp>.md
```

---

## 📖 Usage Guide

### 1. Fill In Your Profile (Profile Tab)
Enter your name, age, city, country, dietary preference (vegetarian / non-veg), health goal, and any medical conditions.

### 2. Generate Your Nutrition Plan (Plan Tab)
Click **🚀 Generate My Nutrition Plan** to get a personalised 7-day meal plan with:
- Daily macro targets (calories, protein, carbs, fats)
- 7-day meal planner (breakfast, lunch, dinner, snacks)
- Foods to include & avoid
- Hydration & lifestyle tips
- Sample grocery list

### 3. Download Your Plan
Export the plan as **Markdown** or **plain text** using the download buttons.

### 4. Ask the AI Nutritionist (Chat Tab)
Ask free-form questions like:
- *"What are the best high-protein vegetarian foods?"*
- *"How much water should I drink with hypertension?"*
- *"Can someone with diabetes eat mangoes?"*

---

## 🛡️ Safety & Guardrails

NutriBot implements **IBM Granite-style HAM** (Helpful, Accurate, Mindful) principles:

- **Content Guardrails**: Blocks harmful, off-topic, or dangerous queries using keyword screening
- **Medical Disclaimer**: Automatically appended to every generated plan
- **Uncertainty Acknowledgment**: The AI never fabricates clinical facts; it recommends consulting a professional when uncertain
- **No Diagnosis or Prescription**: The system prompt explicitly prohibits medical diagnosis or medication advice

---

## 📐 SDLC Phases

This project follows a structured SDLC documented in [`SDLC.md`](SDLC.md):

| Phase | Description |
|---|---|
| 1. Requirements | User stories, functional & non-functional requirements |
| 2. Design | Architecture, data flow, UI wireframes |
| 3. Implementation | Agentic core, Streamlit frontend, Gemini integration |
| 4. Testing | Unit tests, integration tests, guardrail validation |
| 5. Deployment | GitHub deployment, environment setup |
| 6. Maintenance | Bug fixes, model upgrades, feature iterations |

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/your-feature-name`
3. Commit your changes: `git commit -m "feat: add your feature"`
4. Push to the branch: `git push origin feature/your-feature-name`
5. Open a Pull Request

---

## 📄 License

This project is developed for educational purposes as part of the **IBM SkillsBuild 2026 — Gartner Program**.

---

<p align="center">
  Built with ❤️ using <strong>IBM Bob</strong> · <strong>Google Gemini</strong> · <strong>Streamlit</strong>
</p>
