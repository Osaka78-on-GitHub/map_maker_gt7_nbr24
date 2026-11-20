# UDP Splitting
aka Passthrough, Splitter, aka SIP_Splitter

**SimHub docs - Sharing UDP data with other applications**
https://github.com/SHWotever/SimHub/wiki/Sharing-UDP-data-with-other-applications

Wotever makes a good point, some games have no option to change telemetry port.

Gran Turismo has no option to change either:
- 33739 Heartbeart Port 
- 33740 Telemetry Port

So the upside is, the Heartbeat and Telemetry ports can be hardcoded.

Besides, GT7 telemetry is standard unicast UDP. (Spec in footnotes.)

Any system that wants multiple apps to read GT7 Telemetry must solve this problem.

It is an interesting problem. Let's name the problem UDP Splitting (for now).

SimHub can be configured to act as a UDP splitter.

GT7 Proxy is solving this someway too.

This project is looking into UDP splitting for GT7 Telemetry.

It's wise to consider what other GT7 UDP Spitters are doing with port numbers.
You don't want to inadvertently take SimHub's hardcoded port number or something.

The best way to do it is probably user configuration.
- Give user basic list of commonly taken and free ports
- Link them to docs
- Let user decide port number

So that's the lay of the land.

## Footnotes

| RFC                 | Title                                                                                      | Link                                        |
| :------------------ |:------------------------------------------------------------------------------------------ |:------------------------------------------- |
| **RFC 768** (STD 6) | User Datagram Protocol — the core spec (1980)                                              | https://www.rfc-editor.org/rfc/rfc768.html  |
| **RFC 9868**        | Transport Options for UDP — updates RFC 768 (2025)                                         | https://www.rfc-editor.org/rfc/rfc9868.html |
| **RFC 1122**        | Requirements for Internet Hosts – Communication Layers — clarifies host-side UDP behaviour | https://www.rfc-editor.org/rfc/rfc1122.html |
| **RFC 8085**        | UDP Usage Guidelines — congestion control, port usage, etc.                                | https://www.rfc-editor.org/rfc/rfc8085.html |
| **RFC 8304**        | Transport Features of UDP and UDP-Lite — formalises the API primitives                     | https://www.rfc-editor.org/rfc/rfc8304.html |




