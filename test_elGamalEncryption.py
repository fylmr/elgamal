from unittest import TestCase
from elgamalDS_encryption import ElGamalSign
from elgamalDS_decryption import ElGamalSignatureChecker


class TestElGamalSignature(TestCase):
    def try_signature(self, message):
        elgamalenc = ElGamalSign(message)

        elgamalenc.sign()

        publicKey = elgamalenc.publicKey
        signature = elgamalenc.signature

        elgamaldec = ElGamalSignatureChecker(message, publicKey, signature)

        self.assertTrue(elgamaldec.check())

    def test_signatures(self):
        self.try_signature("Hello.")
        self.try_signature("Привет, это более длинная строка, чем раньше.")
        self.try_signature("Это строка на китайском языке: 你好吗")
