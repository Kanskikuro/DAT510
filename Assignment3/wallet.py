from transaction import Transaction
import ecdsa
from ecdsa import SigningKey
import binascii


class Wallet:
    def __init__(self):
        self.private_key = self.generate_private_key()  # Hexadecimal private key
        self.public_key = self.get_public_key(
            self.private_key
        )  # Hexadecimal public key
        self.address = self.public_key  # Simplified address (using public key)

    def __str__(self):
        return (
            f"Wallet(address={self.address[:10]}..., "
            f"public_key={self.public_key[:10]}..., "
            f"private_key=****)"
        )

    @staticmethod
    def generate_private_key():
        """
        Generate a new ECDSA private key.

        Steps:
        - Use the ecdsa library to generate a new SigningKey using the SECP256k1 curve.
        - Convert the private key to bytes using to_string().
        - Convert the bytes to a hex string.
        - Return the hex string representation (utf-8) of the private key.
        """
        # TODO: Implement private key generation (Implemented!)

        # documentation from: https://pypi.org/project/ecdsa/
        # Assumes the signingkey is the private key in this scenario

        private_key = SigningKey.generate(curve=ecdsa.SECP256k1)
        private_key_string = private_key.to_string()
        private_key_hex = private_key_string.hex()

        return private_key_hex

    @ staticmethod
    def get_public_key(private_key_hex):
        """
        Derive the public key from the private key.

        Steps:
        - Convert the private key from hex to bytes.
        - Create a SigningKey object from the private key bytes.
        - Get the verifying key (public key) from the signing key.
        - Convert the public key to bytes using to_string().
        - Convert the bytes to a hex string.
        - Return the hex string representation (utf-8) of the public key.
        """
        # TODO: Implement public key derivation (Implemented!)

        private_key_bytes = bytes.fromhex(private_key_hex)
        signing_key = SigningKey.from_string(
            private_key_bytes, curve=ecdsa.SECP256k1)
        public_key = signing_key.verifying_key
        public_key_string = public_key.to_string()
        public_key_bytes = public_key_string.hex()

        return public_key_bytes

    def create_transaction(self, recipient_address, amount):
        """
        Create and sign a new transaction.

        Steps:
        - Create a Transaction object with the sender's address, recipient's address, and amount.
        - Include the sender's public key in the transaction.
        - Sign the transaction using the sender's private key.
        - Return the signed transaction.
        """
        # TODO: Implement transaction creation and signing (Implemented!)

        transaction_obj = Transaction(
            self.address, recipient_address, amount, self.public_key, self.private_key)
        transaction_obj.sign_transaction(self.private_key)
        #check for transaction.is_valid?
        return transaction_obj
