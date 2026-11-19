## POTENTIALLY USEFUL

**GT7 Telemetry — Public Pipe Architecture**

- Heartbeat → PS5 → ciphertext datagrams written to file (never decrypted on host)
- Browser reads file → passes ciphertext into public pipe
- Pipe validates structure + size; rejects non-conforming peers
- Salsa20 decrypt in browser → display

**Security model (layered):**

| Layer | Defends against |
|---|---|
| Structural validation (size, shape, magic) | Noise, wrong packets, casual probing |
| Salsa20 (public key, in-band nonce) | Passive sniffing, raises attack cost |
| Peer rejection on first bad packet | Untrusted peers, resource exhaustion |

**Known limitation:** Salsa20 layer is not authentication. Key is public, nonce is in-band, no MAC. A determined attacker with the spec can forge valid packets. This layer is intentional — it contributes to a multi-layer design, not a standalone defense.

