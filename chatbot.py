import re, time, random
from collections import deque

# Optional imports
try:
    from flask import Flask, request, jsonify, render_template_string
except:
    Flask = None

try:
    import sympy as sp
except:
    sp = None

# ---------------------- Utilities ----------------------
def normalize_text(s: str) -> str:
    s = s.lower().strip()
    s = s.replace("what's", "whats")
    s = re.sub(r"\s+", " ", s)
    return s

# ---------------------- Dialogue Manager ----------------------
class DialogueManager:
    def __init__(self, memory_size=10):
        self.memory = deque(maxlen=memory_size)

    def add(self, role, text):
        self.memory.append({'role': role, 'text': text, 'ts': time.time()})

    def get_memory(self):
        return list(self.memory)

# ---------------------- Program Executor ----------------------
class ProgramExecutor:
    def eval_math(self, expr: str):
        try:
            if sp:
                return str(sp.N(sp.sympify(expr)))
            else:
                return str(eval(expr, {"__builtins__": {}}, {}))
        except Exception as e:
            return f"error: {e}"

    def safe_exec_python(self, code: str):
        try:
            import subprocess, tempfile
            tf = tempfile.NamedTemporaryFile(delete=False, suffix='.py')
            tf.write(code.encode('utf-8'))
            tf.flush()
            tf.close()
            proc = subprocess.run(
                ['python', tf.name],
                capture_output=True,
                text=True,
                timeout=2
            )
            return proc.stdout + proc.stderr
        except Exception as e:
            return f"error executing: {e}"

# ---------------------- TOC Features ----------------------
class TOCFeatures:
    @staticmethod
    def check_dfa_ends01(string):
        if re.fullmatch(r"[01]*01", string):
            return "Accepted by DFA (ends with '01')"
        return "Rejected by DFA"

    @staticmethod
    def check_balanced_parentheses(expr):
        stack = []
        for c in expr:
            if c == '(':
                stack.append(c)
            elif c == ')':
                if not stack:
                    return "Rejected by PDA (unbalanced parentheses)"
                stack.pop()
        if stack:
            return "Rejected by PDA (unbalanced parentheses)"
        return "Accepted by PDA (balanced parentheses)"

    @staticmethod
    def simple_cfg_check(sentence):
        toy_words = {
            "i", "you", "he", "she", "it", "we", "they",
            "like", "love", "eat", "food", "apples", "bananas"
        }
        tokens = sentence.lower().split()
        if all(t in toy_words for t in tokens):
            return "Valid sentence according to toy CFG"
        return "Invalid sentence according to toy CFG"

    @staticmethod
    def regex_match(pattern, string):
        try:
            if re.fullmatch(pattern, string):
                return "Regex matched!"
            return "Regex did NOT match."
        except Exception as e:
            return f"Regex error: {e}"

    @staticmethod
    def toc_fact():
        facts = [
            "Every regular language can be represented by DFA, NFA, and regex.",
            "Some context-free languages are not regular.",
            "The pumping lemma can prove certain languages are not regular.",
            "Turing machines can simulate any computer algorithm!"
        ]
        return random.choice(facts)

