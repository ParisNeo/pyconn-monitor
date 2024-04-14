import psutil
import datetime
import os
import sys
import time
from multiprocessing import Process
from ascii_colors import ASCIIColors
import socket
import argparse

def get_hostname_and_ipv4(addr):
    if len(addr) == 0:
        return "", "", ""
    
    try:
        hostname, _, _ = socket.gethostbyaddr(addr[0])
    except (socket.herror, socket.gaierror):
        # If reverse lookup fails, use the IP address as the hostname
        hostname = addr[0]

    # Convert IPv6 address to IPv4 format if needed
    ipv4_addr = addr[0]
    port_number = addr[1]  # Get the port number from the address tuple

    if ':' in ipv4_addr:
        # IPv6 address, try to convert to IPv4 format
        try:
            ipv4_addr = socket.inet_ntop(socket.AF_INET, socket.inet_pton(socket.AF_INET6, ipv4_addr))
        except (ValueError, OSError):
            pass

    return hostname, ipv4_addr, port_number


def get_process_name(script_cmd):
    if sys.platform == 'win32':
        # On Windows, processes are always shown with .exe extension
        script_name = os.path.basename(script_cmd.split()[0])
        return f"{script_name}.exe"
    else:
        # On other platforms, use the script name as is
        return os.path.basename(script_cmd.split()[0])

def find_process(process_name, script_cmd):
    # Search for the process with the matching command line
    for p in psutil.process_iter(['name', 'cmdline']):
        if p.info['name'] == process_name and ' '.join(p.info['cmdline']) == script_cmd:
            print(f"Found with script name: {script_cmd}")
            return p
    return None

def get_conn_status_str(status_code):
    """
    Convert a numeric connection status code to a string representation.
    """
    status_map = {
        psutil.CONN_ESTABLISHED: "ESTABLISHED",
        psutil.CONN_SYN_SENT: "SYN_SENT",
        psutil.CONN_SYN_RECV: "SYN_RECV",
        psutil.CONN_FIN_WAIT1: "FIN_WAIT1",
        psutil.CONN_FIN_WAIT2: "FIN_WAIT2",
        psutil.CONN_TIME_WAIT: "TIME_WAIT",
        psutil.CONN_CLOSE: "CLOSE",
        psutil.CONN_CLOSE_WAIT: "CLOSE_WAIT",
        psutil.CONN_LAST_ACK: "LAST_ACK",
        psutil.CONN_LISTEN: "LISTEN",
        psutil.CONN_CLOSING: "CLOSING",
    }
    return status_map.get(status_code, str(status_code))

def monitor_process(script_cmd, log_file, interval=1, suppress_local=False):
    process_name = get_process_name(script_cmd)
    print(f"Searching for process {process_name} with command line '{script_cmd}'...")

    # Search for the process until it's found
    process_found = False
    while not process_found:
        process = find_process(process_name, script_cmd)
        if process:
            pid = process.pid
            print(f"Process found with pid {pid}!")
            process_found = True
        else:
            time.sleep(interval)

    print("Starting to monitor new network connections...")
    existing_connections = set()

    with open(log_file, "a", encoding="utf-8") as log:
        log.write(f"Connections test log file\n")
        log.write(f"Testing program {process.cmdline()} with pid: {process.pid}\n" )
        while True:
            try:
                    
                    # Get the current network connections for the process
                    current_connections = set((conn.laddr, conn.raddr, conn.status) for conn in process.connections())

                    # Log new connections
                    new_connections = current_connections - existing_connections
                    for laddr, raddr, status in new_connections:
                        local_hostname, local_ipv4_addr, local_port_number = get_hostname_and_ipv4(laddr)
                        local_infos = f"{local_hostname} ({local_ipv4_addr}):{local_port_number}"
                        remote_hostname, remote_ipv4_addr, remote_port_number = get_hostname_and_ipv4(raddr)
                        remote_infos = f"{remote_hostname} ({remote_ipv4_addr}):{remote_port_number}"
                        # Determine the connection initiator
                        if len(raddr)>0 and laddr == raddr[0]:
                            initiator = "local"
                        elif len(raddr)>0:
                            initiator = "remote"  
                        else:
                            initiator = "unknown"  
                        # Skip logging for local to local connections if suppress_local is True
                        if suppress_local and remote_ipv4_addr == local_ipv4_addr:
                            continue                                             
                        # Get the connection status
                        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                        log_entry = f"{timestamp}: initiator: {initiator}, status: {get_conn_status_str(status)}, local: {local_infos}, remote: {remote_infos}"
                        ASCIIColors.red(log_entry)
                        log.write(log_entry + "\n")
                        log.flush()

                    # Update the set of existing connections
                    existing_connections = current_connections

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"Process with pid {pid} has terminated or cannot be accessed.")
                break

        time.sleep(interval)

def monitor_connections(script_cmd, log_file, interval=1, suppress_local=False):
    # Open the log file for writing
    log = open(log_file, 'w')

    # Create a separate process for monitoring connections
    monitor_process_ = Process(target=monitor_process, args=(script_cmd, log_file, interval, suppress_local))
    monitor_process_.start()

    # Run the script to be tested
    os.system(script_cmd)

    # Wait for the monitoring process to complete
    monitor_process_.join()

    log.close()  # Close the log file when the script exits

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Monitor connections.")
    parser.add_argument("script_cmd", help="Command to run the script.")
    parser.add_argument("log_file", help="Log file path.")
    parser.add_argument("--interval", type=float, default=1.0, help="Interval in seconds (default: 1.0).")
    parser.add_argument("--suppress-local", action="store_true", help="Suppress local connections.")

    args = parser.parse_args()

    monitor_connections(args.script_cmd, args.log_file, args.interval, args.suppress_local)
