from flask import Flask, send_file, request, jsonify, render_template
import openai

# Read the API key from a file
with open("api_key.txt", "r") as f:
    openai.api_key = f.read()

# Set up the Flask app
app = Flask(__name__, static_folder="web", static_url_path="/")

# Set up the chatbot messages
messages = [{"role": "system", "content": "You are a helpful and kind AI assistant."}]

# Define the route to serve the HTML file
@app.route("/")
def home():
    return send_file("web/index.html")

# Define the route to handle user input and return bot response
@app.route("/ask_bot", methods=["POST"])
def ask_bot():
    input_text = request.form.get("input_text")
    
    # Add the user message to the chat history
    messages.append({"role": "user", "content": input_text})

    # Generate a response from the chatbot
    chat = openai.ChatCompletion.create(model="davinci", messages=messages)
    reply = chat.choices[0].text

    # Add the chatbot response to the chat history
    messages.append({"role": "system", "content": reply})

    # Return the chatbot response to the frontend
    return jsonify({"response": reply})

# Run the Flask app
if __name__ == "__main__":
    app.run()
