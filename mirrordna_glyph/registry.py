"""
Glyph Registry - Binding Meaning to Code.
"""
from typing import Callable, Dict, Any, List
import logging

logger = logging.getLogger("lingos.registry")

class GlyphRegistry:
    """
    Maps Glyph IDs (e.g., "⟡[GENESIS]") to executable Python functions.
    """
    _registry: Dict[str, Callable] = {}

    @classmethod
    def register(cls, glyph_id: str):
        """Decorator to register a function as a Glyph handler."""
        def decorator(func: Callable):
            cls._registry[glyph_id] = func
            return func
        return decorator

    @classmethod
    def get_handler(cls, glyph_id: str) -> Callable:
        """Retrieve the handler for a given Glyph ID."""
        return cls._registry.get(glyph_id)

    @classmethod
    def list_glyphs(cls) -> List[str]:
        return list(cls._registry.keys())
