import re
import json
import time
import yaml
import sys
import sources.Slack
import sinks.neopixels
from threading import Thread


def validate_config(c):

    if not c.has_key('pi-indicator-config'):
        print "Configuration error: Configuration must contain a pi-indicator-config section"
        sys.exit(1)

    if not c['pi-indicator-config'].has_key('sources'):
        print "Configuration error: no sources defined"
        sys.exit(1)

    return

def dispatch(message):
    print "Dispatching message: %s" % message

    global __sink_refs__

    print "Dispatching to sinks"
    for sink,sink_config in __sink_refs__.items():
        match = re.search(sink_config['regex'], message)
        if match:
            print "%s " % sink
            newT = Thread(target = sinks.neopixels.playPixels, args=(sink_config,match,)) 
            newT.daemon = True
            newT.start()
    return

# load config
with open("config.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as exc:
        print exc
        sys.exit(1)

validate_config(config)
piconfig = config['pi-indicator-config']

source_refs = []
__sink_refs__ = {}
mappings = []

# connect sources
print "Connecting sources: "
for source,source_config in piconfig['sources'].items():
    print " - %s" % source
    if source_config['type'] == 'slack':
        slack_conn = sources.Slack.connectSlack(source_config)
        source_refs.append(slack_conn)

# connect sinks
print "Connecting sinks: "
for sink,sink_config in piconfig['sinks'].items():
    print " - %s" % sink
    if sink_config['type'] == 'neopixel':
        pixelBlocks = sinks.neopixels.setup(sink_config)
        __sink_refs__.update(pixelBlocks)

# run dispatcher
print "Starting source threads"
for source in source_refs:
    print "."
    t = Thread(target = sources.Slack.startProducer, args=(source, dispatch, ))
    t.daemon = True
    t.start()

try:
    while True:
        time.sleep(1)
except (KeyboardInterrupt):
    sys.exit(0)
