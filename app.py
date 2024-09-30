from flask import Flask, request
app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "Telegram Marketing Bot is running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    update = request.get_json()
    # Process the update from Telegram bot
    return {"status": "ok"}, 200

if __name__ == '__main__':
    app.run(debug=True)
