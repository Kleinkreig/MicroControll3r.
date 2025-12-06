import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import os

# HID key codes (decimal values, names simplified)
hid_codes = {
    'NONE': 0,
    'ERR_OVF': 1,
    'A': 4,
    'B': 5,
    'C': 6,
    'D': 7,
    'E': 8,
    'F': 9,
    'G': 10,
    'H': 11,
    'I': 12,
    'J': 13,
    'K': 14,
    'L': 15,
    'M': 16,
    'N': 17,
    'O': 18,
    'P': 19,
    'Q': 20,
    'R': 21,
    'S': 22,
    'T': 23,
    'U': 24,
    'V': 25,
    'W': 26,
    'X': 27,
    'Y': 28,
    'Z': 29,
    '1': 30,
    '2': 31,
    '3': 32,
    '4': 33,
    '5': 34,
    '6': 35,
    '7': 36,
    '8': 37,
    '9': 38,
    '0': 39,
    'ENTER': 40,
    'ESC': 41,
    'BACKSPACE': 42,
    'TAB': 43,
    'SPACE': 44,
    'MINUS': 45,
    'EQUAL': 46,
    'LEFTBRACE': 47,
    'RIGHTBRACE': 48,
    'BACKSLASH': 49,
    'HASHTILDE': 50,
    'SEMICOLON': 51,
    'APOSTROPHE': 52,
    'GRAVE': 53,
    'COMMA': 54,
    'DOT': 55,
    'SLASH': 56,
    'CAPSLOCK': 57,
    'F1': 58,
    'F2': 59,
    'F3': 60,
    'F4': 61,
    'F5': 62,
    'F6': 63,
    'F7': 64,
    'F8': 65,
    'F9': 66,
    'F10': 67,
    'F11': 68,
    'F12': 69,
    'SYSRQ': 70,
    'SCROLLLOCK': 71,
    'PAUSE': 72,
    'INSERT': 73,
    'HOME': 74,
    'PAGEUP': 75,
    'DELETE': 76,
    'END': 77,
    'PAGEDOWN': 78,
    'RIGHT': 79,
    'LEFT': 80,
    'DOWN': 81,
    'UP': 82,
    'NUMLOCK': 83,
    'KPSLASH': 84,
    'KPASTERISK': 85,
    'KPMINUS': 86,
    'KPPLUS': 87,
    'KPENTER': 88,
    'KP1': 89,
    'KP2': 90,
    'KP3': 91,
    'KP4': 92,
    'KP5': 93,
    'KP6': 94,
    'KP7': 95,
    'KP8': 96,
    'KP9': 97,
    'KP0': 98,
    'KPDOT': 99,
    '102ND': 100,
    'COMPOSE': 101,
    'POWER': 102,
    'KPEQUAL': 103,
    'F13': 104,
    'F14': 105,
    'F15': 106,
    'F16': 107,
    'F17': 108,
    'F18': 109,
    'F19': 110,
    'F20': 111,
    'F21': 112,
    'F22': 113,
    'F23': 114,
    'F24': 115,
    'OPEN': 116,
    'HELP': 117,
    'PROPS': 118,
    'FRONT': 119,
    'STOP': 120,
    'AGAIN': 121,
    'UNDO': 122,
    'CUT': 123,
    'COPY': 124,
    'PASTE': 125,
    'FIND': 126,
    'MUTE': 127,
    'VOLUMEUP': 128,
    'VOLUMEDOWN': 129,
    'KPCOMMA': 133,
    'RO': 135,
    'KATAKANAHIRAGANA': 136,
    'YEN': 137,
    'HENKAN': 138,
    'MUHENKAN': 139,
    'KPJPCOMMA': 140,
    'HANGEUL': 144,
    'HANJA': 145,
    'KATAKANA': 146,
    'HIRAGANA': 147,
    'ZENKAKUHANKAKU': 148,
    'KPLEFTPAREN': 182,
    'KPRIGHTPAREN': 183,
    'LEFTCTRL': 224,
    'LEFTSHIFT': 225,
    'LEFTALT': 226,
    'LEFTMETA': 227,
    'RIGHTCTRL': 228,
    'RIGHTSHIFT': 229,
    'RIGHTALT': 230,
    'RIGHTMETA': 231,
    'MEDIA_PLAYPAUSE': 232,
    'MEDIA_STOPCD': 233,
    'MEDIA_PREVIOUSSONG': 234,
    'MEDIA_NEXTSONG': 235,
    'MEDIA_EJECTCD': 236,
    'MEDIA_VOLUMEUP': 237,
    'MEDIA_VOLUMEDOWN': 238,
    'MEDIA_MUTE': 239,
    'BROWSER_WWW': 240,
    'BROWSER_BACK': 241,
    'BROWSER_FORWARD': 242,
    'BROWSER_STOP': 243,
    'BROWSER_FIND': 244,
    'BROWSER_SCROLLUP': 245,
    'BROWSER_SCROLLDOWN': 246,
    'BROWSER_EDIT': 247,
    'SLEEP': 248,
    'COFFEE': 249,
    'BROWSER_REFRESH': 250,
    'CALC': 251
}

