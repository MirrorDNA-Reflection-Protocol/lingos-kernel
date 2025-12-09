import sys
from mirrordna_glyph import SovereignKey, Glyph, GlyphPacket, GlyphRuntime

def main():
    print("⟡ LingOS Runtime (GEE) - Execution Test ⟡")
    print("-" * 50)
    
    # 1. Setup Identity
    print("[1] Initializing Sovereign Identity...")
    key = SovereignKey()
    print(f"    Key: {key.public_key_hex[:16]}...")
    
    # 2. Start Runtime (Authorized Mode)
    print("[2] Booting Glyph Runtime...")
    runtime = GlyphRuntime(authorized_keys=[key.public_key_hex])
    print("    Runtime Online. Access List Configured.")
    
    # 3. Create Command
    print("[3] Forming Intent: 🛡️[SYSTEM_STATUS]")
    glyph = Glyph(id="🛡️[SYSTEM_STATUS]", params=[])
    
    packet = GlyphPacket(
        source=key.public_key_hex,
        nonce=1,
        payload=[glyph]
    )
    
    # 4. Sign
    print("[4] Signing Packet...")
    packet.sign(key)
    
    # 5. Execute
    print("[5] Injecting into Runtime...")
    results = runtime.execute_packet(packet)
    
    # 6. Report
    print("-" * 50)
    for i, res in enumerate(results):
        print(f"Result {i+1}: {res}")
        if res.success:
            print(f"    Output: {res.output}")
            print("    ✅ KERNEL EXECUTION SUCCESSFUL")
        else:
            print(f"    ❌ ERROR: {res.error}")

if __name__ == "__main__":
    main()
