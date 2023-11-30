from flask import Flask, request, jsonify
import openai
import json
app = Flask(__name__)
# Định nghĩa đường dẫn để đọc dữ liệu từ tệp JSON
DATA_FILE_PATH = './TAKA.product.json'

# Đọc dữ liệu từ tệp JSON
def read_json_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    return data
# Set your OpenAI API key here
openai.api_key = "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"
def generate_product_suggestions(json_data):
    # Filter products with quantity > 0
    available_products = [product for product in json_data if product['quantity'] > 0]

    # Generate a string describing the available products
    product_descriptions = [f"{product['name']} (còn lại {product['quantity']} sản phẩm, giá: {product['price']} đồng)" for product in available_products]
    product_suggestions = ', '.join(product_descriptions)

    return product_suggestions
@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()

    if 'message' not in data:
        return jsonify({'error': 'Missing "message" parameter'}), 400

    json_data = read_json_file(DATA_FILE_PATH)
    message = data['message']
    product_suggestions = generate_product_suggestions(json_data)
    promt_before= f'Bạn là AI assistant của TAKA, taka là nền tảng ecommerce lớn nhất việt nam, bạn sẽ nhận câu hỏi từ khách hàng và gợi ý các sản phẩm đang có trong taka đang có quantity >0. Dưới đây là tất cả các sản phẩm đang đang bán tại Taka: {product_suggestions}'
    # Customize prompt and other parameters based on your requirements
    prompt = f"User: {message} {json_data}\nAI:"
    
    # Send request to OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Choose the appropriate engine
        messages=[
        {"role": "system", "content": promt_before},
        {"role": "user", "content": message},
        ],
        max_tokens=3000,
        temperature=0.7
    )

    # Extract AI's reply from OpenAI's response
    reply = response['choices'][0]['message']['content'].strip()

    return jsonify({'reply': reply})

if __name__ == '__main__':
    app.run(debug=True)
