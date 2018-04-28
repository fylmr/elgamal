import logging
from unittest import TestCase
from elgamalDS import NumTheory


class TestNumTheory(TestCase):
    def setUp(self):
        self.numMethods = NumTheory()

    def test_inv_modulo(self):
        self.assertEqual(self.numMethods.inv_modulo(14, 17), 11)
        self.assertEqual(self.numMethods.inv_modulo(11, 17), 14)
        self.assertEqual(self.numMethods.inv_modulo(10032020090948682085,
                                                    15642007769692613422),
                         8523566402957105883)

        with self.assertRaises(ValueError):
            self.numMethods.inv_modulo(1, 1)

        with self.assertRaises(ZeroDivisionError):
            self.numMethods.inv_modulo(0, 0)

    def test_gcd(self):
        self.assertEqual(self.numMethods.gcd(17, 333333333333333333332), 1)
        self.assertEqual(self.numMethods.gcd(333333333333333333332, 17), 1)

        self.assertEqual(self.numMethods.gcd(165, 44), 11)

        with self.assertRaises(ZeroDivisionError):
            self.numMethods.gcd(0, 0)

    def test_jacobi(self):
        jacobi = self.numMethods.jacobi

        self.assertEqual(jacobi(219, 383), 1)
        self.assertEqual(jacobi(1001, 9907), -1)

        with self.assertRaises(ValueError):
            jacobi(2, 6)

        with self.assertRaises(ValueError):
            jacobi(3, -3)

    def test_solovay_strassen(self):
        ss = self.numMethods.solovay_strassen

        self.assertEqual(ss(1), False)
        self.assertEqual(ss(11), True)
        self.assertEqual(ss(101), True)

        self.assertEqual(ss(2_038_074_751), True)
        self.assertEqual(ss(1_299_721), True)
        self.assertEqual(ss(60_787), False)  # Псевдопростое Ферма

    def test_find_prime(self):
        ss = self.numMethods.solovay_strassen
        fp = self.numMethods.find_prime

        self.assertTrue(ss(fp()))

        self.assertTrue(len(str(fp(100))), 100)

    def test_find_primitive_root(self):
        fpr = self.numMethods.find_primitive_root

        self.assertIn(fpr(7), (3, 5))
        self.assertIn(fpr(11), (2, 6, 7, 8))

        with self.assertRaises(ValueError):
            fpr(14)
