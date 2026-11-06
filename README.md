# WIP

Designed with assistance from the Brave Search AI assistant.

# Map Maker GT7 NBR24

Dual-panel map editor for annotating the Nürburgring (Nordschleife) using
Rheinland-Pfalz DOP20 aerial imagery. Built with Leaflet + Geoman.

## Demo
https://osaka78-on-github.github.io/map_maker_gt7_nbr24/

## Files

| File          | Purpose       | Method               |
|:--------------|:--------------|:---------------------|
| `index.html`  | Map Maker     | web browser          |
| `bridge.py`   | GT7 Telemetry | Salsa20 to WebSocket |
| `config.json` | Cofiguration  | PlayStation IP       |

## Map Editor

Open `index.html` in a browser. No server needed.

- **Left panel:** OSM road map (toggle with "OSM" button)
- **Right panel:** DOP20 aerial (Rheinland-Pfalz Geoportal WMS)
- **Draw/edit:** Geoman toolbar (top-left of aerial panel)
- **Tags:** "Tags" button opens a panel to add/edit key=value tags per feature
- **Persistence:** All edits auto-save to browser localStorage. Open the page
  later and your work is still there.
- **Export:** "Export" button downloads a GeoJSON file (importable into uMap)

### Deploy to GitHub Pages

1. Push this repo to GitHub (public or private)
2. Settings → Pages → Deploy from branch → main → / (root)
3. Open `https://<username>.github.io/<repo>/`

## Telemetry Bridge (local machine only)

Receives GT7 telemetry via UDP and streams it to the map as a live car dot.

### Requirements
salsa20 and websockets   

```bash
pip install -r requirements.txt
```

### Config
Edit config.json with your console IP(s). Leave the IP empty (or omit the line) for consoles you don't have.

### Use
1. Start bridge.py in a terminal
```
python3 bridge.py   
```
You should see:

```
Listening for telemetry from: {'ps5': '192.168.0.79'}
WebSocket on port 8765
Waiting for packets... (Ctrl+C to stop)
```
2. Open index.html in your browser
3. Start GT7 on the PS5/PS4
4. A yellow dot (PS5) or cyan dot (PS4) + trail appears on the aerial panel

### Requirements
Console on the same LAN as the machine running bridge.py
GT7 running (telemetry only sends while in-game)
Ports 33739 (heartbeat) and 33740 (telemetry) open

## Credits
| What    | Who  | License  | Where  |
|:------  |:-----|:---------|:-------|
| Leaflet | Vladimir Agafonkin + contributors | BSD-2 | leafletjs.com |
| Geoman (leaflet-geoman-free) | geoman-io team | MIT | github.com/geoman-io/leaflet-geoman-free |
| `salsa20` (Python) | — | — | PyPI |
| `websockets` (Python) | Aymeric Augustin + contributors | BSD-3 | github.com/aa1000/pywebsockets |
| `tomli` (Python) | Taneli Hukkinen | MIT | github.com/hukkin/tomli |
| PySceneDetect | Bruce West + contributors | BSD-3 | github.com/BruceDLight/Scenedetect |

GT7 telemetry protocol (the decryption logic in bridge.py):

This is the big one. The Salsa20 key, packet sizes (296/316/344), IV masks (0xDEADBEAF / 0xDEADBEEF / 0x55FABB4F), field offsets, and magic number were all reverse-engineered by the community:
| Who | What they did |
|-----|---------------|
| **Nenkai** | Originally discovered GT7's hidden UDP telemetry, published PDTools (MIT) |
| **Bornhall** | Reverse-engineered the full protocol details (key, nonce derivation, all field offsets) |
| **MacManley** | Wrote gt7-udp (MIT) — well-documented reference implementation covering all 3 packet types |
| **tarnheld** | Contributed to packet documentation on GTPlanet |
| **vwhitteron** | gt-telemetry library, helped document packet variant C |
| **Chi-Ho, Beregoz** | Helped research packet variant C |
| **ddm999** | Car and manufacturer ID database (gt7info) |

| What | Who |
|------|-----|
| DOP20 aerial imagery | State of :inlineEntity{type="inline_entity" conversation="09c5027d81fb71cdeb2681a4af1ec3e94920" name="Rheinland-Pfalz" about="German&#32;state" nonce="39e4f213f270cec83c49da035d624aa0" sig="ed1766ac99d11b46c3ba68c1c51f7113f9172dc041b4978c98e123d52db4f2d8"} Geoportal (government, freely available) |
| OSM road data | OpenStreetMap contributors |
