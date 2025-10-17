# mercury.py
import streamlit as st
import hashlib
import pandas as pd
import time
import os
from datetime import datetime

# ---------- CONFIG ----------
STORAGE_CSV = "registry.csv"
APP_TITLE = "MERCURY — Cognitive Immunity Network"
TAGLINE = "Self-defending intelligence for agentic AI."

# ---------- UTILS ----------
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
    full = hashlib.sha256(text.encode()).hexdigest()
    return full

def ensure_registry(path=STORAGE_CSV):
    if not os.path.exists(path):
        df = pd.DataFrame(columns=["agent_id","threat_label","antibody","timestamp","example"])
        df.to_csv(path, index=False)

def append_registry(agent_id, threat_label, antibody, example, path=STORAGE_CSV):
    ensure_registry(path)
    df = pd.read_csv(path)
    new_row = pd.DataFrame([{
        "agent_id": agent_id,
        "threat_label": threat_label,
        "antibody": antibody,
        "timestamp": datetime.utcnow().isoformat(),
        "example": example[:300]
    }])
    df = pd.concat([df, new_row], ignore_index=True)
    df.to_csv(path, index=False)


def read_registry(path=STORAGE_CSV, limit=10):
    ensure_registry(path)
    df = pd.read_csv(path)
    if df.empty:
        return df
    return df.tail(limit).iloc[::-1]

# ---------- UI ----------
st.set_page_config(page_title="MERCURY", layout="wide")
st.title(APP_TITLE)
st.markdown(f"**{TAGLINE}**")
st.write("---")

left, right = st.columns([2,3])
with left:
    st.subheader("Agent Simulation")
    agent_id = st.text_input("Agent ID", value="Agent-A")
    text = st.text_area("Paste AI input or prompt here", height=200)

    if st.button("Detect Threat"):
        res = detect_threat(text)
        if res["status"] == "no_input":
            st.warning(res["reason"])
        elif res["status"] == "clean":
            st.success("✅ Input Safe — " + res["reason"])
        else:
            st.error("⚠️ " + res["reason"])
        st.write("**Detector verdict:**", res["status"])

    if st.button("Generate Antibody"):
        if not text.strip():
            st.warning("Enter some input first to generate antibody.")
        else:
            sig = generate_antibody(text)
            short = sig[:12] + "..." + sig[-6:]
            st.code(f"Antibody Signature: {short}")
            st.info("This signature is a compact fingerprint of the suspicious input.")
            st.session_state["last_antibody"] = sig

    if st.button("Share To Network"):
        antibody = st.session_state.get("last_antibody", None)
        if antibody is None:
            st.warning("No antibody in session. Generate one first.")
        else:
            append_registry(agent_id, "antibody_shared", antibody, text)
            st.success("🛰️ Antibody shared to registry (mock).")
            st.balloons()
            time.sleep(0.8)

with right:
    st.subheader("Network Registry (Recent)")
    df = read_registry()
    if df.empty:
        st.info("Registry empty. Generate and share an antibody to populate it.")
    else:
        st.table(df)

    st.write("---")
    st.subheader("How the Loop Works (Quick)")
    st.markdown("""
    1. **Detect** suspicious input (prompt injection, data poisoning patterns).  
    2. **Generate Antibody** — deterministic hash signature of the threat.  
    3. **Share** the antibody to the registry so peers can consume and avoid the same attack.  
    4. **Agents update** (simulated) — collective immunity emerges.
    """)
    st.write("---")
    st.caption("Phase-1 demo (mock). Phase-2: zk-anchoring, validator attestations, and decentralized storage.")

st.write("---")
if st.button("Download registry (CSV)"):
    ensure_registry()
    with open(STORAGE_CSV, "rb") as f:
        st.download_button("Download CSV", data=f, file_name="mercury_registry.csv")



