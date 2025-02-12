from flask import Flask, render_template, request, jsonify
from shift_cipher import decrypt_queue, validate_input
import threading
import os
from dotenv import load_dotenv

load_dotenv()

# Define static directory
app = Flask(__name__,
            static_url_path='', 
            static_folder='web/static',
            template_folder='web/templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/decrypt', methods=['POST'])
def decrypt():
    ciphertext = request.json['ciphertext']
    
    if not validate_input(ciphertext):
        return jsonify({'error': 'Invalid input. Please enter text containing letters.'}), 400
    
    # Create an Event to wait for the result
    result_ready = threading.Event()
    result = {}
    
    def callback(decrypt_result):
        nonlocal result
        result = decrypt_result
        result_ready.set()
    
    # Add task to queue
    decrypt_queue.put((ciphertext, callback))
    
    # Wait for result (with timeout)
    if not result_ready.wait(timeout=30):
        return jsonify({'error': 'Decryption timeout'}), 408
    
    if 'error' in result:
        return jsonify(result), 400
        
    return jsonify(result)

# Define port and host to run the app on
port = os.environ.get('PORT', 5000)

# Run the app
# Define port and host to run the app on
if __name__ == "__main__":
    import logging
    from waitress import serve
    # Configure logging to display messages
    logging.basicConfig(level=logging.INFO)
    
    # Start the server with Waitress
    serve(app, host="0.0.0.0", port=port)