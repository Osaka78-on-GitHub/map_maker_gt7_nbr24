# MMGT7 NBR24 Security Boundaries
## INFO: In order for this project to be successful and not hurt anyone, certain security boundaries need to be carefully understood and wisely acted on.
There is more at stake than can I get my GT7 Telemetry on a map with other players at the same time.
- There is Kaz to consider
- There is Sony to consider
- There are GT7 players to consider
- There are GT7 players Mums to consider

## Project Concept
```
Publisher > LAN > Browser > WebRTC PIPE < Browser < LAN < Publisher
                                 |
                                 |
         Consumer > Browser > NBR Map < Browser < Consumer
```
## Project Limits
Single LAN is allowed

Many Publishers and many Consumers allowed

GT7 Multiplayer Lobby is 16 LAN

Theoretical maximum LAN into PIPE is unlimited

## Practically, the Publisher LAN is: 
- 1 done
- 16 easy
- 100 difficult
- 100+ not impossible
- more, not my problem

## Security Limits
### Security boundaries vary based on 2 main things
1. Crossing the LAN
2. Who's on the WebRTC PIPE

## Security Scenarios
1. Number of Publishers = 1
2. Number of Publishers = 1++

## Security Scenario Descriptions
To paint the picture, common relationship language is about to be used.
### Scenario 1 - A single Publisher
A Publisher who knows he wants to be single and never get married to another Publisher is in a good spot, security wise.

He can LOCK the WebRTC PIPE from ever allowing any other Publisher to even ask for a date.

Problem solved.

### Scenario 2 - More than one Publisher
A Publisher who is open to dating another Publisher has a problem, security wise.

This is natural.

If he LOCKS the PIPE, he can never even get a date. So he must devise a way to date safely.

#### NOTE WELL - And remember this very, very important point: 

*What's Kaz gonna say if one of his players gets a broken heart?*

### There is a 3rd Scenario - Holy Matrimony 
As in, exchange rings and vow not to cheat on each other.

In this scenario the rings are KEYS and they LOCK the WebRTC PIPE.

Polygamy is not out of the equation here, in terms of painting this picture.

Side note, this is probably why God invented marriage.

#### Side, side note. 
The pros cons of LOCK KEY scenario is definitely why Sony charges big $$$ for PlayStations and copies of Gran Turismo and why PD keeps the reigns tight on the social side of GT7. The stakes are very high.
One false move and the telemetry feed will be cut off and PSN social will be locked down harder. 

The risk reward here is not optimal.

## Lay of the Land
Scenario 1 and 3 are solved. Pretty much every one is happy with those scenarios.

Various KEYS, LOCKS, AUTHENTICATION: all solved to pretty much everyone's absolute satisfaction.

A lot of people making a lot of money and a lot of happy marriages, security wise.


## Conclusion
**Scenario 2 is very interesting and will be the focus of this project.**

There is basically zero money in making a way that multiple Publishers can securely feed a public WebRTC PIPE
For 2 main reasons:
1. Most Publishers want $$$. So they don't stream their data into an unknown public PIPE.
2. Most Publishers want Consumers $$$. So they don't stream their data into an unknown public PIPE.

If there was $$$ in it, it would be solved.

Recently, I realised money is pretty over-rated.

The best things in life really are FREE.

So here we are...

## TBC
























