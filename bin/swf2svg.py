from swf.movie import SWF
from swf.export import SVGExporter
import sys

try:
    import argparse
    parser = argparse.ArgumentParser(description="Convert an SWF file into an SVG")
    parser.add_argument("--swf", type=argparse.FileType('rb'),
                        help="Location of SWG file to convert", required=True)
    parser.add_argument("--svg", type=argparse.FileType('wb'),
                        help="Location of converted SVG file", required=True)
    options = parser.parse_args()
except ImportError:
    # The argparse module was introduced in Python 2.7. For versions that do
    # not support it, parse the arguments manually.
    if len(sys.argv) < 3:
        sys.stderr.write("Did must receive SWF input path and SVG output path as input\n")
        sys.stderr.write("Usage: python bin/swf2svg.py --swf=input.swf --svg=output.svg\n")
        sys.exit(1)

    import re
    options = {}

    # sys.argv[0] should be the name of this script.
    match = re.match('--(swf|svg)=(.*)', sys.argv[1])
    options[match.group(1)]=open(match.group(2), "wb")

    match = re.match('--(swf|svg)=(.*)', sys.argv[2])
    options[match.group(1)]=open(match.group(2), "wb")

    if ('swf' not in options) or ('svg' not in options):
        sys.stderr.write("Did must receive SWF input path and SVG output path as input\n")
        sys.stderr.write("Usage: python bin/swf2svg.py --swf=input.swf --svg=output.svg\n")
        sys.exit(1)

# load and parse the SWF
swf = SWF(options.swf)

# create the SVG exporter
svg_exporter = SVGExporter()

# export!
svg = swf.export(svg_exporter)

# save the SVG
options.svg.write(svg.read())