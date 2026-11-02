"""
NutriBot — Agentic AI Nutritionist
150-second Project Explainer Video Generator
============================================================
Generates NutriBot_Video.mp4 using Pillow + moviepy.

Run:  python make_video.py
Output: NutriBot_Video.mp4  (1920×1080, 150 s, 24 fps)
"""

import os
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import (
    ImageClip, concatenate_videoclips, VideoFileClip,
    CompositeVideoClip, ColorClip
)

# ── Constants ────────────────────────────────────────────────
W, H   = 1920, 1080
FPS    = 24
OUTPUT = os.path.join(os.path.dirname(__file__), "NutriBot_Video.mp4")

# Colour palette
C_BG_DARK   = (27,  67, 50)   # #1B4332
C_BG_LIGHT  = (240, 255, 244) # #F0FFF4
C_GREEN1    = (64,  145, 108) # #40916C
C_GREEN2    = (45,  106, 79)  # #2D6A4F
C_GREEN3    = (82,  183, 136) # #52B788
C_GREEN4    = (116, 198, 157) # #74C69D
C_LIME      = (183, 228, 199) # #B7E4C7
C_MINT      = (216, 243, 220) # #D8F3DC
C_WHITE     = (255, 255, 255)
C_TEXT_DARK = (26,  46, 26)   # #1a2e1a
C_IBM       = (5,   47, 173)  # #052FAD
C_RED       = (214, 40,  40)  # #D62828
C_YELLOW    = (255, 220, 60)

# Fonts
F_BOLD  = "C:/Windows/Fonts/calibrib.ttf"
F_REG   = "C:/Windows/Fonts/calibri.ttf"
F_MONO  = "C:/Windows/Fonts/cour.ttf"    # fallback to courier

def font(size, bold=False):
    path = F_BOLD if bold else F_REG
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)

def font_mono(size):
    try:
        return ImageFont.truetype(F_MONO, size)
    except Exception:
        return ImageFont.truetype("C:/Windows/Fonts/arial.ttf", size)


# ── Drawing Helpers ──────────────────────────────────────────

def new_canvas(bg=C_BG_LIGHT):
    img = Image.new("RGB", (W, H), bg)
    return img, ImageDraw.Draw(img)

def draw_rect(draw, x, y, w, h, fill, radius=18):
    draw.rounded_rectangle([x, y, x+w, y+h], radius=radius, fill=fill)

def draw_header(draw, text, subtitle=None, bg=C_BG_DARK, stripe=C_GREEN1):
    draw_rect(draw, 0, 0, W, 140, bg, radius=0)
    draw_rect(draw, 0, 140, W, 8, stripe, radius=0)
    draw.text((60, 28), text, font=font(62, bold=True), fill=C_MINT)
    if subtitle:
        draw.text((60, 100), subtitle, font=font(30), fill=C_GREEN4)

