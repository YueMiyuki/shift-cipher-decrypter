# Shift Cipher Decrypter

This project implements a Shift Cipher Decrypter with a web-based user interface. It uses Python for the backend logic and HTML/CSS/JavaScript for the frontend.

## Features

- Decrypts shift ciphers (Caesar ciphers) automatically
- Uses letter frequency analysis for efficient decryption
- Validates decrypted words using an external dictionary API
- Provides a user-friendly web interface
- Supports drag-and-drop file input
- Displays multiple possible decryptions
- Allows downloading of decrypted text

## How it works

1. The program analyzes the frequency of letters in the ciphertext.
2. It tries decryption using the most common English letters first, improving efficiency.
3. For each attempt, it validates the first few words using a dictionary API.
4. It displays all possible decryptions, sorted by likelihood.
5. The user can select any of the displayed decryptions or download the suggested one.

## Dependencies

- Python 3.7+
- Flask
- Requests

## File Structure

- `app.py`: Main Flask application
- `shift_cipher.py`: Core decryption logic
- `web/`: Contains web application
  - `static/`: Contains static files
    - `css/`: Contains CSS Stylesheet
      - `style.css`: CSS Stylesheet
  - `templates/`: Contain HTML Template
    - `index.html`: Frontend code
    - `README.md`: Frontend documentation
- `flowchart/`: Contains flow chart .mermaid files
  - `*.mermaid`: Chart mermaid files
  - `svg/`: Contains svg files from the .mermaid files
    - `*.svg`: All mermaid charts
- `README.md`:  Main documentation
- `requirements.txt`: pip requirements
- `.gitignore`: Git ignore file
- `LICENSE`: License file
- `.env.example`: Environment example
- `test_shift_cipher.py`: Test the core decryption logic


## Setup
1. You need python installed
2. clone the repository:
```
git clone https://github.com/yuemiyuki/shift-cipher-decrypter
```
3. Start a python [venv](https://docs.python.org/3/library/venv.html)
If you are on bash:
```
python3 -m pip install venv
python3 -m venv ./venv
source ./venv/bin/activate
```
4. Install dependencies
```
pip install -r requirements.txt
```
5. Start the app
```
python app.py
```
6. Visit the address shown in the console

## Running the Tests
1. Run the following command:
```
python -m unittest test_shift_cipher.py
```

2. The test results will be displayed in the terminal. You should see output indicating which tests passed or failed.

## Understanding the Test Results

- If all tests pass, you'll see a message like "OK" followed by the number of tests run.
- If any tests fail, you'll see "FAILED" messages with details about which tests failed and why.
