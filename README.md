Designed with assistance from the Brave Search AI assistant.

# Map Maker GT7 NBR24

Dual-panel map editor for annotating the Nürburgring (Nordschleife) using
Rheinland-Pfalz DOP20 aerial imagery. Built with Leaflet + Geoman.

## Demo
https://osaka78-on-github.github.io/map_maker_gt7_nbr24/

## Files

| File          | Purpose       | Method               |
|---------------|---------------|----------------------|
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

### Setup

```bash
pip install salsa20 websockets   
