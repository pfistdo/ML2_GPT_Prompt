from flask import Flask, send_file, request
import openai
import os

app = Flask(__name__, static_folder="web", static_url_path="/")

@app.route("/")
def hello_world():
    return send_file("web/index.html")

@app.route("/model/ask_gpt", methods=["POST"])
def ask_bot():
    if request.method == 'POST':
        input = request.form.get("query")
        print(input)
        response = chatbot(input)
    return response
  
def chatbot(input):


    openai.Model.list()

    messages = [{"role": "system", "content": "You are a helpful and kind AI assistant."}]
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "system", "content": reply})
        print("Reply: ", reply)
        return reply

if __name__ == "__main__":
    # Read the API key from a file
    with open("api_key.txt", "r") as f:
        openai.api_key = f.read()
    app.run()