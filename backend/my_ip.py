import socket
import subprocess

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # doesn't even have to be reachable
        s.connect(('10.254.254.254', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_tailscale_ip():
    try:
        result = subprocess.check_output(['tailscale', 'ip']).decode("utf-8") # attempt to get tailscale ip address
    except Exception as e:
        return None
    
    if "command not found" in result: return None # tailscale not installed
    else: tailscale_ip = result.split()[0] # tailscale installed, get ip address from result

    if validate_ip(tailscale_ip): return tailscale_ip # if it's a valid ip address, return it
    
    return None # invalid ip address

def validate_ip(ip_address: str):
    try:
        socket.inet_aton(ip_address) # attempt to convert to binary
        return True # it worked, valid ip
    except socket.error: # it didn't work
        return False # invalid ip

if __name__ == '__main__':
    print("IP address: "+ get_local_ip() + " (local)" + (f" | {get_tailscale_ip()} (tailscale)" if get_tailscale_ip() else ''))