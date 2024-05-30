import tkinter as tk
from tkinter import scrolledtext
from phase1 import tokenize
from phase2 import semantic_analysis
from phase3 import MemorySimulator

class CompilerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Custom Compiler")

        self.top_frame = tk.Frame(root)
        self.top_frame.pack(padx=10, pady=10)

        self.middle_frame = tk.Frame(root)
        self.middle_frame.pack(padx=10, pady=10)

        self.bottom_frame = tk.Frame(root)
        self.bottom_frame.pack(padx=10, pady=10)

        self.input_frame = tk.Frame(self.top_frame)
        self.input_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.phase1_frame = tk.Frame(self.top_frame)
        self.phase1_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.phase2_frame = tk.Frame(self.bottom_frame)
        self.phase2_frame.pack(side=tk.LEFT, padx=10, pady=10)

        self.phase3_frame = tk.Frame(self.bottom_frame)
        self.phase3_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        tk.Label(self.input_frame, text="Input Code:").pack(anchor=tk.W)
        self.input_text_area = scrolledtext.ScrolledText(self.input_frame, wrap=tk.WORD, width=50, height=10)
        self.input_text_area.pack()

        tk.Label(self.phase1_frame, text="Phase 1 Output:").pack(anchor=tk.W)
        self.phase1_output_area = scrolledtext.ScrolledText(self.phase1_frame, wrap=tk.WORD, width=50, height=10)
        self.phase1_output_area.pack()

        tk.Label(self.phase2_frame, text="Phase 2 Output:").pack(anchor=tk.W)
        self.phase2_output_area = scrolledtext.ScrolledText(self.phase2_frame, wrap=tk.WORD, width=50, height=10)
        self.phase2_output_area.pack()

        tk.Label(self.phase3_frame, text="Phase 3 Output:").pack(anchor=tk.W)
        self.phase3_output_area = scrolledtext.ScrolledText(self.phase3_frame, wrap=tk.WORD, width=50, height=10)
        self.phase3_output_area.pack()

        self.scan_button = tk.Button(self.middle_frame, text="Scan", command=self.scan_code)
        self.scan_button.pack(pady=5)

    def scan_code(self):
        code = self.input_text_area.get("1.0", tk.END)

        tokens = tokenize(code)

        errors = semantic_analysis(tokens)

        self.phase1_output_area.delete("1.0", tk.END)
        for token in tokens:
            self.phase1_output_area.insert(tk.END, f"{token[0]}: {token[1]}\n")
        
        self.phase2_output_area.delete("1.0", tk.END)
        if errors:
            self.phase2_output_area.insert(tk.END, "Errors:\n")
            for error in errors:
                self.phase2_output_area.insert(tk.END, f"{error}\n")
        else:
            self.phase2_output_area.insert(tk.END, "No errors found.")

        memory_simulator = MemorySimulator()
        memory_trace = memory_simulator.execute(tokens)

        self.phase3_output_area.delete("1.0", tk.END)
        for trace in memory_trace:
            self.phase3_output_area.insert(tk.END, f"{trace}\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = CompilerGUI(root)
    root.mainloop()
