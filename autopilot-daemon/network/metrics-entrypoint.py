import os
import subprocess



def main():
    print("[[ NETWORK ]] Evaluating reachability of Multi-NIC CNI.")
    nodename = os.getenv("NODE_NAME")
    command = ['python3', './network/read_status.py', nodename]
    result = subprocess.run(command, capture_output=True, text=True)

    if result.stderr:
        raise SystemExit("Multi-NIC CNI health checker is not reachable - network reachability test cannot run")
    else:
        output = result.stdout
        print(output)

    
    if "OK" in output:
        print("[[ NETWORK ]] SUCCESS")
    else:
        print("[[ NETWORK ]] FAIL")
        print("Host ", os.getenv("NODE_NAME"))
        return 0

    connectable = output.split("Connectable network devices: ")[1]
    devices = int(connectable.split("/")[0])
    if devices == 2:
        lastline = nodename + " 1 1"
    elif devices == 1:
        lastline = nodename + " 1 0"
    elif devices == 0:
        lastline = nodename + " 0 0"
    else:
        lastline = "Cannot determine connectable devices"
    
    print("\n" + lastline)

if __name__ == '__main__':
    main()