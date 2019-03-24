from logging_info import print_logging_info
import logging
print "Example logging_info usage"
print "We initialize logging using logggin.basicConfig()"
logger = logging.basicConfig()
print "We get the root logger with logging.getLogger()"
rl = logging.getLogger()
print "We get a logger named 'foo'"
fool = logging.getLogger('foo.bar')
print "We set the foo logging level to 20"
fool.level=20
print "And now we print out the logging hierarchy:"
print ""
print_logging_info()