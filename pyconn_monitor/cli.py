
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# pyconn_monitor by ParisNeo
# A tool to monitor network connections of programs or Python scripts

"""
pyconn_monitor: Monitor network connections of programs or Python scripts

pyconn_monitor is a command-line tool that allows you to monitor and log network connections
made by a program or Python script during its execution. It can be useful for debugging,
security analysis, or simply understanding the network behavior of an application.

Usage:
    python cli.py <program_path> [-l <log_file>] [-p] [--suppress-local]

Options:
    <program_path>      Path to the program or Python script to be monitored
    -l, --log_file      Path to the log file where connections will be logged
    -p, --python        Indicate that the input is a Python script
    --suppress-local    Suppress logging of local connections
"""

import argparse
from .connection_monitor import monitor_connections
from ascii_colors import ASCIIColors
def main():
    parser = argparse.ArgumentParser(description='Monitor network connections of a program or Python script')
    parser.add_argument('program_path', help='Path to the program or Python script to be monitored')
    parser.add_argument('-l', '--log_file', help='Path to the log file where connections will be logged')
    parser.add_argument('-p', '--python', action='store_true', help='Indicate that the input is a Python script')
    parser.add_argument('-s', '--suppress-local', action='store_true', help='Suppress logging of local connections')
    args = parser.parse_args()
    if args.suppress_local:
        ASCIIColors.yellow("\n\nSuppressing all local communications\n\n")

    if args.python:
        monitor_python_script(args.program_path, args.log_file, args.suppress_local)
    else:
        monitor_executable(args.program_path, args.log_file, args.suppress_local)

def monitor_python_script(script_path, log_file, suppress_local):
    # Code to monitor network connections from a Python script
    monitor_connections(f"python {script_path}", log_file, suppress_local=suppress_local)

def monitor_executable(program_path, log_file, suppress_local):
    monitor_connections(program_path, log_file, suppress_local=suppress_local)

if __name__ == '__main__':
    main()
