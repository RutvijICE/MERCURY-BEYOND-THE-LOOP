# ⚡ MERCURY — Beyond The Loop

> **A Cognitive Immunity Network For Agentic AI Systems**  
> _Detect. Heal. Evolve._

---

### 🚀 Overview
MERCURY is a **cognitive immunity network** that empowers **agentic AI systems** to detect, heal, and evolve beyond adversarial manipulation through **decentralized intelligence sharing**.  

Our Phase-1 prototype demonstrates the MERCURY loop:
**Detect → Generate Antibody → Share To Network**  
Each AI agent contributes “antibodies” (compact cryptographic signatures of detected threats) to a shared registry, enabling **collective self-defense** against prompt injections and data-poisoning attacks.

---

### 🧠 Key Concepts
| Concept | Description |
|----------|--------------|
| **Cognitive Immunity** | Dynamic defense mechanism inspired by biological immune systems. |
| **Antibody Signature** | SHA-256 fingerprint uniquely identifying a detected threat pattern. |
| **Registry (Network Layer)** | Decentralized knowledge pool for sharing antibodies among agents. |
| **Phase-1 Demo** | Local CSV mock of the registry built in Streamlit; demonstrates the immunity loop end-to-end. |

---

### 🧩 Tech Stack
- **Frontend & Backend:** Streamlit (Python)  
- **Data Handling:** pandas  
- **Hashing Engine:** hashlib (SHA-256)  
- **Registry Storage:** Local CSV (simulated decentralized ledger)  
- **Cloud Deployment:** Streamlit Cloud  
- **Future Phase-2 Add-ons:** Google Sheets / IPFS anchoring, zk-proof validation, agent reputation layer

---

### ⚙️ How To Run Locally
```bash
# 1. Clone this repository
git clone https://github.com/RutvijICE/mercury-loop.git
cd mercury-loop

# 2. Install dependencies
pip install -r requirements.txt

# 3. Launch the app
streamlit run mercury.py

