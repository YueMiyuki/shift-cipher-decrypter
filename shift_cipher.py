# ==========================================================================
# Licensed under the GNU General Public License, Version 3 (the "License");
# You may not use this file except in compliance with the License.
# Song Hei Chi - 2025
# http://github.com/YueMiyuki
# ==========================================================================
from collections import Counter

# Used for multi threading
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
import queue

# English dictionary for word validation
import enchant

# Global queue for decryption requests
decrypt_queue = queue.Queue()
# Event to signal early termination
termination_event = threading.Event()
# English dictionary for word validation
english_dict = enchant.Dict("en_US")

# English letter frequencies from Wikipedia
# https://en.wikipedia.org/wiki/Letter_frequency
ENGLISH_FREQUENCIES = {
    'E': 12.7, 'T': 9.1, 'A': 8.2, 'O': 7.5, 'I': 7.0, 
    'N': 6.7, 'S': 6.3, 'H': 6.1, 'R': 6.0, 'L': 4.0, 
    'D': 4.3, 'C': 2.8, 'U': 2.8, 'M': 2.4, 'W': 2.4,
    'F': 2.2, 'G': 2.0, 'Y': 2.0, 'P': 1.9, 'B': 1.5,
    'V': 0.98, 'K': 0.77, 'J': 0.15, 'X': 0.15,
    'Q': 0.095, 'Z': 0.074
}

# Precompute the maximum possible sum of differences
max_sum = sum(ENGLISH_FREQUENCIES.values()) + 100  # Sum of English frequencies plus 100% for non-English letters

def ccase(char, to_upper=False):
    """
    Convert a character to lowercase or uppercase based on the given flag.

    This function takes a single character and a boolean flag as input.
    If the flag is set to False (default), the function converts the character to lowercase.
    If the flag is set to True, the function converts the character to uppercase.

    Args:
        char (str): A single character to be converted.
        to_upper (bool, optional): A flag indicating whether to convert the character to uppercase.
                                   Defaults to False.

    Returns:
        str: The converted character. If the input character is already in the desired case,
             it is returned as is.
    """

    if 'A' <= char <= 'Z' and not to_upper:
        return chr(ord(char) + 32)
    elif 'a' <= char <= 'z' and to_upper:
        return chr(ord(char) - 32)
    return char

def cisalpha(char):
    """
    Check if a character is alphabetic (a-z or A-Z).

    This function determines whether the given character is an alphabetic
    letter, considering both lowercase and uppercase letters.

    Args:
        char (str): A single character to be checked.

    Returns:
        bool: True if the character is an alphabetic letter (a-z or A-Z),
              False otherwise.
    """

    return ('a' <= char <= 'z') or ('A' <= char <= 'Z')


def shift_char(char, shift):
    """
    Shift a single character by a specified number of positions in the alphabet.

    This function applies a Caesar cipher shift to a single character.
    It wraps around the alphabet if the shift goes beyond 'z' or 'Z'.

    Args:
        char (str): A single character to be shifted.
        shift (int): The number of positions to shift the character.
                     Positive values shift forward, negative values shift backward.

    Returns:
        str: The shifted character.

    Note:
        - Lowercase letters ('a' to 'z') are shifted within the lowercase alphabet.
        - Uppercase letters ('A' to 'Z') are shifted within the uppercase alphabet.
        - Non-alphabetic characters are returned unchanged.
    """

    if 'a' <= char <= 'z':
        return chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
    elif 'A' <= char <= 'Z':
        return chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
    return char


def decrypt(text, shift):
    """
    Decrypt a given text using a Caesar cipher with the specified shift.

    This function applies the reverse of the Caesar cipher encryption
    by shifting each character in the text backwards by the given shift value.

    Args:
        text (str): The encrypted text to be decrypted.
        shift (int): The number of positions each character should be shifted backwards.
                     This should be the same value used for encryption.

    Returns:
        str: The decrypted text.

    Note:
        Non-alphabetic characters remain unchanged.
        The function uses the shift_char() function to perform individual character shifts.
    """

    return ''.join(shift_char(char, -shift) for char in text)