# Modifiers dictionary for checkboxes
modifiers = {
    'Left Ctrl': 224,
    'Left Shift': 225,
    'Left Alt': 226,
    'Left Meta': 227,
    'Right Ctrl': 228,
    'Right Shift': 229,
    'Right Alt': 230,
    'Right Meta': 231
}

# Reverse lookup for displaying names
code_to_name = {v: k for k, v in {**hid_codes, **modifiers}.items()}

# Character to HID mapping for text input (US layout)
char_to_hid = {
    'a': (4, False), 'b': (5, False), 'c': (6, False), 'd': (7, False),
    'e': (8, False), 'f': (9, False), 'g': (10, False), 'h': (11, False),
    'i': (12, False), 'j': (13, False), 'k': (14, False), 'l': (15, False),
    'm': (16, False), 'n': (17, False), 'o': (18, False), 'p': (19, False),
    'q': (20, False), 'r': (21, False), 's': (22, False), 't': (23, False),
    'u': (24, False), 'v': (25, False), 'w': (26, False), 'x': (27, False),
    'y': (28, False), 'z': (29, False),
    'A': (4, True), 'B': (5, True), 'C': (6, True), 'D': (7, True),
    'E': (8, True), 'F': (9, True), 'G': (10, True), 'H': (11, True),
    'I': (12, True), 'J': (13, True), 'K': (14, True), 'L': (15, True),
    'M': (16, True), 'N': (17, True), 'O': (18, True), 'P': (19, True),
    'Q': (20, True), 'R': (21, True), 'S': (22, True), 'T': (23, True),
    'U': (24, True), 'V': (25, True), 'W': (26, True), 'X': (27, True),
    'Y': (28, True), 'Z': (29, True),
    '1': (30, False), '2': (31, False), '3': (32, False), '4': (33, False),
    '5': (34, False), '6': (35, False), '7': (36, False), '8': (37, False),
    '9': (38, False), '0': (39, False),
    '!': (30, True), '@': (31, True), '#': (32, True), '$': (33, True),
    '%': (34, True), '^': (35, True), '&': (36, True), '*': (37, True),
    '(': (38, True), ')': (39, True),
    '-': (45, False), '_': (45, True), '=': (46, False), '+': (46, True),
    '[': (47, False), '{': (47, True), ']': (48, False), '}': (48, True),
    '\\': (49, False), '|': (49, True), ';': (51, False), ':': (51, True),
    "'": (52, False), '"': (52, True), ',': (54, False), '<': (54, True),
    '.': (55, False), '>': (55, True), '/': (56, False), '?': (56, True),
    '`': (53, False), '~': (53, True),
    ' ': (44, False),
    '\n': (40, False),  # Enter
    '\t': (43, False),  # Tab
    '\b': (42, False),  # Backspace (if needed)
}

# Advanced text parser for {key} syntax
special_keys = {k.lower(): v for k, v in hid_codes.items()}

def parse_text_to_steps(text):
    steps = []
    i = 0
    while i < len(text):
        if text[i] == '{':
            # Find closing }
            j = text.find('}', i + 1)
            if j == -1:
                break
            key_name = text[i+1:j].strip().upper()
            if key_name in hid_codes:
                steps.append([hid_codes[key_name]])
            else:
                messagebox.showwarning("Warning", f"Unknown special key: {key_name}")
            i = j + 1
        else:
            char = text[i]
            if char in char_to_hid:
                code, shift = char_to_hid[char]
                step = []
                if shift:
                    step.append(225)  # LEFTSHIFT
                step.append(code)
                steps.append(sorted(step))  # Sort for consistency
            else:
                messagebox.showwarning("Warning", f"Unsupported character: {char}")
            i += 1
    return steps

class StepEditor(tk.Toplevel):
    def __init__(self, parent, step=None):
        super().__init__(parent)
        self.title("Edit Step")
        self.vars = {name: tk.BooleanVar(value=False) for name in modifiers}
        for name, var in self.vars.items():
            tk.Checkbutton(self, text=name, variable=var).pack(anchor='w')
        tk.Label(self, text="Key:").pack()
        self.key_var = tk.StringVar()
        keys_list = sorted(set(hid_codes.keys()) - set(['LEFTCTRL', 'LEFTSHIFT', 'LEFTALT', 'LEFTMETA', 'RIGHTCTRL', 'RIGHTSHIFT', 'RIGHTALT', 'RIGHTMETA']))
        self.combobox = ttk.Combobox(self, textvariable=self.key_var, values=keys_list, state='readonly')
        self.combobox.pack()
        if step:
            for code in step:
                for name, mcode in modifiers.items():
                    if code == mcode:
                        self.vars[name].set(True)
                for k, v in hid_codes.items():
                    if v == code and k in keys_list:
                        self.key_var.set(k)
        tk.Button(self, text="OK", command=self.save).pack(pady=10)
        self.result = None

    def save(self):
        codes = [modifiers[name] for name, var in self.vars.items() if var.get()]
        key = self.key_var.get()
        if key:
            codes.append(hid_codes[key])
        if codes:
            self.result = sorted(codes)  # Sort for consistent order (modifiers first)
        self.destroy()

