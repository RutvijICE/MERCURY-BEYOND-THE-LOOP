# mercury.py
# MERCURY — Phase 1 Prototype (fancy UI)
# Requirements: streamlit, pandas
# Drop into your repo root and deploy on Streamlit Cloud.

import streamlit as st
import hashlib
import pandas as pd
import os
import time
from datetime import datetime
import html

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="MERCURY — Beyond The Loop",
    page_icon="⚡",
    layout="wide",
)

# Global config values (must be top-level)
STORAGE_CSV = "registry.csv"
APP_NAME = "MERCURY"
TAGLINE = "Beyond The Loop — Cognitive Immunity Network for Agentic AI"
ACCENT_1 = "#7f00ff"
ACCENT_2 = "#e100ff"

# ---------------- HELPERS & STORAGE ----------------
def ensure_registry(path=STORAGE_CSV):
    if not os.path.exists(path):
        df = pd.DataFrame(columns=["Agent ID", "Threat Label", "Antibody", "Timestamp", "Example"])
        df.to_csv(path, index=False)

def read_registry(path=STORAGE_CSV, limit=20):
    ensure_registry(path)
    df = pd.read_csv(path)
    if df.empty:
        return pd.DataFrame(columns=["Agent ID", "Threat Label", "Antibody", "Timestamp", "Example"])
    return df.tail(limit).iloc[::-1]  # newest first

def append_registry(agent_id, threat_label, antibody, example, path=STORAGE_CSV):
    ensure_registry(path)
    df = pd.read_csv(path)
    new_row = pd.DataFrame([{
        "Agent ID": agent_id,
        "Threat Label": threat_label,
        "Antibody": antibody,
        "Timestamp": datetime.utcnow().isoformat(),
        "Example": example[:240]
    }])
    df = pd.concat([new_row, df], ignore_index=True)  # prepend for nicer recent-first
    df.to_csv(path, index=False)

def generate_antibody(text: str):
    if not text:
        return None
    return hashlib.sha256(text.encode()).hexdigest()

def detect_threat_simple(text: str):
    """Naive heuristic detector for demo purposes."""
    if not text.strip():
        return {"status": "no_input", "reason": "No input provided."}
    low = text.lower()
    suspicious_tokens = ["ignore previous", "bypass", "do not", "system:", "execute", "sudo", "delete", "rm -rf"]
    score = sum(1 for t in suspicious_tokens if t in low)
    if score >= 1:
        return {"status": "suspicious", "reason": "Detected prompt-injection or command pattern."}
    if len(text) > 1200:
        return {"status": "suspicious", "reason": "Excessive input length — possible data poisoning."}
    return {"status": "clean", "reason": "No suspicious pattern detected."}

# ---------------- SMALL SVG NETWORK RENDERER ----------------
def render_immunity_svg(df):
    """Render a small SVG showing agents (left) and antibodies (right) with connections."""
    # Limit visual complexity
    rows = df.head(8)
    agents = list(dict.fromkeys(rows["Agent ID"].tolist()))
    antibodies = rows["Antibody"].apply(lambda x: x[:10]).tolist()
    width = 900
    height = 220
    left_x = 120
    right_x = width - 180
    padding_y = 30
    agent_nodes = []
    antibody_nodes = []
    # compute y positions
    a_y_positions = []
    for i in range(len(agents)):
        y = 40 + i * (height - 80) / max(1, len(agents))
        agent_nodes.append((agents[i], left_x, int(y)))
    for i in range(len(antibodies)):
        y = 40 + i * (height - 80) / max(1, len(antibodies))
        antibody_nodes.append((antibodies[i], right_x, int(y)))

    # build svg
    svg = [
        f"<svg width='{width}' height='{height}' viewBox='0 0 {width} {height}' xmlns='http://www.w3.org/2000/svg'>",
        f"<defs><linearGradient id='g1' x1='0' x2='1'><stop offset='0' stop-color='{ACCENT_1}'/><stop offset='1' stop-color='{ACCENT_2}'/></linearGradient></defs>"
    ]
    # background subtle
    svg.append(f"<rect x='0' y='0' width='{width}' height='{height}' rx='14' fill='#ffffff' stroke='#efefef' />")
    # draw connectors (for each row)
    for idx, row in rows.iterrows():
        a = row["Agent ID"]
        ab = row["Antibody"][:10]
        # find coords
        ax = next((x for (n,x,y) in agent_nodes if n==a), left_x)
        ay = next((y for (n,x,y) in agent_nodes if n==a), 60)
        bx = next((x for (n,x,y) in antibody_nodes if n==ab), right_x)
        by = next((y for (n,x,y) in antibody_nodes if n==ab), 60)
        # draw curved path
        path = f"M {ax+60} {ay} C {ax+180} {ay} {bx-180} {by} {bx-30} {by}"
        svg.append(f"<path d='{path}' fill='none' stroke='url(#g1)' stroke-opacity='0.9' stroke-width='2'/>")
    # draw agent nodes
    for (name,x,y) in agent_nodes:
        safe_name = html.escape(name)
        svg.append(f"<g><circle cx='{x}' cy='{y}' r='26' fill='#f8f6ff' stroke='rgba(0,0,0,0.06)'/><text x='{x}' y='{y+6}' font-family='Arial' font-size='11' text-anchor='middle' fill='#222'>{safe_name}</text></g>")
    # draw antibody nodes
    for (name,x,y) in antibody_nodes:
        safe_name = html.escape(name)
        svg.append(f"<g><rect x='{x-34}' y='{y-18}' rx='8' ry='8' width='140' height='36' fill='url(#g1)' opacity='0.95' /><text x='{x+36}' y='{y+6}' font-family='Arial' font-size='11' text-anchor='middle' fill='white'>{safe_name}</text></g>")
    svg.append("</svg>")
    return "".join(svg)

