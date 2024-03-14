<br/>
<p align="center">
  <h3 align="center">Philips Dynalite Controller</h3>

  <p align="center">
    An (unoffical) Philips Dynalite Gateway Controller.
    <br/>
    <br/>
    <a href="https://github.com/jacobwilson-xyz/philips-dynalite/issues">Report Bug</a>
    .
    <a href="https://github.com/jacobwilson-xyz/philips-dynalite/issues">Request Feature</a>
  </p>
</p>



## About The Project

This Python program allows you to interact with a Philips Dynalite system to control presets and channels. 
<br/>
The way I run this for my current setup is via an Elagto Stream Deck running <a href="https://github.com/bitfocus/companion">Bitfocus Companion</a>.


## Features:

* Set Dynalite presets for specific areas.
* Set the value of individual Dynalite channels.
* Uses configuration from a `.env` file for username, password, gateway URL, and default fade time.

## Installation:

1. Clone this repository or download the zip file.
2. Install required libraries:

   ```bash
   pip install -r requirements.txt
   ```
3. Edit the `.env` file with your dynalite credentials.

## Usage

Run the script from the command line, specifying the desired function and arguments:

   ```bash
   dynet.py set_preset <area_id> <preset_id> [fade_time]
   dynet.py set_channel <area_id> <channel_id> <value> [fade_time]

   # Example
   dynet.py set_preset 2 1 2500
   ```

See `example.py` on how to use this within a Python program.
