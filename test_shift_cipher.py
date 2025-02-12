import unittest
import sys

sys.path.append("../")

from shift_cipher import (
    ccase,
    cisalpha,
    shift_char,
    decrypt,
    count_letters,
    calculate_frequency_score,
    validate_decryption,
    decrypt_with_shift,
)


class TestShiftCipher(unittest.TestCase):

    def test_ccase(self):
        self.assertEqual(ccase("A"), "a")
        self.assertEqual(ccase("a", to_upper=True), "A")
        self.assertEqual(ccase("1"), "1")

    def test_cisalpha(self):
        self.assertTrue(cisalpha("a"))
        self.assertTrue(cisalpha("Z"))
        self.assertFalse(cisalpha("1"))

    def test_shift_char(self):
        self.assertEqual(shift_char("a", 1), "b")
        self.assertEqual(shift_char("z", 1), "a")
        self.assertEqual(shift_char("A", 1), "B")

    def test_decrypt(self):
        self.assertEqual(decrypt("Khoor, Zruog!", 3), "Hello, World!")

    def test_count_letters(self):
        result = count_letters("Hello, World!")
        self.assertAlmostEqual(result["L"], 30.0, places=1)
        self.assertAlmostEqual(result["O"], 20.0, places=1)

    def test_calculate_frequency_score(self):
        frequencies = {"E": 12.7, "T": 9.1, "A": 8.2}
        score = calculate_frequency_score(frequencies)
        self.assertTrue(0 <= score <= 100)

    def test_validate_decryption(self):
        self.assertTrue(validate_decryption("This is a valid English sentence"))
        self.assertFalse(validate_decryption("Xlmw mw rsx e zepmh Irkpmwl wirxirgi"))

    def test_decrypt_with_shift(self):
        result = decrypt_with_shift("Khoor, Zruog!", 3)
        self.assertEqual(result["decrypted"], "Hello, World!")
        self.assertTrue(result["is_valid"])


if __name__ == "__main__":
    unittest.main()
