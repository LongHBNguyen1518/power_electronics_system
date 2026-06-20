# Power Electronics System - From Theory to Practice

This project is a repository for storing, analyzing, and simulating Power Electronics converters from AC/DC to DC/DC. It focuses on high-efficiency converters widely used in Electric Vehicle (EV) Chargers, telecommunications, and renewable energy.

## 🚀 Execution Phases

The learning and design process for each Topology is divided into 3 phases:

1.  **Phase 1: PSIM Blocks** - Visual simulation using PSIM's built-in blocks. Verifies the power stage principles and basic control loop.
2.  **Phase 2: PSIM DLL** - Converts control blocks into C code (DLL). Helps understand embedded programming (writing code for MCU/DSPs like TI C2000, STM32) such as PI/PR controllers, PWM generation, and Phase-Shift.
3.  **Phase 3: MATLAB/Simulink** - In-depth system analysis, Bode Plot design, efficiency calculations, and control loop parameter optimization.

## 🧠 Topology Mindmap (Interactive)

The mindmap below outlines the topologies to be simulated, classified by family and variants.

![Power Electronics Topologies](pe_mindmap.png)

```mermaid
mindmap
  root((Power Electronics))
    AC_DC(AC/DC Converters)
      1_Phase(1-Phase PFC)
        Basic_PFC[Boost PFC]
        Interleaved_PFC[Interleaved Boost]
        Bridgeless_PFC[Bridgeless PFC]
        Totem_Pole(Totem Pole PFC)
          TP_CCM[CCM Mode]
          TP_CrM[CrM Mode]
        Multi_Level_1Ph(Multi-Level)
          FC_1Ph[Flying Capacitor]
      3_Phase(3-Phase PFC)
        2_Level[2-Level AFE]
        Multi_Level_3Ph(Multi-Level)
          Vienna[Vienna Rectifier]
          NPC[NPC 3-Level]
          T_Type[T-Type 3-Level]
    DC_DC(DC/DC Converters)
      Non_Isolated(Non-Isolated)
        Buck(Buck / Step-Down)
          Sync_Buck[Synchronous Buck]
          Int_Buck[Interleaved Buck]
        Boost(Boost / Step-Up)
          Sync_Boost[Synchronous Boost]
          Int_Boost[Interleaved Boost]
        Buck_Boost(Buck-Boost Family)
          SEPIC_Cuk[SEPIC / Cuk / Zeta]
      Isolated(Isolated)
        Resonant(Resonant)
          LLC(LLC)
            LLC_HB[Half-Bridge]
            LLC_FB[Full-Bridge]
            LLC_3Ph[3-Phase LLC]
          CLLC(CLLC Bidirectional)
            CLLC_1Ph[1-Phase CLLC]
            CLLC_3Ph[3-Phase CLLC]
        Phase_Shift(Phase-Shift)
          PSFB_1Ph[1-Phase PSFB]
          PSFB_3Ph[3-Phase PSFB]
        DAB(Dual Active Bridge)
          DAB_1Ph[1-Phase DAB]
          DAB_3Ph[3-Phase DAB]
        Flyback_Forward(Flyback & Forward)
          Flyback(Flyback)
            Std_Flyback[Standard]
            ACF[Active Clamp]
          Forward(Forward)
            Std_Forward[Standard]
            Int_Forward[Interleaved]
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
