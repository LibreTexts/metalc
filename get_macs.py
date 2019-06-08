#!python3
#
# pass in the chicks csv. This looks at the ip field for each row and adds
# rows for enp1s0 and enp2s0 and fills in their mac address
import sys
import csv
import paramiko
from getpass import getpass


# given output of running `ip addr` in the form of string
# gives the 'link/ether' of the given iface_name
def get_ether(ip_out, iface_name):
    beg = ip_out.find(iface_name)
    start = ip_out.find('link/ether', beg)
    end = ip_out.find('\n', start)
    return ip_out[start:end].split()[1]

def get_ip_output(ip_addr, passwd):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(ip_addr, username='spicy', password=passwd)
    inp, outp, errp = ssh.exec_command('ip addr')
    return outp.read().decode('utf-8')

if __name__ == "__main__":
    passwd = getpass("enter password of spicy:")
    ifaces = ['enp1s0', 'enp2s0']
    if len(sys.argv) < 2:
        print('usage: `./get_macs.py chicks.csv`')

    with open(sys.argv[1], 'r') as f:
        reader = csv.DictReader(f)
        fieldnames = reader.fieldnames
        for iface in ifaces:
            if iface not in fieldnames:
                fieldnames.append(iface)
        rows = []
        for row in reader:
            ip_output = get_ip_output(row['ip'], passwd)
            for iface in ifaces:
                row[iface] = get_ether(ip_output, iface)
            rows.append(row)

    with open(sys.argv[1], 'w') as f:
        writer = csv.DictWriter(f, fieldnames)
        writer.writeheader()
        writer.writerows(rows)

