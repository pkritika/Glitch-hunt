import random
import streamlit as st


# ── Pure logic helpers ────────────────────────────────────────────────────────

def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None or raw == "":
        return False, None, "Enter a guess."
    try:
        value = int(float(raw)) if "." in raw else int(raw)
    except Exception:
        return False, None, "That is not a number."
    return True, value, None


def check_guess(guess, secret):
    if guess == secret:
        return "Win", "🎉 Correct!"
    try:
        if guess > secret:
            return "Too High", "📈 Go Lower!"
        else:
            return "Too Low", "📉 Go Higher!"
    except TypeError:
        g = str(guess)
        if g == secret:
            return "Win", "🎉 Correct!"
        if g > secret:
            return "Too High", "📈 Go Lower!"
        return "Too Low", "📉 Go Higher!"


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = max(10, 100 - 10 * (attempt_number + 1))
        return current_score + points
    if outcome == "Too High":
        return current_score + 5 if attempt_number % 2 == 0 else current_score - 5
    if outcome == "Too Low":
        return current_score - 5
    return current_score


# ── Page config ───────────────────────────────────────────────────────────────

st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮", layout="centered")

# ── Global CSS ────────────────────────────────────────────────────────────────

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;600;700;800&display=swap');

/* ── Base ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background: #080818 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    color: #e0e0ff;
}
[data-testid="stHeader"] { background: transparent !important; }
[data-testid="stMainBlockContainer"] { padding-top: 1rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0c0c22 !important;
    border-right: 1px solid #1e1e44 !important;
}
[data-testid="stSidebar"] * { font-family: 'Space Grotesk', sans-serif !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0d0d1a; }
::-webkit-scrollbar-thumb { background: #3333aa; border-radius: 99px; }

/* ── Animations ── */
@keyframes shimmer {
    0%   { background-position: -200% center; }
    100% { background-position:  200% center; }
}
@keyframes fadeSlideIn {
    from { opacity: 0; transform: translateY(12px); }
    to   { opacity: 1; transform: translateY(0); }
}
@keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 8px #aa44ff44; }
    50%       { box-shadow: 0 0 22px #aa44ff99, 0 0 40px #aa44ff33; }
}
@keyframes bounce-in {
    0%   { transform: scale(0.7); opacity: 0; }
    60%  { transform: scale(1.08); }
    100% { transform: scale(1);   opacity: 1; }
}

/* ── Input ── */
div[data-testid="stTextInput"] input {
    background: #11112a !important;
    border: 2px solid #3333aa !important;
    border-radius: 14px !important;
    color: #ffffff !important;
    font-size: 1.3rem !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    padding: 0.7rem 1.2rem !important;
    text-align: center !important;
    letter-spacing: 2px !important;
    transition: border-color 0.25s, box-shadow 0.25s !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: #aa44ff !important;
    box-shadow: 0 0 0 3px #aa44ff33, 0 0 20px #aa44ff44 !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: #44447a !important;
    letter-spacing: 1px !important;
    font-weight: 400 !important;
}

/* ── Buttons ── */
div[data-testid="stButton"] button {
    border-radius: 14px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.6rem 1.4rem !important;
    transition: transform 0.15s, box-shadow 0.15s, filter 0.15s !important;
    border: none !important;
}
div[data-testid="stButton"] button:hover {
    transform: translateY(-3px) !important;
    filter: brightness(1.15) !important;
}
div[data-testid="stButton"] button:active {
    transform: translateY(0px) !important;
}
div[data-testid="stButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #6600cc, #aa44ff, #cc66ff) !important;
    background-size: 200% auto !important;
    animation: pulse-glow 2.5s ease-in-out infinite !important;
    color: white !important;
    letter-spacing: 0.5px !important;
}
div[data-testid="stButton"] button[kind="secondary"] {
    background: #1a1a3a !important;
    color: #aaaaee !important;
    border: 1px solid #2a2a5a !important;
}
div[data-testid="stButton"] button[kind="secondary"]:hover {
    background: #222244 !important;
    color: #ffffff !important;
    box-shadow: 0 4px 14px #00000055 !important;
}

