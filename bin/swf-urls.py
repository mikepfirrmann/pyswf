#!/usr/bin/env python
#!/usr/bin/python
#!python

from swf.actions import ActionGetURL
from swf.movie import SWF
from swf.tag import TagDefineButton2
import sys
import argparse

parser = argparse.ArgumentParser(description="Read and output the URLs linked to in a SWF file.")
parser.add_argument("--swf", type=argparse.FileType('rb'),
                    help="Location of SWF file to parse", required=True)
options = parser.parse_args()

# Load and parse the SWF.
swf = SWF(options.swf)

# Print all of the URLs that are targeted via ActionGetURL actions on Button2 tags.
for button in swf.all_tags_of_type(TagDefineButton2):
    for buttonAction in button.buttonActions:
        for action in buttonAction.actions:
            if isinstance(action, ActionGetURL):
                print action.urlString
