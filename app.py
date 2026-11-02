# ============================================================
# Nutrition Agentic AI — Powered by Google Gemini
# Streamlit Web Application  (app.py)
# SDLC Phase: Implementation — Presentation Layer
#
# Credentials: GEMINI_API_KEY loaded from .env
# ============================================================

import os
import textwrap
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Load .env from the same directory as this file
load_dotenv(dotenv_path=Path(__file__).parent / ".env")

# ── Page Config ──────────────────────────────────────────────
st.set_page_config(
    page_title="NutriBot — Agentic AI Nutritionist",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Inject Custom CSS ────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ═══════════════════════════════════════════════════════
       FORCED LIGHT THEME — explicit colours on every element
       Works regardless of system/dark/light Streamlit setting
    ═══════════════════════════════════════════════════════ */

    /* ── Page & app shell ── */
    html, body, [data-testid="stApp"], .stApp {
        background: linear-gradient(150deg, #d8f3dc 0%, #eaf4ec 45%, #d0eae8 100%) !important;
        color: #1a2e1a !important;
    }

    /* ── Main content block ── */
    [data-testid="stMain"],
    section[data-testid="stMain"] > div {
        background: transparent !important;
    }
    .main .block-container {
        background: #ffffff !important;
        border-radius: 18px !important;
        padding: 2rem 2.5rem !important;
        box-shadow: 0 4px 28px rgba(27, 67, 50, 0.12) !important;
        color: #1a2e1a !important;
    }

    /* ── All text inside main area ── */
    .main .block-container p,
    .main .block-container li,
    .main .block-container span,
    .main .block-container label,
    .main .block-container div,
    .main .block-container h1,
    .main .block-container h2,
    .main .block-container h3,
    .main .block-container h4,
    .main .block-container td,
    .main .block-container th {
        color: #1a2e1a !important;
    }

    /* ── Markdown output (plan text) ── */
    .stMarkdown, .stMarkdown p, .stMarkdown li,
    .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
    .stMarkdown td, .stMarkdown th, .stMarkdown code {
        color: #1a2e1a !important;
    }
    .stMarkdown th { background: #d8f3dc !important; }
    .stMarkdown tr:nth-child(even) td { background: #f3faf4 !important; }
    .stMarkdown code {
        background: #e8f5e9 !important;
        padding: 2px 5px; border-radius: 4px;
    }

    /* ── Input fields in MAIN area ── */
    .main .block-container input,
    .main .block-container textarea,
    .main .block-container select,
    [data-testid="stTextInput"] input,
    [data-testid="stNumberInput"] input,
    [data-testid="stTextArea"] textarea {
        background: #f8fdf9 !important;
        color: #1a2e1a !important;
        border: 1px solid #95d5b2 !important;
        border-radius: 8px !important;
    }
    [data-testid="stTextInput"] label,
    [data-testid="stNumberInput"] label,
    [data-testid="stSelectbox"] label,
    [data-testid="stTextArea"] label,
    [data-testid="stMultiSelect"] label {
        color: #1a2e1a !important;
        font-weight: 600 !important;
    }

    /* ── Chat messages ── */
    [data-testid="stChatMessage"] {
        background: #f0faf2 !important;
        border-radius: 12px !important;
        color: #1a2e1a !important;
    }
    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] span,
    [data-testid="stChatMessage"] div {
        color: #1a2e1a !important;
    }
    [data-testid="stChatInput"] textarea {
        background: #ffffff !important;
        color: #1a2e1a !important;
        border: 1px solid #95d5b2 !important;
    }

    /* ── st.form container ── */
    [data-testid="stForm"] {
        background: #f8fdf9 !important;
        border: 1px solid #b7e4c7 !important;
        border-radius: 14px !important;
        padding: 1.2rem 1.5rem !important;
    }
    [data-testid="stForm"] label,
    [data-testid="stForm"] p,
    [data-testid="stForm"] span,
    [data-testid="stForm"] div {
        color: #1a2e1a !important;
    }
    [data-testid="stForm"] input,
    [data-testid="stForm"] textarea {
        background: #ffffff !important;
        color: #1a2e1a !important;
        border: 1px solid #95d5b2 !important;
        border-radius: 8px !important;
    }
    /* selectbox & multiselect inside form */
    [data-testid="stForm"] [data-baseweb="select"] > div {
        background: #ffffff !important;
        border: 1px solid #95d5b2 !important;
        border-radius: 8px !important;
    }
    [data-testid="stForm"] [data-baseweb="select"] span,
    [data-testid="stForm"] [data-baseweb="select"] div {
        color: #1a2e1a !important;
    }
    /* multiselect tags */
    [data-testid="stForm"] [data-baseweb="tag"] {
        background: #d8f3dc !important;
        color: #1b4332 !important;
    }

    /* ── Expanders (SDLC phases) ── */
    [data-testid="stExpander"] {
        background: #f3faf4 !important;
        border: 1px solid #b7e4c7 !important;
        border-radius: 10px !important;
    }
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] p,
    [data-testid="stExpander"] span {
        color: #1a2e1a !important;
    }

    /* ── Alerts / info / success / warning / error ── */
    [data-testid="stAlert"] { border-radius: 10px !important; }
    [data-testid="stAlert"] p { color: inherit !important; }

    /* ── Tabs ── */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        background: #d8f3dc !important;
        border-radius: 10px 10px 0 0 !important;
        padding: 8px 20px;
        font-weight: 600;
        color: #1b4332 !important;
    }
    .stTabs [aria-selected="true"] {
        background: #40916c !important;
        color: #ffffff !important;
    }

    /* ── Sidebar (dark green) ── */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div {
        background: linear-gradient(160deg, #1b4332 0%, #2d6a4f 50%, #40916c 100%) !important;
    }
    [data-testid="stSidebar"] *,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] div {
        color: #ffffff !important;
    }
    [data-testid="stSidebar"] input,
    [data-testid="stSidebar"] textarea {
        background: rgba(255,255,255,0.15) !important;
        border: 1px solid rgba(255,255,255,0.4) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    /* Sidebar selectbox & multiselect dropdown text */
    [data-testid="stSidebar"] [data-baseweb="select"] div,
    [data-testid="stSidebar"] [data-baseweb="select"] span {
        background: rgba(255,255,255,0.12) !important;
        color: #ffffff !important;
    }

    /* ── Hero banner ── */
    .hero-banner {
        background: linear-gradient(135deg, #1b4332 0%, #40916c 60%, #74c69d 100%) !important;
        border-radius: 16px;
        padding: 28px 36px;
        margin-bottom: 24px;
        color: #ffffff !important;
    }
    .hero-banner h1 { font-size: 2.4rem; margin: 0 0 6px; font-weight: 800; color: #ffffff !important; }
    .hero-banner p  { font-size: 1.05rem; margin: 0; opacity: 0.92; color: #ffffff !important; }

    /* ── Cards ── */
    .card {
        background: #ffffff !important;
        border-radius: 14px;
        padding: 22px 26px;
        box-shadow: 0 2px 10px rgba(0,0,0,0.07);
        margin-bottom: 18px;
        border-left: 5px solid #40916c;
        color: #1a2e1a !important;
    }
    .card * { color: #1a2e1a !important; }
    .card-warning { border-left-color: #f4a261; }
    .card-info    { border-left-color: #4895ef; }

    /* ── Step badges ── */
    .step-badge {
        display: inline-block;
        background: #40916c !important;
        color: #fff !important;
        border-radius: 50%;
        width: 28px; height: 28px;
        text-align: center; line-height: 28px;
        font-weight: 700; font-size: 0.9rem;
        margin-right: 8px;
    }

    /* ── Buttons ── */
    .stButton > button {
        background: linear-gradient(90deg, #2d6a4f, #52b788) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 10px !important;
        padding: 0.55rem 1.6rem !important;
        font-size: 1rem !important;
        font-weight: 600 !important;
    }
    .stButton > button:hover { opacity: 0.88; }
    .stDownloadButton > button {
        background: linear-gradient(90deg, #1b4332, #2d6a4f) !important;
        color: #fff !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }

    /* ── Disclaimer box ── */
    .disclaimer {
        background: #fff8e1 !important;
        border: 1px solid #ffc107 !important;
        border-radius: 10px;
        padding: 14px 18px;
        font-size: 0.88rem;
        color: #6b4c00 !important;
        margin-top: 22px;
    }
    .disclaimer * { color: #6b4c00 !important; }

    /* ── Gemini badge ── */
    .gemini-badge {
        display: inline-flex; align-items: center; gap: 8px;
        background: #1b4332 !important; color: #fff !important;
        border-radius: 8px; padding: 6px 14px;
        font-size: 0.82rem; font-weight: 600;
        letter-spacing: 0.04em;
    }
    .gemini-badge * { color: #fff !important; }
    .gemini-badge .dot { width:10px; height:10px; background:#4285f4; border-radius:50%; display:inline-block; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Session State Defaults ───────────────────────────────────
defaults = {
    "plan_text": "",
    "plan_path": None,
    "chat_history": [],
    "user_data": {},
    "api_configured": False,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Read API key from .env (or allow sidebar override) ───────
env_gemini_key = os.environ.get("GEMINI_API_KEY", "")

# ── Sidebar — Credentials only ───────────────────────────────
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")

    # Pre-fill from .env; user can override in sidebar
    api_key = st.text_input(
        "Gemini API Key",
        type="password",
        value=env_gemini_key,
        help="Loaded from .env (GEMINI_API_KEY). Get yours at aistudio.google.com",
    )

    if api_key:
        st.success("✅ Gemini API Key set")
        st.session_state["api_configured"] = True
    else:
        st.warning("Add GEMINI_API_KEY to .env to activate AI")
        st.session_state["api_configured"] = False

    st.markdown("---")
    st.markdown(
        "### 👤 Your Profile\nFill in the **Your Profile** form in the main area →",
    )
    if st.session_state.get("user_data"):
        ud = st.session_state["user_data"]
        st.markdown(f"**Name:** {ud.get('name','—')}")
        st.markdown(f"**Age:** {ud.get('age','—')}")
        st.markdown(f"**Diet:** {ud.get('diet_preference','—')}")
        st.markdown(f"**Goal:** {ud.get('goal','—')}")

    st.markdown("---")
    st.markdown(
        '<span class="gemini-badge"><span class="dot"></span>Powered by Google Gemini</span>',
        unsafe_allow_html=True,
    )

# ── Hero Banner ──────────────────────────────────────────────
st.markdown(
    """
    <div class="hero-banner">
        <h1>🥗 NutriBot — Agentic AI Nutritionist</h1>
        <p>Personalised nutrition plans & expert Q&A powered by <strong>Google Gemini</strong> with IBM Granite-style guardrails</p>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Tabs ─────────────────────────────────────────────────────
tab_profile, tab_plan, tab_chat, tab_about = st.tabs(
    ["👤 Your Profile", "📋 Generate Nutrition Plan", "💬 Ask NutriBot", "ℹ️ About & SDLC"]
)

# ═══════════════════════════════════════════════════════════════
# TAB 0 — Your Profile
# ═══════════════════════════════════════════════════════════════
with tab_profile:
    st.markdown(
        '<div class="card"><span class="step-badge">1</span>'
        '<strong>Tell us about yourself</strong> so NutriBot can personalise your nutrition plan.</div>',
        unsafe_allow_html=True,
    )

    with st.form("profile_form"):
        col_a, col_b = st.columns(2)
        with col_a:
            name = st.text_input("Full Name", placeholder="e.g. Priya Sharma",
                                 value=st.session_state["user_data"].get("name", "") if st.session_state["user_data"] else "")
            age  = st.number_input("Age", min_value=5, max_value=120,
                                   value=int(st.session_state["user_data"].get("age", 30)) if st.session_state["user_data"] else 30,
                                   step=1)
            city    = st.text_input("City",    placeholder="e.g. Mumbai",
                                    value=st.session_state["user_data"].get("city", "") if st.session_state["user_data"] else "")
            country = st.text_input("Country", placeholder="e.g. India",
                                    value=st.session_state["user_data"].get("country", "") if st.session_state["user_data"] else "")

        with col_b:
            diet = st.selectbox("Dietary Preference",
                                ["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian", "Pescatarian"],
                                index=["Vegetarian", "Non-Vegetarian", "Vegan", "Eggetarian", "Pescatarian"].index(
                                    st.session_state["user_data"].get("diet_preference", "Vegetarian")
                                ) if st.session_state["user_data"] else 0)
            goal = st.selectbox("Health Goal",
                                ["General Health & Wellness", "Weight Loss",
                                 "Weight Gain / Muscle Building", "Manage Blood Sugar",
                                 "Lower Blood Pressure", "Improve Energy Levels",
                                 "Heart-Healthy Diet", "Improve Gut Health"])
            medical = st.multiselect(
                "Medical Conditions (if any)",
                ["None", "Type 2 Diabetes", "Type 1 Diabetes", "High Blood Pressure",
                 "High Cholesterol", "Obesity", "Thyroid Disorder", "PCOS",
                 "Kidney Disease", "Heart Disease", "Lactose Intolerance",
                 "Gluten Intolerance / Celiac", "Anaemia"],
                default=["None"],
            )

        submitted = st.form_submit_button("💾 Save Profile", use_container_width=True)
        if submitted:
            med_str = ", ".join([m for m in medical if m != "None"]) or "None"
            st.session_state["user_data"] = {
                "name": name or "User",
                "age": age,
                "diet_preference": diet,
                "medical_history": med_str,
                "city": city,
                "country": country,
                "goal": goal,
            }
            st.success("✅ Profile saved! Head to the **📋 Generate Nutrition Plan** tab.")

    # Show saved summary card if profile exists
    if st.session_state["user_data"]:
        ud = st.session_state["user_data"]
        st.markdown("---")
        st.markdown(
            f"""
            <div class="card">
              <strong>📌 Saved Profile</strong><br><br>
              <table style="width:100%;border-collapse:collapse;">
                <tr><td style="padding:4px 10px;font-weight:600;color:#1a2e1a;">Name</td><td style="padding:4px 10px;color:#1a2e1a;">{ud.get('name','—')}</td>
                    <td style="padding:4px 10px;font-weight:600;color:#1a2e1a;">Age</td><td style="padding:4px 10px;color:#1a2e1a;">{ud.get('age','—')} yrs</td></tr>
                <tr><td style="padding:4px 10px;font-weight:600;color:#1a2e1a;">Diet</td><td style="padding:4px 10px;color:#1a2e1a;">{ud.get('diet_preference','—')}</td>
                    <td style="padding:4px 10px;font-weight:600;color:#1a2e1a;">Goal</td><td style="padding:4px 10px;color:#1a2e1a;">{ud.get('goal','—')}</td></tr>
                <tr><td style="padding:4px 10px;font-weight:600;color:#1a2e1a;">Location</td><td style="padding:4px 10px;color:#1a2e1a;">{ud.get('city','—')}, {ud.get('country','—')}</td>
                    <td style="padding:4px 10px;font-weight:600;color:#1a2e1a;">Medical</td><td style="padding:4px 10px;color:#1a2e1a;">{ud.get('medical_history','—')}</td></tr>
              </table>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ═══════════════════════════════════════════════════════════════
# TAB 1 — Generate Nutrition Plan
# ═══════════════════════════════════════════════════════════════
with tab_plan:
    st.markdown(
        '<div class="card"><span class="step-badge">2</span>'
        '<strong>Complete your profile</strong> in the <em>👤 Your Profile</em> tab, then generate your plan below.</div>',
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns([1, 2])
    with col1:
        generate_btn = st.button("🚀 Generate My Nutrition Plan", use_container_width=True)

    if generate_btn:
        if not st.session_state["api_configured"]:
            st.error("⚠️ Please add your Gemini API key to the .env file or enter it in the sidebar.")
        elif not st.session_state["user_data"]:
            st.warning("Please fill in your profile in the **👤 Your Profile** tab first.")
        else:
            rate_note = st.info(
                "⏳ **Free-tier note:** Gemini allows 5 requests/min. "
                "If you hit the limit, NutriBot will auto-retry up to 4 times (≈60 s). Please wait…",
                icon="ℹ️",
            )
            with st.spinner("🤖 NutriBot is creating your personalised plan (auto-retries on rate limit)…"):
                try:
                    from agent import run_nutrition_agent
                    plan_text, saved_path = run_nutrition_agent(
                        user_data=st.session_state["user_data"],
                        question=None,
                        api_key=api_key,
                        intent="plan",
                    )
                    st.session_state["plan_text"] = plan_text
                    st.session_state["plan_path"] = saved_path
                    rate_note.empty()
                    st.success("✅ Your personalised nutrition plan is ready!")
                except Exception as exc:
                    rate_note.empty()
                    err = str(exc)
                    if "rate limit" in err.lower() or "quota" in err.lower() or "429" in err:
                        st.error(
                            "⏳ **Gemini free-tier quota exceeded.** "
                            "Please wait ~1 minute and click Generate again. "
                            "To remove this limit, upgrade at https://ai.google.dev/gemini-api/docs/rate-limits"
                        )
                    else:
                        st.error(f"❌ Error generating plan: {exc}")

    if st.session_state["plan_text"]:
        st.markdown("---")
        st.markdown("### 🍽️ Your Personalised Nutrition Plan")
        st.markdown(st.session_state["plan_text"])

        # Download buttons
        st.markdown("---")
        col_dl1, col_dl2 = st.columns(2)
        with col_dl1:
            st.download_button(
                label="⬇️ Download Plan (.md)",
                data=st.session_state["plan_text"],
                file_name=f"nutrition_plan_{st.session_state['user_data'].get('name','user').replace(' ','_')}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with col_dl2:
            st.download_button(
                label="⬇️ Download Plan (.txt)",
                data=st.session_state["plan_text"],
                file_name=f"nutrition_plan_{st.session_state['user_data'].get('name','user').replace(' ','_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        if st.session_state["plan_path"]:
            st.info(
                f"📁 Plan also auto-saved to: `{st.session_state['plan_path']}`",
                icon="💾",
            )

# ═══════════════════════════════════════════════════════════════
# TAB 2 — Ask NutriBot (Agentic Q&A)
# ═══════════════════════════════════════════════════════════════
with tab_chat:
    st.markdown(
        '<div class="card card-info">'
        '<span class="step-badge" style="background:#4895ef">?</span>'
        'Ask NutriBot any nutrition-related question. Your saved profile is used for context.</div>',
        unsafe_allow_html=True,
    )

    # Display chat history
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"], avatar="🧑" if msg["role"] == "user" else "🤖"):
            st.markdown(msg["content"])

    # Chat input
    user_q = st.chat_input("Ask me anything about nutrition, diet, or healthy eating…")

    if user_q:
        st.session_state["chat_history"].append({"role": "user", "content": user_q})
        with st.chat_message("user", avatar="🧑"):
            st.markdown(user_q)

        if not st.session_state["api_configured"]:
            reply = "⚠️ Please add your Gemini API key to the .env file or enter it in the sidebar."
        else:
            with st.spinner("🤖 NutriBot is thinking…"):
                try:
                    from agent import run_nutrition_agent
                    reply, _ = run_nutrition_agent(
                        user_data=st.session_state.get("user_data", {}),
                        question=user_q,
                        api_key=api_key,
                        intent="query",
                    )
                except Exception as exc:
                    reply = f"❌ Error: {exc}"

        st.session_state["chat_history"].append({"role": "assistant", "content": reply})
        with st.chat_message("assistant", avatar="🤖"):
            st.markdown(reply)

        # Append disclaimer after every answer
        st.markdown(
            '<div class="disclaimer">'
            '⚕️ <strong>Reminder:</strong> AI responses are for informational purposes only. '
            'Always consult a registered dietitian or physician before changing your diet.'
            '</div>',
            unsafe_allow_html=True,
        )

    if st.session_state["chat_history"] and st.button("🗑️ Clear Chat"):
        st.session_state["chat_history"] = []
        st.rerun()

# ═══════════════════════════════════════════════════════════════
# TAB 3 — About & SDLC
# ═══════════════════════════════════════════════════════════════
with tab_about:
    st.markdown("## 🏗️ About NutriBot — Agentic AI SDLC")

    sdlc_phases = [
        ("1. Problem Definition & Scope",
         "Define the goal: build a personalised, ethics-aware nutrition assistant. "
         "Identify stakeholders (users, healthcare professionals), constraints (medical safety, "
         "cultural relevance), and success metrics (plan relevance, user satisfaction)."),

        ("2. Requirements Gathering",
         "Functional: collect user profile, generate 7-day meal plan, answer queries. "
         "Non-functional: ethical AI, HAM tone, guardrails, medical disclaimer, "
         "Markdown export. Technology: Google Gemini (gemini-3.8-flash), Python, Streamlit."),

        ("3. Architecture & Design",
         "Three-layer architecture — Presentation (Streamlit), Agentic Core (agent.py), "
         "LLM Backend (Google Gemini API). Agent implements intent detection, tool-like "
         "sub-routines, guardrail checks, and plan-saving. System prompt encodes HAM principles."),

        ("4. Implementation",
         "agent.py: Agentic loop with Gemini SDK, prompt builders, guardrail filter, "
         "Markdown file saver. app.py: Streamlit multi-tab UI, sidebar profile collector, "
         "chat interface, download buttons. .env for GEMINI_API_KEY."),

        ("5. Ethical AI & Guardrails",
         "Safety keyword filter, NEVER-diagnose instruction in system prompt, mandatory "
         "medical disclaimer on every plan, HAM tone enforcement, no hallucinated clinical "
         "facts policy, out-of-scope refusal."),

        ("6. Testing & Validation",
         "Python AST syntax validation, unit tests for guardrail logic, prompt construction, "
         "and file saving. Integration tests with Gemini (live API). Edge-case testing: "
         "missing profile, harmful input, invalid API key."),

        ("7. Deployment & Monitoring",
         "Local: run.bat launcher. Cloud-ready: .env secret management. "
         "Monitoring: plan file audit trail with timestamps, chat history session state. "
         "Future: Streamlit Cloud / GCP Cloud Run deployment."),

        ("8. Maintenance & Iteration",
         "Feedback loop from users → refine system prompt. Model upgrades (Gemini 2.5). "
         "Add meal image generation, calorie tracking API, multi-language support."),
    ]

    for title, desc in sdlc_phases:
        with st.expander(f"🔹 **Phase {title}**", expanded=False):
            st.markdown(desc)

    st.markdown("---")
    st.markdown("### 🤖 Model Details")
    st.markdown(
        textwrap.dedent("""
        | Property       | Value                              |
        |----------------|------------------------------------|
        | Model          | `gemini-3.8-flash`                 |
        | Provider       | Google AI (Gemini API)             |
        | Credentials    | `GEMINI_API_KEY` in `.env`         |
        | Specialisation | Instruction-following, reasoning   |
        | Temperature    | 0.7 (balanced creativity/accuracy) |
        | Max Tokens     | 1500 per response                  |
        """)
    )

    st.markdown("---")
    st.markdown("### 📂 Project Structure")
    st.code(
        textwrap.dedent("""
        NutritionAI/
        ├── app.py            ← Streamlit web application
        ├── agent.py          ← Agentic AI core (Gemini)
        ├── requirements.txt  ← Python dependencies
        ├── .env              ← GEMINI_API_KEY (never commit)
        ├── .env.example      ← Credentials template
        ├── run.bat           ← One-click Windows launcher
        ├── plans/            ← Auto-saved .md nutrition plans
        └── SDLC.md           ← Full SDLC documentation
        """).strip(),
        language="text",
    )

    st.markdown(
        '<div class="disclaimer">'
        '⚕️ <strong>Medical Disclaimer:</strong> NutriBot is an AI-powered informational tool. '
        'All nutrition plans and answers are for general informational purposes only and do '
        '<strong>not</strong> constitute medical advice. Consult a qualified healthcare '
        'professional or registered dietitian before making dietary changes.'
        '</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        "<br><center><small style='color:#888'>Made with ❤️ using Google Gemini · Streamlit · IBM Granite-style Prompting</small></center>",
        unsafe_allow_html=True,
    )