/* ── Checkbox ── */
div[data-testid="stCheckbox"] label {
    color: #8888bb !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 0.9rem !important;
}

/* ── Remove default streamlit spacing noise ── */
div[data-testid="stVerticalBlock"] > div { gap: 0 !important; }
.stAlert { border-radius: 14px !important; }
</style>
""", unsafe_allow_html=True)

# ── Sidebar ───────────────────────────────────────────────────────────────────

st.sidebar.markdown("""
<div style='padding:16px 0 8px;text-align:center'>
  <div style='font-size:2rem'>🎮</div>
  <div style='font-size:1.1rem;font-weight:800;color:#aa44ff;letter-spacing:1px'>GLITCHY GUESSER</div>
  <div style='font-size:0.75rem;color:#555588;margin-top:2px'>v2.0 — now with more glitches</div>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("<hr style='border:none;border-top:1px solid #1e1e44;margin:8px 0'>", unsafe_allow_html=True)

difficulty = st.sidebar.selectbox("⚙️ Difficulty", ["Easy", "Normal", "Hard"], index=1)

attempt_limit_map = {"Easy": 6, "Normal": 8, "Hard": 5}
attempt_limit = attempt_limit_map[difficulty]
low, high = get_range_for_difficulty(difficulty)

diff_cfg = {
    "Easy":   {"color": "#44dd88", "icon": "🟢", "desc": "A gentle warmup"},
    "Normal": {"color": "#ffaa22", "icon": "🟡", "desc": "The real challenge"},
    "Hard":   {"color": "#ff4466", "icon": "🔴", "desc": "Good luck. You'll need it."},
}
dc = diff_cfg[difficulty]

st.sidebar.markdown(
    f"<div style='background:#111128;border-radius:12px;padding:14px 16px;margin:10px 0;"
    f"border:1px solid #1e1e44;border-left:3px solid {dc['color']}'>"
    f"<div style='font-size:1rem;font-weight:700;color:{dc['color']}'>{dc['icon']} {difficulty}</div>"
    f"<div style='color:#666699;font-size:0.8rem;margin-top:4px'>{dc['desc']}</div>"
    f"<hr style='border:none;border-top:1px solid #1e1e44;margin:8px 0'>"
    f"<div style='display:flex;justify-content:space-between;font-size:0.82rem'>"
    f"  <span style='color:#555588'>Range</span>"
    f"  <span style='color:#ffffff;font-weight:700'>{low} – {high}</span>"
    f"</div>"
    f"<div style='display:flex;justify-content:space-between;font-size:0.82rem;margin-top:4px'>"
    f"  <span style='color:#555588'>Max attempts</span>"
    f"  <span style='color:#ffffff;font-weight:700'>{attempt_limit}</span>"
    f"</div>"
    f"</div>",
    unsafe_allow_html=True,
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)
with st.sidebar.expander("🔧 Debug"):
    st.write("Secret:", st.session_state.get("secret", "—"))
    st.write("Attempts:", st.session_state.get("attempts", "—"))
    st.write("Score:", st.session_state.get("score", "—"))

# ── Session state ─────────────────────────────────────────────────────────────

if "secret" not in st.session_state:
    st.session_state.secret = random.randint(low, high)
if "attempts" not in st.session_state:
    st.session_state.attempts = 1
if "score" not in st.session_state:
    st.session_state.score = 0
if "status" not in st.session_state:
    st.session_state.status = "playing"
if "history" not in st.session_state:
    st.session_state.history = []

# ── Header ────────────────────────────────────────────────────────────────────

