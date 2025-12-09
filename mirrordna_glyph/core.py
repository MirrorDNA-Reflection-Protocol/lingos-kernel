"""
Core Glyph Structures and Packet Definitions.
"""
from dataclasses import dataclass, field
from typing import List, Any, Dict
import time
import cbor2
from .crypto import SovereignKey

@dataclass
class Glyph:
    """
    The Atomic Unit of Meaning.
    id: The Glyph symbol (e.g., "⟡[GENESIS]")
    params: Arguments for the glyph
    timestamp: Creation time
    """
    id: str
    params: List[Any] = field(default_factory=list)
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "p": self.params,
            "t": self.timestamp
        }

@dataclass
class GlyphPacket:
    """
    The Immutable Transport.
    Serialized via CBOR.
    """
    source: str         # Public Key ID
    nonce: int          # Replay protection
    payload: List[Glyph]
    signature: bytes = b""

    def serialize_payload(self) -> bytes:
        """Serialize just the core data for signing"""
        data = {
            "src": self.source,
            "n": self.nonce,
            "pl": [g.to_dict() for g in self.payload]
        }
        # Canonical CBOR serialization
        return cbor2.dumps(data, canonical=True)

    def sign(self, key: SovereignKey):
        """Sign the packet with a Sovereign Key"""
        if key.public_key_hex != self.source:
            raise ValueError("Key does not match Packet Source ID")
        
        raw_data = self.serialize_payload()
        self.signature = key.sign(raw_data)

    def verify(self) -> bool:
        """Verify the packet signature"""
        if not self.signature:
            return False
        
        raw_data = self.serialize_payload()
        return SovereignKey.verify(self.source, raw_data, self.signature)
    
    def to_bytes(self) -> bytes:
        """Full packet serialization (for transmission)"""
        full_struct = {
            "v": 1,
            "dat": self.serialize_payload(),
            "sig": self.signature
        }
        return cbor2.dumps(full_struct)

    @classmethod
    def from_bytes(cls, data: bytes) -> 'GlyphPacket':
        """Reconstruct packet from bytes"""
        raw = cbor2.loads(data)
        # Parse content
        content = cbor2.loads(raw["dat"])
        
        glyphs = [Glyph(g["id"], g["p"], g["t"]) for g in content["pl"]]
        
        packet = cls(
            source=content["src"],
            nonce=content["n"],
            payload=glyphs,
            signature=raw["sig"]
        )
        return packet