# ---------------------- Response Generator ----------------------
class ResponseGenerator:
    def __init__(self):
        self.execer = ProgramExecutor()
        self.toc = TOCFeatures()

    def generate(self, text, memory=None):
        text_norm = normalize_text(text)

        # Greetings
        if "good morning" in text_norm:
            return "Good morning! Hope you have a great day!"
        elif "good afternoon" in text_norm:
            return "Good afternoon! How’s your day going?"
        elif "good evening" in text_norm:
            return "Good evening! How was your day?"
        elif "good night" in text_norm:
            return "Good night! Sleep well!"
        elif any(g in text_norm for g in ['hi', 'hello', 'hey', 'yo']):
            return "Hey! I'm your bot. Ask me to solve math, run code, or tell you a joke."

        # Time
        if 'time' in text_norm:
            return time.strftime("It's %H:%M:%S")

        # Small talk
        small_talk = {
            "how are you": "I'm just a bot, but I'm vibing! How about you?",
            "what's up": "Just chatting with cool people like you!",
            "how's it going": "Going great! Ready to solve math or run code?"
        }
        for k, v in small_talk.items():
            if k in text_norm:
                return v

        # Gratitude
        if any(tk in text_norm for tk in ["thank you", "thanks", "thx"]):
            return "You're welcome! 😎"

        # Goodbye
        if any(bk in text_norm for bk in ["bye", "goodbye", "see you", "later"]):
            return "Bye! Catch you later! 👋"

        # Fun fact
        if any(fk in text_norm for fk in ["fun fact", "tell me something interesting"]):
            return self.toc.toc_fact()

        # Programming basics
        prog_keywords = {
            "what is a function": "A function is a block of code that performs a specific task.",
            "explain loop": "A loop repeats a set of instructions until a condition is met.",
            "what is a variable": "A variable stores data that can be used and modified in your program."
        }
        for pk in prog_keywords:
            if pk in text_norm:
                return prog_keywords[pk]

        # Regex checker
        if text_norm.startswith("regex:"):
            try:
                parts = text_norm.split(";")
                pattern = parts[0].replace("regex:", "").strip()
                string = parts[1].replace("string:", "").strip()
                return self.toc.regex_match(pattern, string)
            except:
                return "Format: regex:<pattern>; string:<text>"

        # DFA demo
        if text_norm.startswith("dfa:"):
            string = text_norm.replace("dfa:", "").strip()
            return self.toc.check_dfa_ends01(string)

        # PDA demo
        if text_norm.startswith("pda:"):
            expr = text_norm.replace("pda:", "").strip()
            return self.toc.check_balanced_parentheses(expr)

        # CFG demo
        if text_norm.startswith("cfg:"):
            sentence = text_norm.replace("cfg:", "").strip()
            return self.toc.simple_cfg_check(sentence)

        # Math detection
        if re.match(r'^[0-9\+\-\*\/\(\)\. ]+$', text.strip()):
            return "Result: " + self.execer.eval_math(text)

        math_match = re.search(r'(?:what is|solve)?\s*([0-9\+\-\*\/\(\)\. ]+)', text_norm)
        if math_match:
            expr = math_match.group(1).strip()
            if expr:
                return "Result: " + self.execer.eval_math(expr)

        # Code detection
        if any(kw in text for kw in ['print', 'for ', 'while ', 'def ', 'import ']):
            return "Program output:\n" + self.execer.safe_exec_python(text)

        # Jokes
        if 'joke' in text_norm:
            jokes = [
                "Why did the programmer quit his job? Because he didn't get arrays.",
                "Why do Java developers wear glasses? Because they don't C#.",
                "Why did the functions stop calling each other? Because they had constant arguments.",
                "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
                "Why do programmers prefer dark mode? Because light attracts bugs.",
                "There are 10 types of people in the world: those who understand binary and those who don't.",
                "Why was the computer cold? It left its Windows open.",
                "Why did the programmer go broke? Because he used up all his cache.",
                "Debugging: Removing the needles from the haystack.",
                "I would tell you a UDP joke, but you might not get it.",
                "Why do Python programmers have low self-esteem? They constantly compare themselves to others.",
                "Why was the equal sign so humble? Because it knew it wasn’t less than or greater than anyone else.",
                "Parallel lines have so much in common… it’s a shame they’ll never meet.",
                "Why was six afraid of seven? Because 7 8 9.",
                "Why did the student do multiplication problems on the floor? The teacher told him not to use tables.",
                "Why don’t scientists trust atoms? Because they make up everything."
            ]
            return random.choice(jokes)

        # Fallback
        return "Sorry, I didn't get that. I can do greetings, math, run code, jokes, DFA/PDA/CFG demos, or tell fun facts."

