# WIP WARNING NONE OF THIS IS VALIDATED YET
# Simulator Interface Packet GT7 ver 0.0

Re-expressing the GT7 process using only terminology from Bernstein's *The Salsa family of stream ciphers*:

Salsa20 is used as the **stream cipher**. A **128-bit key** is derived from the string "Simulator Interface Packet GT7 ver 0.0". For each **256-bit block**, Salsa20's **core** (20 rounds of **ARF** — add-rotate-feedback, followed by **whitening**) produces a **256-bit output**. The **keystream** is the concatenation of these outputs. The **plaintext** is obtained by XORing the **ciphertext** with the **keystream**.

The first 32 bits of the **plaintext** are checked: if they equal `0x47375330`, the **decryption** is valid.























start ask brave guess
| position | word | value | source |
|:---|:---|:---|:---|
| 0 | constant word | 0x61707865 | doc |
| 1 | key word | 0x756D6953 | key[0:4] "Simu" |
| 2 | key word | 0x6F74616C | key[4:8] "lato" |
| 3 | key word | 0x6E492072 | key[8:12] "r In" |
| 4 | constant word | 0x3320646E | doc |
| 5 | nonce word | le32(seed ^ mask) | packet[0x40:0x44] |
| 6 | nonce word | le32(seed) | packet[0x40:0x44] |
| 7 | block-counter word | 0 | fixed |
| 8 | block-counter word | 0 | fixed |
| 9 | constant word | 0x79622D32 | doc |
| 10 | key word | 0x66726574 | key[12:16] "terf" |
| 11 | key word | 0x20656361 | key[16:20] "ace " |
| 12 | key word | 0x6B636150 | key[20:24] "Pack" |
| 13 | key word | 0x47207465 | key[24:28] "et G" |
| 14 | key word | 0x76203754 | key[28:32] "T7 v" |
| 15 | constant word | 0x6B206574 | doc |

key = b"Simulator Interface Packet GT7 ver 0.0"[:32]
mask = 0xDEADBEAF (296), 0xDEADBEEF (316), 0x55FABB4F (344)
rounds = 20




end abg





|Array words | Value  |
|:---|:---|
| secret key | Simulator Interface Packet GT7 ver 0.0 |
| block-counter words | 0 |

*The key words and block-counter words of the array.* https://cr.yp.to/snuffle/salsafamily-20071225.pdf

|Packet | mask | bytes |
|:---|:---|:---|
| A | 0xDEADBEAF | 296 |
| B | 0xDEADBEEF | 316 |
| ~ | 0x55FABB4F | 344 |
| C | 0xDEADBEEF | 368 |

*Packet, masks and byte sizes.* https://cr.yp.to/snuffle/salsafamily-20071225.pdf

|Stream Cipher|Value|
|:---|:---|
| rounds | 20 |

**Values assigned to the key, block-counter, and rounds of the 20-round stream cipher.*
https://cr.yp.to/snuffle/salsafamily-20071225.pdf

|State component | Value  |
|:---|:---|
| seed offset | 0x40 |
| nonce formula | le32(seed^mask) + le32(seed) |




| | Key | Mask | Seed Offset | Nonce Lo | Nonce Hi | Counter | Rounds | Size |
|---|---|---|---|---|---|---|---|---|
| A | Simulator Interface Packet GT7 ver 0.0 | 0xDEADBEAF | 0x40 | le32(seed^mask) | le32(seed) | 0 | 20 | 296 |
| B | Simulator Interface Packet GT7 ver 0.0 | 0xDEADBEEF | 0x40 | le32(seed^mask) | le32(seed) | 0 | 20 | 316 |
| ~ | Simulator Interface Packet GT7 ver 0.0 | 0x55FABB4F | 0x40 | le32(seed^mask) | le32(seed) | 0 | 20 | 344 |
| C | Simulator Interface Packet GT7 ver 0.0 | 0xDEADBEEF | 0x40 | le32(seed^mask) | le32(seed) | 0 | 20 | 368 |

seed = u32le(datagram[seed_offset : seed_offset+4])
nonce = nonce_lo + nonce_hi (8 bytes total)
magic check after decrypt: u32le(plaintext[0:4]) == 0x47375330




| Variable | Type | Value / Source |
|---|---|---|
| `key` | 32 B | `Simulator Interface Packet GT7 ver 0.0` |
| `seed` | u32 | `u32le(datagram[0x40:0x44])` |
| `mask` | u32 | per-packet constant |
| `iv2` | u32 | `seed ^ mask` |
| `nonce` | 8 B | `le32(iv2) ‖ le32(seed)` |
| `counter` | 8 B | `0` |
| `rounds` | int | `20` |
| `ciphertext` | N B | received datagram |




