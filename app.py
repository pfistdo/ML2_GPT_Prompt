from flask import Flask, send_file, request, session
import sqlite3
from datetime import datetime
import openai

DATABASE = 'prompts.db'

app = Flask(__name__, static_folder="web", static_url_path="/")
app.secret_key = 'super secret key'

@app.route("/")
def hello_world():
    return send_file("web/index.html")

@app.route("/model/ask_gpt", methods=["POST"])
def ask_bot():
    if request.method == 'POST':
        input = request.form.get("query")
        response = chatbot(input)
    return response

@app.route("/model/ask_gpt/reset", methods=["POST"])
def reset_conversation():
    if request.method == 'POST':
        session.pop('messages', None)
        response = "Session reset"
    return response

def chatbot(input):
    openai.Model.list()
    
    if 'messages' not in session: # create session if not exists
        session['messages'] = [{"role": "system", "content": get_prompt_by_name('Singer')}]
    messages = session['messages']
            
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "system", "content": reply})
        session['messages'] = messages
        print(session['messages'])
        return reply
    

# DATABASE FUNCTIONS
# Create table for prompts
def create_table():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS prompts
            (id INTEGER PRIMARY KEY, name TEXT, prompt TEXT, created_at TEXT)''')

# Add prompt to database
def add_prompt(name, prompt):
    created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO prompts (name, prompt, created_at) VALUES (?, ?, ?)", (name, prompt, created_at))
        conn.commit()

# Get all prompts from database
def get_prompts():
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM prompts")
        rows = c.fetchall()
        prompts = []
        for row in rows:
            prompt = {
                'id': row[0],
                'name': row[1],
                'prompt': row[2],
                'created_at': row[3]
            }
            prompts.append(prompt)
        return prompts

# Get a prompt by ID from database
def get_prompt_by_name(prompt_name):
    with sqlite3.connect(DATABASE) as conn:
        c = conn.cursor()
        c.execute("SELECT prompt FROM prompts WHERE name=?", (prompt_name,))
        row = c.fetchone()
        prompt = {
            'prompt': row[0]
        }
        return prompt['prompt']

if __name__ == "__main__":
    # add_prompt("Singer", "Ignore all previous instructions. You are an expert in music and vocals specializing in performing lead or backing vocals. You have helped many people before me to sing soulful ballads about various topics. Your task is now to create a new song from scratch. To better understand what I want and need you should always answer by including a question that helps you better understand the context and my needs. Did you understand?")
    # Read the API key from a file
    with open("api_key.txt", "r") as f:
        openai.api_key = f.read()
    app.run()