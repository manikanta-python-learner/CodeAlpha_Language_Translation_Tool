"""
CodeAlpha Task 1: Language Translation Tool
GUI: Tkinter | Primary: Google Translate | Fallback: MyMemory

Install:
    python -m pip install -r requirements.txt

Run:
    python main.py
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox

try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
except ImportError:
    GoogleTranslator = None
    MyMemoryTranslator = None


LANGUAGES = {
    "Auto Detect": "auto",
    "English": "en",
    "Telugu": "te",
    "Hindi": "hi",
    "Tamil": "ta",
    "Kannada": "kn",
    "Malayalam": "ml",
    "Bengali": "bn",
    "Marathi": "mr",
    "Gujarati": "gu",
    "Punjabi": "pa",
    "Urdu": "ur",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Arabic": "ar",
    "Chinese (Simplified)": "zh-CN",
    "Japanese": "ja",
    "Korean": "ko",
}

# MyMemory uses regional language codes, unlike Google's short codes.
# These codes match MyMemory's language list (for example, English en-GB
# and Telugu te-IN). Google continues to use the short codes above.
MYMEMORY_CODES = {
    "en": "en-GB",
    "te": "te-IN",
    "hi": "hi-IN",
    "ta": "ta-IN",
    "bn": "bn-IN",
    "ur": "ur-PK",
    "es": "es-ES",
    "fr": "fr-FR",
    "de": "de-DE",
    "it": "it-IT",
    "pt": "pt-PT",
    "ru": "ru-RU",
    "ar": "ar-SA",
    "zh-CN": "zh-CN",
    "ja": "ja-JP",
    "ko": "ko-KR",
}


class TranslationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeAlpha | Language Translation Tool")
        self.root.geometry("900x650")
        self.root.minsize(720, 560)
        self.root.configure(bg="#f3f6fb")

        self.source_var = tk.StringVar(value="English")
        self.target_var = tk.StringVar(value="Telugu")
        self.status_var = tk.StringVar(value="Ready")
        self._build_ui()

    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("TCombobox", padding=7, font=("Segoe UI", 10))
        style.configure("Action.TButton", font=("Segoe UI", 10, "bold"), padding=9)

        header = tk.Frame(self.root, bg="#172554", padx=24, pady=20)
        header.pack(fill="x")
        tk.Label(
            header, text="LANGUAGE TRANSLATION TOOL",
            font=("Segoe UI", 20, "bold"), fg="white", bg="#172554"
        ).pack(anchor="w")
        tk.Label(
            header, text="CodeAlpha Artificial Intelligence Internship • Task 1",
            font=("Segoe UI", 10), fg="#bfdbfe", bg="#172554"
        ).pack(anchor="w", pady=(5, 0))

        content = tk.Frame(self.root, bg="#f3f6fb", padx=24, pady=18)
        content.pack(fill="both", expand=True)

        language_row = tk.Frame(content, bg="#f3f6fb")
        language_row.pack(fill="x", pady=(0, 12))

        tk.Label(language_row, text="Source language", bg="#f3f6fb",
                 fg="#334155", font=("Segoe UI", 10, "bold")).pack(side="left")
        self.source_box = ttk.Combobox(
            language_row, textvariable=self.source_var,
            values=list(LANGUAGES.keys()), state="readonly", width=22
        )
        self.source_box.pack(side="left", padx=(10, 18))

        ttk.Button(language_row, text="⇄ Swap", command=self.swap_languages).pack(side="left")

        tk.Label(language_row, text="Target language", bg="#f3f6fb",
                 fg="#334155", font=("Segoe UI", 10, "bold")).pack(side="left", padx=(18, 10))
        self.target_box = ttk.Combobox(
            language_row, textvariable=self.target_var,
            values=[name for name in LANGUAGES if name != "Auto Detect"],
            state="readonly", width=22
        )
        self.target_box.pack(side="left")

        panels = tk.Frame(content, bg="#f3f6fb")
        panels.pack(fill="both", expand=True)
        panels.columnconfigure(0, weight=1)
        panels.columnconfigure(1, weight=1)
        panels.rowconfigure(1, weight=1)

        tk.Label(panels, text="Enter text", bg="#f3f6fb",
                 fg="#334155", font=("Segoe UI", 11, "bold")).grid(
                     row=0, column=0, sticky="w", pady=(0, 7))
        tk.Label(panels, text="Translation", bg="#f3f6fb",
                 fg="#334155", font=("Segoe UI", 11, "bold")).grid(
                     row=0, column=1, sticky="w", padx=(14, 0), pady=(0, 7))

        self.input_text = tk.Text(
            panels, wrap="word", font=("Segoe UI", 12), height=12,
            relief="solid", bd=1, padx=12, pady=12, undo=True
        )
        self.input_text.grid(row=1, column=0, sticky="nsew")

        self.output_text = tk.Text(
            panels, wrap="word", font=("Segoe UI", 12), height=12,
            relief="solid", bd=1, padx=12, pady=12, state="disabled"
        )
        self.output_text.grid(row=1, column=1, sticky="nsew", padx=(14, 0))

        self.input_text.bind("<KeyRelease>", self.update_character_count)

        bottom = tk.Frame(content, bg="#f3f6fb")
        bottom.pack(fill="x", pady=(12, 0))

        self.char_label = tk.Label(bottom, text="0 characters", bg="#f3f6fb",
                                   fg="#64748b", font=("Segoe UI", 9))
        self.char_label.pack(side="left")

        self.translate_button = ttk.Button(
            bottom, text="Translate", style="Action.TButton",
            command=self.translate
        )
        self.translate_button.pack(side="right")

        ttk.Button(bottom, text="Copy translation",
                   command=self.copy_translation).pack(side="right", padx=8)
        ttk.Button(bottom, text="Clear",
                   command=self.clear_all).pack(side="right", padx=8)

        status_bar = tk.Label(
            self.root, textvariable=self.status_var, anchor="w",
            bg="#e2e8f0", fg="#334155", padx=18, pady=8,
            font=("Segoe UI", 9)
        )
        status_bar.pack(fill="x", side="bottom")

        self.input_text.insert("1.0", "Hello! Welcome to the Language Translation Tool.")
        self.update_character_count()

    def update_character_count(self, _event=None):
        count = len(self.input_text.get("1.0", "end-1c"))
        self.char_label.config(text=f"{count} characters")

    def set_output(self, text):
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.insert("1.0", text)
        self.output_text.config(state="disabled")

    def translate(self):
        source_name = self.source_var.get()
        target_name = self.target_var.get()
        source_code = LANGUAGES[source_name]
        target_code = LANGUAGES[target_name]
        text = self.input_text.get("1.0", "end-1c").strip()

        if not text:
            messagebox.showwarning("Input required", "Please enter text to translate.")
            return
        if len(text) > 5000:
            messagebox.showwarning(
                "Text too long",
                "Please keep the input under 5,000 characters for this demo."
            )
            return
        if source_code == target_code:
            messagebox.showinfo("Same language", "Please choose two different languages.")
            return
        if GoogleTranslator is None or MyMemoryTranslator is None:
            messagebox.showerror(
                "Missing dependency",
                "Translation libraries are not installed.\n"
                "Run: python -m pip install -r requirements.txt"
            )
            return

        self.translate_button.config(state="disabled")
        self.status_var.set("Trying Google Translate...")
        self.set_output("Translating...")

        threading.Thread(
            target=self._translate_worker,
            args=(text, source_code, target_code),
            daemon=True
        ).start()

    def _translate_worker(self, text, source_code, target_code):
        google_error = None

        # First attempt: Google Translate integration.
        try:
            result = GoogleTranslator(
                source=source_code, target=target_code
            ).translate(text)
            if result:
                self.root.after(0, self._translation_success, result, "Google Translate")
                return
            google_error = "Google Translate returned an empty result."
        except Exception as exc:
            google_error = str(exc)

        # Fallback: MyMemory. It needs an explicitly selected source language.
        if source_code == "auto":
            error = (
                "Google Translate failed, and MyMemory fallback needs a selected "
                "source language. Select the source language manually and try again.\n\n"
                f"Google error: {google_error}"
            )
            self.root.after(0, self._translation_error, error)
            return

        try:
            mymemory_source = MYMEMORY_CODES.get(source_code)
            mymemory_target = MYMEMORY_CODES.get(target_code)

            if not mymemory_source or not mymemory_target:
                raise ValueError(
                    "This language pair is not configured for the MyMemory fallback. "
                    "Try another supported language pair or use Google Translate."
                )

            result = MyMemoryTranslator(
                source=mymemory_source, target=mymemory_target
            ).translate(text)
            if result:
                self.root.after(0, self._translation_success, result, "MyMemory fallback")
                return
            raise RuntimeError("MyMemory returned an empty result.")
        except Exception as fallback_error:
            error = (
                "Both translation services failed.\n\n"
                f"Google Translate: {google_error}\n\n"
                f"MyMemory: {fallback_error}\n\n"
                "Check your internet connection. The services may also be "
                "temporarily unavailable or rate-limited."
            )
            self.root.after(0, self._translation_error, error)

    def _translation_success(self, result, provider):
        self.set_output(result)
        self.status_var.set(f"Translation completed using {provider}.")
        self.translate_button.config(state="normal")

    def _translation_error(self, error):
        self.set_output("")
        self.status_var.set("Translation failed.")
        self.translate_button.config(state="normal")
        messagebox.showerror("Translation error", error)

    def copy_translation(self):
        result = self.output_text.get("1.0", "end-1c").strip()
        if not result or result == "Translating...":
            messagebox.showinfo("Nothing to copy", "Translate some text first.")
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(result)
        self.status_var.set("Translation copied to clipboard.")

    def clear_all(self):
        self.input_text.delete("1.0", "end")
        self.set_output("")
        self.update_character_count()
        self.status_var.set("Cleared. Ready for a new translation.")

    def swap_languages(self):
        source = self.source_var.get()
        target = self.target_var.get()
        if source == "Auto Detect":
            messagebox.showinfo(
                "Auto Detect", "Choose a source language before swapping."
            )
            return
        self.source_var.set(target)
        self.target_var.set(source)
        old_input = self.input_text.get("1.0", "end-1c")
        old_output = self.output_text.get("1.0", "end-1c")
        if old_output and old_output != "Translating...":
            self.input_text.delete("1.0", "end")
            self.input_text.insert("1.0", old_output)
            self.set_output(old_input)
            self.update_character_count()


if __name__ == "__main__":
    root = tk.Tk()
    app = TranslationApp(root)
    root.mainloop()
