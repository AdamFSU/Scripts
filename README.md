## Dependencies ##
Must use python3, python2.7 is deprecated as of January 1, 2020.

Required Python packages:
python-nmap

To install run: python3 -m pip install python-nmap

Also, since this script will be run from the command line, the $PYTHONPATH environment variable must be set so that python knows where to look for installed python modules when executing the script. I suggest exporting the environment variable at the bottom of .bashrc or .profile.

example: $ export PYTHONPATH=/usr/lib/python3/dist-packages/

* pythons distribution packages are normally located in: /usr/lib/<python version you are using>/dist-packages/ *

Also don't forget the / at the end like I did

	If you run the script and get the error: "No module named <module name> then python cannot find the module from the PYTHONPATH environment variable and you may need to troubleshoot.

## Script Info ##

I've added as many comments as possible to be verbose as possible so the script is easy to maintain if and when changes are made to your configuration. *Disclaimer: I've not tested this thoroughly, and don't even have an SMTP server setup*