def draw_footer(draw, text="NutriBot  ·  IBM SkillsBuild 2026  ·  Gartner Program"):
    draw_rect(draw, 0, H-52, W, 52, C_BG_DARK, radius=0)
    draw.text((W//2, H-36), text, font=font(24), fill=C_GREEN4, anchor="mm")

def wrap_text(draw, text, x, y, max_w, line_h, fnt, fill=C_TEXT_DARK):
    """Word-wrap text into box of max_w pixels wide."""
    words = text.split()
    lines, line = [], []
    for word in words:
        test = " ".join(line + [word])
        bbox = draw.textbbox((0, 0), test, font=fnt)
        if bbox[2] > max_w and line:
            lines.append(" ".join(line))
            line = [word]
        else:
            line.append(word)
    if line:
        lines.append(" ".join(line))
    for i, l in enumerate(lines):
        draw.text((x, y + i * line_h), l, font=fnt, fill=fill)
    return y + len(lines) * line_h

def bullet_list(draw, items, x, y, fnt, fill=C_TEXT_DARK, gap=12, bullet="●"):
    cy = y
    for item in items:
        draw.text((x, cy), bullet, font=fnt, fill=C_GREEN1)
        draw.text((x + 36, cy), item, font=fnt, fill=fill)
        bbox = draw.textbbox((0, 0), item, font=fnt)
        cy += bbox[3] - bbox[1] + gap
    return cy

def pill(draw, x, y, label, bg, fg=C_WHITE, fsize=28):
    fnt = font(fsize, bold=True)
    bbox = draw.textbbox((0, 0), label, font=fnt)
    pw = bbox[2] - bbox[0] + 40
    ph = bbox[3] - bbox[1] + 20
    draw_rect(draw, x, y, pw, ph, bg, radius=ph//2)
    draw.text((x + 20, y + 10), label, font=fnt, fill=fg)
    return x + pw + 16

def card(draw, x, y, w, h, title, lines, bg=C_BG_LIGHT, title_bg=C_GREEN2, title_fg=C_WHITE, body_fg=C_TEXT_DARK, fsize=26):
    draw_rect(draw, x, y, w, h, bg, radius=14)
    draw_rect(draw, x, y, w, 54, title_bg, radius=14)
    draw_rect(draw, x, y+40, w, 14, title_bg, radius=0)  # square bottom of title
    draw.text((x+16, y+10), title, font=font(fsize, bold=True), fill=title_fg)
    cy = y + 68
    fnt = font(fsize - 4)
    for line in lines:
        draw.text((x + 16, cy), line, font=fnt, fill=body_fg)
        cy += fsize + 4
    return cy

def pil_to_nparray(img):
    return np.array(img)

def make_clip(img, duration):
    arr = pil_to_nparray(img)
    return ImageClip(arr).set_duration(duration)

def fade_in(clip, t=0.4):
    return clip.crossfadein(t)

def fade_out(clip, t=0.4):
    return clip.crossfadeout(t)


# ════════════════════════════════════════════════════════════
#  SCENE BUILDERS  (12 scenes × ~12-13 s = 150 s)
# ════════════════════════════════════════════════════════════

# Scene 1 — Title / Intro  (14 s)
def scene_title():
    img, draw = new_canvas(C_BG_DARK)
    # green gradient strips
    for i, (c, y_, h_) in enumerate([
        (C_GREEN1, 0,    8),
        (C_GREEN2, H-8,  8),
    ]):
        draw_rect(draw, 0, y_, W, h_, c, radius=0)

    # big emoji
    draw.text((W//2, 160), "🥗", font=font(180), fill=C_MINT, anchor="mm")

    draw.text((W//2, 360), "NutriBot", font=font(140, bold=True), fill=C_MINT, anchor="mm")
    draw.text((W//2, 490), "Agentic AI Nutritionist", font=font(56), fill=C_GREEN4, anchor="mm")

    draw.text((W//2, 600),
              "Personalised 7-Day Nutrition Plans powered by Google Gemini",
              font=font(34), fill=C_GREEN3, anchor="mm")
    draw.text((W//2, 650),
              "IBM Granite-style Guardrails  ·  Built with IBM Bob  ·  Streamlit",
              font=font(30), fill=C_GREEN3, anchor="mm")

    # IBM badge
    draw_rect(draw, W//2-320, 730, 640, 60, C_IBM, radius=30)
    draw.text((W//2, 762), "IBM SkillsBuild 2026 — Gartner Program  |  Day 02",
              font=font(28, bold=True), fill=C_WHITE, anchor="mm")

    draw_footer(draw)
    return make_clip(img, 14)


# Scene 2 — Problem Statement  (12 s)
def scene_problem():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "⚠️  The Problem", "Why do millions lack good nutrition guidance?")
    draw_footer(draw)

    problems = [
        "Millions lack access to personalised, affordable dietary guidance",
        "Generic meal plans ignore medical conditions (diabetes, hypertension)",
        "No consideration of cultural food preferences or regional availability",
        "Age-specific macro & micro nutritional needs are often overlooked",
        "Health goals (gut health, weight loss, muscle gain) need custom plans",
    ]
    cy = 200
    for p in problems:
        draw_rect(draw, 60, cy, W-120, 72, C_MINT, radius=10)
        draw.text((110, cy+18), "✗", font=font(36, bold=True), fill=C_RED)
        draw.text((165, cy+18), p, font=font(34), fill=C_TEXT_DARK)
        cy += 90

    draw_rect(draw, 60, cy+10, W-120, 80, C_GREEN1, radius=14)
    draw.text((W//2, cy+52), "💡  Solution: NutriBot — Your Agentic AI Nutritionist",
              font=font(38, bold=True), fill=C_WHITE, anchor="mm")
    return make_clip(img, 12)


# Scene 3 — Project Overview  (12 s)
def scene_overview():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "🌿  Project Overview", "What NutriBot does for you")
    draw_footer(draw)

    boxes = [
        ("📥", "Collects",   "User profile:\nname, age, diet,\ngoals, medical\nhistory, location",   C_BG_DARK),
        ("🤖", "Generates",  "7-Day Personalised\nNutrition Plan\npowered by\nGemini LLM",           C_GREEN2),
        ("💬", "Answers",    "Free-form Q&A:\nNutrition queries\nin natural\nlanguage chat",          C_GREEN1),
        ("💾", "Saves",      "Timestamped .md\nplan saved to\nplans/ folder\nfor future use",         C_GREEN3),
    ]
    bw, bh, gap = 400, 420, 56
    total_w = len(boxes) * bw + (len(boxes)-1) * gap
    sx = (W - total_w) // 2
    for i, (emoji, title, body, bg) in enumerate(boxes):
        bx = sx + i * (bw + gap)
        by = 200
        draw_rect(draw, bx, by, bw, bh, bg, radius=20)
        draw.text((bx + bw//2, by + 70),  emoji, font=font(72), fill=C_WHITE, anchor="mm")
        draw.text((bx + bw//2, by + 155), title, font=font(38, bold=True), fill=C_WHITE, anchor="mm")
        cy = by + 200
        for line in body.split("\n"):
            draw.text((bx + bw//2, cy), line, font=font(28), fill=C_LIME, anchor="mm")
            cy += 40
        if i < len(boxes)-1:
            draw.text((bx + bw + gap//2, by + bh//2), "→",
                      font=font(80, bold=True), fill=C_GREEN4, anchor="mm")
    return make_clip(img, 12)


# Scene 4 — Tech Stack  (10 s)
def scene_tech():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "🛠️  Tech Stack", "Technologies powering NutriBot")
    draw_footer(draw)

    items = [
        ("🐍", "Python 3.10+",          "Core language",                  C_BG_DARK),
        ("🌐", "Streamlit ≥1.35",       "Web UI framework",               C_GREEN2),
        ("🤖", "Google Gemini",         "gemini-2.0-flash LLM",           C_GREEN1),
        ("⚡", "Agentic Core",          "IBM Granite-style prompting",     C_GREEN3),
        ("🔒", "python-dotenv",         "Secure credential management",    C_GREEN4),
        ("🎨", "Custom Theme",          "Green-health Streamlit config",   (100,180,120)),
    ]
    cols, rows = 3, 2
    cw, ch, gx, gy = 570, 230, 30, 20
    total_w = cols*cw + (cols-1)*gx
    sx = (W - total_w) // 2
    for idx, (emoji, title, desc, bg) in enumerate(items):
        col, row = idx % cols, idx // cols
        x = sx + col*(cw+gx)
        y = 200 + row*(ch+gy)
        draw_rect(draw, x, y, cw, ch, bg, radius=16)
        draw.text((x+50, y + ch//2 - 20), emoji, font=font(56), fill=C_WHITE, anchor="mm")
        draw.text((x+110, y+50), title, font=font(36, bold=True), fill=C_WHITE)
        draw.text((x+110, y+100), desc, font=font(28), fill=C_LIME)

    draw_rect(draw, W//2-380, 900, 760, 60, C_IBM, radius=30)
    draw.text((W//2, 932), "🔷  Developed using IBM Bob  ·  IBM SkillsBuild 2026",
              font=font(28, bold=True), fill=C_WHITE, anchor="mm")
    return make_clip(img, 10)


# Scene 5 — System Architecture  (12 s)
def scene_arch():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "🏗️  System Architecture", "3-layer design: UI → Agentic Core → Gemini API")
    draw_footer(draw)

    layers = [
        ("🌐  User Browser  (Streamlit — localhost:8501)",
         ["👤 Profile Tab", "📅 Plan Tab", "💬 Chat Tab", "ℹ️ About Tab"],
         C_BG_DARK, C_GREEN2),
        ("🤖  Agentic Core  —  agent.py",
         ["🛡️ Guardrail Filter", "🔧 Prompt Builder", "💾 Plan Saver (.md)"],
         C_GREEN2, C_GREEN1),
        ("☁️  Google Gemini API  (gemini-2.0-flash)  —  IBM Granite System Prompt",
         [],
         C_IBM, C_IBM),
    ]
    lh, gap, lw = 160, 50, W - 200
    cy = 195
    for (title, subtabs, bg, stripe) in layers:
        draw_rect(draw, 100, cy, lw, lh, bg, radius=14)
        draw.text((W//2, cy + 36), title, font=font(36, bold=True), fill=C_WHITE, anchor="mm")
        if subtabs:
            tw = (lw - 80) // len(subtabs)
            for j, tab in enumerate(subtabs):
                tx = 140 + j * (tw + 10)
                draw_rect(draw, tx, cy+72, tw, 68, stripe, radius=10)
                draw.text((tx + tw//2, cy + 107), tab, font=font(24, bold=True),
                          fill=C_WHITE, anchor="mm")
        if cy + lh + gap < H - 80:
            # draw arrow
            draw.text((W//2, cy + lh + 8), "↓  HTTPS API  ↓" if "Gemini" in title else "↓",
                      font=font(36, bold=True), fill=C_GREEN1, anchor="mm")
        cy += lh + gap
    return make_clip(img, 12)


# Scene 6 — Agentic Loop  (12 s)
def scene_loop():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "🔁  Agentic AI Loop", "How NutriBot processes every request")
    draw_footer(draw)

    steps = [
        ("1", "📥 User Input",    "Profile + question",    C_BG_DARK),
        ("2", "🎯 Intent",        "plan / query",           C_GREEN2),
        ("3", "🛡️ Guardrail",    "keyword scan",           C_GREEN1),
        ("4", "🔧 Prompt Build",  "tool sub-routine",       C_GREEN3),
        ("5", "☁️ Gemini API",   "with retry logic",       C_IBM),
        ("6", "📝 Post-process",  "+ disclaimer\n+ save .md", (100,180,120)),
    ]
    sw, sh, gx = 260, 200, 20
    total_w = len(steps)*sw + (len(steps)-1)*gx
    sx = (W - total_w) // 2
    sy = 210

    for i, (num, title, body, bg) in enumerate(steps):
        x = sx + i*(sw+gx)
        draw_rect(draw, x, sy, sw, sh, bg, radius=14)
        draw_rect(draw, x, sy, 52, 52, C_GREEN1, radius=26)
        draw.text((x+26, sy+26), num, font=font(28, bold=True), fill=C_WHITE, anchor="mm")
        draw.text((x+sw//2, sy+90),  title, font=font(28, bold=True), fill=C_WHITE, anchor="mm")
        for li, line in enumerate(body.split("\n")):
            draw.text((x+sw//2, sy+135+li*32), line, font=font(24), fill=C_LIME, anchor="mm")
        if i < len(steps)-1:
            ax = x + sw + gx//2
            draw.text((ax, sy+sh//2), "→", font=font(48, bold=True), fill=C_GREEN4, anchor="mm")

    # Fail path
    draw_rect(draw, sx + 2*(sw+gx), sy+sh+30, sw, 62, C_RED, radius=10)
    draw.text((sx+2*(sw+gx)+sw//2, sy+sh+62), "FAIL → ⚠️ Safety Refusal",
              font=font(24, bold=True), fill=C_WHITE, anchor="mm")

    # Return arrow
    draw_rect(draw, 100, sy+sh+130, W-200, 60, C_MINT, radius=10)
    draw.text((W//2, sy+sh+162), "↑  Response returned to Streamlit UI  ↑",
              font=font(30, bold=True), fill=C_BG_DARK, anchor="mm")

    # Retry note
    draw.text((W//2, sy+sh+230),
              "Retry logic: up to 4 attempts with back-off on Gemini 429 rate-limit errors",
              font=font(26), fill=C_GREEN2, anchor="mm")

    return make_clip(img, 12)


# Scene 7 — User Profile UI  (12 s)
def scene_profile():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "👤  User Profile Setup", "Step 1 — Fill in your health profile")
    draw_footer(draw)

    # Simulated form
    fx, fy, fw = 90, 185, 1100
    draw_rect(draw, fx, fy, fw, 820, C_WHITE, radius=16)
    draw_rect(draw, fx, fy, fw, 54, C_GREEN2, radius=16)
    draw_rect(draw, fx, fy+40, fw, 14, C_GREEN2, radius=0)
    draw.text((fx+24, fy+12), "👤  Your Profile", font=font(32, bold=True), fill=C_WHITE)

    fields = [
        ("Full Name",          "Vignesh"),
        ("Age",                "30"),
        ("City",               "Chennai"),
        ("Country",            "India"),
        ("Dietary Preference", "Non-Vegetarian  ▼"),
        ("Health Goal",        "Improve Gut Health  ▼"),
        ("Medical Conditions", "None  ✕"),
    ]
    cy = fy + 80
    for i, (label, val) in enumerate(fields):
        col = i % 2
        row = i // 2
        if i == 6:
            col, row = 0, 3
            fw2 = fw - 32
        else:
            fw2 = (fw - 48) // 2

        cx = fx + 16 + col * (fw2 + 16)
        cy2 = fy + 80 + row * 130

        draw.text((cx, cy2), label, font=font(24), fill=C_GREEN2)
        draw_rect(draw, cx, cy2+30, fw2, 56, (245,250,246), radius=8)
        draw.text((cx+14, cy2+42), val, font=font(28, bold=True), fill=C_TEXT_DARK)

    btn_y = fy + 82 + 4*130 - 10
    draw_rect(draw, fx+16, btn_y, fw-32, 64, C_GREEN1, radius=12)
    draw.text((fx + fw//2, btn_y+34), "💾  Save Profile",
              font=font(32, bold=True), fill=C_WHITE, anchor="mm")

    draw_rect(draw, fx+16, btn_y+76, fw-32, 54, C_MINT, radius=10)
    draw.text((fx+24, btn_y+100),
              "✅  Profile saved! Switch to Plan tab to generate your nutrition plan.",
              font=font(26), fill=C_BG_DARK)

    # right panel: about the sidebar
    rx = fx + fw + 60
    draw_rect(draw, rx, 185, W-rx-60, 820, C_MINT, radius=16)
    draw.text((rx+24, 210), "⚙️  Sidebar", font=font(34, bold=True), fill=C_BG_DARK)
    sidebar_lines = [
        "🔑 Gemini API Key",
        "  [ enter key here ]",
        "",
        "📋 App Info:",
        "  NutriBot v1.0",
        "  Google Gemini 2.0 Flash",
        "  Built with IBM Bob",
        "",
        "Theme: Green-Health",
        "Custom .streamlit/config.toml",
    ]
    cy3 = 270
    for line in sidebar_lines:
        draw.text((rx+24, cy3), line, font=font(26 if line.startswith(" ") else 28), fill=C_BG_DARK)
        cy3 += 52
    return make_clip(img, 12)


# Scene 8 — Generated Plan  (14 s)
def scene_plan_output():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "🥗  Generated Nutrition Plan", "Real output from NutriBot for Vignesh, Chennai")
    draw_footer(draw)

    # meta bar
    draw_rect(draw, 60, 190, W-120, 52, C_BG_DARK, radius=10)
    draw.text((W//2, 217),
              "🤖 NutriBot  ·  Google Gemini  ·  November 02, 2026  ·  Gut Health Focus",
              font=font(26), fill=C_GREEN4, anchor="mm")

    # profile row
    draw_rect(draw, 60, 254, W-120, 54, C_GREEN2, radius=10)
    draw.text((W//2, 282),
              "Vignesh  |  30 yrs  |  Non-Vegetarian  |  No Medical Conditions  |  Chennai, India  |  Goal: Gut Health",
              font=font(26, bold=True), fill=C_WHITE, anchor="mm")

    # Macro targets
    draw_rect(draw, 60, 320, W-120, 52, C_GREEN1, radius=10)
    draw.text((120, 338), "📊  Daily Macro Targets", font=font(28, bold=True), fill=C_WHITE)

    macros = [
        ("🔥 Calories",   "2,050–2,150 kcal", C_BG_DARK),
        ("💪 Protein",    "95–110 g",          C_GREEN2),
        ("🌾 Carbs",      "240–260 g",         C_GREEN1),
        ("🥦 Fiber",      "35–40 g ⭐",        C_GREEN3),
        ("🥜 Fats",       "55–65 g",           (100,180,120)),
    ]
    mw = (W-160) // len(macros)
    mx = 80
    for i, (lbl, val, bg) in enumerate(macros):
        draw_rect(draw, mx + i*mw, 382, mw-10, 110, bg, radius=12)
        draw.text((mx + i*mw + mw//2, 418), lbl, font=font(26, bold=True), fill=C_WHITE, anchor="mm")
        draw.text((mx + i*mw + mw//2, 462), val, font=font(30, bold=True), fill=C_MINT, anchor="mm")

    # Day 1 & Day 2 side by side
    draw_rect(draw, 60, 504, W-120, 48, C_GREEN2, radius=10)
    draw.text((120, 518), "📅  7-Day Meal Plan  — Sample Days (from saved plan)", font=font(26, bold=True), fill=C_WHITE)

    day_data = [
        ("Day 1",
         "🍳 Ragi Idlis + Tomato-Mint Chutney + Boiled Egg",
         "🍱 Brown Rice + Fish Curry (Sankara) + Keerai Kootu",
         "🥛 Neer Moru (spiced buttermilk)",
         "🌙 Phulkas + Methi Chicken + Steamed Okra"),
        ("Day 2",
         "🍚 Red Rice Poha + Peas + Roasted Peanuts + Curry Leaves",
         "🍱 Pazhaya Sadam (fermented rice) + Shallots + Curd",
         "🥜 Almonds & Walnuts + Tender Coconut Water",
         "🌙 Foxtail Millet Dosa + Drumstick Sambar + Mint Thuvaiyal"),
    ]
    dw = (W - 160) // 2
    for di, (day, bf, ln, sn, dn) in enumerate(day_data):
        dx = 80 + di * (dw + 20)
        dy = 564
        draw_rect(draw, dx, dy, dw, 420, C_WHITE, radius=14)
        draw_rect(draw, dx, dy, dw, 52, C_BG_DARK, radius=14)
        draw_rect(draw, dx, dy+40, dw, 12, C_BG_DARK, radius=0)
        draw.text((dx+dw//2, dy+26), day, font=font(30, bold=True), fill=C_GREEN4, anchor="mm")
        meal_labels = ["Breakfast", "Lunch", "Snack", "Dinner"]
        meals = [bf, ln, sn, dn]
        meal_colors = [C_MINT, (220,245,225), C_MINT, (220,245,225)]
        cy2 = dy + 64
        for ml, mv, mc in zip(meal_labels, meals, meal_colors):
            draw_rect(draw, dx+8, cy2, dw-16, 80, mc, radius=8)
            draw.text((dx+20, cy2+6),  ml+":", font=font(22, bold=True), fill=C_GREEN2)
            wrap_text(draw, mv, dx+20, cy2+30, dw-40, 26, font(22), fill=C_TEXT_DARK)
            cy2 += 88

    return make_clip(img, 14)


# Scene 9 — Full 7-Day Table  (12 s)
def scene_meal_table():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "📅  Full 7-Day Meal Planner", "Traditional South Indian gut-health foods (Chennai)")
    draw_footer(draw)

    rows_data = [
        ("Day 1", "Ragi Idlis + Egg",         "Fish Curry + Keerai Kootu", "Neer Moru",                "Phulkas + Methi Chicken"),
        ("Day 2", "Red Rice Poha + Peanuts",  "Pazhaya Sadam + Curd",      "Almonds + Coconut water",  "Millet Dosa + Drumstick Sambar"),
        ("Day 3", "Egg Omelette + Sourdough", "Barnyard Millet + Rasam",   "Greek Yoghurt + Papaya",   "Idiyappam + Veg Stew"),
        ("Day 4", "Ragi Dosas + Chutney",     "Samai Curd Rice + Chicken", "Peanuts + Jeera Water",    "Rotis + Moong Dal"),
        ("Day 5", "Pesarattu + Ginger Chutney","Brown Rice + Egg Curry",   "Roasted Makhana",          "Khichdi + Raita"),
        ("Day 6", "Poha + Chia Seeds",        "Millet Sambar + Rasam",     "Tender Coconut + Walnuts", "Paneer Bhurji + Rotis"),
        ("Day 7", "Idli + Sambar",            "Red Rice + Chicken Curry",  "Sundal (Black Chana)",     "Idiyappam + Egg Curry"),
    ]
    headers = ["Day", "Breakfast", "Lunch", "Snack", "Dinner"]
    col_w   = [100, 420, 420, 360, 420]
    sx, ty  = 60, 190
    hh, rh  = 54, 92

    # header row
    cx = sx
    for i, (h, w) in enumerate(zip(headers, col_w)):
        draw_rect(draw, cx, ty, w, hh, C_BG_DARK, radius=0)
        draw.text((cx + w//2, ty + hh//2), h, font=font(28, bold=True), fill=C_GREEN4, anchor="mm")
        cx += w

    # data rows
    for ri, row in enumerate(rows_data):
        cy = ty + hh + ri * rh
        bg = C_MINT if ri % 2 == 0 else C_WHITE
        cx = sx
        for ci, (cell, w) in enumerate(zip(row, col_w)):
            draw_rect(draw, cx, cy, w, rh, bg, radius=0)
            fnt = font(22, bold=(ci == 0))
            fill = C_GREEN2 if ci == 0 else C_TEXT_DARK
            wrap_text(draw, cell, cx+8, cy+8, w-16, 26, fnt, fill)
            cx += w

    draw.text((W//2, 200 + hh + 7*rh + 16),
              "★  All meals are culturally relevant to Chennai, India  ·  Fermented foods provide natural probiotics",
              font=font(26), fill=C_GREEN2, anchor="mm")

    return make_clip(img, 12)


# Scene 10 — Chat Interface  (12 s)
def scene_chat():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "💬  AI Chat Interface", "Ask NutriBot anything about nutrition")
    draw_footer(draw)

    # chat window
    cx, cy_, cw, ch = 80, 190, 1260, 810
    draw_rect(draw, cx, cy_, cw, ch, C_WHITE, radius=16)
    draw_rect(draw, cx, cy_, cw, 54, C_BG_DARK, radius=16)
    draw_rect(draw, cx, cy_+40, cw, 14, C_BG_DARK, radius=0)
    draw.text((cx+24, cy_+14), "💬  NutriBot Chat — Ask me anything about nutrition", font=font(28, bold=True), fill=C_GREEN4)

    convos = [
        ("user",    "What are the best probiotic foods for gut health in Chennai?"),
        ("bot",     "Great question, Vignesh! For your gut, the best probiotics available in Chennai are:\n"
                    "• Homemade curd (richest natural probiotic)\n"
                    "• Fermented idli/dosa batter (Lactobacillus)\n"
                    "• Pazhaya Sadam (fermented overnight rice)\n"
                    "• Neer Moru — spiced buttermilk with ginger & curry leaves\n"
                    "Aim for 1–2 servings daily. Pair with garlic & onions for amplified prebiotic effect!"),
        ("user",    "Can I eat fish every day on this plan?"),
        ("bot",     "Yes! Wild-caught Sankara (Red Snapper) and Tengali are excellent sources of omega-3s that\n"
                    "reduce gut inflammation. Aim for 3–4 times per week for dietary diversity. On non-fish days,\n"
                    "eggs and lean chicken are excellent protein alternatives for your gut-health goal."),
    ]

    msg_y = cy_ + 70
    for role, text in convos:
        if role == "user":
            bg_msg, fg_msg, label = C_MINT, C_TEXT_DARK, "👤  You:"
        else:
            bg_msg, fg_msg, label = (230, 248, 235), C_TEXT_DARK, "🤖  NutriBot:"
        lines = text.split("\n")
        mh = max(70, 36 + len(lines)*30 + 12)
        draw_rect(draw, cx+14, msg_y, cw-28, mh, bg_msg, radius=10)
        draw.text((cx+28, msg_y+8), label, font=font(24, bold=True), fill=C_GREEN2)
        ly = msg_y + 36
        for l in lines:
            draw.text((cx+28, ly), l, font=font(24), fill=fg_msg)
            ly += 30
        msg_y += mh + 12

    # input box
    iy = cy_ + ch - 64
    draw_rect(draw, cx+14, iy, cw-28, 50, (240,248,240), radius=10)
    draw.text((cx+28, iy+12), "Ask me anything about nutrition, diet, or healthy eating…  ▶",
              font=font(26), fill=C_GREEN4)

    # right panel: guardrail info
    rx = cx + cw + 60
    draw_rect(draw, rx, 190, W-rx-60, 810, C_MINT, radius=16)
    draw.text((rx+20, 210), "🛡️ Chat Safety", font=font(32, bold=True), fill=C_BG_DARK)
    features = [
        "✅ Profile-aware context",
        "✅ Full session history",
        "✅ Guardrail active",
        "✅ Medical disclaimer",
        "✅ HAM tone enforced",
        "✅ Clear chat button",
        "",
        "Guardrail blocks:",
        "❌ harmful queries",
        "❌ self-harm topics",
        "❌ illegal substances",
        "❌ off-topic content",
    ]
    gy2 = 270
    for f in features:
        fnt = font(26, bold=f.startswith("Guardrail"))
        draw.text((rx+20, gy2), f, font=fnt, fill=C_BG_DARK if f else C_GREEN2)
        gy2 += 46

    return make_clip(img, 12)


# Scene 11 — Ethical AI & Guardrails  (12 s)
def scene_ethics():
    img, draw = new_canvas(C_BG_LIGHT)
    draw_header(draw, "🛡️  Ethical AI & Guardrails", "HAM: Helpful · Accurate · Mindful (IBM Granite-style)")
    draw_footer(draw)

    # HAM 3 pillars
    pillars = [
        ("🤝", "HELPFUL",   C_BG_DARK,  [
            "Structured, actionable plans",
            "Grocery lists included",
            "Hydration & lifestyle tips",
            "Cultural meal context",
        ]),
        ("🎯", "ACCURATE",  C_GREEN2, [
            "Evidence-based guidelines",
            "Uncertainty acknowledged",
            "No clinical hallucinations",
            "No diagnosis or prescription",
        ]),
        ("💚", "MINDFUL",   C_GREEN1, [
            "Warm, respectful tone",
            "Culturally sensitive suggestions",
            "No stigmatising language",
            "Medical disclaimer always",
        ]),
    ]
    pw, ph = 480, 420
    gx2 = (W - 3*pw) // 4
    for i, (emoji, title, bg, bullets) in enumerate(pillars):
        px = gx2 + i*(pw+gx2)
        py = 190
        draw_rect(draw, px, py, pw, ph, bg, radius=18)
        draw.text((px + pw//2, py + 70),  emoji, font=font(64), fill=C_WHITE, anchor="mm")
        draw.text((px + pw//2, py + 145), title, font=font(40, bold=True), fill=C_WHITE, anchor="mm")
        draw_rect(draw, px+20, py+175, pw-40, 3, C_GREEN4, radius=2)
        by2 = py + 196
        for b in bullets:
            draw.text((px+32, by2), "•  " + b, font=font(26), fill=C_LIME)
            by2 += 48

    # Guardrail code box
    draw_rect(draw, 80, 630, W-160, 340, C_BG_DARK, radius=14)
    draw.text((120, 650), "Guardrail Implementation", font=font(28, bold=True), fill=C_GREEN4)
    code_lines = [
        'GUARDRAIL_KEYWORDS = [',
        '    "suicide", "self-harm", "overdose", "poison", "kill yourself",',
        '    "illegal drug", "narcotic", "bomb", "weapon"',
        ']',
        '',
        '→  All user inputs scanned BEFORE any Gemini API call',
        '→  Match = immediate safety refusal  (zero LLM cost)',
        '→  System prompt additionally PROHIBITS diagnosis & prescription',
    ]
    cy3 = 694
    for cl in code_lines:
        fnt = font_mono(24) if cl.startswith((' ', 'G', ']', '')) else font(24)
        fill = C_GREEN4 if cl.startswith("→") else (200, 235, 215)
        draw.text((120, cy3), cl, font=fnt, fill=fill)
        cy3 += 34

    return make_clip(img, 12)


# Scene 12 — Deployment / Summary / Outro  (14 s)
def scene_outro():
    img, draw = new_canvas(C_BG_DARK)
    draw_rect(draw, 0, 0, W, 8,  C_GREEN1, radius=0)
    draw_rect(draw, 0, H-8, W, 8, C_GREEN1, radius=0)

    draw.text((W//2, 80), "🚀  Deployment & Summary", font=font(70, bold=True), fill=C_MINT, anchor="mm")

    # GitHub box
    draw_rect(draw, 80, 140, W-160, 100, C_GREEN2, radius=16)
    draw.text((W//2, 168), "📦  GitHub Repository", font=font(32, bold=True), fill=C_WHITE, anchor="mm")
    draw.text((W//2, 212), "🔗  github.com/vignesh2396/NutritionAgent_IBMBob",
              font=font(34, bold=True), fill=C_MINT, anchor="mm")

    # Quick start
    draw_rect(draw, 80, 258, 860, 380, (30,55,40), radius=14)
    draw.text((110, 275), "⚡  Quick Start", font=font(30, bold=True), fill=C_GREEN4)
    qs = [
        "git clone github.com/vignesh2396/NutritionAgent_IBMBob",
        "pip install -r requirements.txt",
        "cp .env.example .env   # add GEMINI_API_KEY",
        "streamlit run app.py",
        "",
        "→  Opens at http://localhost:8501",
        "→  Windows: double-click run.bat",
    ]
    qy = 320
    for q in qs:
        fnt = font_mono(24) if not q.startswith("→") else font(24)
        fill = C_GREEN4 if q.startswith("→") else (180, 230, 200)
        draw.text((110, qy), q, font=fnt, fill=fill)
        qy += 38

    # Summary checklist
    draw_rect(draw, 970, 258, W-1050, 380, (30,55,40), radius=14)
    draw.text((1000, 275), "✅  Project Achievements", font=font(30, bold=True), fill=C_GREEN4)
    achievements = [
        "Personalised 7-day meal plan for Vignesh",
        "Culturally-aware South Indian menu (Chennai)",
        "Macros: 2050–2150 kcal, 35–40g fibre",
        "4-tab Streamlit UI (Profile/Plan/Chat/About)",
        "HAM guardrails + medical disclaimer",
        "SDLC: 8 phases fully documented",
        "Deployed to GitHub (public repo)",
        "IBM SkillsBuild 2026 — Gartner Program ✓",
    ]
    ay = 320
    for a in achievements:
        draw.text((1000, ay), "✅  " + a, font=font(26), fill=C_LIME)
        ay += 40

    # Thank you
    draw_rect(draw, 80, 660, W-160, 110, C_GREEN1, radius=18)
    draw.text((W//2, 716), "🥗  Thank You!  NutriBot — Agentic AI Nutritionist",
              font=font(42, bold=True), fill=C_WHITE, anchor="mm")

    draw_rect(draw, 80, 790, W-160, 60, C_IBM, radius=14)
    draw.text((W//2, 822),
              "Built with IBM Bob  ·  Google Gemini  ·  Streamlit  ·  IBM SkillsBuild 2026",
              font=font(28, bold=True), fill=C_WHITE, anchor="mm")

    draw.text((W//2, 910),
              "Developer: Vignesh  ·  github.com/vignesh2396  ·  app: localhost:8501",
              font=font(26), fill=C_GREEN4, anchor="mm")

    draw.text((W//2, 970), "http://localhost:8501", font=font(32, bold=True), fill=C_MINT, anchor="mm")

    return make_clip(img, 14)


# ════════════════════════════════════════════════════════════
#  ASSEMBLE & RENDER
# ════════════════════════════════════════════════════════════

def main():
    print("=" * 60)
    print("  NutriBot — 150s Video Generator")
    print("  Output:", OUTPUT)
    print("=" * 60)

    print("\nBuilding scenes...")
    scenes_fns = [
        ("01  Title",           scene_title),
        ("02  Problem",         scene_problem),
        ("03  Overview",        scene_overview),
        ("04  Tech Stack",      scene_tech),
        ("05  Architecture",    scene_arch),
        ("06  Agentic Loop",    scene_loop),
        ("07  User Profile",    scene_profile),
        ("08  Plan Output",     scene_plan_output),
        ("09  Meal Table",      scene_meal_table),
        ("10  Chat",            scene_chat),
        ("11  Ethical AI",      scene_ethics),
        ("12  Outro/Deploy",    scene_outro),
    ]

    clips = []
    total = 0
    for name, fn in scenes_fns:
        print(f"  Rendering scene {name}...", end=" ", flush=True)
        clip = fn()
        clip = fade_in(clip).crossfadeout(0.4)
        clips.append(clip)
        total += clip.duration
        print(f"{clip.duration:.0f}s  (running total: {total:.0f}s)")

    print(f"\nTotal duration: {total:.0f}s")
    print("\nConcatenating clips...")
    final = concatenate_videoclips(clips, method="compose")

    print(f"Writing {OUTPUT} ...")
    final.write_videofile(
        OUTPUT,
        fps=FPS,
        codec="libx264",
        audio=False,
        preset="medium",
        ffmpeg_params=["-crf", "22"],
        verbose=False,
        logger=None,
    )
    print(f"\n✅  Done!  Video saved to:\n    {OUTPUT}")
    print(f"   Duration: {final.duration:.1f}s  |  Resolution: {W}×{H}  |  FPS: {FPS}")


if __name__ == "__main__":
    main()
