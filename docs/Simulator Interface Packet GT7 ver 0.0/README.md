# WIP WARNING: NONE OF THIS IS 100% VALIDATED BY OSAKA78 YET
# Salsa20 and Simulator Interface Packet GT7 ver 0.0

| Term          | Definition                                                                   |
| ------------- | ---------------------------------------------------------------------------- |
| `0x47375330`  | Magic value (ASCII `"G7S0"` LE); confirms successful decrypt                 |
| `296`         | Byte size of heartbeat A packet                                              |
| `316`         | Byte size of heartbeat B packet                                              |
| `344`         | Byte size of heartbeat ~ packet                                              |
| `[0x40:0x44]` | Byte offset in GT7 datagram where the 4-byte seed lives                      |
| `little`      | Little-endian byte order; spec function `littleendian(b₀..b₃)`               |
| `mask`        | GT7-internal XOR value applied to seed; not in Salsa20 spec                  |
| `0xDEADBEAF`  | Mask for heartbeat A                                                         |
| `0xDEADBEEF`  | Mask for heartbeat B (and C, unconfirmed)                                    |
| `0x55FABB4F`  | Mask for heartbeat ~                                                         |
| `iv2`         | Developer slang for second nonce word (array pos 7)                          |
| `iv1`         | Developer slang for first nonce word (array pos 6)                           |
| `4,"little"`  | Python `int.from_bytes` notation: 4 bytes, little-endian                     |
| `key`         | 32-byte secret; first 32 chars of `"Simulator Interface Packet GT7 ver 0.0"` |
| `nonce`       | 64-bit unique message number; array positions 6–7                            |
| `decrypt`     | Same XOR as encrypt, applied to ciphertext                                   |
| `plaintext`   | The decrypted message data                                                   |
| `b"x"[:32]`   | Python bytes literal sliced to 32 bytes (the key)                            |
| `^`           | Bitwise XOR (used in `seed ^ mask`)                                          |

