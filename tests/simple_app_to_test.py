import socket
import time

def main():
    # Connect to Google's DNS server
    dns_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dns_conn.connect(("8.8.8.8", 53))
    time.sleep(5)  # Keep the connection open for 5 seconds
    dns_conn.close()

    # Connect to a website
    website_conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    website_conn.connect(("www.example.com", 80))
    time.sleep(5)  # Keep the connection open for 5 seconds
    website_conn.close()

if __name__ == "__main__":
    main()
