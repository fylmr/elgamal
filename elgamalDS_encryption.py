import logging
import random
from numtheory import NumTheory


class ElGamalEncryption:
    def __init__(self, message):
        logging.basicConfig(format='%(levelname)s, %(lineno)d: %(message)s', level=logging.INFO)
        logging.debug("Started El Gamal Encryption.")

        self.numTheory = NumTheory()

        self.message = message
        self.messageHash = self.numTheory.hash(message)

        keys = self.generate_keys()
        self.p = keys[0][0]
        self.g = keys[0][1]
        self.b = keys[0][2]

        self.x = keys[1]

        self.publicKey = (self.g, self.b, self.p)
        self.signature = (None, None)

    def generate_keys(self, iNumBits=256, iConfidence=32):
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

        x = random.randint(1, (p - 1))

        b = self.numTheory.modexp(g, x, p)

        publicKey = (p, g, b)
        privateKey = x

        return publicKey, privateKey

    def check_message_len(self, M):
        if M >= self.p:
            raise ValueError("Message is longer than modulo.")

    def sign(self):
        h = self.messageHash
        self.check_message_len(h)

        # Generating r: r < p-1, gcd(r, p-1) = 1
        r = random.randint(0, self.p - 2)
        while self.numTheory.gcd(r, self.p - 1) != 1:
            r = random.randint(0, self.p - 1)

        # Calculating y = g^r mod p
        y = self.numTheory.modexp(self.g, r, self.p)

        # s = (message - a^y)(r^-1) mod p-1
        rInv = self.numTheory.inv_modulo(r, self.p - 1)
        s = ((h - self.x * y) * rInv) % (self.p - 1)

        self.signature = (y, s)
