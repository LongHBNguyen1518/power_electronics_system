# Power Electronics System - From Theory to Practice

This project is a repository for storing, analyzing, and simulating Power Electronics converters from AC/DC to DC/DC. It focuses on high-efficiency converters widely used in Electric Vehicle (EV) Chargers, telecommunications, and renewable energy.

## 🚀 Execution Phases

The learning and design process for each Topology is divided into 3 phases:

1.  **Phase 1: PSIM Blocks** - Visual simulation using PSIM's built-in blocks. Verifies the power stage principles and basic control loop.
2.  **Phase 2: PSIM DLL** - Converts control blocks into C code (DLL). Helps understand embedded programming (writing code for MCU/DSPs like TI C2000, STM32) such as PI/PR controllers, PWM generation, and Phase-Shift.
3.  **Phase 3: MATLAB/Simulink** - In-depth system analysis, Bode Plot design, efficiency calculations, and control loop parameter optimization.

## 🧠 Topology Mindmap (Interactive)

The mindmap below outlines the topologies to be simulated, classified by family and variants.

```mermaid
flowchart TD
    %% Node definitions
    PE(["⚡ Power Electronics"])

    %% AC/DC Subgraph
    subgraph ACDC ["🔌 AC/DC Converters"]
        AC_1P["1-Phase PFC"]
        AC_3P["3-Phase PFC"]

        %% 1-Phase Topologies
        AC_1P --> Boost_PFC["Boost PFC"]
        AC_1P --> Interleaved_PFC["Interleaved Boost"]
        AC_1P --> Bridgeless_PFC["Bridgeless PFC"]
        AC_1P --> Totem_Pole["Totem Pole PFC"]
        AC_1P --> ML_1P["Multi-Level"]

        %% Totem Pole & ML Details
        Totem_Pole --> TP_CCM["CCM Mode"]
        Totem_Pole --> TP_CrM["CrM Mode"]
        ML_1P --> FC_1P["Flying Capacitor"]

        %% 3-Phase Topologies
        AC_3P --> AFE_2L["2-Level AFE"]
        AC_3P --> ML_3P["Multi-Level"]

        %% 3-Phase Details
        ML_3P --> Vienna["Vienna Rectifier"]
        ML_3P --> NPC["NPC 3-Level"]
        ML_3P --> T_Type["T-Type 3-Level"]
    end

    %% DC/DC Subgraph
    subgraph DCDC ["🔋 DC/DC Converters"]
        Non_Iso["Non-Isolated"]
        Iso["Isolated"]

        %% Non-Isolated
        Non_Iso --> Buck["Buck (Step-Down)"]
        Non_Iso --> Boost["Boost (Step-Up)"]
        Non_Iso --> Buck_Boost["Buck-Boost Family"]

        Buck --> Sync_Buck["Synchronous Buck"]
        Buck --> Int_Buck["Interleaved Buck"]

        Boost --> Sync_Boost["Synchronous Boost"]
        Boost --> Int_Boost["Interleaved Boost"]

        Buck_Boost --> SEPIC_Cuk["SEPIC / Cuk / Zeta"]

        %% Isolated
        Iso --> Resonant["Resonant"]
        Iso --> PS["Phase-Shift"]
        Iso --> DAB["Dual Active Bridge"]
        Iso --> FF["Flyback & Forward"]

        %% Isolated Details
        Resonant --> LLC["LLC"]
        Resonant --> CLLC["CLLC Bidirectional"]
        
        LLC --> LLC_HB["Half-Bridge"]
        LLC --> LLC_FB["Full-Bridge"]
        LLC --> LLC_3P["3-Phase LLC"]
        
        CLLC --> CLLC_1P["1-Phase CLLC"]
        CLLC --> CLLC_3P["3-Phase CLLC"]

        PS --> PSFB_1P["1-Phase PSFB"]
        PS --> PSFB_3P["3-Phase PSFB"]

        DAB --> DAB_1P["1-Phase DAB"]
        DAB --> DAB_3P["3-Phase DAB"]

        FF --> Flyback["Flyback"]
        FF --> Forward["Forward"]

        Flyback --> Std_Flyback["Standard"]
        Flyback --> ACF["Active Clamp"]

        Forward --> Std_Forward["Standard"]
        Forward --> Int_Forward["Interleaved"]
    end

    %% Root to Subgraphs
    PE --> ACDC
    PE --> DCDC

    %% Custom Styles (CSS-like)
    classDef rootStyle fill:#4F46E5,stroke:#3730A3,stroke-width:2px,color:#FFF,font-weight:bold,font-size:14px;
    classDef acdcSub fill:#E0F2FE,stroke:#0284C7,stroke-width:1.5px,color:#0369A1,font-weight:bold;
    classDef dcdcSub fill:#DCFCE7,stroke:#15803D,stroke-width:1.5px,color:#166534,font-weight:bold;
    classDef subSec fill:#FFF,stroke:#0284C7,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef subSecDC fill:#FFF,stroke:#15803D,stroke-width:2px,color:#0F172A,font-weight:bold;
    classDef topo fill:#F8FAFC,stroke:#94A3B8,stroke-width:1.5px,color:#1E293B;
    classDef leaf fill:#F1F5F9,stroke:#CBD5E1,stroke-width:1px,stroke-dasharray: 2 2,color:#475569,font-size:11px;

    %% Apply Classes
    class PE rootStyle;
    class ACDC acdcSub;
    class DCDC dcdcSub;
    class AC_1P,AC_3P subSec;
    class Non_Iso,Iso subSecDC;
    
    class Boost_PFC,Interleaved_PFC,Bridgeless_PFC,Totem_Pole,ML_1P,AFE_2L,ML_3P topo;
    class Buck,Boost,Buck_Boost,Resonant,PS,DAB,FF topo;
    
    class TP_CCM,TP_CrM,FC_1P,Vienna,NPC,T_Type,Sync_Buck,Int_Buck,Sync_Boost,Int_Boost,SEPIC_Cuk,LLC,CLLC,LLC_HB,LLC_FB,LLC_3P,CLLC_1P,CLLC_3P,PSFB_1P,PSFB_3P,DAB_1P,DAB_3P,Flyback,Forward,Std_Flyback,ACF,Std_Forward,Int_Forward leaf;
```

## 📂 Directory Structure

*   `/docs/` - Theory, pros/cons, and modulation strategies for each topology.
*   `/simulations/`
    *   `/Phase_1_PSIM_Block/`
    *   `/Phase_2_PSIM_DLL/`
    *   `/Phase_3_MATLAB/`
*   `/scripts/` - Parameter calculation scripts (Python/MATLAB).

---
*This project is constantly updated. Check the `TODO.md` file for current progress.*
