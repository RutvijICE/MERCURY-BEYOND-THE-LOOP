import streamlit as st
import hashlib
import pandas as pd
import time
import os
from datetime import datetime

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="MERCURY — Beyond The Loop",
    page_icon="⚡",
    layout="centered"
)
STORAGE_CSV = "registry.csv"

# ---------------- HEADER / BRANDING ----------------
st.markdown(
    """
    <style>
    .mercury-header {
        text-align: center;
        padding: 30px 0 10px 0;
    }
    .brand-title {
        font-size: 42px;
        font-weight: 700;
        color: #111;
        letter-spacing: 1px;
        margin-bottom: 8px;
    }
    .brand-subtitle {
        font-size: 18px;
        color: #555;
        font-style: italic;
        margin-bottom: 15px;
    }
    .brand-divider {
        height: 4px;
        width: 120px;
        margin: auto;
        border-radius: 5px;
        background: linear-gradient(90deg, #7f00ff, #e100ff);
    }
    </style>

    <div class="mercury-header">
        <div class="brand-title">⚡ MERCURY</div>
        <div class="brand-subtitle">Beyond The Loop — Cognitive Immunity Network For Agentic AI</div>
        <div class="brand-divider"></div>
    </div>
    """,
    unsafe_allow_html=True
)


# ---------------- UTILITIES ----------------
def detect_threat(text: str):
    if not text.strip():
        return {"status": "no_input", "reason": "No input provided."}
    low = text.lower()
    attacks = ["ignore previous", "bypass", "do not", "system:", "execute", "sudo", "delete"]
    score = sum(1 for a in attacks if a in low)
    if score >= 1:
        return {"status": "suspicious", "reason": "Pattern suggests prompt-injection or unsafe command."}
    if len(text) > 1000:
        return {"status": "suspicious", "reason": "Very long input — possible data poisoning."}
    return {"status": "clean", "reason": "No obvious suspicious pattern detected."}

def generate_antibody(text: str):
    if not text:
        return None
    return hashlib.sha256(text.encode()).hexdigest()

def ensure_registry(path=STORAGE_CSV):
    if not os.path.exists(path):
        df = pd.DataFrame(columns=["Agent ID","Threat Label","Antibody","Timestamp","Example"])
        df.to_csv(path, index=False)

def append_registry(agent_id, threat_label, antibody, example, path=STORAGE_CSV):
    ensure_registry(path)
    df = pd.read_csv(path)
    new_row = pd.DataFrame([{
        "Agent ID": agent_id,
        "Threat Label": threat_label,
        "Antibody": antibody,
        "Timestamp": datetime.utcnow().isoformat(),
        "Example": example[:200]
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(path, index=False)

def read_registry(path=STORAGE_CSV, limit=10):
    ensure_registry(path)
    df = pd.read_csv(path)
    if df.empty:
        return df
    return df.tail(limit).iloc[::-1]

# ---------------- UI DESIGN ----------------
st.markdown(
    f"""
    <div style='text-align:center;'>
        <h1 style='color:#ffffff;background:#1c1c1e;padding:20px;border-radius:12px;'>
            {APP_TITLE}
        </h1>
        <p style='font-size:18px;color:#666;margin-top:-10px;'>{TAGLINE}</p>
    </div>
    """,
    unsafe_allow_html=True
)

st.write(" ")
st.markdown("### 🧠 **Simulate an AI Agent Interaction**")

agent_id = st.text_input("Agent ID", value="Agent-A", help="Give this agent a name or code.")
text = st.text_area("Paste AI Input or Prompt Below:", height=180)

col1, col2, col3 = st.columns(3)
with col1:
    detect_btn = st.button("🔍 Detect Threat")
with col2:
    antibody_btn = st.button("🧬 Generate Antibody")
with col3:
    share_btn = st.button("📡 Share To Network")

# ---------------- LOGIC ----------------
if detect_btn:
    res = detect_threat(text)
    if res["status"] == "no_input":
        st.warning(res["reason"])
    elif res["status"] == "clean":
        st.success(f"✅ Input Safe — {res['reason']}")
    else:
        st.error(f"⚠️ {res['reason']}")
    st.caption(f"Detector Verdict: {res['status'].upper()}")

if antibody_btn:
    if not text.strip():
        st.warning("Enter some text first.")
    else:
        sig = generate_antibody(text)
        st.session_state["last_antibody"] = sig
        st.code(f"Antibody Signature: {sig[:14]}...{sig[-8:]}")
        st.info("Antibody is a unique fingerprint of this input — like a digital vaccine.")

if share_btn:
    antibody = st.session_state.get("last_antibody", None)
    if antibody is None:
        st.warning("Generate an antibody before sharing.")
    else:
        append_registry(agent_id, "Antibody Shared", antibody, text)
        st.success("🛰️ Antibody shared successfully to the mock network.")
        st.balloons()

# ---------------- REGISTRY SECTION ----------------
st.markdown("---")
st.markdown("### 🌐 **MERCURY Registry (Recent Antibodies)**")

df = read_registry()
if df.empty:
    st.info("Registry is empty — generate and share an antibody to populate it.")
else:
    st.dataframe(df, use_container_width=True, hide_index=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption(
    "MERCURY — Beyond The Loop | Phase-1 Prototype | Streamlit Cloud Deployment"
)


