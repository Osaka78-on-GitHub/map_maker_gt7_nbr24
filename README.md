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

## Telemetry Bridge (optional)

Receives GT7 telemetry via UDP and streams it to the map as a live car dot.

### Requirements
salsa20 and websockets   

```bash
pip install -r requirements.txt
```

### Config
Edit config.json with your console IP(s). Leave the IP empty (or omit the line) for consoles you don't have.

### run
```
python3 bridge.py   
```
You should see:

```
Listening for telemetry from: {'ps5': '192.168.0.79'}
WebSocket on port 8765
Waiting for packets... (Ctrl+C to stop)
```

### Use
1. Start bridge.py in a terminal
2. Open index.html in your browser
3. Start GT7 on the PS5/PS4
4. A yellow dot (PS5) or cyan dot (PS4) + trail appears on the aerial panel

### Requirements
Console on the same LAN as the machine running bridge.py
GT7 running (telemetry only sends while in-game)
Ports 33739 (heartbeat) and 33740 (telemetry) open