def count_letters(text):
    """
    Count the frequency of letters in the given text.

    This function calculates the percentage frequency of each alphabetic
    character in the input text, ignoring case and non-alphabetic characters.

    Args:
        text (str): The input text to analyze.

    Returns:
        dict: A dictionary where keys are uppercase letters and values are
              their percentage frequencies in the text.

    Example:
        >>> count_letters("Hello, World!")
        {'H': 10.0, 'E': 10.0, 'L': 30.0, 'O': 20.0, 'W': 10.0, 'R': 10.0, 'D': 10.0}
    """

    counter = Counter(ccase(char) for char in text if cisalpha(char))
    total = sum(counter.values())
    return {k.upper(): (v / total * 100) for k, v in counter.items()}

def calculate_frequency_score(frequencies):
    """
    Calculate a score based on letter frequency in the decrypted text.

    This function compares the frequency of letters in the decrypted text
    to standard English frequencies and calculates a similarity score.

    Args:
        frequencies (dict): A dictionary containing letter frequencies
                            in the decrypted text.

    Returns:
        float: A score between 0 and 100, where 100 indicates a perfect
               match to standard English letter frequencies.

    Note:
        - The function uses a global ENGLISH_FREQUENCIES dictionary for comparison.
        - The score is calculated as a percentage of similarity, with adjustments
          to ensure it falls within the 0-100 range.
    """

    total_difference = 0.0
    for letter, freq in frequencies.items():
        english_freq = ENGLISH_FREQUENCIES.get(letter, 0.0)
        total_difference += abs(freq - english_freq)
    # Calculate the score, ensuring it's within 0-100
    score = ((max_sum - total_difference) / max_sum) * 100
    return max(0.0, min(100.0, score))

def analyze_text(text):
    """
    Analyze the given text by calculating letter frequencies and a frequency score.

    Args:
        text (str): The text to be analyzed.

    Returns:
        tuple: A tuple containing two elements:
               - frequencies (dict): Letter frequencies in the text.
               - score (float): The calculated frequency score.

    Note:
        This function uses the count_letters() and calculate_frequency_score()
        functions to perform the analysis.
    """

    frequencies = count_letters(text)
    score = calculate_frequency_score(frequencies)
    return frequencies, score

def validate_decryption(decrypted):
    """
    Validate a decrypted text by checking if it contains valid English words.

    This function checks if a significant portion of the words in the
    decrypted text are valid English words.

    Args:
        decrypted (str): The decrypted text to be validated.

    Returns:
        bool: True if the text is considered valid, False otherwise.

    Note:
        - For texts with more than 5 words, it checks the first 5 words.
        - For texts with 3-5 words, it checks the first 3 words.
        - For texts with 1-2 words, it checks all words.
        - The function uses a global english_dict object for word validation.
    """

    if len(decrypted.split()) > 5:
        words = [word.lower() for word in decrypted.split() if word.isalpha()]
        valid_words = sum(1 for word in words[:5] if english_dict.check(word))  # Check up to first 5 words
        return valid_words >= 5  # Consider valid if at least 5 words are valid
    # Case that fix short sentence
    elif len(decrypted.split()) <= 5 and len(decrypted.split()) > 2:
        words = [word.lower() for word in decrypted.split() if word.isalpha()]
        valid_words = sum(1 for word in words[:3] if english_dict.check(word))
        return valid_words >= 2
    elif len(decrypted.split()) <= 2:
        words = [word.lower() for word in decrypted.split() if word.isalpha()]
        valid_words = sum(1 for word in words[:2] if english_dict.check(word))
        return valid_words >= 1

# Function to decrypt with a specific shift and analyze the result
# This is used by the multithreading process to test each possible shift
def decrypt_with_shift(ciphertext, shift):
    """
    Decrypt the ciphertext with a specific shift and analyze the result.

    This function is designed to be used in a multithreading process to test
    each possible shift for decryption.

    Args:
        ciphertext (str): The text to be decrypted.
        shift (int): The number of positions to shift for decryption.

    Returns:
        dict: A dictionary containing the decryption result, including:
              - shift: The shift used for decryption.
              - decrypted: The decrypted text.
              - frequencies: Letter frequencies in the decrypted text.
              - score: The calculated frequency score.
              - is_valid: Boolean indicating if the decryption is valid.

    Note:
        - This function checks a global termination_event to allow early
          termination of the decryption process.
        - It uses the decrypt(), count_letters(), calculate_frequency_score(),
          and validate_decryption() functions.
    """

    if termination_event.is_set():
        return None
        
    decrypted = decrypt(ciphertext, shift)
    frequencies = count_letters(decrypted)
    score = calculate_frequency_score(frequencies)
    
    result = {
        'shift': shift,
        'decrypted': decrypted,
        'frequencies': frequencies,
        'score': score,
        'is_valid': validate_decryption(decrypted)
    }
    
    return result

