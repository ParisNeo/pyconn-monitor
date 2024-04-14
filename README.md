# pyconn-monitor

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python Version](https://img.shields.io/badge/python-3.6+-blue.svg)](https://python.org)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

`pyconn-monitor` is a Python library and command-line tool that helps you monitor and log network connections made by untrusted programs or Python scripts. It can be useful for identifying potential data leaks or unauthorized communication with remote servers.

## Why Use pyconn-monitor?

When running untrusted or third-party programs on your system, it's essential to ensure that they're not secretly leaking sensitive data or establishing unauthorized connections with remote servers. `pyconn-monitor` provides a way to monitor and log all network connections made by a program or Python script, allowing you to identify and investigate any suspicious activity.

## Features

- Monitor network connections made by a program or Python script
- Log connection details (timestamp, local and remote addresses, connection status, etc.)
- Support for Windows and Unix-like operating systems
- Command-line interface for easy usage

## Installation

You can install `pyconn-monitor` using pip:

```
pip install pyconn-monitor
```

## Usage

### Command-line Interface

To monitor a program or Python script, use the `pyconn-monitor` command with the appropriate arguments:

```
pyconn-monitor <program_path> [-l <log_file>] [-p]
```

- `program_path`: Path to the program or Python script to be monitored.
- `-l`, `--log_file`: Path to the log file where connections will be logged (optional).
- `-p`, `--python`: Indicate that the input is a Python script.

Example usage:

```
# Monitor a program and log connections to connections.log
pyconn-monitor /path/to/program -l connections.log

# Monitor a Python script
pyconn-monitor /path/to/script.py -p -l connections.log

# You can use --suppress-local option or -s to remove local connections logging which may be useful to reduce the number of logged entries if your objective is to view external connections
pyconn-monitor /path/to/script.py -p -l connections.log -s

```

### Python Library

You can also use `pyconn-monitor` as a Python library:

```python
from pyconn_monitor import monitor_connections

# Monitor a program and log connections to connections.log
monitor_connections("/path/to/program", "connections.log")

# Monitor a Python script
monitor_connections("python /path/to/script.py", "connections.log")
```

Optionally you can suppress all local connections to vew only remote or unknown connections:

```python
from pyconn_monitor import monitor_connections

# Monitor a program and log connections to connections.log
monitor_connections("/path/to/program", "connections.log", suppress_local=True)

# Monitor a Python script
monitor_connections("python /path/to/script.py", "connections.log", suppress_local=True)
```

## Contributing

Contributions to `pyconn-monitor` are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request on the [GitHub repository](https://github.com/ParisNeo/pyconn-monitor).

## License

`pyconn-monitor` is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0).

See ya!
```

This README provides an overview of the `pyconn-monitor` application, its purpose, features, installation instructions, usage examples (both for the command-line tool and Python library), contribution guidelines, and license information.

Feel free to modify or expand the README as needed to better suit your project's requirements.