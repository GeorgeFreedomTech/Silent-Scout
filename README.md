# Silent-Scout

### **By George Freedom**
Silent Scout is a low-profile, passive WiFi reconnaissance system designed for **Digital Resilience and Field Situational Awareness**.

Born from a philosophy of Tactical Minimalism, it rejects "fragile efficiency" and automated cloud dependencies. Instead, it focuses on a decoupled "Agent-HQ" architecture: an expendable, disconnected field sensor (Agent) and a centralized analytical dashboard (HQ).

This project is a practical application of **Cyber-EDC** principles—building tools that are simple, transparent, and resilient by design.

Full Story:

### ⚙️ Core System Capabilities:
The system is engineered to demonstrate high-stakes data principles: maximizing intelligence while minimizing the digital attack surface.

* **Passive Edge Reconnaissance (Agent):** Deploys a zero-footprint sniffer using MicroPython on ESP32. It operates in "Dead Metal" mode—performing rapid 802.11 signal captures without network association or credential storage, ensuring the hardware is tactically expendable.

* **Air-Gapped Data Pipeline (ETL):** Implements a deliberate "Manual Ingest" workflow. By eliminating automated cloud syncing (Flask/REST), the system removes the most common remote vulnerability point, ensuring a secure, physical chain of custody for all field data.

* **Tactical Intelligence Engine (HQ):** A sophisticated post-processing layer in Python. It performs vendor identification (OUI mapping), security risk assessment, and automated threat tagging (CCTV, Mobile Hotspots, Stealth SSIDs).

* **High-Performance Visual Recon:** An interactive Streamlit dashboard utilizing a Single-load RAM Cache Strategy. This moves the entire SQLite vault into memory upon launch, providing instantaneous data exploration and signal distribution analysis.

* **RSSI Proximity Grading:** Translates raw decibel values into actionable distance estimations (Near/Medium/Far), allowing operators to visually prioritize targets based on physical proximity.

* **Decoupled Architecture:** Strictly separates the Sensing (Field) from the Intelligence (Base). This separation of concerns ensures that a compromise in the field does not lead to a compromise of the central infrastructure.

---

## 🚀 Key Features
* **Passive Reconnaissance:** Sniffs 802.11 beacon frames without network association—leaving zero digital footprint.

* **Expendable Hardware:** Optimized for $5 ESP32 microcontrollers. If the hardware is lost, your home network credentials remain secure.

* **Separation of Concerns:** Sensing happens in the field; Intelligence happens at HQ. No "smart" automation—total manual control.

* **Field-Tested Architecture:** Built to be wrapped in heat-shrink, powered by a Li-Po, and operated via a single tactile button.

* **Tactical Analytics:** HQ Dashboard identifies surveillance infrastructure (CCTV), mobile hotspots, and hidden networks using a single-load RAM cache strategy.

---

## 🏗️ Project Architecture
The system follows a decoupled architecture. The Agent is optimized for reliability and power efficiency in the field, while the HQ is designed for deep data exploration and tactical decision-making.

### System Diagram

```mermaid
graph TD;
    subgraph "FIELD UNIT (scout-agent)"
        HW[ESP32 Hardware] --> MP[MicroPython Core]
        MP -- "Passive Sniffing" --> HW
        MP -- "Logging" --> SD[Local CSV Vault]
    end

    SD -- "Manual Data Transfer" --> PC[Operator Workstation]

    subgraph "COMMAND CENTER (scout-hq)"
        PC --> Ingest[ingest.py ETL]
        Ingest -- "Batch Insert" --> DB[(SQLite Database)]
        
        subgraph "Memory Intelligence Layer"
            DB -- "load_database()" --> Cache[Master DataFrame /RAM/]
            Cache -- "Pandas Filtering" --> UI[app.py Orchestrator]
        end
        
        subgraph "Analysis Modules"
            UI --> Analyser[analyser.py]
            UI --> Viz[visualizer.py]
        end
    end

    %% User Interaction
    UI -- "Instant Rendering" --> User[User Browser]
    Analyser -- "Threat Tags & OUI" --> UI
    Viz -- "Plotly Components" --> UI
```

