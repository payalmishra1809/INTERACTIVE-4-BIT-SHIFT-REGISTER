# pipo_box_ui.py
# 4-bit PIPO (Parallel-In, Parallel-Out) — box-style UI (no circuit diagram)
# Interface:
# - Four input toggles D3..D0 (click to switch 0/1)
# - "Load (Latch)" button captures inputs to outputs (true PIPO behavior)
# - Four large output boxes Q3..Q0
# - Big violet word box showing Parallel Output (Q3..Q0)
# - Reset button


import tkinter as tk
from tkinter import ttk

# ------------------------- Model -------------------------
class PIPO4:
    def __init__(self):
        # Store outputs as MSB..LSB = [Q3, Q2, Q1, Q0]
        self.q = [0, 0, 0, 0]
        self.loads = 0  # number of latch operations

    def reset(self):
        self.q = [0, 0, 0, 0]
        self.loads = 0

    def load(self, bits_msb_to_lsb):
        """
        bits_msb_to_lsb must be [D3, D2, D1, D0].
        On load, Q3..Q0 <= D3..D0 (all in parallel).
        """
        b = [1 if x else 0 for x in bits_msb_to_lsb]
        self.q = b[:4]
        self.loads += 1

    @property
    def word_str(self):
        # Render as Q3..Q0
        return f"{self.q[0]}{self.q[1]}{self.q[2]}{self.q[3]}"

# ------------------------- App UI -------------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PIPO Shift Register — Box UI")
        self.geometry("900x560")
        self.configure(bg="#f7f7fb")
        self.resizable(False, False)

        # Model and inputs: D3..D0
        self.m = PIPO4()
        self.d = [0, 0, 0, 0]  # [D3, D2, D1, D0]

        self._build_header()
        self._build_inputs()
        self._build_outputs()
        self._refresh()

    # ---------- Header ----------
    def _build_header(self):
        header = tk.Frame(self, bg="#111827")
        header.pack(fill="x")
        tk.Label(
            header,
            text="4-bit PIPO — Parallel In ▸ Parallel Out",
            bg="#111827",
            fg="#f8fafc",
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left", padx=16, pady=10)
        self.count_lab = tk.Label(
            header, text="Loads: 0", bg="#111827", fg="#cbd5e1", font=("Segoe UI", 11)
        )
        self.count_lab.pack(side="right", padx=16)

    # ---------- Inputs (D3..D0) ----------
    def _build_inputs(self):
        wrap = tk.Frame(self, bg="#f7f7fb")
        wrap.pack(pady=(12, 6))

        tk.Label(
            wrap,
            text="Parallel Input (D3..D0):",
            bg="#f7f7fb",
            fg="#0f172a",
            font=("Segoe UI", 12, "bold"),
        ).grid(row=0, column=0, sticky="w", padx=10)

        self.in_btns = []  # four toggles for D3..D0
        colors = ["#fde68a", "#bbf7d0", "#93c5fd", "#fca5a5"]  # pretty pastels

        for i in range(4):
            btn = tk.Button(
                wrap,
                text="0",
                width=3,
                relief="raised",
                bg=colors[i],
                fg="#111",
                font=("Segoe UI", 14, "bold"),
                command=lambda idx=i: self._toggle_input(idx),
            )
            # Place as D3 D2 D1 D0 (left -> right)
            btn.grid(row=0, column=i + 1, padx=8, pady=4)
            self.in_btns.append(btn)

        # Load / Reset controls
        self.load_btn = ttk.Button(wrap, text="Load (Latch)", command=self.on_load)
        self.load_btn.grid(row=0, column=5, padx=14)
        self.reset_btn = ttk.Button(wrap, text="Reset", command=self.on_reset)
        self.reset_btn.grid(row=0, column=6, padx=6)

    def _toggle_input(self, idx):
        # idx 0..3 corresponds to D3..D0
        self.d[idx] = 0 if self.d[idx] == 1 else 1
        self._refresh_inputs()

    def _refresh_inputs(self):
        for val, btn in zip(self.d, self.in_btns):
            btn.configure(text=str(val))

    # ---------- Outputs (boxes + word) ----------
    def _build_outputs(self):
        out_wrap = tk.Frame(self, bg="#f7f7fb")
        out_wrap.pack(pady=(8, 6))

        # Big violet word box
        self.word_canvas = tk.Canvas(
            out_wrap, width=780, height=90, bg="#f7f7fb", highlightthickness=0
        )
        self.word_canvas.pack()
        self._rounded(
            self.word_canvas,
            10,
            10,
            770,
            80,
            r=16,
            fill="#ede9fe",
            outline="#7c3aed",
            width=3,
        )
        self.word_canvas.create_text(
            350,
            45,
            text="Parallel Output  (Q3 .. Q0):",
            font=("Segoe UI", 18, "bold"),
            fill="#4c1d95",
            anchor="e",
        )
        self.word_text_id = self.word_canvas.create_text(
            750,
            45,
            text="0000",
            font=("Consolas", 36, "bold"),
            fill="#4c1d95",
            anchor="e",
        )

        # Four large output boxes in a row (Q3..Q0 left->right)
        grid = tk.Frame(self, bg="#f7f7fb")
        grid.pack(pady=(6, 10))

        self.q_labels = []
        box_colors = ["#f5d0fe", "#d9f99d", "#bae6fd", "#fecaca"]
        for i, name in enumerate(["Q3", "Q2", "Q1", "Q0"]):
            cell = tk.Frame(
                grid, width=120, height=120, bg=box_colors[i], bd=2, relief="ridge"
            )
            cell.grid_propagate(False)
            cell.grid(row=0, column=i, padx=12, pady=6)

            val = tk.Label(
                cell,
                text="0",
                bg=box_colors[i],
                fg="#111",
                font=("Consolas", 34, "bold"),
            )
            val.place(relx=0.5, rely=0.55, anchor="center")
            self.q_labels.append(val)

            name_lbl = tk.Label(
                grid,
                text=name,
                bg="#f7f7fb",
                fg="#0f172a",
                font=("Segoe UI", 12, "bold"),
            )
            name_lbl.grid(row=1, column=i, pady=(4, 2))

    def _rounded(self, c, x1, y1, x2, y2, r=12, **kw):
        pts = [
            x1 + r, y1, x2 - r, y1, x2, y1,
            x2, y1 + r, x2, y2 - r, x2, y2,
            x2 - r, y2, x1 + r, y2, x1, y2,
            x1, y2 - r, x1, y1 + r, x1, y1
        ]
        return c.create_polygon(pts, smooth=True, **kw)

    # ---------- Actions ----------
    def on_load(self):
        # d is [D3..D0], latch into q [Q3..Q0]
        self.m.load(self.d)
        self._refresh()

    def on_reset(self):
        self.m.reset()
        self.d = [0, 0, 0, 0]
        self._refresh()

    # ---------- Refresh ----------
    def _refresh(self):
        # Header count
        self.count_lab.config(text=f"Loads: {self.m.loads}")
        # Inputs
        self._refresh_inputs()
        # Output word
        self.word_canvas.itemconfigure(self.word_text_id, text=self.m.word_str)
        # Update Q3..Q0 boxes (labels show digits)
        for lab, bit in zip(self.q_labels, self.m.q):
            lab.config(text=str(bit))

# ------------------------- Run App -------------------------
if __name__ == "__main__":
    App().mainloop()
