# A simple test for the library
from pyconn_monitor import monitor_connections

# Monitor a Python script
monitor_connections("python simple_app_to_test.py", "connections.log")
