import tkinter as tk
import keyboard
import pyautogui

class ScrollEmulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scroll Emulator by valdemir")
        self.root.geometry("400x300")
        

        self.key_up = None
        self.key_down = None
        self.emulation_enabled = tk.BooleanVar(value=True)
        self.continuous_scroll_enabled = tk.BooleanVar(value=False)
        self.log = []

        self.create_widgets()
        self.check_keys()

    def create_widgets(self):
        # Key configuration
        tk.Label(self.root, text="Key for Scroll Up:").pack(pady=5)
        self.key_up_entry = tk.Entry(self.root, state='disabled')
        self.key_up_entry.pack(pady=5)
        tk.Button(self.root, text="Capture Key Up", command=self.capture_key_up).pack(pady=5)

        tk.Label(self.root, text="Key for Scroll Down:").pack(pady=5)
        self.key_down_entry = tk.Entry(self.root, state='disabled')
        self.key_down_entry.pack(pady=5)
        tk.Button(self.root, text="Capture Key Down", command=self.capture_key_down).pack(pady=5)

        # Continuous scroll toggle
        self.continuous_scroll_btn = tk.Checkbutton(self.root, text="Continuous Scroll", variable=self.continuous_scroll_enabled)
        self.continuous_scroll_btn.pack(pady=5)

        # Emulation toggle
        tk.Checkbutton(self.root, text="Enable Emulation", variable=self.emulation_enabled).pack(pady=5)

        # Log display
        self.log_display = tk.Text(self.root, height=10, state='disabled')
        self.log_display.pack(pady=5)

    def capture_key_up(self):
        self.key_up_entry.config(state='normal')
        self.key_up_entry.delete(0, tk.END)
        self.key_up_entry.insert(0, "Press a key...")
        self.root.bind('<KeyPress>', self.set_key_up)

    def set_key_up(self, event):
        self.key_up = event.keysym
        self.key_up_entry.delete(0, tk.END)
        self.key_up_entry.insert(0, self.key_up)
        self.key_up_entry.config(state='disabled')
        self.root.unbind('<KeyPress>')

    def capture_key_down(self):
        self.key_down_entry.config(state='normal')
        self.key_down_entry.delete(0, tk.END)
        self.key_down_entry.insert(0, "Press a key...")
        self.root.bind('<KeyPress>', self.set_key_down)

    def set_key_down(self, event):
        self.key_down = event.keysym
        self.key_down_entry.delete(0, tk.END)
        self.key_down_entry.insert(0, self.key_down)
        self.key_down_entry.config(state='disabled')
        self.root.unbind('<KeyPress>')

    def scroll_up(self):
        pyautogui.scroll(250)  # Scroll up faster
        self.log_event("Scrolled up")

    def scroll_down(self):
        pyautogui.scroll(-250)  # Scroll down faster
        self.log_event("Scrolled down")

    def log_event(self, event):
        self.log.append(event)
        self.update_log_display()

    def update_log_display(self):
        self.log_display.config(state='normal')
        self.log_display.delete(1.0, tk.END)
        for event in self.log:
            self.log_display.insert(tk.END, event + '\n')
        self.log_display.config(state='disabled')

    def check_keys(self):
        if self.emulation_enabled.get():
            if self.key_up and keyboard.is_pressed(self.key_up):
                if self.continuous_scroll_enabled.get():
                    self.root.after(10, self.scroll_up)  # Faster scrolling
                else:
                    self.scroll_up()
            if self.key_down and keyboard.is_pressed(self.key_down):
                if self.continuous_scroll_enabled.get():
                    self.root.after(10, self.scroll_down)  # Faster scrolling
                else:
                    self.scroll_down()

        self.root.after(10, self.check_keys)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScrollEmulatorApp(root)
    root.mainloop()
