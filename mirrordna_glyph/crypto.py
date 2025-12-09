"""
LingOS Sovereign Key Implementation
Uses Ed25519 via PyNaCl for high-speed signatures.
"""
from typing import Tuple
import nacl.signing
import nacl.encoding
import base64

class SovereignKey:
    """
    Represents a Sovereign Identity Key pair.
    Used to sign Glyph Packets.
    """
    def __init__(self, private_key_b64: str = None):
        if private_key_b64:
            # Load existing key
            raw_key = base64.b64decode(private_key_b64)
            self._signing_key = nacl.signing.SigningKey(raw_key)
        else:
            # Generate new Genesis key
            self._signing_key = nacl.signing.SigningKey.generate()
            
        self._verify_key = self._signing_key.verify_key
        
    @property
    def public_key_hex(self) -> str:
        """Returns hex-encoded public key (Identity ID)"""
        return self._verify_key.encode(encoder=nacl.encoding.HexEncoder).decode('utf-8')

    @property
    def private_key_b64(self) -> str:
        """Export private key for safe storage (base64)"""
        return base64.b64encode(self._signing_key.encode()).decode('utf-8')

    def sign(self, message: bytes) -> bytes:
        """Sign a binary message (packet payload)"""
        return self._signing_key.sign(message).signature

    @staticmethod
    def verify(public_key_hex: str, message: bytes, signature: bytes) -> bool:
        """
        Verify a signature against a public key ID.
        Returns True if valid, False otherwise.
        """
        try:
            verify_key = nacl.signing.VerifyKey(public_key_hex, encoder=nacl.encoding.HexEncoder)
            verify_key.verify(message, signature)
            return True
        except nacl.exceptions.BadSignatureError:
            return False