st.markdown("""
<div style='text-align:center;padding:1rem 0 1.4rem;animation:fadeSlideIn 0.6s ease'>
  <div style='font-size:3rem;margin-bottom:4px'>🎮</div>
  <h1 style='font-family:"Space Grotesk",sans-serif;font-size:2.8rem;font-weight:800;
     background:linear-gradient(90deg,#aa44ff,#44aaff,#ff44aa,#aa44ff);
     background-size:300% auto;
     -webkit-background-clip:text;-webkit-text-fill-color:transparent;
     animation:shimmer 4s linear infinite;margin:0;letter-spacing:-1px'>
    Glitchy Guesser
  </h1>
  <p style='color:#44446a;font-size:0.9rem;margin-top:6px;letter-spacing:1px'>
    AN AI-GENERATED GUESSING GAME · SOMETHING IS OFF
  </p>
</div>
""", unsafe_allow_html=True)

# ── Stats cards ───────────────────────────────────────────────────────────────

attempts_used = st.session_state.attempts - 1
attempts_left = attempt_limit - st.session_state.attempts
score         = st.session_state.score

left_color = "#44dd88" if attempts_left > 2 else "#ffaa22" if attempts_left > 1 else "#ff4466"

def stat_card(icon, value, label, color, glow=False):
    shadow = f"box-shadow:0 0 24px {color}44,0 2px 12px #00000066;" if glow else "box-shadow:0 2px 12px #00000066;"
    return (
        f"<div style='background:linear-gradient(145deg,#111128,#0d0d22);border-radius:16px;"
        f"padding:18px 12px;text-align:center;border:1px solid #1e1e44;"
        f"border-top:2px solid {color};{shadow}animation:fadeSlideIn 0.5s ease'>"
        f"<div style='font-size:1.8rem;margin-bottom:4px'>{icon}</div>"
        f"<div style='font-size:2rem;font-weight:800;color:{color};line-height:1'>{value}</div>"
        f"<div style='color:#44446a;font-size:0.72rem;text-transform:uppercase;"
        f"letter-spacing:1.5px;margin-top:6px;font-weight:600'>{label}</div>"
        f"</div>"
    )

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(stat_card("⭐", score, "Score", "#aa44ff", glow=True), unsafe_allow_html=True)
with c2:
    st.markdown(stat_card("💡", attempts_left, "Attempts Left", left_color), unsafe_allow_html=True)
with c3:
    st.markdown(stat_card(dc["icon"], difficulty, "Difficulty", dc["color"]), unsafe_allow_html=True)

st.markdown("<div style='height:20px'></div>", unsafe_allow_html=True)

# ── Attempt bubbles ───────────────────────────────────────────────────────────

bubbles = ""
for i in range(attempt_limit):
    if i < attempts_used:
        bubbles += f"<div style='width:28px;height:28px;border-radius:50%;background:{left_color};" \
                   f"box-shadow:0 0 8px {left_color}88;flex-shrink:0'></div>"
    else:
        bubbles += "<div style='width:28px;height:28px;border-radius:50%;background:#111128;" \
                   "border:2px solid #2a2a5a;flex-shrink:0'></div>"

st.markdown(
    f"<div style='background:#0c0c20;border-radius:14px;padding:14px 18px;"
    f"border:1px solid #1a1a38;margin-bottom:20px'>"
    f"<div style='font-size:0.7rem;color:#44446a;letter-spacing:1.5px;font-weight:600;"
    f"text-transform:uppercase;margin-bottom:10px'>Attempts Used</div>"
    f"<div style='display:flex;gap:8px;align-items:center;flex-wrap:wrap'>{bubbles}</div>"
    f"</div>",
    unsafe_allow_html=True,
)

# ── Number line (shows last guess position) ───────────────────────────────────

valid_history = [h for h in st.session_state.history if isinstance(h, dict) and "Guess" in h]

