#!/usr/bin/env python
#!/usr/bin/python
#!python

from swf.actions import ActionGetURL
from swf.actions import ActionConstantPool
from swf.movie import SWF
from swf.tag import TagDefineButton2
import sys
import argparse
import yaml

class Result(object):
    def __init__(self, buttonName):
        self.url = None
        self.buttonName = buttonName
        self.constants = []

    def addConstant(self, constantName):
        self.constants.append(constantName)

    def setUrl(self, url):
        self.url = url

    def isEmpty(self):
        return self.url == None and not self.constants


parser = argparse.ArgumentParser(description="Read and output the URLs linked to in a SWF file.")
parser.add_argument("--swf", type=argparse.FileType('rb'),
                    help="Location of SWF file to parse", required=True)
options = parser.parse_args()

# Load and parse the SWF.
swf = SWF(options.swf)

results = []

# Print all of the URLs that are targeted via ActionGetURL actions on Button2 tags.
for button in swf.all_tags_of_type(TagDefineButton2):
    for buttonAction in button.buttonActions:
        for action in buttonAction.actions:
            result = Result(button.name)
            if isinstance(action, ActionGetURL):
                result.setUrl(action.urlString)
            elif isinstance(action, ActionConstantPool):
                for constant in action.constants:
                    result.addConstant(constant)
            if result.isEmpty() == False:
                results.append(result) 

yaml.dump(results, sys.stdout)