## File Structure

```
silent-scout/
│
├── scout-agent/                # 🛰️ Field Unit Firmware (MicroPython)
│   ├── main.py                 # Agent entry point & operation loop
│   └── scout/                  # Core Agent package
│       ├── __init__.py         # Module exposure
│       ├── hardware.py         # LED, Button, and Radio drivers
│       └── logic.py            # Scanning and CSV logging logic
│
├── scout-hq/                   # 📡 Command Center (Streamlit)
│   ├── app.py                  # Dashboard Orchestrator
│   ├── config.py               # Global paths and project identity
│   ├── ingest.py               # ETL: CSV to SQLite transfer
│   ├── assets/                 # UI Styling (Custom CSS)
│   ├── data/                   # Storage (Database & Static JSONs)
│   └── modules/                # Analytical & Visual components
│       ├── __init__.py
│       ├── db_manager.py       # SQLite operations & indexing
│       ├── analyser.py         # Tactical analysis & OUI lookup
│       └── visualizer.py       # UI rendering & Plotly charts
│
└── README.md                   # This file
```

## 💡 Development Philosophy & AI Collaboration
This project was built using a **"Human-Architect, AI-Builder"** methodology.

The process involved:

* **Human-led Strategy:** Defining the tactical scope (WiFi reconnaissance), hardware-software split, and the "Silent Scout" brand identity. Establishing the data schema for cross-platform compatibility.

* **AI-assisted Engineering:** Using AI to optimize the ESP32's non-blocking hardware loops and refactor the HQ modules for professional Python standards (Type Hints, Row Factory, Indexing).

* **AI-augmented Analysis:** Leveraging AI to generate extensive OUI vendor databases and prototype complex Plotly visualizations for the RF channel occupation charts.

## ⚙️ Setup and running
Unlike standard web apps, **Silent Scout** requires a coordinated setup between hardware and software.

**Phase 1: Environment & Repository**
Before deploying to hardware, prepare your local workstation:
1.1. Clone the Repository:
```bash
git clone https://github.com/GeorgeFreedomTech/silent-scout.git
cd silent-scout
```

1.2. Set Up Python Environment:
```bash
python -m venv venv
    # On Windows: venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate

pip install -r requirements.txt
```

**Phase 2: Field Unit Deployment (Agent)**
Deploy the reconnaissance firmware to your ESP32:

* **Hardware:** Any ESP32 development board.

* **Firmware:** Ensure MicroPython (v1.20+) is flashed to the device.

* **Upload:** Use Thonny or mpremote to upload the entire contents of the scout-agent/ folder to the ESP32 root.

* **Operation:** Power the device. Use the onboard BOOT button to trigger a scan. Results are logged to scout_vault.csv on the device's flash memory.

**Phase 3: Intelligence Processing (HQ)**

3. **Data Ingest:**
Transfer and analyze the captured data:

3.1. Data Ingest: Copy csv from the ESP32 to scout-hq/data/inbox/ and run the ETL script:
```bash
python ingest.py
```
This populates the SQLite database with your field observations.

3.2 **Launch Dashboard:**
Start the command center to visualize the results:
```bash
streamlit run app.py
```

## 🔗 Let's Connect:

* Visit my website: **[https://GeorgeFreedom.com](https://GeorgeFreedom.com)**
* Connect on LinkedIn: **[https://www.linkedin.com/in/georgefreedom/](https://www.linkedin.com/in/georgefreedom/)**
* Let's talk: **[https://cal.com/georgefreedom](https://cal.com/georgefreedom)**


## 📜 License:

Copyright (c) 2025 Jiří Svoboda (George Freedom) / George Freedom Tech

This project is licensed under:
* Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License

---

We build for the Future!
