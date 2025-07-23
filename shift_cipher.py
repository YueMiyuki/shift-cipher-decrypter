# ==========================================================================  
# Licensed under the GNU General Public License, Version 3 (the "License");
# You may not use this file except in compliance with the License.
# Song Hei Chi - 2025
# http://github.com/YueMiyuki
# ==========================================================================

# English dictionary for word validation
import enchant
# Import enchant to check if words are valid English words

english_dict = enchant.Dict("en_US")
# Create an English dictionary object for checking word validity

# English letter frequencies from Wikipedia
# https://en.wikipedia.org/wiki/Letter_frequency
ENGLISH_FREQUENCIES = {
    "E": 12.7,
    "T": 9.1,
    "A": 8.2,
    "O": 7.5,
    "I": 7.0,
    "N": 6.7,
    "S": 6.3,
    "H": 6.1,
    "R": 6.0,
    "L": 4.0,
    "D": 4.3,
    "C": 2.8,
    "U": 2.8,
    "M": 2.4,
    "W": 2.4,
    "F": 2.2,
    "G": 2.0,
    "Y": 2.0,
    "P": 1.9,
    "B": 1.5,
    "V": 0.98,
    "K": 0.77,
    "J": 0.15,
    "X": 0.15,
    "Q": 0.095,
    "Z": 0.074,
}

# Custom sum function
def c_sum(iterable):
    total = 0
    for x in iterable:
        total += x
    return total

# Custom any function
def c_any(iterable):
    for x in iterable:
        if x:
            return True
    return False

# Custom min function
def c_min(a, b):
    return a if a < b else b

# Custom random sampling (Fisher-Yates shuffle, then take first k)
def sample(seq, k):
    seq = list(seq)
    n = len(seq)
    # Simple deterministic shuffle using a hash of the sequence and k
    # (not cryptographically secure, but avoids random module)
    for i in range(n - 1, 0, -1):
        j = (i * 7 + k * 13) % (i + 1)
        seq[i], seq[j] = seq[j], seq[i]
    return seq[:k]

# Custom c_isalpha
def c_isalpha(char):
    """
    Check if a character is alphabetic (a-z or A-Z).
    """
    return ("a" <= char <= "z") or ("A" <= char <= "Z")

# Custom c_case
def c_case(char, to_upper=False):
    """
    Convert a character to lowercase or uppercase based on the given flag.
    """
    if "A" <= char <= "Z" and not to_upper:
        return chr(ord(char) + 32)
    elif "a" <= char <= "z" and to_upper:
        return chr(ord(char) - 32)
    return char

def shift_char(char, shift):
    """
    Shift a single character by a specified number of positions in the alphabet.
    """
    if "a" <= char <= "z":
        return chr((ord(char) - ord("a") + shift) % 26 + ord("a"))
    elif "A" <= char <= "Z":
        return chr((ord(char) - ord("A") + shift) % 26 + ord("A"))
    return char

def decrypt(text, shift):
    """
    Decrypt a given text using a Caesar cipher with the specified shift.
    """
    return "".join(shift_char(char, -shift) for char in text)

# Custom letter counting
def count_letters(text):
    """
    Count the frequency of letters in the given text.
    """
    freq = {}
    for char in text:
        if c_isalpha(char):
            c = c_case(char, to_upper=True)
            if c in freq:
                freq[c] += 1
            else:
                freq[c] = 1
    total = c_sum(freq.values())
    return {k: (v / total * 100) for k, v in freq.items()} if total > 0 else {}

def calculate_frequency_score(frequencies):
    """
    Calculate a score based on letter frequency in the decrypted text.
    """
    max_sum = c_sum(ENGLISH_FREQUENCIES.values())
    total_difference = 0.0
    for letter, freq in frequencies.items():
        english_freq = ENGLISH_FREQUENCIES.get(letter, 0.0)
        total_difference += abs(freq - english_freq)
    score = ((max_sum - total_difference) / max_sum) * 100
    return max(0.0, min(100.0, score))

def analyze_text(text):
    """
    Analyze the given text by calculating letter frequencies and a frequency score.
    """
    frequencies = count_letters(text)
    score = calculate_frequency_score(frequencies)
    return frequencies, score

def validate_decryption(decrypted, sample_size=10, threshold=0.7):
    """
    Validate the decrypted text by checking the percentage of valid English words.
    """
    all_words = decrypted.split()
    cleaned_words = []
    valid_flags = []
    for word in all_words:
        cleaned = "".join([c for c in word if c_isalpha(c)]).lower()
        cleaned_words.append(cleaned)
        is_valid = english_dict.check(cleaned) if cleaned else False
        valid_flags.append(is_valid)
    if not cleaned_words:
        return (False, False, [])
    has_any_valid = c_any(valid_flags)
    words_to_check = c_min(sample_size, len(cleaned_words))
    if len(cleaned_words) > sample_size:
        sampled_indices = sample(range(len(cleaned_words)), words_to_check)
    else:
        sampled_indices = list(range(len(cleaned_words)))
    valid_count = c_sum(valid_flags[i] for i in sampled_indices)
    valid_percentage = valid_count / words_to_check if words_to_check > 0 else 0
    return (valid_percentage >= threshold, has_any_valid, valid_flags)

def decrypt_with_shift(ciphertext, shift):
    """
    Decrypt the ciphertext with a specific shift and analyze the result.
    """
    # No early termination event needed in sequential version
    decrypted = decrypt(ciphertext, shift)
    frequencies = count_letters(decrypted)
    score = calculate_frequency_score(frequencies)
    is_valid, has_any_valid, valid_words_info = validate_decryption(decrypted)
    result = {
        "shift": shift,
        "decrypted": decrypted,
        "frequencies": frequencies,
        "score": score,
        "is_valid": is_valid,
        "has_any_valid": has_any_valid,
        "valid_words_info": valid_words_info,
    }
    return result

def decrypt_message(ciphertext):
    """
    Decrypt a message using the Caesar cipher and analyze the results.
    """
    # No need to clear a termination event in sequential version
    original_frequencies, original_score = analyze_text(ciphertext)
    results = []
    # Sequentially try all 26 possible shifts
    for shift in range(26):
        result = decrypt_with_shift(ciphertext, shift)
        if result:
            results.append(result)
    results.sort(
        key=lambda x: (
            x["is_valid"],
            c_sum(x["valid_words_info"]) if not x["is_valid"] else 0,
            x["score"]
        ),
        reverse=True
    )
    best_match = results[0] if results else None
    response = {
        "original_frequencies": original_frequencies,
        "original_score": original_score,
        "results": results,
        "best_match": best_match,
    }
    if best_match:
        response["status"] = "success"
        if best_match["is_valid"]:
            response["message"] = (
                f"Successfully decrypted with shift {best_match['shift']} (high confidence)"
            )
        else:
            response["message"] = (
                f"Possible decryption found with shift {best_match['shift']} (low confidence)"
            )
    else:
        response["status"] = "error"
        response["message"] = "Unable to find any decryption results."
    return response

def validate_input(text):
    """
    Validate the input text to ensure it contains at least some alphabetic characters.
    """
    for char in text:
        if c_isalpha(char):
            return True
    return False

# Miyuki Yue, 2025
# https://github.com/YueMiyuki
