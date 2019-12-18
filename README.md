# WiFi Reconnaissance

A python script that looks for local devices connected to the network you're connected to.

Works on linux only, and depends on [`netifices`](https://pypi.org/project/netifaces/) to get the IP addresses and network subnet. \
Install with `pip install netifices`

[![asciicast](https://asciinema.org/a/nYlD8jWVhYxyNPKr9iVMyoejm.svg)](https://asciinema.org/a/nYlD8jWVhYxyNPKr9iVMyoejm)

### How the script works

The script first finds your network's IP subnet, which act as a list of possible IP addresses on the network. \
It then pings every IP to check if there's a device on the other end. \
After confirming devices on the network, the script fetches the MAC addresses of the found devices from the ARP cache.


