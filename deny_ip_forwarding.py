import subprocess, os

def check_ip_forwarding_status():
    try:
        ipv4_forwarding = subprocess.run(['sysctl', '-n', 'net.ipv4.ip_forwarding'], text=True, capture_output=True)
        ipv6_forwarding = subprocess.run(['sysctl', '-n', 'net.ipv6.conf.all.forwarding'], text=True, capture_output=True)
        if ipv4_forwarding.stdout.strip() == "0" and ipv6_forwarding.stdout.strip() == "0":
            return True
        else:
            return False
    except subprocess.CalledProcessError:
        return False
    
def disable_ip_forwarding():
    try:
        set_ipv4_forwarding = subprocess.run(['sudo', 'sysctl', '-w', 'net.ipv4.ip_forward=0'], text=True, capture_output=True)
        set_ipv6_forwarding = subprocess.run(['sudo', 'sysctl', '-w', 'net.ipv6.conf.all.forwarding=0'], text=True, capture_output=True)
        return True
    except subprocess.CalledProcessError:
        return False
    
uid = os.getuid()

if __name__ == "__main__":
    if uid == 0:
        print("Verifying IP Forwarding Status")
        if check_ip_forwarding_status():
            print("IP Forwarding Is Already Disabled")
        else:
            print("IP Forwarding Is Not Disabled")
            if disable_ip_forwarding():
                print("IP Forwarding Has Been Successfully Disabled")
            else:
                print("Failed To Disable IP Forwarding")
    else:
        print("Run The Script As Root")
