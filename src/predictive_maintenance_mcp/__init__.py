"""
Predictive Maintenance MCP Server

A Model Context Protocol server for industrial machinery diagnostics,
vibration analysis, and predictive maintenance.

Installable as 'predictive-maintenance-mcp' from PyPI.
Package name: predictive_maintenance_mcp (mapped from src/ directory).
"""

__version__ = "0.12.0"
__author__ = "Luigi Gianpio Di Maggio"
__license__ = "MIT"


def main() -> None:
    """CLI entry point. Delegates to server.main()."""
    from .server import main as _main
    _main()


def __getattr__(name: str):
    """Lazy module-level __getattr__ for deferred imports."""
    if name == "mcp":
        from .server import mcp
        return mcp
    raise AttributeError(f"module 'predictive_maintenance_mcp' has no attribute {name!r}")


__all__ = ["mcp", "main", "__version__"]
