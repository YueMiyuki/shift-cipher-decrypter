from flask import Flask, render_template, request, jsonify
# Import Flask and related modules for web app (serving, templating, API)
from shift_cipher import decrypt_message, validate_input
# Import decryption logic and helpers from the shift_cipher module
import os
# Import os for environment variable access (e.g., PORT)
from dotenv import load_dotenv
# Import dotenv for loading .env files into environment variables

load_dotenv()
# Load environment variables from .env file into the process environment

# Define static directory
app = Flask(
    __name__,
    # Name of the current module, used by Flask to locate resources
    static_url_path="",
    # URL path for static files (empty means root)
    static_folder="web/static",
    # Directory for static files (CSS, JS, images)
    template_folder="web/templates",
    # Directory for HTML templates (Jinja2)
)

@app.route("/")
def index():
    return render_template("index.html")
    # Render the index.html template for the root URL

@app.route("/decrypt", methods=["POST"])
def decrypt():
    ciphertext = request.json["ciphertext"]
    # Get ciphertext from JSON request body

    if not validate_input(ciphertext):
        # Validate input contains at least one letter
        return (
            jsonify({"error": "Invalid input. Please enter text containing letters."}),
            # Return error message as JSON if input is invalid
            400,
            # HTTP 400 Bad Request status code
        )

    # Sequentially process the decryption request and return the result directly
    try:
        result = decrypt_message(ciphertext)
        # Run the decryption logic and get the result directly (no background thread)
        return jsonify(result)
        # Return the result as a JSON response
    except Exception as e:
        return jsonify({"error": str(e)})
        # If an error occurs, return the error message as JSON

PORT = os.environ.get("PORT", 5000)
# Get the port number from the environment or use 5000 as default

if __name__ == "__main__":
    # Only run this block if the script is executed directly (not imported)
    import logging
    # Import logging for server logs
    from waitress import serve
    # Import waitress for running the production server

    logging.basicConfig(level=logging.INFO)
    # Set logging level to INFO so server logs are shown

    serve(app, host="0.0.0.0", port=PORT)
    # Run the Flask app using Waitress on all network interfaces and the specified port
