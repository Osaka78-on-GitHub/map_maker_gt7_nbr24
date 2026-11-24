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
CLI for "Simulator Interface Packet GT7 ver 0.0."

WIP Prints raw GT7 telemetry.

   



### Config
Add your PlayStation(s) to config.py.

### Use
1. Run main.py in terminal
```
python3.15 main.py   
```



3. Start GT7
4. Your telem on map WIP

### Minimum Requirements
PlayStation, GT7 and SIPxGT7 on same LAN
(Tested on GT7 1.72, PS4, PS5, Ubuntu22, Python3.15 and Vivaldi)


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

GT7 telemetry protocol (the decryption logic in bridge.py):

This is the big one. The Salsa20 key, packet sizes (296/316/344), IV masks (0xDEADBEAF / 0xDEADBEEF / 0x55FABB4F), field offsets, and magic number were all reverse-engineered by the community:
| Who                 | What they did                                                                                                                      |
| ------------------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| **Nenkai**          | Originally discovered GT7's hidden UDP telemetry, published [PDTools](https://github.com/Nenkai/PDTools) (MIT)                     |
| **Bornhall**        | Built many tools such as this beauty: [gt7telemetry](https://github.com/Bornhall/gt7telemetry)                                     |
| **MacManley**       | Wrote [gt7-udp](https://github.com/MacManley/gt7-udp) (MIT) — well-documented reference implementation covering all 3 packet types |
| **tarnheld**        | Contributed to packet documentation on GTPlanet                                                                                    |
| **vwhitteron**      | gt-telemetry library, helped document packet variant C                                                                             |
| **Chi-Ho, Beregoz** | Helped research packet variant C                                                                                                   |
| **ddm999**          | Car and manufacturer ID database (gt7info)                                                                                         |
| **MoebiusX**        | [Minimal Java Script Salsa20 stream cipher](https://github.com/MoebiusX/gt7-telemetry-analyzer/blob/main/src/capture/salsa20.js)   |
| **GT Planet**       | Gave us a place to talk [GTPlanet.net](https://www.gtplanet.net)                                                                   |




## Other credits

|                |                                                                                 |
| -------------- | ------------------------------------------------------------------------------- |
| Dual Maps Free | Years of inspiration. Thank you [Map Channels](https://dualmaps.com/opensource) |


# LET THERE BE LIGHT
