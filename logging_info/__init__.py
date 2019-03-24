
import logging


class HandlerInfo(object):
    """
    Logging Handler Info - provides basic info about a logging Handler
    """
    def __init__(self, handler):
        self.name = handler.name
        self.class_name = handler.__class__.__name__
        self.level = handler.level
        self.filters = [FilterInfo(x) for x in handler.filters]
    def __repr__(self):
        return "<HandlerInfo name: {} class: {} level: {} filters: {}>".format(self.name, self.class_name, self.level, len(self.filters))

class FilterInfo(object):
    """
    Provides basic information about a logging.Filter
    """
    def __init__(self, filter):
        self.class_name = filter.__class__.__name__

    def __repr__(self):
        return "<FilterInfo class: {}>".format(self.class_name)


class LoggerInfo(object):
    """
    Provides basic information about a logging.Logger
    """
    def __init__(self, name, logger):
        assert logger.name == name, "logging name mismatch {} != {}".format(name, logger.name)
        self.name = logger.name
        self.level = logger.level
        self.handlers = [HandlerInfo(x) for x in logger.handlers]
        self.filters = [FilterInfo(x) for x in logger.filters]

    def __repr__(self):
        return "<LoggerInfo name: {} level: {} handlers: {} filters: {}>".format(self.name, self.level, len(self.handlers), len(self.filters))


class LoggerPlaceHolderInfo(object):
    """
    Provides basic information about a logging.LoggerPlaceholder
    """
    def __init__(self, name, placeholder):
        self.name = name
        self.handlers = []
        self.filters = []

    def __repr__(self):
        return "<LoggerPlaceHolderInfo name: {}>".format(self.name)

class InfoFactory(object):
    def __init__(self):
        self._registry = {}

    def register(self, logging_cls, info_cls):
        self._registry[logging_cls] = info_cls
        return self

    def create(self, name, instance):
        if not self._registry.has_key(instance.__class__):
            raise KeyError("InfoFactory does not have {} class registered. Keys:{}".format(instance.__class__.__name__, self._registry.keys()))

        for k,v in self._registry.iteritems():
            if isinstance(instance, k):
                return v(name, instance)


def default_info_factory():
    """
    Construct the default InfoFactory
    """
    return InfoFactory()\
           .register(logging.Logger, LoggerInfo)\
           .register(logging.PlaceHolder, LoggerPlaceHolderInfo)


class LoggerMgrInfo(object):
    """
    Provides basic information about the logging.Manager
    """
    def __init__(self, info_factory=default_info_factory()):
        import logging
        self.__info_factory = info_factory
        root = logging.getLogger()
        self.mgr = root.manager
        self.__loggers = self._loggers()

    def _loggers(self):
        return [self.logger(x) for x in self.logger_names()]

    def loggers(self):
        """
        Get a list of loggers
        """
        return self.__loggers

    def logger_names(self):
        """
        Get a sorted list of logger names, starting with the root logger
        """
        keys= self.mgr.loggerDict.keys()
        keys.sort()
        retval = ['root']
        retval.extend(keys)
        return retval

    def logger(self, name):
        """
        Get a logging info instance with the provided name
        """
        if name == 'root':
            return LoggerInfo("root", self.mgr.root)

        logger = self.mgr.loggerDict.get(name)
        return self.__info_factory.create(name, logger)
        # if isinstance(logger, logging.Logger):
        #     return LoggerInfo(logger)
        # elif isinstance(logger, logging.PlaceHolder):
        #     return LoggerPlaceholderInfo(name, logger)


def print_logging_info(mgrinfo=None):
    """
    Given an optional manager info instance, print out the logging hierarchy
    """
    if mgrinfo == None:
        mgrinfo = LoggerMgrInfo()
    for x in mgrinfo.loggers():
        print x
        if len(x.handlers) > 0:
            for y in x.handlers:
                print "\t{}".format(y)
                if len(y.filters) > 0:
                    for z in y.filters:
                        print "\t\t{}".format(z)
        if len(x.filters) > 0:
            for y in x.filters:
                print "\t{}".format(y)


if __name__ == '__main__':
    import logging
    logger = logging.basicConfig()
    rl = logging.getLogger()
    fool = logging.getLogger('foo')
    fool.level=20
    print_logging_info()