| | Key | Mask | Nonce | Counter |
|---|---|---|---|---|
| **A** | `Simulator Interface Packet GT7 ver 0.0` | `0xDEADBEAF` | `le32(seed^mask) ‖ le32(seed)` | `0` |
| **B** | same | `0xDEADBEEF` | same | `0` |
| **~** | same | `0x55FABB4F` | same | `0` |
| **C** | same | `0xDEADBEEF` | same | `0` |


## Salsa20 LUT — GT7 Telemetry



| | **A** | **B** | **~** | **C** |
|---|---|---|---|---|
| **Key** (32 B) | `Simulator Interface Packet GT7 ver 0.0` | same | same | same |
| **Mask** (u32) | `0xDEADBEAF` | `0xDEADBEEF` | `0x55FABB4F` | `0xDEADBEEF` |
| **Nonce** (8 B) | `le32(seed^mask) ‖ le32(seed)` | same | same | same |
| **Counter** (8 B) | `0` | `0` | `0` | `0` |
| **Rounds** | 20 | 20 | 20 | 20 |
| **Block size** | 64 B | 64 B | 64 B | 64 B |
| **Packet size** | 296 B | 316 B | 344 B | 368 B |
| **Blocks** | 5 (last 16 B) | 5 (last 36 B) | 6 (last 8 B) | 6 (last 32 B) |

Where `seed = u32le(datagram[0x40:0x44])`.

Everything else is identical across all four — only the **mask** and **packet size** change.



You're right — no single clean reference page exists. Here it is, consolidated:

---

## GT7 Simulator Interface Packet Protocol

**Salsa20 Key** (first 32 bytes): `Simulator Interface Packet GT7 ver 0.0`

**Nonce derivation**: seed = LE u32 at offset `0x40` of the received datagram; nonce = `u32le(seed ^ mask) ‖ u32le(seed)`

**Post-decrypt magic**: `0x47375330` (LE) at offset 0

| Packet | Heartbeat | Size | IV XOR Mask | Added over previous |
|--------|-----------|------|-------------|---------------------|
| **A** | `A` | 296 B (`0x128`) | `0xDEADBEAF` | — |
| **B** | `B` | 316 B (`0x13C`) | `0xDEADBEEF` | + wheel rotation, steering angular velocity, sway, heave, surge |
| **~** | `~` | 344 B (`0x158`) | `0x55FABB4F` | + surface type, filtered throttle/brake, energy recovery, misc |
| **C** | `C` | 368 B (`0x170`) | `0xDEADBEEF` | + front/rear aero downforce, trans oil temp, car category, wheelbase, wheel steering angles, current lap ms |

**Ports**: heartbeat → PS5 UDP **33739**, telemetry ← PS5 UDP **33740**

**Frequency**: 60 Hz for all types

**Notes**:
- C uses the same mask as B (`0xDEADBEEF`), confirmed by the gt7-switch-sim-ddu protocol matrix.
- A running stream won't switch format until it lapses (~8 s after last heartbeat), then the next heartbeat determines the new type.
- C was introduced around GT7 update 1.68.

---

