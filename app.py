from flask import Flask, request, jsonify
import openai

app = Flask(__name__)

# Set your OpenAI API key here
openai.api_key = "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"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if 'message' not in data:
        return jsonify({'error': 'Missing "message" parameter'}), 400

    message = data['message']
    
    # Customize prompt and other parameters based on your requirements
    prompt = f"User: {message}\nAI:"
    
    # Send request to OpenAI API
    response = openai.Completion.create(
        engine="text-davinci-002",  # Choose the appropriate engine
        prompt=prompt,
        max_tokens=150,
        temperature=0.7
    )

    # Extract AI's reply from OpenAI's response
    reply = response['choices'][0]['text'].strip()

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
