#!/usr/bin/env python
#!/usr/bin/python
#!python

from swf.actions import ActionGetURL
from swf.actions import ActionConstantPool
from swf.movie import SWF
from swf.tag import TagDefineButton
from swf.tag import TagDefineButton2
#from swf.tag import TagPlaceObject
#from swf.tag import TagPlaceObject2
#from swf.tag import TagPlaceObject3
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

#for tag in (TagPlaceObject, TagPlaceObject2, TagPlaceObject3):
#    for placeObject in swf.all_tags_of_type(TagPlaceObject):
#        if not (placeObject.clipActions is None):
#            print "tag {} action: {}".format(tag, placeObject.clipActions.records)
#            for record in placeObject.clipActions.records:
#                print "record actions: {}".format(record.actions)
    
# Print all of the URLs that are targeted via ActionGetURL actions on Button2 tags.
for tag in (TagDefineButton, TagDefineButton2):
    for button in swf.all_tags_of_type(tag):
        for buttonAction in button.buttonActions:
            for action in buttonAction.actions:
                result = Result(button.name)
                if isinstance(action, ActionGetURL):
                    result.setUrl(action.url)
                elif isinstance(action, ActionConstantPool):
                    for constant in action.constants:
                        result.addConstant(constant)
                if result.isEmpty() == False:
                    results.append(result) 
    
yaml.dump(results, sys.stdout)
