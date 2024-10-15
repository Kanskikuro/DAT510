from transaction import Transaction
import ecdsa
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
        # TODO: Implement private key generation
        pass

    @staticmethod
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
        # TODO: Implement public key derivation
        pass

    def create_transaction(self, recipient_address, amount):
        """
        Create and sign a new transaction.

        Steps:
        - Create a Transaction object with the sender's address, recipient's address, and amount.
        - Include the sender's public key in the transaction.
        - Sign the transaction using the sender's private key.
        - Return the signed transaction.
        """
        # TODO: Implement transaction creation and signing
        pass
