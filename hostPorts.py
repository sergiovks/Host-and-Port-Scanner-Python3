import subprocess
import re
import socket

def scan_ports(host, start_port, end_port):
    """Scan for open ports on the given host"""
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((host, port))
                open_ports.append(port)
        except:
            pass
    return open_ports

def get_networks():
    """Get a list of networks from the 'ip a' command output"""
    networks = []
    output = subprocess.check_output(['ip', 'a']).decode()
    for match in re.finditer(r'inet (\d+\.\d+\.\d+\.\d+)/\d+', output):
        network = match.group(1)
        if network != '127.0.0.1':
            networks.append(network)
    return networks

if __name__ == '__main__':
    # Scan ports for all networks found with 'ip a'
    networks = get_networks()
    for network in networks:
        print(f"Scanning ports for network {network}")
        open_ports = scan_ports(network, 1, 65535)
        if open_ports:
            print(f"Open ports on network {network}: {open_ports}")
        else:
            print(f"No open ports found on network {network}")