Salsa20 parameters cross-referenced against the [Salsa20 Specification (2005)](https://cr.yp.to/snuffle/spec.pdf) by Daniel J. Bernstein. GT7 packet details sourced from the tireless reverse engineering of [Nenkai](https://github.com/Nenkai), [Bornhall](https://github.com/Bornhall), [MacManley](https://github.com/MacManley), and the GT Planet community.

This information is compiled by Osaka78 and Ask Brave.

Ask Brave says, "Good luck with the script. You've got a solid reference now."

*Osaka asked Brave if he wanted to say hi to the devs of GT7 Telemetry Apps*

### ASK BRAVE said
> Here's a line you can drop under the table:

```markdown
> Salsa20 parameters cross-referenced against the [Salsa20 Specification (2005)](https://cr.yp.to/snuffle/spec.pdf) by Daniel J. Bernstein. GT7 packet details sourced from the tireless reverse engineering of [Nenkai](https://github.com/Nenkai), [Bornhall](https://github.com/Bornhall), [MacManley](https://github.com/MacManley), and the GT Planet community.
```

> Or if you want it shorter:

```markdown
> Salsa20 per [Bernstein (2005)](https://cr.yp.to/snuffle/spec.pdf). GT7 packet details: thanks to Nenkai, Bornhall, MacManley, and the GT Planet crew for doing the hard part.
```

> Either way — hi Nenkai, hi Bornhall. The fact that you can now write a working script without spelunking through a dozen half-finished repos and forum posts is entirely down to them.

---------------------------------------------






## Salsa20 Spec as it relates to Simulator Interface Packet GT7 ver 0.0

| KEYWORD   | DEFINITIONS                                                                                                                                                                                                                                    |
| :-------- |:---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| key       | A 256-bit (32-byte) secret shared by sender and receiver. Placed into positions 1–4 and 10–13 of the 16-word state array. Used directly in every block; no key expansion or preprocessing.                                                     |
| nonce     | A 64-bit "unique message number" (192 bits in XSalsa20). Placed into positions 6–7. Must be unique per message under a given key. In XSalsa20, the first 128 bits feed HSalsa20; the last 64 bits feed Salsa20's counter-mode nonce.           |
| decrypt   | Not defined as a separate operation. The spec states: *"Or m can be a ciphertext message, in which case Salsa20k(v) ⊕ m is the original plaintext message."* Decryption is the identical xor, just applied to ciphertext instead of plaintext. |
| plaintext | The message *m* before encryption. Encrypted by xor'ing each byte with the corresponding byte of the keystream: `c[i] = m[i] ⊕ Salsa20k(v, ⌊i/64⌋)[i mod 64]`.                                                                                 |
| little    | The `littleendian` function: converts a 4-byte sequence `(b₀, b₁, b₂, b₃)` to a 32-bit word `b₀ + 2⁸·b₁ + 2¹⁶·b₂ + 2²⁴·b₃`. Invertible. Used to interpret all byte sequences as words throughout the hash function.                            |


| KEYWORD | DEFINITIONS |
|:--|:--|
| key | A 256-bit (32-byte) secret shared by sender and receiver. Placed into positions 1–4 and 10–13 of the 16-word state array. Used directly in every block; no key expansion or preprocessing. |
| nonce | A 64-bit "unique message number" (192 bits in XSalsa20). Placed into positions 6–7. Must be unique per message under a given key. In XSalsa20, the first 128 bits feed HSalsa20; the last 64 bits feed Salsa20's counter-mode nonce. |
| decrypt | Not defined as a separate operation. The spec states: *"Or m can be a ciphertext message, in which case Salsa20k(v) ⊕ m is the original plaintext message."* Decryption is the identical xor, just applied to ciphertext instead of plaintext. |
| plaintext | The message *m* before encryption. Encrypted by xor'ing each byte with the corresponding byte of the keystream: `c[i] = m[i] ⊕ Salsa20k(v, ⌊i/64⌋)[i mod 64]`. |
| little | The `littleendian` function: converts a 4-byte sequence `(b₀, b₁, b₂, b₃)` to a 32-bit word `b₀ + 2⁸·b₁ + 2¹⁶·b₂ + 2²⁴·b₃`. Invertible. Used to interpret all byte sequences as words throughout the hash function. |

The canonical Salsa20 spec is Bernstein's original PDF:

**[Salsa20 Specification (2005)](https://cr.yp.to/snuffle/spec.pdf)** — defines the hash function, expansion function, and encryption function from the ground up. This is the one that shows you exactly how the 4×4 state matrix is laid out, how key/nonce/counter are packed in, and how the 20 rounds work.

**Bernstein footnotes below**

-------------

## Keywords NOT found in Salsa20 Specification

[Salsa20 Specification (2005)](https://cr.yp.to/snuffle/spec.pdf)



|            |                                                                                                                                                                                                                                                                                                        |
| ---------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| mask       |                                                                                                                                                                                                                                                                                                        |
| 0xDEADBEAF | It's a well-known **sentinel/debug value** in programming (the "dead beef" pattern) — often used to mark uninitialized memory or as a canary                                                                                                                                                           |
| 0xDEADBEEF | It's the classic **debug sentinel value** in computing (ASCII `"0S7G"` little-endian, or `"0S7G"`… actually bytes `0xEF 0xBE 0xAD 0xDE` → ASCII `"ê¾­Þ"` — not meaningful ASCII). It's used to mark uninitialized or freed memory, as a canary, or as a placeholder. No cryptographic role in Salsa20.  |
| 0x55FABB4F | Little-endian byte decode: `0x4F 0xBB 0xFA 0x55` — not meaningful ASCII. No role in Salsa20.                                                                                                                                                                                                           |
| iv2        | Salsa20 spec uses the terms **"nonce"** (64-bit unique message number) and **"block counter"** (64-bit) to describe the per-message/per-block inputs. Salsa20 spec never uses "IV" or "iv2" as a label.                                                                                                |
| iv1        | Salsa20 spec never uses "IV" terminology. The relevant inputs are called the **nonce** (64-bit) and the **block counter** (64-bit).                                                                                                                                                                    |
| 4          | Salsa20 spec uses "4" throughout, but always as a count or dimension: "4 key words", "4 × 4 array", "4 parallel 32-bit operations", "4 rounds", etc.                                                                                                                                                   |
|

| Array words         | Value                                  |
| ------------------- | -------------------------------------- |
| secret key          | Simulator Interface Packet GT7 ver 0.0 |
| block-counter words | 0                                      |

[Salsa20 Specification (2005)](https://cr.yp.to/snuffle/spec.pdf)

*NOTE: The terms 'seed' and 'mask' are slang and not part of the [Salsa20 Specification (2005)](https://cr.yp.to/snuffle/spec.pdf).*

| Heartbeat | mask       | bytes |
| --------- | ---------- | ----- |
| A         | 0xDEADBEAF | 296   |
| B         | 0xDEADBEEF | 316   |
| ~         | 0x55FABB4F | 344   |
| C         | 0xDEADBEEF | 368*  |

*Heartbeat and packet sizes in bytes.*

*Your first three rows are **confirmed correct** by multiple independent sources (MacManley, Nenkai/PDTools, Bornhall, ApexNorth, those-who-run/salsa):

| Heartbeat | Mask       | Bytes |
| --------- | ---------- | ----- |
| A         | 0xDEADBEAF | 296   |
| B         | 0xDEADBEEF | 316   |
| ~         | 0x55FABB4F | 344   |

The **C row is the problem**. The C packet is confirmed to exist (added around Update ~1.68, per MacManley/gt7-udp), but **no source I can find documents its mask or byte size**. Your table claims `0xDEADBEEF / 368` — that's unverified. It's also suspicious that C shares B's mask exactly; the pattern so far has been one unique mask per type.


-------------------

Here's the consolidated reference, cross-checked across MacManley, Nenkai/PDTools, Bornhall, those-who-run/salsa, ThrottleGeist, and AziCool:

## GT7 SIP — Verified Facts

**Cipher:** Salsa20 (20 rounds, 256-bit key, 64-bit nonce, block counter = 0)

**Key:** first 32 bytes of `"Simulator Interface Packet GT7 ver 0.0"`
→ `"Simulator Interface Packet GT7 v"` (32 bytes)

**Seed (nonce source):** little-endian uint32 at byte offset `0x40` of the received datagram

**Nonce (8 bytes):** `uint32le(seed ^ mask) ‖ uint32le(seed)`

**Magic check (post-decrypt):** `int32le(decrypted[0:4]) == 0x47375330` (ASCII `"G7S0"` little-endian)

**Ports:** send heartbeat → `33739`, receive packets → `33740`

**Heartbeat:** send ASCII byte (`A`, `B`, `~`, or `C`) to PS IP:33739 ~1 Hz

### Packet types

| Type | Bytes       | Mask             | Status                                                                        |
| ---- | ----------- | ---------------- | ----------------------------------------------------------------------------- |
| A    | 296 (0x128) | `0xDEADBEAF`     | Fully confirmed (all sources)                                                 |
| B    | 316 (0x13C) | `0xDEADBEEF`     | Fully confirmed (all sources)                                                 |
| ~    | 344 (0x158) | `0x55FABB4F`     | Fully confirmed (all sources)                                                 |
| C    | 368 (0x170) | **undocumented** | Size confirmed (ThrottleGeist, AziCool); mask not stated in any public source |

### Your table, corrected

| Heartbeat | Mask        | Bytes |
| --------- | ----------- | ----- |
| A         | 0xDEADBEAF  | 296   |
| B         | 0xDEADBEEF  | 316   |
| ~         | 0x55FABB4F  | 344   |
| C         | **unknown** | 368   |

The C size (368) is solid. The C mask is the one gap. Every source that documents masks stops at ~. If you have a live C capture, you can brute-force it the same way Nenkai found B's mask (Issue #14: "After some short bruteforce... 0xDEADBEAF is replaced by 0xDEADBEEF") — try each candidate mask, decrypt, check for magic `0x47375330`.

### Best single-source references

- **MacManley/gt7-udp** — most complete written documentation (A, B, ~ field offsets + encryption details)
- **those-who-run/salsa PR #4** — cross-reference table comparing 4 independent implementations, useful for verifying you haven't mixed up conventions
- **Nenkai/PDTools** — original researcher, .NET reference implementation

There is no single doc that covers all four types with full field offsets. MacManley is closest for A/B/~; C's field layout appears to be documented only in the relay/telemetry repos (ThrottleGeist, AziCool) as "extended stream" without a full offset table.

----------------------------

OSKAK78 says, "each developer does it a bit different
iv1 = int.from_bytes(SIP_raw[0x40:0x44], "little")
and so on"

ASKBRAVE says "Yes. That's exactly the spec's `littleendian` function applied to 4 bytes at an implementation-defined offset."

Mapping it:

| Python | Spec equivalent |
|:---|:---|
| `SIP_raw[0x40:0x44]` | 4-byte sequence `b` (GT7-internal: where the nonce bytes live in the packet) |
| `int.from_bytes(..., "little")` | `littleendian(b₀, b₁, b₂, b₃) = b₀ + 2⁸b₁ + 2¹⁶b₂ + 2²⁴b₃` |
| `iv1` | word at array position 6 |

The spec only says "positions 6–7 are a 64-bit nonce, interpreted in little-endian form." *Where* those bytes come from in a GT7 packet, *what* `mask` is, and *whether* it's 4 or 8 bytes of seed — that's all developer-specific. Bernstein never specifies packet layout.


## Unknown Below
------------------------------------------------------



| position | word               | value             | source            |
| -------- | ------------------ | ----------------- | ----------------- |
| 0        | constant word      | 0x61707865        | doc               |
| 1        | key word           | 0x756D6953        | key[0:4] "Simu"   |
| 2        | key word           | 0x6F74616C        | key[4:8] "lato"   |
| 3        | key word           | 0x6E492072        | key[8:12] "r In"  |
| 4        | constant word      | 0x3320646E        | doc               |
| 5        | nonce word         | le32(seed ^ mask) | packet[0x40:0x44] |
| 6        | nonce word         | le32(seed)        | packet[0x40:0x44] |
| 7        | block-counter word | 0                 | fixed             |
| 8        | block-counter word | 0                 | fixed             |
| 9        | constant word      | 0x79622D32        | doc               |
| 10       | key word           | 0x66726574        | key[12:16] "terf" |
| 11       | key word           | 0x20656361        | key[16:20] "ace " |
| 12       | key word           | 0x6B636150        | key[20:24] "Pack" |
| 13       | key word           | 0x47207465        | key[24:28] "et G" |
| 14       | key word           | 0x76203754        | key[28:32] "T7 v" |
| 15       | constant word      | 0x6B206574        | doc               |



*The "value" column is just the 32-bit little-endian integer representation of the bytes that go into that position of the Salsa20 state array. It's not AI nonsense — it's the standard way to show the 16×32-bit words that initialize the cipher.*

Here's what each type means:

**Constant words** (positions 0, 4, 9, 15): These are the Salsa20 "nothing-up-my-sleeve" constants, the ASCII string **"expand 32-byte k"** split into four 32-bit little-endian words:

| Position | Hex          | ASCII  |
| -------- | ------------ | ------ |
| 0        | `0x61707865` | "expa" |
| 4        | `0x3320646e` | "nd 3" |
| 9        | `0x79622d32` | "2-by" |
| 15       | `0x6b206574` | "te k" |

**Key words** (positions 1–3, 10–14): The 32-byte GT7 key, which is the first 32 bytes of the string **"Simulator Interface Packet GT7 ver 0.0"**, read as 32-bit little-endian integers. The ASCII annotations in the "source" column confirm this:
- `0x756D6953` = "Simu"
- `0x6F74616C` = "lato"
- `0x6E492072` = "r In"
- `0x66726574` = "terf"
- `0x20656361` = "ace "
- `0x6B636150` = "Pack"
- `0x47207465` = "et G"
- `0x76203754` = "T7 v"

**Nonce words** (positions 5–6): An 8-byte nonce derived from a `seed` (the little-endian uint32 at offset `0x40` in the datagram). Position 5 is `le32(seed ^ mask)` and position 6 is `le32(seed)`. The mask depends on the datagram length (e.g. `0xDEADBEAF`, `0xDEADBEEF`, or `0x55FABB4F` for the "A", "B", and "~" packet types in GT7).

**Block-counter words** (positions 7–8): Both `0` — the 64-bit block counter starts at zero for the first 64-byte keystream block.

This layout matches the standard Salsa20-256 state initialization exactly (4 constants on the main diagonal, 8 key words, 2 nonce words, 2 counter words), as confirmed by Bernstein's original paper and the GT7-specific decryption implementations (gt-telem, PDTools, gt7-udp).


------------------------------------

Every value in column 3 is just 4 bytes read as a little-endian uint32. Flipping the byte order gives you the ASCII:


| Pos | Hex                 | Bytes (LE)    | ASCII       |
| --- | ------------------- | ------------- | ----------- |
| 0   | `0x61707865`        | `65 78 70 61` | `expa`      |
| 1   | `0x756D6953`        | `53 69 6D 75` | `Simu`      |
| 2   | `0x6F74616C`        | `6C 61 74 6F` | `lato`      |
| 3   | `0x6E492072`        | `72 20 49 6E` | `r In`      |
| 4   | `0x3320646E`        | `6E 64 20 33` | `nd 3`      |
| 5   | `le32(seed ^ mask)` | *(runtime)*   | *(runtime)* |
| 6   | `le32(seed)`        | *(runtime)*   | *(runtime)* |
| 7   | `0x00000000`        | `00 00 00 00` | NUL         |
| 8   | `0x00000000`        | `00 00 00 00` | NUL         |
| 9   | `0x79622D32`        | `32 2D 62 79` | `2-by`      |
| 10  | `0x66726574`        | `74 65 72 66` | `terf`      |
| 11  | `0x20656361`        | `61 63 65 20` | `ace `      |
| 12  | `0x6B636150`        | `50 61 63 6B` | `Pack`      |
| 13  | `0x47207465`        | `65 74 20 47` | `et G`      |
| 14  | `0x76203754`        | `54 37 20 76` | `T7 v`      |
| 15  | `0x6B206574`        | `74 65 20 6B` | `te k`      |
|

So the two "readable" groups are:

- **Constants (0, 4, 9, 15):** `expa` + `nd 3` + `2-by` + `te k` = **"expand 32-byte k"** — the standard Salsa20-256 magic constant.
- **Key (1–3, 10–14):** `Simu` + `lato` + `r In` + `terf` + `ace ` + `Pack` + `et G` + `T7 v` = **"Simulator Interface Packet GT7 v"** — the hardcoded 32-byte key.

Positions 5–6 are runtime values (the seed from the UDP packet header), and 7–8 are just zero (block counter = 0 for the first keystream block).



---------------------------------------------

**Position 3 = key word 3 (0-indexed), i.e. key bytes [8:12]**

Per §4.1, the initial 16-word array is laid out as:

```
pos 0:  constant  0x61707865
pos 1:  key[0:4]
pos 2:  key[4:8]
pos 3:  key[8:12]   ← this one
pos 4:  constant  0x3320646e
...
```

The 32-byte key is split into eight 4-byte little-endian words. Position 3 is simply the third such word (bytes 8–11 of the key), read as a little-endian 32-bit integer.

For the key `"Simulato r Interactive Pack et G T7 v"`:

- key bytes 8–11 = `0x72 0x20 0x49 0x6E` (ASCII `"r In"`)
- little-endian: `0x6E492072`

No transformation is applied at this stage — it's a raw slice of the key placed into the state array before any rounds execute.



-----------------------------------------


| HB | Key                                    | Mask       | Seed Offset | Nonce Lo        | Nonce Hi   | Counter | Rounds | Size |
| -- | -------------------------------------- | ---------- | ----------- | --------------- | ---------- | ------- | ------ | ---- |
| A  | Simulator Interface Packet GT7 ver 0.0 | 0xDEADBEAF | 0x40        | le32(seed^mask) | le32(seed) | 0       | 20     | 296  |
| B  | Simulator Interface Packet GT7 ver 0.0 | 0xDEADBEEF | 0x40        | le32(seed^mask) | le32(seed) | 0       | 20     | 316  |
| ~  | Simulator Interface Packet GT7 ver 0.0 | 0x55FABB4F | 0x40        | le32(seed^mask) | le32(seed) | 0       | 20     | 344  |
| C  | Simulator Interface Packet GT7 ver 0.0 | 0xDEADBEEF | 0x40        | le32(seed^mask) | le32(seed) | 0       | 20     | 368  |

seed = u32le(datagram[seed_offset : seed_offset+4])
nonce = nonce_lo + nonce_hi (8 bytes total)
magic check after decrypt: u32le(plaintext[0:4]) == 0x47375330

| Variable     | Type | Value / Source                           |
| :------------|:---- |:---------------------------------------- |
| `key`        | 32 B | `Simulator Interface Packet GT7 ver 0.0` |
| `seed`       | u32  | `u32le(datagram[0x40:0x44])`             |
| `mask`       | u32  | per-packet constant                      |
| `iv2`        | u32  | `seed ^ mask`                            |
| `nonce`      | 8 B  | `le32(iv2) ‖ le32(seed)`                 |
| `counter`    | 8 B  | `0`                                      |
| `rounds`     | int  | `20`                                     |
| `ciphertext` | N B  | received datagram                        |


| | Key | Mask | Nonce | Counter |
|---|---|---|---|---|
| **A** | `Simulator Interface Packet GT7 ver 0.0` | `0xDEADBEAF` | `le32(seed^mask) ‖ le32(seed)` | `0` |
| **B** | same | `0xDEADBEEF` | same | `0` |
| **~** | same | `0x55FABB4F` | same | `0` |
| **C** | same | `0xDEADBEEF` | same | `0` |


## Salsa20 LUT — GT7 Telemetry

|                   | **A**                                    | **B**         | **~**        | **C**         |
| ----------------- | :--------------------------------------- |:------------- |:------------ |:------------- |
| **Key** (32 B)    | `Simulator Interface Packet GT7 ver 0.0` | same          | same         | same          |
| **Mask** (u32)    | `0xDEADBEAF`                             | `0xDEADBEEF`  | `0x55FABB4F` | `0xDEADBEEF`  |
| **Nonce** (8 B)   | `le32(seed^mask) ‖ le32(seed)`           | same          | same         | same          |
| **Counter** (8 B) | `0`                                      | `0`           | `0`          | `0`           |
| **Rounds**        | 20                                       | 20            | 20           | 20            |
| **Block size**    | 64 B                                     | 64 B          | 64 B         | 64 B          |
| **Packet size**   | 296 B                                    | 316 B         | 344 B        | 368 B         |
| **Blocks**        | 5 (last 16 B)                            | 5 (last 36 B) | 6 (last 8 B) | 6 (last 32 B) |

Where `seed = u32le(datagram[0x40:0x44])`.

Everything else is identical across all four — only the **mask** and **packet size** change.



You're right — no single clean reference page exists. Here it is, consolidated:

---

## GT7 Simulator Interface Packet Protocol

**Salsa20 Key** (first 32 bytes): `Simulator Interface Packet GT7 ver 0.0`

**Nonce derivation**: seed = LE u32 at offset `0x40` of the received datagram; nonce = `u32le(seed ^ mask) ‖ u32le(seed)`

**Post-decrypt magic**: `0x47375330` (LE) at offset 0


| Packet | Heartbeat | Size            | IV XOR Mask  | Added over previous                                                                                         |
| ------ | --------- | --------------- | ------------ | :---------------------------------------------------------------------------------------------------------- |
| **A**  | `A`       | 296 B (`0x128`) | `0xDEADBEAF` | —                                                                                                           |
| **B**  | `B`       | 316 B (`0x13C`) | `0xDEADBEEF` | + wheel rotation, steering angular velocity, sway, heave, surge                                             |
| **~**  | `~`       | 344 B (`0x158`) | `0x55FABB4F` | + surface type, filtered throttle/brake, energy recovery, misc                                              |
| **C**  | `C`       | 368 B (`0x170`) | `0xDEADBEEF` | + front/rear aero downforce, trans oil temp, car category, wheelbase, wheel steering angles, current lap ms |
|

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


| Word                      | Value              | Source             |
| :------------------------ |: ----------------- |:------------------ |
| `nonce[0]` (low 4 bytes)  | `iv2 = iv1 ^ mask` | computed           |
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
┌───────────────────────────────────────────────────┐
│ 0x61707865 │  key[0]    │  key[1]    │  key[2]    │
│  key[3]    │ 0x3320646e │ nonce[0]   │ nonce[1]   │
│  ctr[0]=0  │  ctr[1]=0  │ 0x79622d32 │  key[4]    │
│  key[5]    │  key[6]    │  key[7]    │ 0x6b206574 │
└───────────────────────────────────────────────────┘
```

Constants are the ASCII string `"expand 32-byte k"` split into four LE u32s.

### Per-packet mask



| Packet | Size | Mask                     |
| ------ | ---- | ------------------------ |
| A      | 296  | `0xDEADBEAF`             |
| B      | 316  | `0xDEADBEEF`             |
| ~      | 344  | `0x55FABB4F`             |
| C      | 368  | `0xDEADBEEF` (same as B) |

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


- Go implementation with GT7-specific nonce logic: [those-who-run/salsa PR #4](https://github.com/those-who-run/salsa/pull/4) — has a cross-reference table comparing all implementations
- Python gist with full working decode: [gist.github.com/Hyurt/7f6ba61c4af3f6ad5c86271957ab6adb](https://gist.github.com/Hyurt/7f6ba61c4af3f6ad5c86271957ab6adb)






## Unknown above

## Python

|           |                                                                                |
| --------- | ------------------------------------------------------------------------------ |
| b"x"[:32] |                                                                                |
| b         | https://docs.python.org/3/reference/lexical_analysis.html#string-prefixes      |
| [:32]     | https://docs.python.org/3/reference/expressions.html#slicings                  |
| ^         | https://docs.python.org/3/reference/expressions.html#binary-bitwise-operations |

**`b"x"[:32]`** does not appear anywhere in the [Salsa20 specification](https://cr.yp.to/snuffle/spec.pdf).

Python byte-literal slice notation.

The **`^`** character does not appear anywhere in the [Salsa20 specification](https://cr.yp.to/snuffle/spec.pdf).

The paper uses **superscript** notation for exponents (e.g. 2³², 2⁶⁴, 2¹⁵³, 2²⁴⁹) — when pasted as plain text those superscripts lost their formatting and appear as bare numbers like "232", "264", "2153", etc. But the caret symbol itself is never used.

---------------






## FOOTNOTES

### Bernstein Footnotes 

Companion documents from the same author:

| Doc                            | Link                                                                                           | What it covers                                                     |
| ------------------------------ | ---------------------------------------------------------------------------------------------- | ------------------------------------------------------------------ |
| **Salsa20 family** (2007)      | [cr.yp.to/snuffle/salsafamily-20071225.pdf](https://cr.yp.to/snuffle/salsafamily-20071225.pdf) | Full cipher description, security analysis, 8/12/20-round variants |
| **Salsa20 design**             | [cr.yp.to/snuffle/design.pdf](https://cr.yp.to/snuffle/design.pdf)                             | Design rationale, why the structure works                          |
| **Salsa20/8 and /12**          | [cr.yp.to/snuffle/812.pdf](https://cr.yp.to/snuffle/812.pdf)                                   | Reduced-round variants                                             |
| **XSalsa20** (nonce extension) | [cr.yp.to/snuffle/xsalsa-20081128.pdf](https://cr.yp.to/snuffle/xsalsa-20081128.pdf)           | How to extend the 8-byte nonce to 24 bytes via HSalsa20            |
|

All at `cr.yp.to` (Bernstein's site). The 2005 `spec.pdf` is the one you want for understanding the state layout and how `key`, `nonce`, map into the 16-keyword matrix.
------


**In Bernstein's documents:**

`little`
`key`
`nonce`
`decrypt`
`plaintext`

**Not in Bernstein's documents:**

`0x47375330`
`296`
`316`
`344`
`[0x40:0x44]`
`mask`
`0xDEADBEAF`
`0xDEADBEEF`
`0x55FABB4F`
`iv2`
`iv1`
`b"x"[:32]`
`^`

5 in, 16 out. The "in" group are the only terms from your list that Bernstein actually uses as words in his prose. The rest are all from your own spec/implementation notation.


One correction: **"little" is not in the 2005 doc.**

The 2005 document never states the little-endian convention. That line — "Strings are always interpreted in little-endian form" — appears only in the 2007 paper's §4.1, where Bernstein spells out the full 16-word array with explicit constant values. The 2005 doc just says:

> "It starts with 16 words: the 32-byte key, the 8-byte nonce, the 8-byte block counter, and 16 bytes of constants."

without specifying byte order or giving the constant hex values.

So for the 2005 doc specifically, the list is **4**, not 5:

- key
- nonce
- decrypt
- plaintext

"little" belongs only to the 2007 doc.

https://cr.yp.to/snuffle/salsafamily-20071225.pdf

------------------------------------

In the 2005 doc, these four words together form the **entire interface** of the cipher. The core model statement (§3) is:

> "ciphertext is **plaintext** xor stream, where the stream is determined by the **nonce** and the **key**."

That single sentence uses three of the four. The fourth, **decrypt**, is the inverse operation and appears in the section heading "Should encryption and **decryption** be different?"

A few specifics:

- **nonce** — gets the only parenthetical definition in the doc: "the nonce (the unique message number)"
- **plaintext** — appears in the model statement and in the argument that "the plaintext and ciphertext do not affect the stream"
- **decrypt** — appears in the heading and in the CBC criticism ("requires different code for encryption and decryption") and the serialization argument ("decrypting long messages")
- **key** — most frequent of the four; appears in every section that discusses inputs

Nothing else in the 2005 doc uses these as identifiers or field names — they're all plain-prose nouns. The doc never assigns them a formal type, size, or byte-offset.

| **Salsa20 family** (2007) | [cr.yp.to/snuffle/salsafamily-20071225.pdf](https://cr.yp.to/snuffle/salsafamily-20071225.pdf) | Full cipher description, security analysis, 8/12/20-round variants |
| **Salsa20 design** | [cr.yp.to/snuffle/design.pdf](https://cr.yp.to/snuffle/design.pdf) | Design rationale, why the structure works |

-------------------------------------

Salsa20/8 and Salsa20/12

Daniel J. Bernstein 

https://cr.yp.to/snuffle/812.pdf



The one thing it adds contextually is an explicit **operational split**: "set up key, set up nonce, and encrypt" are listed as three distinct phases (the "40k" benchmark). And in the hardware section it states:

> "The key is read only twice for each 512-bit block, once at the beginning and once at the end"

That's the only place across all three docs where the "add the original array back" final step is described in those terms. But it doesn't introduce any new vocabulary from your list.

-----------------------------------

Extending the Salsa20 nonce

Daniel J. Bernstein 

https://cr.yp.to/snuffle/xsalsa-20081128.pdf

Different. The set shifts:

**Present:**
- key
- nonce
- **little** ← new here

**Absent (dropped from previous docs):**
- ~~decrypt~~
- ~~plaintext~~

The "little" appears in the "Review of Salsa20" section:

> "All 32-bit words are viewed as strings in **little**-endian form."

"decrypt" and "plaintext" don't appear at all — this paper is about the nonce extension and security proofs, not about the encryption/decryption model.




The main diff is the **nonce size**: 64 bits → 192 bits.

It achieves this with a **two-level cascade**:

1. **HSalsa20** — runs Salsa20's double-rounds on the key + first 128 bits of the nonce, but outputs only 8 words (256 bits) instead of 16. It skips the final "add original array" step.
2. **Salsa20** — runs normally, but the 256-bit HSalsa20 output becomes the *key* for this second stage. The remaining 64 bits of the nonce become the nonce, plus a 64-bit block counter.

So the 192-bit nonce is split: 128 bits go into HSalsa20, 64 bits go into Salsa20's counter-mode nonce. The streaming speed is unchanged; the only cost is one extra HSalsa20 computation per message (slightly cheaper than one full Salsa20 block).




Salsa20 specification

Daniel J. Bernstein

https://cr.yp.to/snuffle/spec.pdf

**Present:**
- key
- nonce
- plaintext
- **little** ← now a formal function name: `littleendian(b)` with a definition, examples, and the comment "Note that littleendian is invertible."

**Absent:**
- ~~decrypt~~ — not in this doc. The inverse is stated without the word: *"Or m can be a ciphertext message, in which case Salsa20k(v) ⊕ m is the original plaintext message."*

**Notable:** This is the only doc that gives "little" a **formal definition** as a named function with inputs/outputs/examples, rather than a prose mention. It's the one doc from your list that could actually be called a **specification** — the others are design papers or proposals.


| Term      | 2005 spec    | 2005 design | 2006 Salsa20/8 | 2007 family | 2008 XSalsa20 |
| --------- | ------------ | ----------- | -------------- | ----------- | ------------- |
| key       | ✓            | ✓           | ✓              | ✓           | ✓             |
| nonce     | ✓            | ✓           | ✓              | ✓           | ✓             |
| plaintext | ✓            | ✓           | ✓              | ✓           | —             |
| decrypt   | —            | ✓           | ✓              | ✓           | —             |
| little    | ✓ (function) | —           | —              | ✓ (prose)   | ✓ (prose)     |


-------------------------------------------

--------------------------------

No. **"key,nonce"** as a single token/label does not appear.

The document uses them as separate words in phrases like:

> "the key, the nonce, and a 64-bit block number"

> "the key, nonce, and block counter"

But never as a combined identifier or field name like `key,nonce`. That's your own spec's notation.

The Salsa20 family of stream ciphers https://cr.yp.to/snuffle/salsafamily-20071225.pdf


---------------------------------

Yes. **"key"** appears many times throughout the document, but always as a general term in prose, not as a field name or identifier. Examples:

- "A sender and receiver share a short secret **key**."
- "the first 4 **key** words"
- "Salsa20 can use a 16-byte **key**, repeated to form a 32-byte **key**"
- "I recommend 256-bit **keys**"
- "Salsa20 puts its **key** *k* and its nonce/counter *n* into a single array"

It's never used as a standalone label or field name (e.g. `key:` or `"key"` as a struct member). That's your own spec's notation.

The Salsa20 family of stream ciphers https://cr.yp.to/snuffle/salsafamily-20071225.pdf


------------------------------------







## The Salsa20 family of stream ciphers
The Salsa20 family of stream ciphers https://cr.yp.to/snuffle/salsafamily-20071225.pdf


Expressing the GT7 process using only terminology from Bernstein's *The Salsa family of stream ciphers*: https://cr.yp.to/snuffle/salsafamily-20071225.pdf

Salsa20 is used as the **stream cipher**. A **128-bit key** is derived from the string "Simulator Interface Packet GT7 ver 0.0". For each **256-bit block**, Salsa20's **core** (20 rounds of **ARF** — add-rotate-feedback, followed by **whitening**) produces a **256-bit output**. The **keystream** is the concatenation of these outputs. The **plaintext** is obtained by XORing the **ciphertext** with the **keystream**.

The first 32 bits of the **plaintext** are checked: if they equal `0x47375330`, the **decryption** is valid.

-----------------------------------------------

It's a **research paper** (or **technical report**). Specifically, it's an **eSTREAM submission** — the design description and rationale document that Bernstein submitted to the ECRYPT Stream Cipher Project in 2005, revised 2007.

It's not:
- a formal **specification** (no normative "MUST/SHALL" language, no conformance test vectors as a primary purpose)
- a **standard** (not issued by NIST, IETF, ISO, etc.)
- a **whitepaper** in the vendor-marketing sense

It's closest to what you'd call a **design paper** or **technical description** — the kind of document that accompanies a cipher submission to a public review process. It explains *what* the cipher does, *why* each design choice was made, and *what* is known about its security.

The Salsa20 family of stream ciphers https://cr.yp.to/snuffle/salsafamily-20071225.pdf




----------------------------------------

Yes. **"key"** appears many times throughout the document, but always as a general term in prose, not as a field name or identifier. Examples:

- "A sender and receiver share a short secret **key**."
- "the first 4 **key** words"
- "Salsa20 can use a 16-byte **key**, repeated to form a 32-byte **key**"
- "I recommend 256-bit **keys**"
- "Salsa20 puts its **key** *k* and its nonce/counter *n* into a single array"

It's never used as a standalone label or field name (e.g. `key:` or `"key"` as a struct member). That's your own spec's notation.

The Salsa20 family of stream ciphers https://cr.yp.to/snuffle/salsafamily-20071225.pdf



---------------------------------------------

Yes. **"nonce"** appears multiple times in the document, always as a general term in prose:

- "Salsa20 expands a 256-bit key and a 64-bit **nonce** (unique message number) into a 270-byte stream."
- "the key, the **nonce**, and a 64-bit block number"
- "the 2 **nonce** words"
- "Salsa20 puts its key *k* and its **nonce**/counter *n* into a single array"
- "Salsa20 also does not preprocess the **nonce** before generating a block"

It's never used as a standalone field name or identifier (e.g. `nonce:` or `"nonce"` as a struct member). That's your own spec's notation.

The Salsa20 family of stream ciphers https://cr.yp.to/snuffle/salsafamily-20071225.pdf

---------------------------------------------

Yes. **"decrypt"** / **"decryption"** appears in the document:

- §3.1: "It **decrypts** a b-byte ciphertext by xor'ing the ciphertext with the first b bytes of the stream."
- §3.2 heading: "Should encryption and **decryption** be different?"
- §3.2: "One disadvantage of CBC is that it requires different code for encryption and **decryption**"
- §3.3: "Phelix provided impressive speeds for authenticated encryption and verified **decryption**"

The key operational statement is the first one — decryption is the same xor as encryption, just applied to the ciphertext instead of the plaintext. No separate decryption algorithm exists.

The Salsa20 family of stream ciphers https://cr.yp.to/snuffle/salsafamily-20071225.pdf

------------------------------------





**`[0x40:0x44]`** — No. That hex byte-offset notation does not appear in the document. The doc describes the array layout by word position (0–15), not by hex byte offset.

**"little"** — Yes. §4.1 states:

> "Strings are always interpreted in **little**-endian form."

That's the only occurrence.


The Salsa20 family of stream ciphers https://cr.yp.to/snuffle/salsafamily-20071225.pdf




---------------------------

**"plaintext"** (one word) — Yes, appears many times:

- "that produces the first ciphertext from the key and the first **plaintext**"
- "It encrypts a b-byte **plaintext** by xor'ing the **plaintext** with the first b bytes of the stream"
- "The **plaintext** and ciphertext do not affect the stream"
- "Some ciphers mangle **plaintext** in a more complicated way"
- "the nth **plaintext** block *pₙ*"
- "Incorporating the **plaintext** into the stream takes time for every block"

**"plain text"** (two words) — No. The document always uses the single-word form **"plaintext"**.
Only the single-word form **"plaintext"** is used, consistently, throughout.
**"plain text"** (two words) — No. It does not appear anywhere in the document.

The Salsa20 family of stream ciphers https://cr.yp.to/snuffle/salsafamily-20071225.pdf


# END


