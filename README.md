# BitdefenderVPN To OVPN

my personnal script to create .ovpn file from Bitdefender vpn (since they don't have any linux client).

[poorly written docs (wip)](tests/notes.md)

```bash
usage: BitdefenderVPN To OVPN [-h] -t TOKEN [-l LOCATION] [-p {tcp,udp}]

Generate ovpn configs from Bitdefender VPN, don't need the vpn client installed and works anywhere including linux.

options:
  -h, --help            show this help message and exit
  -t, --token TOKEN     The access token for Bitdefender VPN
  -l, --location LOCATION
                        Location for the VPN connection (default is france-paris)
  -p, --protocol {tcp,udp}
                        Protocol for the VPN connection (tcp or udp, default is tcp)
```

example use :
```bash
python3 main.py --token xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx --protocol udp --location france-paris
[INFO] Got configuration infos
[SUCCESS] Generating the openvpn/auth configuration done.

Username : aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
Password : bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb
Saved as Bitdefender.ovpn
> Friendly reminder: those are only valid for 24 hours.

```

the script only require python 3 and requests.
may not work for you, don't execept to get any support from me.

<p align="center">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
<img src="https://i.imgur.com/Ptm0bAD.png" alt="image" width="50" height="50">
</p>
all the reverse engeinnering was made using [HTTP Toolkit](https://httptoolkit.com/) with [Frida](https://frida.re/docs/android/) on a rooted android phone in a day.

![terry the terible](https://media1.tenor.com/m/MsDhsn6a3EIAAAAd/terry-davis.gif "")

it also only works on the unlimited plan since bitdefender does not use the same provider for the free and unlimited plan (idk why).