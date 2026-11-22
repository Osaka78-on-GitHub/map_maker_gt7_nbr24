# WIP

Designed with assistance from the Brave Search AI assistant.

# Map Maker GT7 NBR24

Map for Nürburgring using beautiful
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
| Who                 | What they did                                                                              |
| ------------------- | ------------------------------------------------------------------------------------------ |
| **Nenkai**          | Originally discovered GT7's hidden UDP telemetry, published [PDTools](https://github.com/Nenkai/PDTools) (MIT)                  |
| **Bornhall**        | Reverse-engineered the full protocol details (key, nonce derivation, all field offsets)    |
| **MacManley**       | Wrote [gt7-udp](https://github.com/MacManley/gt7-udp) (MIT) — well-documented reference implementation covering all 3 packet types |
| **tarnheld**        | Contributed to packet documentation on GTPlanet                                            |
| **vwhitteron**      | gt-telemetry library, helped document packet variant C                                     |
| **Chi-Ho, Beregoz** | Helped research packet variant C                                                           |
| **ddm999**          | Car and manufacturer ID database (gt7info)                                                 |
| **GT Planet**       | Gave us a place to talk [GTPlanet](https://www.gtplanet.net)                                              |




## Credits

-  — BSD-2
-  — MIT
- , Bornhall, , tarnheld, vwhitteron, Chi-Ho, Beregoz, and others. See [GTPlanet thread](https://www.gtplanet.net/forum/threads/gt7-is-compatible-with-motion-rig.410728/).
- 
- Map editor designed with assistance from the Brave Search AI assistant   

| What | Who |
|------|-----|
| DOP20 aerial imagery | State of :inlineEntity{type="inline_entity" conversation="09c5027d81fb71cdeb2681a4af1ec3e94920" name="Rheinland-Pfalz" about="German&#32;state" nonce="39e4f213f270cec83c49da035d624aa0" sig="ed1766ac99d11b46c3ba68c1c51f7113f9172dc041b4978c98e123d52db4f2d8"} Geoportal (government, freely available) |
| OSM road data | OpenStreetMap contributors |
