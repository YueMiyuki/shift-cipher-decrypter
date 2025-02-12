from flask import Flask, render_template, request, jsonify
from shift_cipher import decrypt_message, validate_input, termination_event
import threading
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import queue

load_dotenv()

# Define static directory
app = Flask(
    __name__,
    static_url_path="",
    static_folder="web/static",
    template_folder="web/templates",
)

# Create a ThreadPoolExecutor
executor = ThreadPoolExecutor(max_workers=5)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/decrypt", methods=["POST"])
def decrypt():
    ciphertext = request.json["ciphertext"]

    if not validate_input(ciphertext):
        return (
            jsonify({"error": "Invalid input. Please enter text containing letters."}),
            400,
        )

    # Create a new queue for this specific request
    result_queue = queue.Queue()

    # Submit task to the executor
    future = executor.submit(process_decryption, ciphertext, result_queue)

    try:
        # Wait for result (with timeout)
        result = result_queue.get(timeout=30)
        return jsonify(result)
    except queue.Empty:
        # Cancel the future if it's still running
        future.cancel()
        termination_event.set()  # Signal early termination
        return jsonify({"error": "Decryption timeout"}), 408


def process_decryption(ciphertext, result_queue):
    try:
        # Directly call decrypt_message instead of using a global queue
        result = decrypt_message(ciphertext)
        result_queue.put(result)
    except Exception as e:
        result_queue.put({"error": str(e)})


# Define port and host to run the app on
port = os.environ.get("PORT", 5000)

# Run the app
if __name__ == "__main__":
    import logging
    from waitress import serve

    # Configure logging to display messages
    logging.basicConfig(level=logging.INFO)

    # Start the server with Waitress
    serve(app, host="0.0.0.0", port=port)