def decrypt_message(ciphertext):
    """
    Decrypt a message using the Caesar cipher and analyze the results.

    This function orchestrates the entire decryption process, including
    multithreading to test all possible shifts.

    Args:
        ciphertext (str): The encrypted text to be decrypted.

    Returns:
        dict: A dictionary containing the decryption results, including:
              - original_frequencies: Letter frequencies in the original text.
              - original_score: Frequency score of the original text.
              - results: List of all decryption attempts and their analyses.
              - best_match: The most likely correct decryption.
              - status: 'success' if a valid decryption was found, 'error' otherwise.
              - message: A descriptive message about the decryption result.

    Note:
        - This function uses multithreading to test all 26 possible shifts concurrently.
        - It sorts the results based on validity and score to determine the best match.
        - The function uses a global termination_event to allow early termination.
    """

    # Reset termination event
    termination_event.clear()
    
    # Analyze original text
    original_frequencies, original_score = analyze_text(ciphertext)
    
    # Initialize results list
    results = []
    
    # Try all possible shifts using multithreading
    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_shift = {
            executor.submit(decrypt_with_shift, ciphertext, shift): shift 
            for shift in range(26)
        }
        
        for future in as_completed(future_to_shift):
            result = future.result()
            if result:
                results.append(result)
    
    # Sort results by score and validity
    results.sort(key=lambda x: (x['is_valid'], x['score']), reverse=True)
    
    # Find the best valid result
    best_match = results[0] if results else None
    
    response = {
        'original_frequencies': original_frequencies,
        'original_score': original_score,
        'results': results,  # Return all results
        'best_match': best_match
    }
    
    if best_match and best_match['is_valid']:
        response['status'] = 'success'
        response['message'] = f"Successfully decrypted with shift {best_match['shift']}"
    else:
        response['status'] = 'error'
        response['message'] = "Unable to find a valid decryption, but here is a result that have the highest confidence."
    
    return response

def validate_input(text):
    """
    Validate the input text to ensure it contains at least some alphabetic characters.

    Args:
        text (str): The input text to be validated.

    Returns:
        bool: True if the text contains at least one alphabetic character, False otherwise.

    Note:
        This function uses the cisalpha() function to check for alphabetic characters.
    """

    return any(cisalpha(char) for char in text)

# Queue processor function
# This runs in a separate thread to process decryption requests from the queue
def process_queue():
    """
    Process decryption requests from a queue in a separate thread.

    This function runs in a loop, continuously checking for and processing
    tasks from the decrypt_queue.

    Note:
        - The function uses a global decrypt_queue to receive tasks.
        - It will terminate when it receives a None task.
        - Each task is expected to be a tuple containing the ciphertext and a callback function.
        - The function calls decrypt_message() for each task and invokes the callback with the result.
        - Any exceptions during processing are caught and printed, but do not stop the queue processing.
    """

    while True:
        # Attempt to get a task from the queue with a timeout
        try:
            task = decrypt_queue.get(timeout=60)
        except queue.Empty:
            # Timeout occurred, continue waiting
            continue
        
        try:
            if task is None:  # Terminate the thread
                break
                
            ciphertext, callback = task
            result = decrypt_message(ciphertext)
            callback(result)
        except Exception as e:
            print(f"Error processing task: {e}")
        finally:
            # Mark the task as done, regardless of processing success
            decrypt_queue.task_done()

# Start queue processor thread
queue_thread = threading.Thread(target=process_queue, daemon=True)
queue_thread.start()

# Miyuki Yue, 2025
# https://github.com/YueMiyuki