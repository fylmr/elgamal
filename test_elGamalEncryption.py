from unittest import TestCase
from elgamalDS_encryption import ElGamalEncryption
from elgamalDS_decryption import ElGamalDecryption


class TestElGamalSignature(TestCase):
    def try_signature(self, message):
        elgamalenc = ElGamalEncryption(message)

        elgamalenc.sign()

        publicKey = elgamalenc.publicKey
        signature = elgamalenc.signature

        elgamaldec = ElGamalDecryption(message, publicKey, signature)

        self.assertTrue(elgamaldec.check())

    def test_signatures(self):
        self.try_signature("Hello.")
        self.try_signature("Привет, это более длинная строка, чем раньше.")
        self.try_signature("Это строка на китайском языке: 你好吗")
