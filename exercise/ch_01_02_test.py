import unittest
from exercise.ch_01_02 import factorize, factors_to_latex


class TestFactorize(unittest.TestCase):
    def test_basic_composite_numbers(self):
        self.assertEqual(factorize(10), [2, 5])
        self.assertEqual(factorize(100), [2, 2, 5, 5])
        self.assertEqual(factorize(24), [2, 2, 2, 3])

    def test_prime_numbers(self):
        self.assertEqual(factorize(2), [2])
        self.assertEqual(factorize(11), [11])
        self.assertEqual(factorize(17), [17])

    def test_number_one(self):
        self.assertEqual(factorize(1), [])

    def test_large_numbers(self):
        self.assertEqual(factorize(999), [3, 3, 3, 37])
        self.assertEqual(factorize(1000), [2, 2, 2, 5, 5, 5])

    def test_repeated_prime_factors(self):
        self.assertEqual(factorize(8), [2, 2, 2])
        self.assertEqual(factorize(27), [3, 3, 3])


class TestFactorsToLatex(unittest.TestCase):
    """소인수분해 결과의 LaTeX 문자열 변환 테스트"""

    def test_basic_cases(self):
        """기본적인 변환 케이스 테스트"""
        self.assertEqual(factors_to_latex([]), '')
        self.assertEqual(factors_to_latex([2]), '2')
        self.assertEqual(factors_to_latex([2, 5]), '2 \\cdot 5')

    def test_power_notation(self):
        """거듭제곱 표기 테스트"""
        self.assertEqual(factors_to_latex([2, 2, 2]), '2^{3}')
        self.assertEqual(factors_to_latex([2, 2, 5, 5]), '2^{2} \\cdot 5^{2}')
        self.assertEqual(factors_to_latex([3, 3, 3, 37]), '3^{3} \\cdot 37')
        self.assertEqual(factors_to_latex(
            [2, 2, 2, 5, 5]), '2^{3} \\cdot 5^{2}'
        )


if __name__ == '__main__':
    unittest.main()
