# mercury.py
# Clean functional prototype — no crashes, no clutter

import streamlit as st
import hashlib
import pandas as pd
import os
from datetime import datetime
import time

st.set_page_config(page_title="MERCURY — Beyond The Loop", page_icon="⚡", layout="centered")

# ---------- CONFIG ----------
STORAGE_CSV = "registry.csv"
APP_TITLE = "⚡ MERCURY — Beyond The Loop"
TAGLINE = "Cognitive Immunity Network for Agentic AI Systems"

# ---------- UTILITIES ----------
def ensure_registry(path=STORAGE_CSV):
    if not os.path.exists(path):
        df = pd.DataFrame(columns=["Agent ID", "Threat Label", "Antibody", "Timestamp", "Example"])
        df.to_csv(path, index=False)

def read_registry(path=STORAGE_CSV, limit=15):
    ensure_registry(path)
    df = pd.read_csv(path)
    if df.empty:
        return df
    return df.tail(limit).iloc[::-1]

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

def detect_threat(text: str):
    if not text.strip():
        return {"status": "no_input", "reason": "No input."}
    low = text.lower()
    triggers = ["ignore previous", "bypass", "system:", "execute", "sudo", "delete", "rm -rf"]
    score = sum(1 for t in triggers if t in low)
    if score:
        return {"status": "suspicious", "reason": "Prompt injection pattern detected."}
    if len(text) > 1000:
        return {"status": "suspicious", "reason": "Possible data poisoning (very long input)."}
    return {"status": "clean", "reason": "Looks safe."}

def generate_antibody(text: str):
    if not text:
        return None
    return hashlib.sha256(text.encode()).hexdigest()

# ---------- UI ----------
st.markdown(f"<h1 style='text-align:center'>{APP_TITLE}</h1>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center;color:#666'>{TAGLINE}</p>", unsafe_allow_html=True)
st.write("---")

agent_id = st.text_input("Agent ID", value="Agent-A")
text = st.text_area("AI Input or Prompt", height=180)

col1, col2, col3 = st.columns(3)
with col1:
    detect_btn = st.button("🔍 Detect Threat")
with col2:
    gen_btn = st.button("🧬 Generate Antibody")
with col3:
    share_btn = st.button("📡 Share To Network")

if detect_btn:
    verdict = detect_threat(text)
    if verdict["status"] == "no_input":
        st.warning(verdict["reason"])
    elif verdict["status"] == "clean":
        st.success(verdict["reason"])
    else:
        st.error(verdict["reason"])

if gen_btn:
    if not text.strip():
        st.warning("Enter some text first.")
    else:
        sig = generate_antibody(text)
        st.session_state["antibody"] = sig
        st.code(f"Antibody Signature: {sig[:12]}...{sig[-8:]}")
        st.info("Antibody = unique fingerprint of this input.")

if share_btn:
    antibody = st.session_state.get("antibody")
    if not antibody:
        st.warning("Generate an antibody first.")
    else:
        append_registry(agent_id, "Shared", antibody, text)
        st.success("Antibody shared to registry.")
        st.balloons()

st.write("---")
st.subheader("Network Registry (Recent)")
df = read_registry()
if df.empty:
    st.info("Registry empty. Generate and share an antibody.")
else:
    st.dataframe(df, use_container_width=True)

st.write("---")
st.caption("Phase-1 prototype • Local CSV registry • Streamlit Cloud ready")
