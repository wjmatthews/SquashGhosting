# SquashGhosting
Script to simulate playing an opponent on a squash court.

#### The Basics
The goal of this program is to mimic the actions of a squash opponent for the purposes of a personal workout on a squash court.  The program outputs one of six court locations where the 'opponent' 'plays' a shot to via an audio cue (ex. 'front right' or 'back left').  The idea is you move to that location and 'play' your shot, and return to the tee.  There is a varying time interval between each shot from the opponent.  The chance any one shot is played varies with each shot, based on what has previously happened.  The goal is to replicate various play flows (a series of long drives, a series of drop shots), but with enough randomness to feel like a weak-to-middling amateur player.

#### Current State
Logic to generate audio cues as well as audio cues are implemented, if you're running from an IDE or terminal.

#### Goals and Future Features
Long term is to finish as an app that can be downloaded for iOS and Android so it can actaully be used on a squash court!

Nice to have features would be the ability to tune some of the parameters via the app for personal customization.  These would be things like min/max time bewteen shots and max number of repeated shots.

#### Requirements
Currently requires simpleAudio package to be installed.
https://simpleaudio.readthedocs.io/en/latest/installation.html#installation-ref