if valid_history:
    last = valid_history[-1]
    last_guess = last["Guess"]
    last_result = last["Result"]
    pct = max(0, min(100, round((last_guess - low) / max(high - low, 1) * 100)))
    marker_color = {"✅ Correct!": "#44dd88", "📈 Too High": "#ff6655", "📉 Too Low": "#44aaff"}.get(last_result, "#aaaaee")

    st.markdown(
        f"<div style='background:#0c0c20;border-radius:14px;padding:14px 18px;"
        f"border:1px solid #1a1a38;margin-bottom:20px'>"
        f"<div style='font-size:0.7rem;color:#44446a;letter-spacing:1.5px;font-weight:600;"
        f"text-transform:uppercase;margin-bottom:10px'>Last Guess: "
        f"<span style='color:{marker_color}'>{last_guess}</span></div>"
        f"<div style='position:relative;height:8px;background:#1a1a38;border-radius:99px'>"
        f"  <div style='position:absolute;left:0;top:0;height:100%;width:{pct}%;"
        f"background:linear-gradient(90deg,#3333aa,{marker_color});border-radius:99px'></div>"
        f"  <div style='position:absolute;top:-6px;left:calc({pct}% - 10px);width:20px;height:20px;"
        f"border-radius:50%;background:{marker_color};box-shadow:0 0 10px {marker_color};"
        f"border:2px solid #080818'></div>"
        f"</div>"
        f"<div style='display:flex;justify-content:space-between;margin-top:14px;"
        f"font-size:0.75rem;color:#33335a'>"
        f"  <span>{low}</span><span>{high}</span>"
        f"</div>"
        f"</div>",
        unsafe_allow_html=True,
    )

# ── Range banner + input ──────────────────────────────────────────────────────

st.markdown(
    f"<div style='text-align:center;font-size:0.85rem;color:#44446a;letter-spacing:1px;"
    f"text-transform:uppercase;margin-bottom:8px'>"
    f"Pick a number between "
    f"<span style='color:#aa44ff;font-weight:700'>{low}</span> and "
    f"<span style='color:#44aaff;font-weight:700'>{high}</span>"
    f"</div>",
    unsafe_allow_html=True,
)

raw_guess = st.text_input(
    "guess",
    placeholder=f"{low}  –  {high}",
    key=f"guess_input_{difficulty}",
    label_visibility="collapsed",
)

st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

col1, col2, col3 = st.columns([5, 4, 2])
with col1:
    submit = st.button("🚀  Submit Guess", use_container_width=True, type="primary")
with col2:
    new_game = st.button("🔁  New Game", use_container_width=True)
with col3:
    show_hint = st.checkbox("Hints", value=True)

# ── New game ──────────────────────────────────────────────────────────────────

if new_game:
    st.session_state.attempts = 1
    st.session_state.secret   = random.randint(low, high)
    st.session_state.history  = []
    st.session_state.status   = "playing"
    st.rerun()

# ── Game-over gate ────────────────────────────────────────────────────────────

if st.session_state.status != "playing":
    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    if st.session_state.status == "won":
        st.markdown(
            "<div style='background:linear-gradient(135deg,#0d2a1a,#0a3320);border-radius:18px;"
            "padding:28px;text-align:center;border:1px solid #44dd8866;"
            "box-shadow:0 0 40px #44dd8822;animation:bounce-in 0.5s ease'>"
            "<div style='font-size:3rem'>🏆</div>"
            "<div style='font-size:1.5rem;color:#44dd88;font-weight:800;margin-top:8px'>"
            "You won this round!</div>"
            "<div style='color:#557755;margin-top:8px;font-size:0.9rem'>"
            "Hit New Game to play again.</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            "<div style='background:linear-gradient(135deg,#2a0d0d,#330a1a);border-radius:18px;"
            "padding:28px;text-align:center;border:1px solid #ff446666;"
            "box-shadow:0 0 40px #ff446622;animation:bounce-in 0.5s ease'>"
            "<div style='font-size:3rem'>💀</div>"
            "<div style='font-size:1.5rem;color:#ff4466;font-weight:800;margin-top:8px'>"
            "Game Over!</div>"
            "<div style='color:#774455;margin-top:8px;font-size:0.9rem'>"
            "Hit New Game to try again.</div>"
            "</div>",
            unsafe_allow_html=True,
        )
    st.stop()

