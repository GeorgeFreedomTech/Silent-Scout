# Silent-Scout

### **By George Freedom**
A dual-component surveillance system designed for radio frequency reconnaissance, combining an **ESP32 Edge Agent** with a sophisticated **Streamlit Command Center (HQ)**.

This project demonstrates a complete **Hardware-to-Intelligence pipeline**: capturing raw 802.11 signals in the field, managing a local data vault, and performing tactical analysis to identify security risks and infrastructure patterns.

It serves as a professional blueprint for **IoT & Data Engineering**, of an embedded hardware sensing and high-level analytical visualization using a modern, AI-augmented workflow.

### ⚙️ Core System Capabilities:
It demonstrates key engineering concepts including:

* **Edge Intelligence (Hardware):** Deploying a passive reconnaissance agent using MicroPython on ESP32 to sniff, filter, and log WiFi environments without network association.

* **Data Vault & Ingestion (ETL):** A robust process for transferring "field logs" (CSV) into a centralized SQLite database, ensuring data integrity and historical persistence.

* **Tactical Analysis Engine:** The core processing logic. Translating raw MAC addresses into vendor identities (OUI) and assigning risk tags based on signal patterns.

* **Visual Reconnaissance:** An interactive Streamlit dashboard featuring custom CSS, tactical legends, and Plotly charts for signal distribution and channel occupation analysis.

* **System Architecture:** A modular "Agent-HQ" design, separating low-level hardware constraints from high-level data science and visualization.

---

## 🚀 Key Features
* **Stealth Reconnaissance:** The ESP32 Agent operates in passive mode, logging SSIDs, BSSIDs, and RSSI levels without leaving a digital footprint.

* **Mission-Based Tracking:** Organize data by Locality IDs and Timestamps, allowing for comparative analysis of the same location over time.

* **Automated Threat Tagging:** Intelligent identification of mobile hotspots, surveillance infrastructure (CCTV), and hidden networks.

* **RSSI Proximity Grading:** Visual color-coding of signal strength to estimate physical distance to targets (Near/Medium/Far).

* **RF Environment Profiling:** Detailed breakdown of channel occupation to identify network congestion or potential interference.

* **Hardware Interface:** Real-time visual feedback on the Agent via LED signaling for successful scans and system readiness.

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
