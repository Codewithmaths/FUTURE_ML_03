from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(force=True)
    intent_name = req.get('queryResult', {}).get('intent', {}).get('displayName')

    # Sample intent handling:
    if intent_name == 'ask-weather':
        response_text = "It looks like rain today. The sky is gray."
    elif intent_name == 'greetings-and-wellbeing':
        response_text = "I'm fine, thank you for asking! How can I help you today?"
    else:
        response_text = "Sorry, I didn't quite understand that. Can you rephrase?"

    # Respond in Dialogflow-expected format
    return jsonify({'fulfillmentText': response_text})

if __name__ == '__main__':
    app.run(debug=True, port=5000)