# ── Submit logic ──────────────────────────────────────────────────────────────

if submit:
    st.session_state.attempts += 1
    ok, guess_int, err = parse_guess(raw_guess)

    st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

    if not ok:
        st.session_state.history.append({"guess": raw_guess, "Result": "❌ Invalid"})
        st.markdown(
            f"<div style='background:#1a0a0a;border-radius:14px;padding:16px 20px;"
            f"border:1px solid #ff446644;animation:fadeSlideIn 0.3s ease'>"
            f"<div style='font-size:0.75rem;color:#ff4466;letter-spacing:1px;text-transform:uppercase;"
            f"font-weight:700;margin-bottom:4px'>Invalid Input</div>"
            f"<div style='font-size:1rem;color:#cc8888'>⚠️ {err}</div>"
            f"</div>",
            unsafe_allow_html=True,
        )
    else:
        outcome, message = check_guess(guess_int, st.session_state.secret)

        if outcome == "Win":
            result_display = "✅ Correct!"
            if show_hint:
                st.markdown(
                    "<div style='background:linear-gradient(135deg,#0d2a1a,#0a3320);border-radius:14px;"
                    "padding:20px 24px;border:1px solid #44dd8844;"
                    "box-shadow:0 0 30px #44dd8822;animation:bounce-in 0.4s ease'>"
                    "<div style='font-size:2.5rem;text-align:center'>🎉</div>"
                    "<div style='font-size:1.3rem;font-weight:800;color:#44dd88;text-align:center;"
                    "margin-top:6px'>Correct! You nailed it!</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )
        elif outcome == "Too High":
            result_display = "📈 Too High"
            if show_hint:
                st.markdown(
                    "<div style='background:#180808;border-radius:14px;padding:20px 24px;"
                    "border:1px solid #ff665544;animation:fadeSlideIn 0.3s ease'>"
                    "<div style='display:flex;align-items:center;gap:14px'>"
                    "  <div style='font-size:2.8rem'>📈</div>"
                    "  <div>"
                    "    <div style='font-size:1.15rem;font-weight:800;color:#ff6655'>Too High!</div>"
                    "    <div style='color:#774444;font-size:0.85rem;margin-top:2px'>Go lower →</div>"
                    "  </div>"
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )
        else:
            result_display = "📉 Too Low"
            if show_hint:
                st.markdown(
                    "<div style='background:#08101a;border-radius:14px;padding:20px 24px;"
                    "border:1px solid #44aaff44;animation:fadeSlideIn 0.3s ease'>"
                    "<div style='display:flex;align-items:center;gap:14px'>"
                    "  <div style='font-size:2.8rem'>📉</div>"
                    "  <div>"
                    "    <div style='font-size:1.15rem;font-weight:800;color:#44aaff'>Too Low!</div>"
                    "    <div style='color:#335566;font-size:0.85rem;margin-top:2px'>Go higher →</div>"
                    "  </div>"
                    "</div>"
                    "</div>",
                    unsafe_allow_html=True,
                )

        st.session_state.history.append({
            "Attempt": len(st.session_state.history) + 1,
            "Guess":   guess_int,
            "Result":  result_display,
        })

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
            st.markdown(
                f"<div style='background:linear-gradient(135deg,#0d2a1a,#0a3320);border-radius:18px;"
                f"padding:28px;text-align:center;border:1px solid #44dd8866;"
                f"box-shadow:0 0 40px #44dd8822;margin-top:16px;animation:bounce-in 0.5s ease'>"
                f"<div style='font-size:3rem'>🏆</div>"
                f"<div style='font-size:1.5rem;color:#44dd88;font-weight:800;margin-top:8px'>You cracked it!</div>"
                f"<div style='color:#557755;margin-top:8px'>The secret number was "
                f"<span style='color:#aa44ff;font-size:1.3rem;font-weight:800'>{st.session_state.secret}</span></div>"
                f"<div style='margin-top:12px;display:inline-block;background:#0a2016;"
                f"border-radius:99px;padding:6px 20px;border:1px solid #44dd8833'>"
                f"<span style='color:#ffaa22;font-size:1.1rem;font-weight:700'>⭐ {st.session_state.score} pts</span>"
                f"</div></div>",
                unsafe_allow_html=True,
            )
        elif st.session_state.attempts >= attempt_limit:
            st.session_state.status = "lost"
            st.markdown(
                f"<div style='background:linear-gradient(135deg,#2a0d0d,#330a1a);border-radius:18px;"
                f"padding:28px;text-align:center;border:1px solid #ff446666;"
                f"box-shadow:0 0 40px #ff446622;margin-top:16px;animation:bounce-in 0.5s ease'>"
                f"<div style='font-size:3rem'>💀</div>"
                f"<div style='font-size:1.5rem;color:#ff4466;font-weight:800;margin-top:8px'>Out of attempts!</div>"
                f"<div style='color:#774455;margin-top:8px'>The secret was "
                f"<span style='color:#aa44ff;font-size:1.3rem;font-weight:800'>{st.session_state.secret}</span></div>"
                f"<div style='margin-top:12px;display:inline-block;background:#1a0810;"
                f"border-radius:99px;padding:6px 20px;border:1px solid #ff446633'>"
                f"<span style='color:#ffaa22;font-size:1.1rem;font-weight:700'>⭐ {st.session_state.score} pts</span>"
                f"</div></div>",
                unsafe_allow_html=True,
            )

# ── Guess history (timeline) ──────────────────────────────────────────────────

valid_history = [h for h in st.session_state.history if isinstance(h, dict) and "Guess" in h]

if valid_history:
    st.markdown(
        "<div style='margin:32px 0 12px;font-size:0.7rem;color:#44446a;"
        "letter-spacing:2px;font-weight:700;text-transform:uppercase'>📋 Guess History</div>",
        unsafe_allow_html=True,
    )

    RESULT_CFG = {
        "✅ Correct!": {"color": "#44dd88", "bg": "#0d2a1a", "border": "#44dd8844", "dot": "#44dd88"},
        "📈 Too High": {"color": "#ff6655", "bg": "#1a0a08", "border": "#ff665533", "dot": "#ff6655"},
        "📉 Too Low":  {"color": "#44aaff", "bg": "#08101a", "border": "#44aaff33", "dot": "#44aaff"},
    }

    items = ""
    for h in reversed(valid_history):
        cfg = RESULT_CFG.get(h["Result"], {"color": "#888", "bg": "#111", "border": "#33333344", "dot": "#888"})
        is_latest = h == valid_history[-1]
        ring = f"box-shadow:0 0 0 3px {cfg['dot']}33,0 0 12px {cfg['dot']}44;" if is_latest else ""
        items += (
            f"<div style='display:flex;align-items:center;gap:14px;padding:12px 16px;"
            f"background:{cfg['bg']};border-radius:12px;border:1px solid {cfg['border']};"
            f"margin-bottom:6px;animation:fadeSlideIn 0.3s ease;{ring}'>"
            f"  <div style='width:36px;height:36px;border-radius:50%;background:#0d0d1a;"
            f"border:2px solid {cfg['dot']};display:flex;align-items:center;justify-content:center;"
            f"font-size:0.75rem;font-weight:800;color:{cfg['dot']};flex-shrink:0'>{h['Attempt']}</div>"
            f"  <div style='font-size:1.5rem;font-weight:800;color:#ffffff;min-width:48px'>{h['Guess']}</div>"
            f"  <div style='font-size:0.9rem;font-weight:700;color:{cfg['color']}'>{h['Result']}</div>"
            f"</div>"
        )

    st.markdown(items, unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────

st.markdown(
    "<div style='text-align:center;color:#22223a;font-size:0.72rem;margin-top:40px;"
    "letter-spacing:1px'>BUILT BY AN AI THAT CLAIMS THIS IS PRODUCTION-READY</div>",
    unsafe_allow_html=True,
)
