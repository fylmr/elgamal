import logging
from numtheory import NumTheory


class ElGamalSignatureChecker:
    def __init__(self, message, publickey, signature):
        """
        ElGamal decryption client.

        :param message: string
        :param publickey: (g, b, p)
        :param signature: (y, s)
        """
        logging.debug("Started El Gamal Decryption.")

        hashFunc = NumTheory().hash

        self.publicKey = publickey
        self.signature = signature

        self.message = message
        self.messageHash = hashFunc(message)

    def check(self):
        """
        Checks if signature correct.

        :return: True or False
        """
        modexp = NumTheory.modexp

        g, b, p = self.publicKey
        y, s = self.signature
        h = self.messageHash

        # y, s < p
        if not (0 < y < p):
            return False
        if not (0 < s < p - 1):
            return False

        v1 = (modexp(y, s, p) * modexp(b, y, p)) % p
        v2 = modexp(g, h, p)

        if v1 == v2:
            return True
        else:
            return False
