# Created by jkaberg, https://github.com/jkaberg
import socket
import fcntl
import struct
import os

### Settings
ip_range = "178.132"
intf = "tun0"
settings_file = "/home/joel/.rtorrent.rc"
exec_cmd = "service bittorrent restart"

# Fetches the IP of given interface
def intf_addr(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

# Writes the new IP address to the config file
def write_addr(cfg_file, bind_addr):
    f = open(cfg_file)
    first_line, the_rest = f.readline(), f.read()
    t = open(cfg_file,"w")
    t.write(bind_addr + "\n")
    t.write(the_rest)
    t.close()

def main():
    ip_addr = intf_addr(intf)

    if not ip_addr.startswith(ip_range):
        write_addr(settings_file, "bind = %s" % ip_addr)
        os.system(exec_cmd)

if __name__ == "__main__":
    main()