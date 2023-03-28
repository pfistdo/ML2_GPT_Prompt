from flask import Flask, request, render_template
import openai

# Read the API key from a file
with open("api_key.txt", "r") as f:
    openai.api_key = f.read()

# Initialize the Flask app
app = Flask(__name__, static_folder="web", static_url_path="/")

# Set up the chatbot messages
messages = [{"role": "system", "content": "You are a helpful and kind AI assistant."}]

# Define the chatbot route
@app.route('/chatbot')
def chatbot():
    # Get the user input from the query string
    input = request.args.get('input')

    # Add the user message to the chat history
    messages.append({"role": "user", "content": input})

    # Generate a response from the chatbot
    chat = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    reply = chat.choices[0].text

    # Add the chatbot response to the chat history
    messages.append({"role": "system", "content": reply})

    # Render the HTML template with the chatbot response
    return render_template('web/index.html', response=reply)

# Run the Flask app
if __name__ == '__main__':
    app.run()
