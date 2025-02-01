import unittest
from exercise.ch_01_01 import count_number_of_prime_numbers_up_to


class TestPrimeNumbers(unittest.TestCase):
    def test_negative_input(self):
        self.assertEqual(count_number_of_prime_numbers_up_to(-100), 0)

    def test_zero_input(self):
        self.assertEqual(count_number_of_prime_numbers_up_to(0), 0)

    def test_one_input(self):
        self.assertEqual(count_number_of_prime_numbers_up_to(1), 0)

    def test_two_input(self):
        self.assertEqual(count_number_of_prime_numbers_up_to(2), 1)

    def test_hundred_input(self):
        self.assertEqual(count_number_of_prime_numbers_up_to(100), 25)


if __name__ == '__main__':
    unittest.main()