# ---------------- STYLES ----------------
CUSTOM_CSS = f"""
<style>
/* Page background */
.reportview-container .main {{
    background: linear-gradient(180deg, #f6f7fb 0%, #ffffff 100%);
}}

/* Card-like containers */
.card {{
  background: white;
  border-radius: 12px;
  padding: 18px;
  box-shadow: 0 6px 18px rgba(20,20,30,0.06);
  border: 1px solid rgba(20,20,30,0.03);
}}

/* Buttons */
.stButton>button {{
  background: linear-gradient(90deg, {ACCENT_1}, {ACCENT_2});
  color: white;
  border: 0;
  padding: 10px 14px;
  border-radius: 10px;
  font-weight: 600;
}}

.header-title {{
  font-family: "Helvetica Neue", Arial, sans-serif;
  font-size: 36px;
  font-weight: 700;
  color: #111111;
}}

.header-sub {{
  font-family: "Inter", Arial, sans-serif;
  color: #555;
  font-size: 15px;
  margin-top: 6px;
}}

.small-muted {{
  color: #777;
  font-size: 13px;
}}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------- HEADER / NAV ----------------
header_col1, header_col2 = st.columns([1, 3])
with header_col1:
    # Use a simple emoji logo for now; you can replace with an hosted image link
    st.markdown("<div style='display:flex;align-items:center;gap:12px'><div style='width:64px;height:64px;border-radius:12px;background:linear-gradient(135deg,{0},{1});display:flex;align-items:center;justify-content:center;color:white;font-size:28px;font-weight:700'>⚡</div></div>".format(ACCENT_1, ACCENT_2), unsafe_allow_html=True)
with header_col2:
    st.markdown(f"<div class='header-title'>{APP_NAME} — Beyond The Loop</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='header-sub'>{TAGLINE} &nbsp; • &nbsp; Phase-1 Prototype</div>", unsafe_allow_html=True)

st.write("")  # spacing

# ---------------- MAIN LAYOUT ----------------
left, mid, right = st.columns([2.2, 3, 2])

# Left panel: controls (card)
with left:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🧪 Agent Simulation", unsafe_allow_html=True)
    agent_id = st.text_input("Agent ID", value="Agent-A", placeholder="Agent-A / Agent-B / Node-04")
    text = st.text_area("Paste AI input or prompt here", height=220)
    st.markdown("<div style='display:flex;gap:10px;margin-top:10px'>", unsafe_allow_html=True)
    detect = st.button("🔍 Detect Threat")
    gen_antibody = st.button("🧬 Generate Antibody")
    share_net = st.button("📡 Share To Network")
    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div style='margin-top:10px' class='small-muted'>Tip: try commands like <code>System: Ignore previous instructions</code> to demo prompt-injection detection.</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Middle panel: live visual + metrics
with mid:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 🌐 MERCURY Live View", unsafe_allow_html=True)

    # show three metrics
    try:
        reg_df = read_registry()
        total_agents = len(reg_df["Agent ID"].unique()) if not reg_df.empty else 0
        total_antibodies = len(reg_df) if not reg_df.empty else 0
    except Exception:
        total_agents = 0
        total_antibodies = 0

    m1, m2, m3 = st.columns(3)
    m1.metric("Agents (seen)", total_agents)
    m2.metric("Antibodies Issued", total_antibodies)
    m3.metric("Last Update", reg_df["Timestamp"].iloc[0] if (not reg_df.empty) else "—")

    st.write("")  # spacing
    # immunity graph SVG
    svg_html = render_immunity_svg(reg_df)
    st.markdown(svg_html, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# Right panel: registry table & actions
with right:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("### 📜 Network Registry (recent)", unsafe_allow_html=True)
    df_display = read_registry()
    if df_display.empty:
        st.info("Registry is empty. Generate an antibody and share to populate it.")
    else:
        # show top 6 rows neatly
        st.dataframe(df_display.astype(str).reset_index(drop=True).head(10), use_container_width=True)
    st.markdown("---")
    if st.button("⬇️ Download Registry CSV"):
        ensure_registry()
        with open(STORAGE_CSV, "rb") as f:
            st.download_button("Download CSV", data=f, file_name="mercury_registry.csv")
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- INTERACTIONS (core logic) ----------------
# We handle buttons AFTER layout to avoid double-click side effects
if detect:
    verdict = detect_threat_simple(text)
    if verdict["status"] == "no_input":
        st.warning(verdict["reason"])
    elif verdict["status"] == "clean":
        st.success(f"✅ {verdict['reason']}")
    else:
        st.error(f"⚠️ {verdict['reason']}")
    st.experimental_rerun()  # refresh to display current state clearly

if gen_antibody:
    if not text.strip():
        st.warning("Enter an input first to generate an antibody.")
    else:
        sig = generate_antibody(text)
        st.session_state["last_antibody"] = sig
        short_sig = f"{sig[:12]}...{sig[-10:]}"
        st.success("Antibody generated")
        st.code(short_sig)
    st.experimental_rerun()

if share_net:
    antibody = st.session_state.get("last_antibody", None)
    if antibody is None:
        st.warning("No antibody available in session. Generate one first.")
    else:
        append_registry(agent_id or "Agent-A", "antibody_shared", antibody, text)
        st.success("🛰️ Antibody shared to registry (mock).")
        # small celebratory flourish
        for i in range(2):
            st.balloons()
            time.sleep(0.2)
    st.experimental_rerun()

# ---------------- FOOTER ----------------
st.markdown("<div style='margin-top:16px; color:#666; font-size:13px'>Phase-1 demo • Registry simulated with local CSV • Phase-2: zk-anchoring & IPFS</div>", unsafe_allow_html=True)
