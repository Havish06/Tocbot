# TOC + Fun Chatbot 🤖

This is a chatbot that mixes **fun conversations** with **Theory of Computation (TOC) demos** and **basic programming/math utilities**.
It can run either as a **Flask web app** (with a chat UI) or in **CLI mode** directly from the terminal.

---

## ✨ Features

* **Greetings & Small Talk**

  * Friendly responses to "hi", "hello", "good morning", etc.
  * Small talk like "how are you", "what's up", etc.

* **Math Evaluator**

  * Can evaluate math expressions (`2+3*4`, `(5/2) + 7`).
  * Uses **Sympy** if available, falls back to Python’s `eval`.

* **Code Execution**

  * Safely runs short Python snippets (prints output or errors).

* **TOC (Theory of Computation) Demos**

  * **DFA demo:** `dfa:10101` → checks if string ends with `01`.
  * **PDA demo:** `pda:(())` → checks for balanced parentheses.
  * **CFG demo:** `cfg:I like apples` → validates a toy grammar.
  * **Regex demo:** `regex:[0-9]+; string:12345`.

* **Programming Concepts**

  * Explains basics like *functions*, *loops*, *variables*.

* **Jokes & Fun Facts**

  * Huge list of programming jokes.
  * Random TOC facts like "Every regular language can be represented by DFA, NFA, and regex."

* **Time**

  * Tells the current system time.

* **Memory**

  * Keeps track of conversation history in a sliding window.

---

## 🚀 Running the Chatbot

### 1. Requirements

* Python 3.8+
* Optional: [Flask](https://flask.palletsprojects.com/) (for web UI), [Sympy](https://www.sympy.org/en/index.html) (for math)

Install dependencies (if needed):

```bash
pip install flask sympy
```

### 2. Run in Web Mode (Flask UI)

```bash
python chatbot.py
```

Then open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.
You’ll see a simple chat interface with bubbles.

### 3. Run in CLI Mode (Terminal)

If Flask isn’t installed, the bot automatically falls back to **CLI mode**:

```bash
python chatbot.py
```

Example:

```
TOC Chatbot CLI. Type exit to quit.
You: hi
Bot: Hey! I'm your bot. Ask me to solve math, run code, or tell you a joke.
```

---

## 🛠️ Project Structure

* **DialogueManager** → Stores chat memory.
* **ProgramExecutor** → Evaluates math + executes Python code.
* **TOCFeatures** → DFA, PDA, CFG, Regex, TOC facts.
* **ResponseGenerator** → Core logic for generating replies.
* **Chatbot** → Ties everything together.
* **HTML UI** → Minimal chat interface styled with CSS.
* **CLI Mode** → Simple REPL fallback if Flask is not installed.

---

## 📚 Example Prompts

* `2 + 2 * 5` → `Result: 12`
* `dfa:10101` → `Accepted by DFA (ends with '01')`
* `pda:(())()` → `Accepted by PDA (balanced parentheses)`
* `cfg:I love bananas` → `Valid sentence according to toy CFG`
* `regex:[a-z]+; string:hello` → `Regex matched!`
* `tell me a joke` → Random programming joke
* `fun fact` → Random TOC fact

---

## 👨‍💻 Author

Built as a fun **Theory of Computation + Chatbot** mashup project.
Works both in **browser** (with Flask) and **terminal** (CLI mode).

---
