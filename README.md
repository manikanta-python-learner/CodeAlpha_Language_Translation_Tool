# CodeAlpha – Language Translation Tool (Task 1)

A desktop language translation application built with Python and Tkinter.

## Features

- Source language selection, including Auto Detect for Google Translate
- Target language selection
- Primary translation attempt through Google Translate integration
- Automatic MyMemory fallback if Google translation fails
- Copy translated text to clipboard
- Swap source and target languages
- Clear input and output
- Character counter and input validation
- Background-thread translation to keep the GUI responsive
- Error messages that explain when both providers fail

## Requirements

- Python 3.10 or newer
- Internet connection
- Tkinter
- `deep-translator`

## Installation

```bash
python -m pip install -r requirements.txt
```

## Run

```bash
python main.py
```

## How to use

1. Enter text in the left panel.
2. Select the source language. For the MyMemory fallback, select a specific source language; Auto Detect is supported only by the primary Google integration. The app maps common language codes to MyMemory regional codes (for example, English `en-GB` and Telugu `te-IN`).
3. Select the target language.
4. Click **Translate**.
5. The result appears in the right panel. The status bar shows which provider returned the translation.
6. Click **Copy translation** to copy the result.

## Translation providers and limitations

- The primary provider is `GoogleTranslator` through the `deep-translator` package. This is not the official Google Cloud Translation API and does not require a Google Cloud API key.
- If the primary provider raises an error or returns no result, the app attempts MyMemory through `MyMemoryTranslator`.
- MyMemory may have usage limits and may not support every language pair or long text. The fallback is configured only for language codes listed in `MYMEMORY_CODES` in `main.py`.
- Both providers require internet access and can be temporarily unavailable or rate-limited.
- Do not submit private or confidential text to third-party translation services.

## Project structure

```text
CodeAlpha_Language_Translation_Tool/
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## GitHub upload

Create a public repository named `CodeAlpha_Language_Translation_Tool`, then run:

```bash
git init
git add .
git commit -m "Complete CodeAlpha Task 1 Language Translation Tool"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/CodeAlpha_Language_Translation_Tool.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username.

## CodeAlpha requirement mapping

| Requirement | Implementation |
|---|---|
| Enter text | Tkinter input text area |
| Select source and target languages | Language dropdowns |
| Use a translation API/service | Google Translate integration + MyMemory fallback |
| Send text and receive translation | Provider `translate()` methods |
| Display translated text | Output text area |
| Optional copy feature | Copy translation button |

## Author

CodeAlpha AI Internship – Task 1
