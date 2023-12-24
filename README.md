# Nettyboi
## a bit better than scraping through netstat output if you're paranoid about outbound connections
### But only marginally, plus the code is bad

## Installation
### Linux only. Not supporting windows with this nonsense so don't even think about it
0. Download the [latest release](https://github.com/birdybirdonline/Nettyboi/releases/tag/tool "nettyboi 1.0")
1. `chmod u+x ./installer.sh` to make the installer script executable. (You'll need to `sudo` it probs)
2. Done. Should be able to execute `nettyboi` from anywhere now. If it doesn't work I'm sorry, too bad I guess.

not gunna run on windows unless it gets packaged on windows. cba

## Usage
run `nettyboi` from cli.
It'll take a minute. Basically it runs netstat, Does some extra operations to get (marginally) better info for
name resolution for remote address connections. It'll give you a list at the end of any it wasn't able to fully resolve.

Also strips out all connections to a local address because why would you want that?

Hth
