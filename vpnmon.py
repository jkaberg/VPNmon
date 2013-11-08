# Created by jkaberg, https://github.com/jkaberg
import socket
import fcntl
import struct
import os
import re

### Requirements!
# First line in .rtorrent.rc needs to be the bind value, for example: bind = 192.168.1.1
# Python 2.6

### Settings
ip_range = "178.132"
intf = "tun0"
settings_file = "/home/joel/.rtorrent.rc"
exec_cmd = "service bittorrent restart"

# Fetches the IP of given interface
def intf_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def read_addr(cfg_file):
    f = open(cfg_file)
    first_line = f.readline()
    f.close()
    return ''.join(re.findall(r"\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}", first_line))

# Writes the new IP address to the config file
def write_addr(cfg_file, bind_addr):
    f = open(cfg_file)
    first_line, the_rest = f.readline(), f.read()
    t = open(cfg_file,"w")
    t.write(bind_addr + "\n")
    t.write(the_rest)
    t.close()
    return

def main():
    ip_addr = intf_addr(intf)
    if not ip_addr.startswith(ip_range) or read_addr(settings_file) != ip_addr:
        write_addr(settings_file, "bind = %s" % ip_addr)
        os.system(exec_cmd)

if __name__ == "__main__":
    main()