# ---------------------- Main Chatbot ----------------------
class Chatbot:
    def __init__(self):
        self.dialogue = DialogueManager()
        self.generator = ResponseGenerator()

    def handle(self, user_text: str):
        self.dialogue.add('user', user_text)
        resp = self.generator.generate(user_text, memory=self.dialogue.get_memory())
        self.dialogue.add('bot', resp)
        return {'a': resp}

# ---------------------- HTML UI ----------------------
_SIMPLE_HTML = """
<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>TOC + Fun Chatbot</title>
<style>
  body { font-family: Arial, sans-serif; background:#f0f2f5; margin:0; }
  .container {
    max-width: 800px; margin: 30px auto; background:#fff;
    border-radius: 12px; box-shadow:0 8px 16px rgba(0,0,0,0.15);
    padding:20px;
  }
  h2 { text-align:center; color:#333; }
  #chat {
    max-height:400px; overflow-y:auto; padding:10px;
    border:1px solid #ddd; border-radius:8px; background:#fafafa;
    margin-bottom:10px;
  }
  .message { display:flex; margin-bottom:8px; }
  .message.user { justify-content:flex-end; }
  .message.bot { justify-content:flex-start; }
  .bubble {
    max-width:70%; padding:10px 15px; border-radius:20px;
    font-size:14px; line-height:1.4; white-space:pre-wrap;
  }
  .user .bubble { background:#0b5; color:#fff; border-bottom-right-radius:0; }
  .bot .bubble { background:#06f; color:#fff; border-bottom-left-radius:0; }
  input#q {
    width:75%; padding:10px; border-radius:20px; border:1px solid #ccc; outline:none;
  }
  button#sendBtn {
    width:20%; padding:10px; border:none; background:#06f; color:#fff;
    border-radius:20px; cursor:pointer; font-weight:bold; transition:background 0.3s;
  }
  button#sendBtn:hover { background:#004bb5; }
</style>
</head>
<body>
<div class="container">
  <h2>TOC + Fun Chatbot 🤖</h2>
  <div id="chat"></div>
  <div style="display:flex;gap:5px;">
    <input id="q" placeholder="Type your message..." autofocus />
    <button id="sendBtn">Send</button>
  </div>
</div>
<script>
const chat = document.getElementById('chat');
const input = document.getElementById('q');
const sendBtn = document.getElementById('sendBtn');

function appendMessage(role, text) {
  const div = document.createElement('div');
  div.className = 'message ' + role;
  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;
  div.appendChild(bubble);
  chat.appendChild(div);
  chat.scrollTop = chat.scrollHeight;
}

async function sendMessage() {
  const q = input.value;
  if(!q) return;
  appendMessage('user', q);
  input.value = '';
  const res = await fetch('/api/chat', {
    method:'POST',
    headers:{'Content-Type':'application/json'},
    body: JSON.stringify({q})
  });
  const j = await res.json();
  appendMessage('bot', j.a);
}

sendBtn.addEventListener('click', sendMessage);
input.addEventListener('keypress', function(e){
  if(e.key === 'Enter') sendMessage();
});
</script>
</body>
</html>
"""

# ---------------------- Flask App ----------------------
app = None
if Flask is not None:
    app = Flask(__name__)
    bot = Chatbot()

    @app.route('/')
    def index():
        return render_template_string(_SIMPLE_HTML)

    @app.route('/api/chat', methods=['POST'])
    def api_chat():
        j = request.get_json() or {}
        q = j.get('q','')
        out = bot.handle(q)
        return jsonify(out)

# ---------------------- CLI Mode ----------------------
def repl_mode():
    print('TOC Chatbot CLI. Type exit to quit.')
    cb = Chatbot()
    while True:
        u = input('You: ')
        if u.strip().lower() in ['exit','quit']:
            break
        r = cb.handle(u)
        print('Bot:', r['a'])

if __name__ == '__main__':
    if Flask is not None:
        print('Starting web server on http://127.0.0.1:5000')
        app.run(debug=False)
    else:
        repl_mode()
