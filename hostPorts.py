import subprocess
import re
import socket

def banners():
    print("""
    *********************************************
        Host and TCP-UDP Port Scanner
        Author: sergiovks
    *********************************************
    """)
banners

def scan_ports(host, start_port, end_port, protocol='tcp'):
    """Scan for open ports on the given host and protocol"""
    open_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if protocol == 'tcp':
                    s.connect((host, port))
                else:
                    s.sendto(b'', (host, port))
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
        tcp_open_ports = scan_ports(network, 1, 65535, protocol='tcp')
        udp_open_ports = scan_ports(network, 1, 65535, protocol='udp')
        if tcp_open_ports:
            print(f"Open TCP ports on network {network}: {tcp_open_ports}")
        else:
            print(f"No open TCP ports found on network {network}")
        if udp_open_ports:
            print(f"Open UDP ports on network {network}: {udp_open_ports}")
        else:
            print(f"No open UDP ports found on network {network}")
