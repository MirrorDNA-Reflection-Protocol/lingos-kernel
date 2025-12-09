"""
Standard Library of Core Glyphs.
"""
from .registry import GlyphRegistry

@GlyphRegistry.register("⟡[GENESIS]")
def genesis(version: str, mode: str):
    """Bootstrap the kernel."""
    return f"Kernel Bootstrapped. Version: {version}, Mode: {mode}"

@GlyphRegistry.register("⟡[ECHO]")
def echo(message: str):
    """Return the message (ping/pong)."""
    return f"ECHO: {message}"

@GlyphRegistry.register("🛡️[SYSTEM_STATUS]")
def system_status():
    """Report system health."""
    import platform
    return f"System OK. Running on {platform.system()} {platform.release()}"
