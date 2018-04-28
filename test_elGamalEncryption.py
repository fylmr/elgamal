from unittest import TestCase
import elgamalDS
import logging


class TestElGamalSignature(TestCase):
    def test_signature(self):
        m1 = "Hello."

        elgamalenc = elgamalDS.ElGamalEncryption(m1)

        elgamalenc.sign()

        publicKey = elgamalenc.publicKey
        signature = elgamalenc.signature

        elgamaldec = elgamalDS.ElGamalDecryption(m1, publicKey, signature)

        self.assertTrue(elgamaldec.check())