Sources cross-referenced: [gt7-udp](https://github.com/MacManley/gt7-udp), [PDTools](https://github.com/Nenkai/PDTools), [gt-telem](https://github.com/RaceCrewAI/gt-telem), [gt7-switch-sim-ddu](https://github.com/d9053326-bot/gt7-switch-sim-ddu), [gt-racing-broadcast #711](https://github.com/jegr78/gt-racing-broadcast/issues/711).




Here's the full Salsa20 reference for GT7, consolidated from all sources:

---

## Salsa20/256 — GT7 Telemetry

**Variant**: Salsa20 with 256-bit key, 64-bit nonce, 64-bit block counter, 20 rounds.

### Key (32 bytes)

```
"Simulator Interface Packet GT7 ver 0.0"
```
(Exactly 32 ASCII bytes. Truncated to 32 by any library that takes the full string.)

### Nonce (8 bytes) — the "IV"

The 8-byte Salsa20 nonce is assembled from two 32-bit LE words:

| Word | Value | Source |
|------|-------|--------|
| `nonce[0]` (low 4 bytes) | `iv2 = iv1 ^ mask` | computed |
| `nonce[1]` (high 4 bytes) | `iv1` (the "seed") | read from datagram |

Where:
- **`iv1`** = `uint32le(datagram[0x40 : 0x44])` — always at the same offset in every received packet
- **`mask`** = per-packet-type constant (see table below)

So the 8-byte nonce as a byte string is:

```
[ iv2 as LE u32 ][ iv1 as LE u32 ]
[ 4 bytes       ][ 4 bytes       ]
```

### Block counter (8 bytes)

Always **zero**. All implementations (`x/crypto/salsa20`, `pycryptodome`, PDTools `_salsa.Set(0)`) start at block 0.

### Salsa20 state layout (4×4 matrix of 32-bit LE words)

```
┌─────────────────────────────────────────────────────────┐
│ 0x61707865 │  key[0]   │  key[1]   │  key[2]   │       │
│  key[3]   │ 0x3320646e │ nonce[0]  │ nonce[1]  │       │
│  ctr[0]=0 │  ctr[1]=0  │ 0x79622d32│  key[4]   │       │
│  key[5]   │  key[6]    │  key[7]   │ 0x6b206574│       │
└─────────────────────────────────────────────────────────┘
```

Constants are the ASCII string `"expand 32-byte k"` split into four LE u32s.

### Per-packet mask

| Packet | Size | Mask |
|--------|------|------|
| A | 296 | `0xDEADBEAF` |
| B | 316 | `0xDEADBEEF` |
| ~ | 344 | `0x55FABB4F` |
| C | 368 | `0xDEADBEEF` (same as B) |

### Decryption procedure

1. Receive datagram on UDP port **33740**
2. Determine packet type from length (or try each until magic matches)
3. `seed = u32le(datagram[0x40:0x44])`
4. `iv2 = seed ^ mask`
5. `nonce = le32(iv2) ‖ le32(seed)` (8 bytes)
6. `plaintext = salsa20_xor(ciphertext=datagram, key=KEY[0:32], nonce=nonce, counter=0)`
7. Verify: `u32le(plaintext[0:4]) == 0x47375330`

### Magic value

`0x47375330` — this is the ASCII bytes `30 53 37 47` = `"0S7G"`, which is `"G7S0"` read in little-endian (i.e., the string "G7S0" stored as a LE uint32).

### Reference links

- Salsa20 spec (Bernstein): [cr.yp.to/snuffle/salsafamily-20071225.pdf](https://cr.yp.to/snuffle/salsafamily-20071225.pdf)
- Wikipedia: [en.wikipedia.org/wiki/Salsa20](https://en.wikipedia.org/wiki/Salsa20)
- Go implementation with GT7-specific nonce logic: [those-who-run/salsa PR #4](https://github.com/those-who-run/salsa/pull/4) — has a cross-reference table comparing all implementations
- Python gist with full working decode: [gist.github.com/Hyurt/7f6ba61c4af3f6ad5c86271957ab6adb](https://gist.github.com/Hyurt/7f6ba61c4af3f6ad5c86271957ab6adb)


The canonical Salsa20 spec is Bernstein's original PDF:

**[Salsa20 Specification (2005)](https://cr.yp.to/snuffle/spec.pdf)** — defines the hash function, expansion function, and encryption function from the ground up. This is the one that shows you exactly how the 4×4 state matrix is laid out, how key/nonce/counter are packed in, and how the 20 rounds work.

Companion documents from the same author:

| Doc | Link | What it covers |
|-----|------|---------------|
| **Salsa20 family** (2007) | [cr.yp.to/snuffle/salsafamily-20071225.pdf](https://cr.yp.to/snuffle/salsafamily-20071225.pdf) | Full cipher description, security analysis, 8/12/20-round variants |
| **Salsa20 design** | [cr.yp.to/snuffle/design.pdf](https://cr.yp.to/snuffle/design.pdf) | Design rationale, why the structure works |
| **Salsa20/8 and /12** | [cr.yp.to/snuffle/812.pdf](https://cr.yp.to/snuffle/812.pdf) | Reduced-round variants |
| **XSalsa20** (nonce extension) | [cr.yp.to/snuffle/xsalsa-20081128.pdf](https://cr.yp.to/snuffle/xsalsa-20081128.pdf) | How to extend the 8-byte nonce to 24 bytes via HSalsa20 |

All at `cr.yp.to` (Bernstein's site). The 2005 `spec.pdf` is the one you want for understanding the state layout and how `key`, `nonce`, `counter` map into the 16-word matrix.








