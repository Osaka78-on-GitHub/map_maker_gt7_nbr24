# WIP

Designed with assistance from the Brave Search AI assistant.

# Map Maker GT7 NBR24

Map for Gran Turismo 7 Nürburgring layout using beautiful
Rheinland-Pfalz DOP20 aerial imagery.

## Demo
https://osaka78-on-github.github.io/map_maker_gt7_nbr24/

## Notable

| File          | Function      | Method               |
|:--------------|:--------------|:---------------------|
| `demo url`    | Map           | Standard browser     |
| `SIPxGT7`     | CLI           | Python3.15           |
| `main.py`     | GT7 Telemetry | write to file        |
| `config.py`   | User config   | PlayStation IP       |
| `cloudflare`  | Signal server | WebRTC pipe          |

## Map Maker



- **Left panel:** OSM base map (toggle with "OSM" button)
- **Right panel:** DOP20 aerial photography (Rheinland-Pfalz Geoportal WMS)
- **Draw/edit:** Geoman toolbar (top-left of aerial panel)
- **Tags:** "Tags" button opens a panel to add/edit key=value tags per feature.
- **Persistence:** All edits auto-save to browser localStorage. Open the page
  later and your work is still there.
- **Export:** "Export" button downloads a GeoJSON file.



## SIPxGT7
CLI for 'Simulator Interface Packet GT7 ver 0.0.'



   



### Config
Add your PlayStation(s) to `config.py`

### Use
1. Run main.py in terminal
```
python3.15 main.py   
```

2. CLI will notify you what it's doing and report status

3. SIPxGT7 writes SIP raw packet to `SIP_raw` file.

4. Ctrl+C to stop SIPxGT7.

### Minimum Requirements
PlayStation, GT7 and SIPxGT7 on same LAN
(Tested on GT7 1.72, PS4, PS5, Ubuntu22, Python3.15)


## Credits
| What            | Who                       | License | Where                                                                                                         |
| --------------- | ------------------------- | ------- | ------------------------------------------------------------------------------------------------------------- |
| `GT7`           | Kaz                       | PD      | [gran-turismo.com](https://www.gran-turismo.com)                                                              |
| `Ask Brave`     | Brendan Eich              | Brave   | https://api-dashboard.search.brave.com/terms-of-service                                                       |
| `Leaflet`       | Vladimir Agafonkin        | BSD-2   | [Leaflet](https://leafletjs.com/)                                                                             |
| `Geoman`        | geoman-io team            | MIT     | [Geoman](https://github.com/geoman-io/leaflet-geoman-free)                                                    |
| `Salsa20`       | Daniel J. Bernstein       | —       | [Salsa20 Specification (2005)](https://cr.yp.to/snuffle/spec.pdf)                                             |
| `webRTC`        | Ian Hickson               | W3C     | https://www.w3.org/TR/webrtc/                                                                                 |
| `Python`        | Guido van Rossum          | BSD     | https://docs.python.org/3/license.html                                                                        |
| `Cloudflare`    | Cloudflare                | CCSA4.0 | [Cloudflare licence](https://developers.cloudflare.com/fundamentals/reference/policies-compliances/licenses/) |
| `OSM`           | Steve Coast               | ODbL    | https://www.openstreetmap.org/copyright                                                                       |
| `DOP20 imagery` | Rheinland-Pfalz Geoportal | DLDE2.0 | https://www.geoportal.rlp.de                                                                                  | 

## Credits for Decoding the 'Simulator Interface Packet GT7 ver 0.0'

This is the big one. The Salsa20 key, packet sizes, masks (0xDEADBEAF / 0xDEADBEEF / 0x55FABB4F), field offsets, and magic number were all reverse-engineered by the Gran Turismo community. God bless you, one and all:
| Who                 | What they did                                                                                                                                |
| ------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| **Nenkai**          | Originally discovered GT7's hidden UDP telemetry, published [PDTools](https://github.com/Nenkai/PDTools) (MIT)                               |
| **Bornhall**        | Built many tools such as this beauty: [gt7telemetry](https://github.com/Bornhall/gt7telemetry) (GNU)                                         |
| **MacManley**       | Wrote [gt7-udp](https://github.com/MacManley/gt7-udp) (MIT) — well-documented reference implementation covering all 3 packet types           |
| **vwhitteron**      | Much input into development of tools for SIP, most notably: [gt-telemetry](https://github.com/zetetos/gt-telemetry) (MIT)                    |
| **ddm999**          | GT7 Online Dealerships & Info: [gt7info](https://ddm999.github.io/gt7info/)                                                                  |
| **snimat**          | [Overview of GT7 Telemetry Software](https://www.gtplanet.net/forum/threads/overview-of-gt7-telemetry-software.418011/)                      |
| **tarnheld**        | [GT7 is compatible with motion rig ?](https://www.gtplanet.net/forum/threads/gt7-is-compatible-with-motion-rig.410728/page-4#post-13799643)  |
| **Chi-Ho**          | Feature: "C" telemetry format discovered: [Missing bytes](https://github.com/Nenkai/PDTools/issues/18#issuecomment-4105783379)               |
| **Beregoz**         | Feature: "C" telemetry format discovered: [Surfaces](https://github.com/Nenkai/PDTools/issues/18#issuecomment-4156683754)                    |
| **MoebiusX**        | [Minimal Java Script Salsa20 stream cipher](https://github.com/MoebiusX/gt7-telemetry-analyzer/blob/main/src/capture/salsa20.js)             |
| **GT Planet**       | Gave us a place to talk [GTPlanet.net](https://www.gtplanet.net)                                                                             |



## Other credits

|                |                                                                                 |
| -------------- | ------------------------------------------------------------------------------- |
| Dual Maps Free | Years of inspiration. Thank you [Map Channels](https://dualmaps.com/opensource) |


# LET THERE BE LIGHT
