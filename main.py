import openai

openai.api_key = "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"
openai.Model.list()

messages = [{"role": "system", "content": "You are a helpful and kind AI assistant."}]

def chatbot(input):
    if input:
        messages.append({"role": "user", "content": input})
        chat = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo", messages=messages
        )
        reply = chat.choices[0].message.content
        messages.append({"role": "system", "content": reply})
        return reply

response = chatbot("Tu mangi pollo?")
print(response)