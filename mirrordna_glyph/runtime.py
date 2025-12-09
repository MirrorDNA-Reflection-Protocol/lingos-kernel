"""
Glyph Execution Runtime - The Engine.
"""
import logging
from typing import List, Any
from .core import GlyphPacket
from .registry import GlyphRegistry
from .crypto import SovereignKey

logger = logging.getLogger("lingos.runtime")

class ExecutionResult:
    def __init__(self, success: bool, output: Any = None, error: str = None):
        self.success = success
        self.output = output
        self.error = error
    
    def __repr__(self):
        status = "✅" if self.success else "❌"
        return f"{status} result={self.output} error={self.error}"

class GlyphRuntime:
    """
    The secure execution environment for Glyph Packets.
    """
    def __init__(self, authorized_keys: List[str]):
        self.authorized_keys = set(authorized_keys)

    def execute_packet(self, packet: GlyphPacket) -> List[ExecutionResult]:
        """
        1. Verify Signature
        2. Check Authorization
        3. Execute Glyphs
        """
        # 1. Verify Signature Integrity
        if not packet.verify():
            return [ExecutionResult(False, error="Invalid Signature")]

        # 2. Check Authorization (Sovereignty)
        if packet.source not in self.authorized_keys:
             return [ExecutionResult(False, error=f"Unauthorized Key: {packet.source}")]

        results = []
        # 3. Execute Payload
        for glyph in packet.payload:
            handler = GlyphRegistry.get_handler(glyph.id)
            
            if not handler:
                results.append(ExecutionResult(False, error=f"Unknown Glyph: {glyph.id}"))
                continue
            
            try:
                # Execute the bound function with params
                output = handler(*glyph.params)
                results.append(ExecutionResult(True, output=output))
            except Exception as e:
                logger.error(f"Execution failed for {glyph.id}: {e}")
                results.append(ExecutionResult(False, error=str(e)))
        
        return results
