from flask import Flask, send_file, request, session
import openai

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
        session['messages'] = [{"role": "system", "content": "You are a helpful and kind AI assistant."}]
    messages = session['messages']
            
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "system", "content": reply})
        session['messages'] = messages
        return reply

if __name__ == "__main__":
    # Read the API key from a file
    with open("api_key.txt", "r") as f:
        openai.api_key = f.read()
    app.run()