import logging
import random


class NumTheory:

    def inv_modulo(self, a, m):
        """
        Get inverted number by modulo m
        :param a: number to inverse
        :param m: modulo
        :return:
        """

        if m == 0:
            raise ZeroDivisionError("Modulo should be greater than 2")
        if m - 2 < 0:
            raise ValueError("Modulo should be greater than 2")

        return self.modexp(a, m - 2, m)

    @staticmethod
    def gcd(a, b):
        logging.debug("GCD of {0} and {1}".format(a, b))

        if (a == 0 or b == 0):
            raise ZeroDivisionError("Args should not be zero")

        if a < b:
            a, b = b, a
        while b != 0:
            c = a % b
            a = b
            b = c

        logging.debug("GCD is {0}".format(a))
        return a  # a is returned if b == 0

    @staticmethod
    def modexp(base, exp, modulus):
        return pow(base, exp, modulus)

    def jacobi(self, a, n):
        """
        Computes the jacobi symbol of a/n.

        :param a: numerator
        :param n: denominator
        :return: integer from {-1, 0, 1}
        """

        if n <= 0:
            raise ValueError("n should be > 0")
        if n % 2 == 0:
            raise ValueError("n should be odd")

        if a == 0:
            if n == 1:
                return 1
            else:
                return 0
        # property 1 of the jacobi symbol
        elif a == -1:
            if n % 2 == 0:
                return 1
            else:
                return -1
        # if a == 1, jacobi symbol is equal to 1
        elif a == 1:
            return 1
        # property 4 of the jacobi symbol
        elif a == 2:
            if n % 8 == 1 or n % 8 == 7:
                return 1
            elif n % 8 == 3 or n % 8 == 5:
                return -1
        # property of the jacobi symbol:
        # if a = b mod n, jacobi(a, n) = jacobi( b, n )
        elif a >= n:
            return self.jacobi(a % n, n)
        elif a % 2 == 0:
            return self.jacobi(2, n) * self.jacobi(a // 2, n)
        # law of quadratic reciprocity
        # if a is odd and a is coprime to n
        else:
            if a % 4 == 3 and n % 4 == 3:
                return -1 * self.jacobi(n, a)
            else:
                return self.jacobi(n, a)

    def solovay_strassen(self, num, iConfidence=32):
        """
        Solovay-Strassen primality test.

        :param num: number to be tested
        :param iConfidence: times to repeat test
        :return: bool
        """
        logging.info("Testing {0} for primality ".format(num))

        if num == 1:
            return False

        for i in range(iConfidence):
            a = random.randint(1, num - 1)

            # if a is not relatively prime to n, n is composite
            if self.gcd(a, num) > 1:
                logging.info("{0} is composite".format(num))
                return False

            # declares n prime if jacobi(a, n) is congruent to a^((n-1)/2) mod n
            if not self.jacobi(a, num) % num == self.modexp(a, (num - 1) // 2, num):
                logging.info("{0} is composite".format(num))
                return False

        # if there have been t iterations without failure, num is believed to be prime
        logging.debug("{0} is prime".format(num))
        return True

    def find_prime(self, iNumBits=64, iConfidence=32):
        """
        Find n-bit prime.

        :param iNumBits: n
        :param iConfidence: Confidence that this is a prime number
        :return: p - a prime number
        """

        # keep testing until one is found
        while 1:
            # generate potential prime randomly
            p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))

            # make sure it is odd
            while p % 2 == 0:
                p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))

            # keep doing this if the SS-test fails
            while not self.solovay_strassen(p, iConfidence):
                p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))
                while p % 2 == 0:
                    p = random.randint(2 ** (iNumBits - 2), 2 ** (iNumBits - 1))

            # if p is prime compute p = 2*p + 1
            # if p is prime, we have succeeded; else, start over
            p = p * 2 + 1
            if self.solovay_strassen(p, iConfidence):
                return p

    def find_primitive_root(self, p):
        """
        finds a primitive root for prime p.

        :param p: modulo
        :return:
        """

        if not self.solovay_strassen(p):
            raise ValueError("p is not prime")

        if p == 2:
            return 1
        # the prime divisors of p-1 are 2 and (p-1)/2 because
        # p = 2x + 1 where x is a prime
        p1 = 2
        p2 = (p - 1) // p1

        # test random g's until one is found that is a primitive root mod p
        while (1):
            g = random.randint(2, p - 1)
            # g is a primitive root if for all prime factors of p-1, p[i]
            # g^((p-1)/p[i]) (mod p) is not congruent to 1
            if not (self.modexp(g, (p - 1) // p1, p) == 1):
                if not self.modexp(g, (p - 1) // p2, p) == 1:
                    return g


class ElGamalEncryption:
    def __init__(self):
        self.numTheory = NumTheory()

        keys = self.generate_keys()
        self.p = keys[0][0]
        self.g = keys[0][1]
        self.b = keys[0][2]

        self.x = keys[1]

    def generate_keys(self, iNumBits=64, iConfidence=32):
        """
        Generates public key (p, g, b) and private key x. \n

        p is the prime
        g is the primitive root
        b = g ^ x mod p

        x is random in [0, p-1]

        :param iNumBits:
        :param iConfidence:
        :return: ((p, g, b), x)
        """

        p = self.numTheory.find_prime(iNumBits, iConfidence)
        g = self.numTheory.find_primitive_root(p)
        g = self.numTheory.modexp(g, 2, p)  # todo check this

        x = random.randint(1, (p - 1) // 2)

        b = self.numTheory.modexp(g, x, p)

        publicKey = (p, g, b)
        privateKey = x

        return (publicKey, privateKey)

    def check_message_len(self, message):
        if len(str(message)) >= self.p:
            raise ValueError("Message is longer than modulo.")

    def sign(self, message):
        self.check_message_len(message)

        # Generating r: r < p-1, gcd(r, p-1) = 1
        r = random.randint(0, self.p - 1)
        while self.numTheory.gcd(r, self.p - 1) != 1:
            r = random.randint(0, self.p - 1)

        logging.debug("Generated r: {0}".format(r))

        # Calculating y = g^r mod p
        y = self.numTheory.modexp(self.g, r, self.p)

        logging.debug("Generated y: {0}".format(y))

        # Calculating s = (message - a^y)(r^-1) mod p-1
        rInv = self.numTheory.inv_modulo(r, self.p - 1)
        # noinspection PyArgumentList
        s = (message - pow(self.x, y, self.p - 1, self.p - 1)) * rInv % self.p - 1
