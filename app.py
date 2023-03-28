from flask import Flask, send_file, request
import os

app = Flask(__name__, static_folder="web", static_url_path="/")

@app.route("/")
def hello_world():
    return send_file("web/index.html")

@app.route("/model/ask_gpt", methods=["POST"])
def ask_bot():
    if request.method == 'POST':
        input = request.form.get("query")
    return "Bot response"
  
if __name__ == "__main__":
    app.run()