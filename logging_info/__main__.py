from logging_info import print_logging_info
import logging
print "--------------------------"
print "Example logging_info usage"
print "--------------------------"
print "1 - We initialize logging using loggging.basicConfig()"
logger = logging.basicConfig()
print "2 - We get the root logger with logging.getLogger()"
rl = logging.getLogger()
print "3 - We get a logger named 'foo.bar'"
fool = logging.getLogger('foo.bar')
print "4 - We set the foo.bar logging level to 20"
fool.level=20
print "5 - And now we print out the logging hierarchy:"
print "--------------------------"
print_logging_info()