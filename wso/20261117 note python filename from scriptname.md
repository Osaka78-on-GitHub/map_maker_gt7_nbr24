START Ask Brave
can python make a filename from the script name?



Searched Python script filename derivation
Exploring Python script filename derivation

Skipping web search; using known Python knowledge

python get script filename from __file__ pathlib
Yes:

from pathlib import Path

stem = Path(__file__).stem  # "GT7_udp_C_raw_tap"
out = Path(f"{stem}.pcap")  # "GT7_udp_C_raw_tap.pcap"

.name gives you GT7_udp_C_raw_tap.py, .stem gives you GT7_udp_C_raw_tap (no extension). So you can name your output file after the script with zero hardcoding — rename the script and the output follows.
END Ask Brave
