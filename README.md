# Pagerduty Oncall Schedule

This is a very basic script I use to check who is on call on Pagerduty.

## Usage

Just set the vars with PD_TOKEN (you can generate one on your PD account).

    $ PD_TOKEN=**************

    Example

    ./oncall.py -h
    usage: PageDutyInfo.py [-h] [-l] [-s SCHEDULE]

    Menue based SRE automation script ...

    optional arguments:
      -h, --help   show this help message and exit
      -l           Give the full list of Schedule avaiable in PD in [ID,NAME] format, pass the NAME into -s argument
      -s SCHEDULE  Get the full list of SCHEDULE ./PageDutyInfo.py -l, keep the argument to -s inside the double/single quote
