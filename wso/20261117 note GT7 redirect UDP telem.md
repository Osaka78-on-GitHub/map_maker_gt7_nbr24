START Ask Brave
im not talking about that. im saying two ps one port, youre saying 1 ps 2 ports


Checked PS5 GT7 UDP port configuration
You're right, my bad — I answered the wrong question.

No. GT7 has no setting to change the destination port.  The PS5 always sends telemetry to port 33740 on whatever IP you enter in the game. There's no in-game option, no PS5 system setting, nothing. 

So if you have two PS5s both pointed at the same PC, both will try to send to that PC's port 33740 and they'll conflict.

The only workaround is a network-level redirect on the PC side — e.g. an iptables/nftables rule (Linux) or a third-party tool that intercepts packets from one PS5's source IP and rewrites the destination port before the application receives them:

# Linux example: redirect PS5 #2's traffic from :33740 → :33741
iptables -t nat -A PREROUTING -i eth0 -s 192.168.1.50 -p udp --dport 33740 -j REDIRECT --to-port 33741

Then your receiving app binds 33740 for PS5 #1 and 33741 for PS5 #2. Each PS5 still "thinks" it's sending to 33740 — the PC just silently rewrites one of them.

On Windows this is harder (no native equivalent of iptables); you'd need something like netsh interface portproxy won't work for UDP, so you're looking at a small custom relay or a Linux box as the network gateway.


Copy


ok good. so its solved



Confirmed problem solved
Yeah, the iptables redirect on the PC side is the cleanest fix. Both PS5s keep their default 33740 config, and the PC just splits them apart before the app sees them.
END Ask Brave
