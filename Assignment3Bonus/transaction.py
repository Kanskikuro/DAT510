from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from assignment2 import singleRat
import base64
import hashlib
import json
import ecdsa
from ecdsa import ECDH
# Transaction Class with Digital Signature
class Transaction:
    def __init__(
        self,
        sender_address,
        recipient_address,
        amount,
        sender_public_key=None,
        signature=None,
        encrypted_message=None,
        nonce=None,
        key=None
    ):
        self.sender_address  = (
            # Address of the sender (public key or wallet address)
            sender_address
        )
        self.recipient_address = recipient_address  # Address of the recipient
        self.amount = amount  # Amount to transfer
        self.sender_public_key = sender_public_key # Sender's public key (hex string)
        self.signature = signature  # Digital signature (hex string)
        self.encrypted_message = encrypted_message
        self.nonce = nonce
        self.key = key

    def __str__(self):
        return (
            f"Transaction(sender={self.sender_address[:10]}..., "
            f"recipient={self.recipient_address[:10]}..., "
            f"amount={self.amount}"
            f"encrypted_message={self.encrypted_message})"
        )
    def key_exchange(self,private_key):
        ecdh = ECDH(curve=ecdsa.SECP256k1)
        ecdh.private_key = private_key
        ecdh.public_key = self.sender_address
        ecdh.load_received_public_key_pem(self.recipient_address)
        secret = ecdh.generate_sharedsecret_bytes()
        return secret
        
    def encrypt_message(self, message):
        secret = self.key_exchange()
        cipher_text , nonce , key = singleRat(secret, message)
        self.nonce = nonce
        self.key = key
        return cipher_text

    def decrypt_message(self, message):
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=base64.b64decode(self.nonce))
        cipher_text = base64.b64decode(message)
        plaintext = cipher.decrypt(cipher_text)
        return plaintext.decode('utf-8')

    def to_dict(self):
        """
        Convert the transaction details to a dictionary format.
        This is useful for serialization and hashing.
        """
        return {
            "sender_address": self.sender_address,
            "recipient_address": self.recipient_address,
            "amount": self.amount,
            "encrypted_message": self.encrypted_message,
            "nonce": self.nonce,
        }

    def compute_hash(self):
        """
        Compute the SHA-256 hash of the transaction.

        Steps:
        - Convert the transaction dictionary to a JSON string with sorted keys.
        - Encode the string to bytes.
        - Compute the SHA-256 hash of the bytes.
        - Return the hexadecimal digest of the hash.
        """
        # TODO: Implement the hashing logic (Implemented!)
        transaction_string = json.dumps(self.to_dict(), sort_keys=True)
        transcation_encoded = transaction_string.encode("utf-8")
        transaction_sha256 = hashlib.sha256(transcation_encoded)
        return transaction_sha256.hexdigest()

    def sign_transaction(self, private_key):
        """
        Sign the transaction using the sender's private key.

        Steps:
        - Compute the hash of the transaction (self.compute_hash()).
        - Convert the private key from hex to bytes.
        - Create a SigningKey object using the private key and SECP256k1 curve.
        - Sign the transaction hash (utf-8) using deterministic ECDSA signing.
        - Convert the signature to a hex string (utf-8) and store it in self.signature.

        Note:
        - Use the sign_deterministic method to ensure consistent signatures for testing.
        """
        # TODO: Implement the signing logic (Implemented!)
        transaction_hash = self.compute_hash()
        private_key_bytes = bytes.fromhex(private_key)
        signing_key_obj = ecdsa.SigningKey.from_string(
            private_key_bytes, curve=ecdsa.SECP256k1)
        signature = signing_key_obj.sign_deterministic(
            transaction_hash.encode('utf-8'))
        self.signature = signature.hex()

    def is_valid(self):
        """
        Verify the transaction signature.

        Steps:
        - Check if the transaction is a mining reward (sender_address == "0").
          If so, return True.
        - Ensure that both the signature and sender's public key are present.
          If not, return False.
        - Convert the sender's public key and signature from hex to bytes.
        - Create a VerifyingKey object using the public key and SECP256k1 curve.
        - Compute the hash of the transaction.
        - Verify the signature using the verifying key and transaction hash (utf-8).
        - Return True if the signature is valid; otherwise, return False.

        Exception Handling:
        - If any error occurs during verification (e.g., invalid signature format),
          catch the exception and return False.
        """
        # TODO: Implement the verification logic (Implemented!)
        try:
            if self.sender_address == "0":
                return True

            if not self.signature or not self.sender_public_key:
                return False

            sender_public_key_bytes = bytes.fromhex(self.sender_public_key)
            signature_bytes = bytes.fromhex(self.signature)
            verifying_key_obj = ecdsa.VerifyingKey.from_string(
                sender_public_key_bytes, curve=ecdsa.SECP256k1)
            transaction_hash = self.compute_hash()
            verifying_key_obj.verify(
                signature_bytes, transaction_hash.encode('utf-8'))
            return True

        except (ecdsa.BadSignatureError, ValueError, TypeError):
            return False

