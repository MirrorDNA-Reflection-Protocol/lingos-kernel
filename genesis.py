import sys
from mirrordna_glyph import SovereignKey, Glyph, GlyphPacket

def main():
    print("⟡ MirrorDNA LingOS Kernel - Genesis Sequence ⟡")
    print("-" * 50)
    
    # 1. Generate Identity
    print("[1] Generating Sovereign Identity...")
    key = SovereignKey()
    print(f"    Identity ID: {key.public_key_hex[:16]}...")
    
    # 2. Form Intent
    print("[2] Forming Genesis Glyph...")
    genesis_glyph = Glyph(
        id="⟡[GENESIS]",
        params=["version=0.1.0", "mode=sovereign"]
    )
    print(f"    Glyph: {genesis_glyph}")
    
    # 3. Create Packet
    print("[3] Creating Glyph Packet...")
    packet = GlyphPacket(
        source=key.public_key_hex,
        nonce=1,
        payload=[genesis_glyph]
    )
    
    # 4. Sign (The Sovereign Act)
    print("[4] Signing Packet (Ed25519)...")
    packet.sign(key)
    print(f"    Signature: {packet.signature.hex()[:16]}...")
    
    # 5. Serialize
    print("[5] Serializing Transport (CBOR)...")
    wire_data = packet.to_bytes()
    print(f"    Wire Size: {len(wire_data)} bytes")
    
    # 6. Verify (The Kernel Check)
    print("[6] Verify Packet Integrity...")
    
    # Reconstruct from wire
    received = GlyphPacket.from_bytes(wire_data)
    is_valid = received.verify()
    
    if is_valid:
        print("\n✅ GENESIS PACKET VERIFIED. SOVEREIGNTY ESTABLISHED.")
        print(f"    Executed: {received.payload[0].id}")
    else:
        print("\n❌ VERIFICATION FAILED.")

if __name__ == "__main__":
    main()
