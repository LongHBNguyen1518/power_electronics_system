import os
import sys
import webbrowser
import tkinter as tk
from tkinter import ttk, messagebox

# Data structure for power electronics topologies
TOPOLOGY_DATA = {
    "AC/DC Converters": {
        "1-Phase PFC": {
            "Diode Bridge + Boost PFC": {
                "desc": "Standard single-phase boost converter for power factor correction. Uses a full-bridge diode rectifier followed by a boost stage.",
                "pros": ["Simple design and low component count", "Low cost", "Mature control algorithms (Average Current Mode)"],
                "cons": ["High conduction losses through the input diode bridge", "Limited to low-to-medium power (< 1.5 kW)", "No bidirectional power capability"],
                "doc": "docs/ac_dc/1_phase/diode_bridge_boost_pfc.md"
            },
            "Interleaved Totempole Boost PFC": {
                "desc": "A two-phase interleaved bridgeless totem-pole PFC converter where the two high-frequency legs are operated 180 degrees out of phase to achieve input current ripple cancellation.",
                "pros": ["Substantially reduced grid current ripple via interleaving", "Smaller EMI filter requirement", "Distributed thermal stress across phases", "Maintains ultra-high efficiency of totem-pole configuration"],
                "cons": ["Increased component count (extra inductors and gate drives)", "Requires precise current sharing control and ZC spike mitigation"],
                "doc": "docs/ac_dc/1_phase/interleaved_totempole_boost_pfc.md"
            },
            "Bridgeless PFC": {
                "desc": "PFC topology that eliminates the input diode bridge rectifier to improve efficiency.",
                "pros": ["Higher efficiency due to fewer diode drops", "Better thermal management"],
                "cons": ["High common-mode noise / EMI issues", "Complex voltage/current sensing required"],
                "doc": "docs/ac_dc/1_phase/bridgeless_pfc.md"
            },
            "Totempole Boost PFC": {
                "desc": "A premium bridgeless PFC leg utilizing wide-bandgap (SiC/GaN) devices in a totem-pole arrangement alongside line-frequency switches.",
                "pros": ["Very high efficiency (>99%)", "Bidirectional power flow capability (V2G)", "Low common-mode EMI compared to other bridgeless topologies"],
                "cons": ["Requires high-performance SiC/GaN switches", "Complex control algorithms and dead-time management"],
                "doc": "docs/ac_dc/1_phase/totempole_boost_pfc.md"
            },
            "Flying Capacitor PFC": {
                "desc": "Multilevel single-phase converter utilizing flying capacitors to reduce voltage stress on semiconductors.",
                "pros": ["Reduced switch voltage rating", "Smaller inductors due to multiplied effective switching frequency"],
                "cons": ["Requires capacitor voltage balancing control", "High control complexity"],
                "doc": "docs/ac_dc/1_phase/flying_capacitor_pfc.md"
            }
        },
        "3-Phase PFC": {
            "2-level Active Front End (AFE)": {
                "desc": "Standard bidirectional 3-phase PFC using 6 active switches. Capable of rectifying and regenerating energy back to the grid.",
                "pros": ["Fully bidirectional (supports Vehicle-to-Grid - V2G)", "Low input current THD", "Unity power factor"],
                "cons": ["High switch voltage stress (must withstand full DC bus)", "Large EMI filters required"],
                "doc": "docs/ac_dc/3_phase/two_level_afe.md"
            },
            "Vienna Rectifier": {
                "desc": "A popular 3-phase, 3-level unidirectional PFC rectifier. Widely used in EV fast chargers.",
                "pros": ["3-level operation reduces switch voltage stress", "Very low current THD", "High reliability and no shoot-through risk"],
                "cons": ["Unidirectional only (no energy regeneration to grid)", "Complex control of neutral-point voltage"],
                "doc": "docs/ac_dc/3_phase/vienna_rectifier.md"
            },
            "T-Type 3-Level PFC": {
                "desc": "A 3-level converter using a T-type switch configuration, offering low conduction losses.",
                "pros": ["Lower conduction losses compared to NPC", "Bidirectional capability", "Reduced switching losses due to 3-level output"],
                "cons": ["Switches have unequal voltage stress ratings", "Complex gate-driver routing"],
                "doc": "docs/ac_dc/3_phase/t_type_3_level_pfc.md"
            },
            "NPC 3-Level PFC": {
                "desc": "Neutral Point Clamped 3-level converter utilizing clamping diodes to split the DC link voltage.",
                "pros": ["Equal switch voltage stress (half of DC bus)", "Excellent THD performance", "Highly suited for high-voltage applications"],
                "cons": ["Large number of active switches and clamping diodes", "Unequal loss distribution"],
                "doc": "docs/ac_dc/3_phase/npc_3_level_pfc.md"
            }
        }
    },
    "DC/DC Converters": {
        "Non-Isolated": {
            "Synchronous Buck/Boost": {
                "desc": "A Buck/Boost converter replacing passive diodes with active switches (MOSFETs) to eliminate diode drop losses.",
                "pros": ["High efficiency due to low switch conduction losses", "Inherent bidirectional power flow capability"],
                "cons": ["Risk of shoot-through (requires precise dead-time)", "Requires complex gate drives"],
                "doc": "docs/dc_dc/non_isolated/sync_buck_boost.md"
            },
            "Interleaved Buck Converter": {
                "desc": "Multiple buck stages connected in parallel and operated out of phase to handle high currents and reduce output ripple.",
                "pros": ["Significantly reduced input/output current ripple", "Distributed thermal stress across phases", "Reduces output filter capacitor requirements for high-current CPU/GPU VRMs"],
                "cons": ["Higher component count (multiple inductors and gate drives)", "Requires precise current sharing control"],
                "doc": "docs/dc_dc/non_isolated/interleaved_buck_converter.md"
            },
            "3-Level Buck Converter": {
                "desc": "A buck converter that uses a flying capacitor to split the switch voltage stress in half and reduce the inductor size.",
                "pros": ["Half the switch voltage stress (uses lower voltage rating switches)", "Substantially smaller inductor size due to doubled effective ripple frequency", "Low switching losses", "Widely used in high-power dense chargers (e.g., Anker Prime 160W)"],
                "cons": ["Requires flying capacitor voltage balancing control", "More complex gate driver and control circuitry"],
                "doc": "docs/dc_dc/non_isolated/3_level_buck_converter.md",
                "refs": [
                    {"title": "TI SLYT807 Application Note", "url": "https://www.ti.com/lit/an/slyt807/slyt807.pdf?ts=1781940609608"},
                    {"title": "Anker Prime 160W Charger Teardown", "url": "https://www.youtube.com/watch?v=yGiHjUCxM8A"}
                ]
            }
        },
        "Isolated": {
            "LLC Resonant": {
                "desc": "Resonant converter operating with Pulse Frequency Modulation (PFM) to achieve soft switching.",
                "pros": ["Zero Voltage Switching (ZVS) on primary and Zero Current Switching (ZCS) on secondary", "Extremely high efficiency", "Low EMI"],
                "cons": ["Narrow output voltage regulation range", "Complex resonant tank design", "Unidirectional only in standard configurations"],
                "doc": "docs/dc_dc/isolated/llc_resonant.md"
            },
            "CLLC Resonant": {
                "desc": "Symmetric resonant converter enabling high-efficiency bidirectional operation, ideal for EV chargers.",
                "pros": ["ZVS and ZCS in both directions", "Fully symmetrical bidirectional operation", "High efficiency"],
                "cons": ["Very complex parameter design", "Requires symmetrical resonant networks"],
                "doc": "docs/dc_dc/isolated/cllc_resonant.md"
            },
            "Phase-Shift Full Bridge (PSFB)": {
                "desc": "Full-bridge isolated DC/DC converter regulating output voltage by shifting the phase of diagonal switches.",
                "pros": ["ZVS for primary switches", "Constant switching frequency (easy filter design)", "Easy to control"],
                "cons": ["Duty cycle loss due to leakage inductance", "High voltage spikes on output rectifier diodes", "High circulating currents at light loads"],
                "doc": "docs/dc_dc/isolated/psfb.md"
            },
            "Dual Active Bridge (DAB)": {
                "desc": "A bidirectional isolated converter using two active bridges linked by a leakage inductor.",
                "pros": ["High power density", "Seamless bidirectional power flow", "Soft-switching (ZVS) capability"],
                "cons": ["High circulating current at light loads", "Sensitive to mismatch in phase shift"],
                "doc": "docs/dc_dc/isolated/dab.md"
            }
        }
    }
}

class PowerElectronicsApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Power Electronics Topology Explorer")
        self.geometry("950x700")
        
        # Dark Theme Palette
        self.bg_dark = "#121212"
        self.bg_panel = "#1e1e1e"
        self.fg_white = "#f0f0f0"
        self.fg_gray = "#888888"
        self.accent_blue = "#3498db"
        self.accent_green = "#2ecc71"
        self.accent_orange = "#e67e22"
        
        self.configure(bg=self.bg_dark)
        self.setup_styles()
        self.create_widgets()
        self.load_status()

    def setup_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        
        # Treeview styling
        style.configure("Treeview",
                        background=self.bg_panel,
                        foreground=self.fg_white,
                        fieldbackground=self.bg_panel,
                        rowheight=25)
        style.map("Treeview",
                  background=[("selected", self.accent_blue)],
                  foreground=[("selected", self.fg_white)])
        
        # Button styling
        style.configure("TButton",
                        background="#2d2d2d",
                        foreground=self.fg_white,
                        bordercolor="#121212",
                        font=("Segoe UI", 9, "bold"))
        style.map("TButton",
                  background=[("active", self.accent_blue)],
                  foreground=[("active", self.fg_white)])
        
        # Notebook (Tab) styling
        style.configure("TNotebook", background=self.bg_dark, borderwidth=0)
        style.configure("TNotebook.Tab", 
                        background=self.bg_panel, 
                        foreground=self.fg_white, 
                        borderwidth=1, 
                        padding=[12, 6],
                        font=("Segoe UI", 9, "bold"))
        style.map("TNotebook.Tab", 
                  background=[("selected", self.accent_blue)], 
                  foreground=[("selected", self.fg_white)])

    def load_status(self):
        """Parse TODO.md to read project completion status."""
        self.status = {}
        todo_path = os.path.join(os.path.dirname(__file__), 'TODO.md')
        if not os.path.exists(todo_path):
            return
        
        try:
            with open(todo_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            current_top = None
            for line in lines:
                line_str = line.strip()
                if '**' in line_str:
                    parts = line_str.split('**')
                    if len(parts) >= 3:
                        current_top = parts[1].strip()
                        self.status[current_top] = {'p1': False, 'p2': False, 'p3': False}
                elif current_top and 'Phase 1' in line_str:
                    self.status[current_top]['p1'] = '[x]' in line_str.lower()
                elif current_top and 'Phase 2' in line_str:
                    self.status[current_top]['p2'] = '[x]' in line_str.lower()
                elif current_top and 'Phase 3' in line_str:
                    self.status[current_top]['p3'] = '[x]' in line_str.lower()
        except Exception as e:
            print(f"Error reading TODO.md: {e}")

    def create_widgets(self):
        # Header Title
        title_label = tk.Label(self, text="⚡ Power Electronics Topology Explorer", 
                               bg=self.bg_dark, fg=self.fg_white,
                               font=("Segoe UI", 16, "bold"), pady=15)
        title_label.pack(side=tk.TOP, fill=tk.X)
        
        # Main container (PanedWindow)
        paned = tk.PanedWindow(self, orient=tk.HORIZONTAL, bg=self.bg_dark, bd=0, sashwidth=5)
        paned.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        # Left Panel (Treeview)
        left_frame = tk.Frame(paned, bg=self.bg_dark)
        paned.add(left_frame, width=280)
        
        tree_scroll = ttk.Scrollbar(left_frame)
        tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(left_frame, yscrollcommand=tree_scroll.set, show="tree")
        self.tree.pack(fill=tk.BOTH, expand=True)
        tree_scroll.config(command=self.tree.yview)
        
        # Populate Tree
        for section, sub_sections in TOPOLOGY_DATA.items():
            sec_id = self.tree.insert("", "end", text=section, open=True)
            for sub_sec, topologies in sub_sections.items():
                sub_id = self.tree.insert(sec_id, "end", text=sub_sec, open=True)
                for top_name in topologies.keys():
                    self.tree.insert(sub_id, "end", text=top_name)
                    
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        
        # Right Panel (Detail Viewer)
        self.right_frame = tk.Frame(paned, bg=self.bg_panel, bd=1, relief=tk.SOLID)
        paned.add(self.right_frame)
        
        # Detail widgets (Initial blank page)
        self.show_placeholder()

    def show_placeholder(self):
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        placeholder = tk.Label(self.right_frame, 
                               text="Select a Topology from the tree\nto view details, pros/cons, and simulation status.",
                               bg=self.bg_panel, fg=self.fg_gray,
                               font=("Segoe UI", 11, "italic"), justify=tk.CENTER)
        placeholder.pack(expand=True)

    def get_topology_path_segments(self, name):
        """Helper to get standardized path segments for folders."""
        for section, sub_secs in TOPOLOGY_DATA.items():
            for sub_sec, topologies in sub_secs.items():
                if name in topologies:
                    sec_folder = "ac_dc" if "AC/DC" in section else "dc_dc"
                    
                    sub_folder = "1_phase" if "1-Phase" in sub_sec else (
                        "3_phase" if "3-Phase" in sub_sec else (
                            "non_isolated" if "Non-Isolated" in sub_sec else "isolated"
                        )
                    )
                    
                    # Clean folder name
                    clean_name = name.lower().replace(' + ', '_').replace(' +', '_').replace('+ ', '_').replace('+', '_').replace(' ', '_').replace('__', '_').replace('/', '_').replace('-', '_').replace('(', '').replace(')', '')
                    
                    return sec_folder, sub_folder, clean_name
        return None, None, None

    def on_tree_select(self, event):
        selected_item = self.tree.selection()
        if not selected_item:
            return
            
        item_text = self.tree.item(selected_item[0], "text")
        
        # Find if selected item is a leaf node (topology)
        topology_info = None
        for sec, sub_secs in TOPOLOGY_DATA.items():
            for sub_sec, topologies in sub_secs.items():
                if item_text in topologies:
                    topology_info = topologies[item_text]
                    break
            if topology_info:
                break
                
        if topology_info:
            self.show_details(item_text, topology_info)
        else:
            self.show_placeholder()

    def show_details(self, name, info):
        # Clear right frame
        for widget in self.right_frame.winfo_children():
            widget.destroy()
            
        # 1. Overview & Operating Principle (Header + Description)
        top_info_frame = tk.Frame(self.right_frame, bg=self.bg_panel, padx=20, pady=15)
        top_info_frame.pack(fill=tk.X)
        
        title = tk.Label(top_info_frame, text=name, bg=self.bg_panel, fg=self.accent_blue,
                         font=("Segoe UI", 16, "bold"), anchor="w")
        title.pack(fill=tk.X)
        
        lbl_sec1 = tk.Label(top_info_frame, text="1. Overview & Operating Principle", bg=self.bg_panel, fg=self.fg_white,
                            font=("Segoe UI", 11, "bold"), anchor="w")
        lbl_sec1.pack(fill=tk.X, pady=(10, 2))
        
        desc_text = tk.Label(top_info_frame, text=info["desc"], bg=self.bg_panel, fg=self.fg_white,
                             font=("Segoe UI", 10), justify=tk.LEFT, anchor="w", wraplength=620)
        desc_text.pack(fill=tk.X, pady=5)
        
        # 2. Phase Selector & Actions
        lbl_sec2 = tk.Label(self.right_frame, text="2. Phase-level Simulations & Progress", bg=self.bg_panel, fg=self.fg_white,
                            font=("Segoe UI", 11, "bold"), anchor="w", padx=20)
        lbl_sec2.pack(fill=tk.X, pady=(5, 2))

        notebook = ttk.Notebook(self.right_frame)
        notebook.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        
        # Get paths
        sec_folder, sub_folder, clean_name = self.get_topology_path_segments(name)
        top_status = self.status.get(name, {'p1': False, 'p2': False, 'p3': False})
        
        # Create Phase Tabs
        self.create_phase_tab(notebook, "Phase 1: PSIM Block", "p1", top_status['p1'], sec_folder, sub_folder, clean_name, info["doc"])
        self.create_phase_tab(notebook, "Phase 2: PSIM DLL (C-Code)", "p2", top_status['p2'], sec_folder, sub_folder, clean_name, info["doc"])
        self.create_phase_tab(notebook, "Phase 3: MATLAB/Simulink", "p3", top_status['p3'], sec_folder, sub_folder, clean_name, info["doc"])
        
        # 3. Advantages & Disadvantages (Pros/Cons side-by-side at the bottom)
        pc_frame = tk.Frame(self.right_frame, bg=self.bg_panel, padx=20, pady=10, bd=1, relief=tk.RIDGE)
        pc_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=15)
        
        tk.Label(pc_frame, text="3. Advantages & Disadvantages", bg=self.bg_panel, fg=self.fg_white,
                 font=("Segoe UI", 11, "bold"), anchor="w").pack(fill=tk.X, pady=(0, 5))
        
        lists_frame = tk.Frame(pc_frame, bg=self.bg_panel)
        lists_frame.pack(fill=tk.X)
        
        # Pros
        pros_frame = tk.Frame(lists_frame, bg=self.bg_panel)
        pros_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(pros_frame, text="🟢 Pros", bg=self.bg_panel, fg=self.accent_green, 
                 font=("Segoe UI", 10, "bold"), anchor="w").pack(fill=tk.X)
        for pro in info["pros"]:
            tk.Label(pros_frame, text=f"• {pro}", bg=self.bg_panel, fg=self.fg_white,
                     font=("Segoe UI", 9), justify=tk.LEFT, anchor="w", wraplength=280).pack(fill=tk.X, pady=1)
            
        # Cons
        cons_frame = tk.Frame(lists_frame, bg=self.bg_panel)
        cons_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        tk.Label(cons_frame, text="🔴 Cons", bg=self.bg_panel, fg=self.accent_orange, 
                 font=("Segoe UI", 10, "bold"), anchor="w").pack(fill=tk.X)
        for con in info["cons"]:
            tk.Label(cons_frame, text=f"• {con}", bg=self.bg_panel, fg=self.fg_white,
                     font=("Segoe UI", 9), justify=tk.LEFT, anchor="w", wraplength=280).pack(fill=tk.X, pady=1)

        # 4. References & Learning Resources (stacked above Pros/Cons)
        ref_frame = tk.Frame(self.right_frame, bg=self.bg_panel, padx=20, pady=5)
        ref_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=20, pady=(5, 5))
        
        ref_header = tk.Frame(ref_frame, bg=self.bg_panel)
        ref_header.pack(fill=tk.X)
        
        tk.Label(ref_header, text="🔗 References & Learning Resources", bg=self.bg_panel, fg=self.accent_blue,
                 font=("Segoe UI", 10, "bold"), anchor="w").pack(side=tk.LEFT)
        
        add_ref_btn = tk.Label(ref_header, text="[Add Reference Link]", bg=self.bg_panel, fg=self.fg_gray,
                               font=("Segoe UI", 8, "underline"), cursor="hand2")
        add_ref_btn.pack(side=tk.RIGHT)
        add_ref_btn.bind("<Button-1>", lambda e: messagebox.showinfo(
            "How to Add References",
            "To add or share videos, PDFs, or articles for any topology:\n\n"
            "Open 'visualizer.py' and add a 'refs' key to the corresponding topology in the 'TOPOLOGY_DATA' dictionary. Example:\n\n"
            "\"refs\": [\n"
            "    {\"title\": \"TI App Note\", \"url\": \"https://...\"},\n"
            "    {\"title\": \"YouTube Video\", \"url\": \"https://...\"}\n"
            "]"
        ))
        
        links_frame = tk.Frame(ref_frame, bg=self.bg_panel)
        links_frame.pack(fill=tk.X, pady=5)
        
        if "refs" in info and info["refs"]:
            for ref in info["refs"]:
                btn = ttk.Button(links_frame, text=ref["title"], command=lambda url=ref["url"]: webbrowser.open(url))
                btn.pack(side=tk.LEFT, padx=(0, 10), pady=2)
        else:
            tk.Label(links_frame, text="No references added yet. Click [Add Reference Link] to see how to add yours.",
                     bg=self.bg_panel, fg=self.fg_gray, font=("Segoe UI", 9, "italic"), anchor="w").pack(side=tk.LEFT)

    def create_phase_tab(self, notebook, tab_title, phase_key, is_done, sec_folder, sub_folder, clean_name, doc_path):
        tab_frame = tk.Frame(notebook, bg=self.bg_panel, padx=15, pady=15)
        notebook.add(tab_frame, text=tab_title)
        
        # Define simulation path based on phase
        phase_dir_map = {
            "p1": f"simulations/Phase_1_PSIM_Block/{sec_folder}/{sub_folder}/{clean_name}",
            "p2": f"simulations/Phase_2_PSIM_DLL/{sec_folder}/{sub_folder}/{clean_name}",
            "p3": f"simulations/Phase_3_MATLAB/{sec_folder}/{sub_folder}/{clean_name}",
        }
        rel_sim_path = phase_dir_map[phase_key]
        
        # Header Info Row: Status & Path
        info_row = tk.Frame(tab_frame, bg=self.bg_panel)
        info_row.pack(fill=tk.X, pady=(0, 10))
        
        status_color = self.accent_green if is_done else self.fg_gray
        status_text = f"Status: {'Completed (✓)' if is_done else 'Pending (○)'}"
        status_lbl = tk.Label(info_row, text=status_text, bg=self.bg_panel, fg=status_color,
                              font=("Segoe UI", 11, "bold"), anchor="w")
        status_lbl.pack(side=tk.LEFT)
        
        # Focus/Objective note
        objectives = {
            "p1": "Objective: Build and verify the schematic power stage using built-in PSIM blocks (switches, passive components, sensors, and basic logic controls).",
            "p2": "Objective: Develop control algorithms (PI, PR, state machine) in C code, compile into a DLL file, and link it inside PSIM to replace visual blocks.",
            "p3": "Objective: Model the circuit mathematically in MATLAB/Simulink, perform small-signal analysis, plot Bode, and design optimal control loops."
        }
        obj_lbl = tk.Label(tab_frame, text=objectives[phase_key], bg=self.bg_panel, fg=self.fg_white,
                           font=("Segoe UI", 10, "italic"), justify=tk.LEFT, anchor="w", wraplength=580)
        obj_lbl.pack(fill=tk.X, pady=(0, 15))
        
        # Visual Helper / Tips on viewing results
        tip_text = (
            "💡 To view full high-resolution waveform graphs and detailed step-by-step "
            "simulation timelines (0.2s, 0.3s, 0.4s, etc.), click the button below to "
            "open the documentation file, then press Ctrl+Shift+V in VS Code."
        )
        tip_lbl = tk.Label(tab_frame, text=tip_text, bg="#252525", fg="#dcdcdc", bd=1, relief=tk.SOLID,
                           font=("Segoe UI", 9), justify=tk.LEFT, anchor="w", wraplength=580, padx=10, pady=8)
        tip_lbl.pack(fill=tk.X, pady=(0, 15))

        # Action Buttons frame
        btn_frame = tk.Frame(tab_frame, bg=self.bg_panel)
        btn_frame.pack(fill=tk.X, pady=(5, 0))
        
        open_folder_btn = ttk.Button(btn_frame, text="📁 Open Simulation Folder", 
                                     command=lambda: self.open_folder(rel_sim_path))
        open_folder_btn.pack(side=tk.LEFT, padx=(0, 10), ipady=3)
        
        open_doc_btn = ttk.Button(btn_frame, text="📖 Open Documentation & Results", 
                                  command=lambda: self.open_document(doc_path))
        open_doc_btn.pack(side=tk.LEFT, ipady=3)
        
        # Path details label
        path_lbl = tk.Label(tab_frame, text=f"Local directory: {rel_sim_path}", bg=self.bg_panel, fg=self.fg_gray, font=("Segoe UI", 8, "italic"))
        path_lbl.pack(fill=tk.X, side=tk.BOTTOM, anchor="w")

    def open_document(self, relative_path):
        full_path = os.path.join(os.path.dirname(__file__), relative_path)
        if os.path.exists(full_path):
            webbrowser.open(full_path)
        else:
            # Create a stub document if it doesn't exist
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w', encoding='utf-8') as f:
                name = os.path.basename(relative_path).replace('_', ' ').replace('.md', '').title()
                f.write(f"# {name}\n\nDocumentation and analysis stub for {name}.\n")
            webbrowser.open(full_path)

    def open_folder(self, relative_path):
        full_path = os.path.join(os.path.dirname(__file__), relative_path)
        if not os.path.exists(full_path):
            os.makedirs(full_path, exist_ok=True)
        os.startfile(full_path)

if __name__ == "__main__":
    app = PowerElectronicsApp()
    app.mainloop()
