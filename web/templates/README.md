# Shift Cipher Decrypter Web UI

This directory contains the HTML template for the Shift Cipher Decrypter web application.

## Features

- Clean, responsive design
- Dark/Light mode toggle
- Drag-and-drop file input
- Interactive results table
- Download functionality for decrypted text

## Font

The web UI uses the [Roboto](https://fonts.google.com/specimen/Roboto) font from Google Fonts. It's a clean, modern sans-serif font that provides excellent readability across various screen sizes and resolutions.

## Special Features

1. **Dark/Light Mode Toggle**: The UI supports both dark and light modes, with automatic detection of the user's system preference.

2. **Responsive Design**: The layout adjusts to different screen sizes for optimal viewing on desktop and mobile devices.

3. **Drag and Drop**: Users can drag and drop text files directly into the input area for easy cipher input.

4. **Interactive Results**: The possible decryptions are displayed in an interactive table, allowing users to click and view different decryption attempts.

5. **Multiple Decryption Candidates**: The UI displays up to 8 possible decryptions, ranked by their likelihood of being correct.

6. **Download Functionality**: Users can download the decrypted text as a .txt file.

7. **Accessibility**: The design considers accessibility, with appropriate color contrasts and semantic HTML structure.


## JavaScript Functionality

The JavaScript code handles:
- User interactions (button clicks, drag-and-drop)
- API calls to the backend for decryption
- Dynamic updating of the UI with decryption results
- Downloading of decrypted text
- Dark/Light mode toggling