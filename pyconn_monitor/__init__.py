"""
pyconn-monitor: A Python library to monitor and log network connections of untrusted programs.
"""

__version__ = "0.1.0"

from .connection_monitor import monitor_connections

__all__ = [
    "monitor_connections",
]
