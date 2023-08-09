import subprocess

def get_open_ports():
    try:
        # Run netstat command to get open ports
        output = subprocess.check_output(["netstat", "-tuln"], universal_newlines=True)
        lines = output.strip().split('\n')[2:]
        open_ports = set()
        for line in lines:
            parts = line.split()
            if len(parts) >= 6 and parts[5] == "LISTEN":
                address = parts[3].split(':')
                if len(address) == 2 and (address[0] == "0.0.0.0" or address[0] == "::"):
                    port = address[1]
                    open_ports.add(port)
        return open_ports
    except subprocess.CalledProcessError:
        return set()

def add_ufw_rules(open_ports):
    for port in open_ports:
        try:
            subprocess.run(["sudo", "ufw", "allow", port], check=True)
            print(f"Added UFW rule to allow incoming traffic on port {port}")
        except subprocess.CalledProcessError:
            print(f"Failed to add UFW rule for port {port}")

if __name__ == "__main__":
    open_ports = get_open_ports()
    if open_ports:
        add_ufw_rules(open_ports)
    else:
        print("No open ports found.")