class TextEditor(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Add Text Sequence")
        tk.Label(self, text="Enter text (use {ENTER}, {TAB}, etc. for specials):").pack()
        self.text_entry = tk.Text(self, height=5, width=50)
        self.text_entry.pack()
        tk.Button(self, text="OK", command=self.save).pack(pady=10)
        self.result = None

    def save(self):
        text = self.text_entry.get("1.0", tk.END).strip()
        if text:
            self.result = parse_text_to_steps(text)
        self.destroy()

class MacroGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Macro Board Configurator")
        self.path = None
        self.path_label = tk.Label(self.root, text="No device path selected")
        self.path_label.pack(pady=10)
        tk.Button(self.root, text="Select Device Path", command=self.select_path).pack()
        self.macros = [[] for _ in range(4)]
        self.listboxes = []
        for i in range(4):
            frame = tk.Frame(self.root)
            tk.Label(frame, text=f"Button {i+1} Macros").pack()
            lb = tk.Listbox(frame, width=50, height=5)
            lb.pack()
            self.listboxes.append(lb)
            btn_frame = tk.Frame(frame)
            tk.Button(btn_frame, text="Add Step", command=lambda idx=i: self.add_step(idx)).pack(side=tk.LEFT)
            tk.Button(btn_frame, text="Add Text", command=lambda idx=i: self.add_text(idx)).pack(side=tk.LEFT)
            tk.Button(btn_frame, text="Edit Step", command=lambda idx=i: self.edit_step(idx)).pack(side=tk.LEFT)
            tk.Button(btn_frame, text="Delete Step", command=lambda idx=i: self.delete_step(idx)).pack(side=tk.LEFT)
            btn_frame.pack()
            frame.pack(pady=10)
        tk.Button(self.root, text="Load Macros", command=self.load).pack()
        tk.Button(self.root, text="Save Macros", command=self.save).pack(pady=10)
        self.update_listboxes()
        self.root.mainloop()

    def select_path(self):
        self.path = filedialog.askdirectory(title="Select Mounted Device Path")
        if self.path:
            self.path_label.config(text=self.path)

    def load(self):
        if not self.path:
            messagebox.showerror("Error", "Select device path first.")
            return
        file_path = os.path.join(self.path, 'macros.json')
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
                self.macros = data.get('macros', [[] for _ in range(4)])
            self.update_listboxes()
            messagebox.showinfo("Success", "Macros loaded.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load: {e}")
            self.macros = [[] for _ in range(4)]
            self.update_listboxes()

    def save(self):
        if not self.path:
            messagebox.showerror("Error", "Select device path first.")
            return
        file_path = os.path.join(self.path, 'macros.json')
        data = {'macros': self.macros}
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f)
            messagebox.showinfo("Success", "Macros saved.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {e}")

    def update_listboxes(self):
        for i, lb in enumerate(self.listboxes):
            lb.delete(0, tk.END)
            for step in self.macros[i]:
                step_str = ' + '.join([code_to_name.get(code, str(code)) for code in step])
                lb.insert(tk.END, step_str or "Empty")

    def add_step(self, btn_idx):
        dialog = StepEditor(self.root)
        self.root.wait_window(dialog)
        if dialog.result:
            self.macros[btn_idx].append(dialog.result)
            self.update_listboxes()

    def add_text(self, btn_idx):
        dialog = TextEditor(self.root)
        self.root.wait_window(dialog)
        if dialog.result:
            self.macros[btn_idx].extend(dialog.result)
            self.update_listboxes()

    def edit_step(self, btn_idx):
        lb = self.listboxes[btn_idx]
        sel = lb.curselection()
        if not sel:
            messagebox.showwarning("Warning", "Select a step to edit.")
            return
        step_idx = sel[0]
        step = self.macros[btn_idx][step_idx]
        dialog = StepEditor(self.root, step)
        self.root.wait_window(dialog)
        if dialog.result:
            self.macros[btn_idx][step_idx] = dialog.result
            self.update_listboxes()

    def delete_step(self, btn_idx):
        lb = self.listboxes[btn_idx]
        sel = lb.curselection()
        if sel:
            del self.macros[btn_idx][sel[0]]
            self.update_listboxes()

if __name__ == "__main__":
    MacroGUI()
