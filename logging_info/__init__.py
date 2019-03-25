
import logging

class HandlerInfo(object):
    """
    Logging Handler Info - provides basic info about a logging Handler
    """
    def __init__(self, handler):
        self.name = handler.name
        self.class_name = handler.__class__.__name__
        self.level = handler.level
        self.__formatter = FormatterInfo.from_logging(handler.formatter) if not handler.formatter is None else None
        self.__filters = [FilterInfo.from_logging(x) for x in handler.filters]

    @property
    def formatter(self):
        return self.__formatter

    @property
    def has_formatter(self):
        return not self.__formatter is None

    @property
    def filter_cnt(self):
        """
        The number of filters registered against this Handler
        """
        return len(self.__filters)

    @property
    def filters(self):
        """
        A generator that yields the filters for this Handler
        """
        for filter in self.__filters:
            yield filter

    def __repr__(self):
        return "<HandlerInfo name: {} class: {} level: {} formatter: {} filters: {}>".format(self.name, self.class_name, self.level, self.has_formatter, self.filter_cnt)

    def __str__(self):
        return "{} - Handler ({{class:'{}', level:{}, formatter:{}, filters:{}}})".format(self.name, self.class_name, self.level, self.has_formatter, self.filter_cnt)

class FormatterInfo(object):
    def __init__(self, format_string):
        self.fmt = format_string

    @classmethod
    def from_logging(cls, formatter):
        """
        Initialize a FormatterInfo instance with a logging.Formattter
        """
        return cls(formatter._fmt)

    def __repr__(self):
        return "<FormatterInfo fmt: {}>".format(self.fmt)

    def __str__(self):
        return "Formatter ({{fmt:'{}'}})".format(self.fmt)

class FilterInfo(object):
    """
    Provides basic information about a logging.Filter
    """
    def __init__(self, class_name):
        """
        Initialize a FilterInfo instance with a class_name of the filter
        """
        self.class_name = class_name

    @classmethod
    def from_logging(cls, filter):
        """
        Given a logging.Filter, return a FilterInfo instance
        """
        return cls(filter.__class__.__name__)

    def __repr__(self):
        return "<FilterInfo class: {}>".format(self.class_name)

    def __str__(self):
        return "{} - Filter ({{class:'{}'}})".format(self.class_name)

class LoggerInfo(object):
    """
    Provides basic information about a logging.Logger
    """
    def __init__(self, name, level, propagate, handlers, filters):
        self.name = name
        self.level = level
        self.propagate = propagate
        self.__handlers = [HandlerInfo(x) for x in handlers]
        self.__filters = [FilterInfo.from_logging(x) for x in filters]

    @classmethod
    def from_logging(cls, name, logger):
        assert logger.name == name, "logging name mismatch {} != {}".format(name, logger.name)
        return cls(name, logger.level, True if logger.propagate else False, logger.handlers, logger.filters )

    @property
    def handlers(self):
        """
        A generator which yields the handlers registered with this Logger
        """
        for handler in self.__handlers:
            yield handler

    @property
    def handler_cnt(self):
        """
        The number of handlers registered with this Logger
        """
        return len(self.__handlers)

    @property
    def filters(self):
        """
        A generator which yields the filters associated with this Logger.
        """
        for filter in self.__filters:
            yield filter

    @property
    def filter_cnt(self):
        """
        The number of filters registered with this Logger
        """
        return len(self.__filters)

    def __repr__(self):
        return "<LoggerInfo name: '{}' level: {} propagate: {} handlers: {} filters: {}>".format(self.name, self.level, self.propagate, self.handler_cnt, self.filter_cnt)

    def __str__(self):
        return "{} - Logger ({{level:{}, propagate:{}, handlers:{}, filters:{}}})".format(self.name, self.level, self.propagate, self.handler_cnt, self.filter_cnt)

class LoggerPlaceHolderInfo(object):
    """
    Provides basic information about a logging.LoggerPlaceholder
    """
    def __init__(self, name):
        self.name = name
        self.__handlers = frozenset([])
        self.__filters = frozenset([])

    @classmethod
    def from_logging(cls, name, placeholder):
        return cls(name)

    @property
    def handlers(self):
        return self.__handlers

    @property
    def handler_cnt(self):
        return 0

    @property
    def filters(self):
        return self.__filters

    @property
    def filter_cnt(self):
        return 0

    def __repr__(self):
        return "<LoggerPlaceHolderInfo name: '{}'>".format(self.name)

    def __str__(self):
        return "{} - LoggerPlaceHolder".format(self.name)

class InfoFactory(object):
    """
    Tracks mapping between logging classes and logging_info classes
    and provides means to instantiate one from the other via the
    `create` method.

    InfoFactory follows the builder pattern, meaning one inits
    an empty InfoFactory and calls the `register` method repeatedly
    to register logging_info classes.
    """
    def __init__(self):
        """
        Initialize an empty InfoFactory
        """
        self._registry = {}

    def register(self, logging_cls, info_cls):
        """
        Register a logging_info class for a given logging class.

        :param logging_cls: The logging class to register against.
        :type logging_cls: A class in the logging package

        :param info_cls: The logging_info class we wish to associate with
        the previously supplied logging_cls.
        :type info_cls: A class in the logging_info package

        :returns: self, to facilitate the builder pattern.
        """
        self._registry[logging_cls] = info_cls
        return self

    def create(self, name, instance):
        """
        Instantiate an instance of the appropriate logging_info class, given
        a name and an instance of a logging class.

        :param name: The name of the entity we are going to instantiate
        :type name: str

        :param instance: an instance of a logging class (eg Logger)
        :type instance: logging.Logger, logging.PlaceHolder, etc

        :raises: KeyError if the supplied instance's class is not a key
        in the internal registry

        :returns: An instance of the logging_info class associated with the supplied
        logging class
        """
        if not self._registry.has_key(instance.__class__):
            raise KeyError("InfoFactory does not have {} class registered. Keys:{}".format(instance.__class__.__name__, self._registry.keys()))

        for k,v in self._registry.iteritems():
            if isinstance(instance, k):
                return v.from_logging(name, instance)

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
        """
        Initialize the LoggerMgrInfo, given an InfoFactory instance.

        :param info_factory: An optional instance of an InfoFactory. If none
        is explicitly supplied, we create a default InfoFactory, which should
        suffice under normal circumstances.
        :type info_factory: InfoFactory
        """
        self.__info_factory = info_factory
        root = logging.getLogger()
        self.mgr = root.manager
        self.__loggers = [self.logger(x) for x in self.logger_names()]

    @property
    def loggers(self):
        """
        Get a list of loggers, starting with the root logger, and
        followed by the rest of the loggers in alphabetical order.
        :returns: logging_info.LoggerInfo and logging_info.PlaceHolderInfo instances
        """
        return self.__loggers

    @property
    def logger_cnt(self):
        """
        Return the number of loggers that the manager is managing.
        """
        return len(self.__loggers)

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
        Get a logging info instance with the provided name.

        :param name: The name of the logger to fetch.
        :type name: string
        :raises: KeyError, if a `name`ed logger does not exists
        :returns: instance of class registered with internal the InfoFactory.
        This should typically be an instance of logging_info.LoggerInfo or
        logging_info.PlaceHolderInfo.
        """
        if name == 'root':
            return LoggerInfo.from_logging("root", self.mgr.root)

        logger = self.mgr.loggerDict.get(name)
        return self.__info_factory.create(name, logger)

class bgcolors(object):
    def __init__(self, use_colors):
        self.use_colors = use_colors
    @property
    def HEADER(self):
        if self.use_colors:
            return '\033[95m'
        return ''

    @property
    def OKBLUE(self):
        if self.use_colors:
            return '\033[94m'
        return ''

    @property
    def OKGREEN(self):
        if self.use_colors:
            return '\033[92m'
        return ''

    @property
    def WARNING(self):
        if self.use_colors:
            return '\033[93m'
        return ''

    @property
    def FAIL(self):
        if self.use_colors:
            return '\033[91m'
        return ''

    @property
    def ENDC(self):
        if self.use_colors:
            return '\033[0m'
        return ''

    @property
    def BOLD(self):
        if self.use_colors:
            return '\033[1m'
        return ''

    @property
    def UNDERLINE(self):
        if self.use_colors:
            return '\033[4m'
        return ''

def print_logging_info(mgrinfo=None, tab_size=3, colors=True):
    """
    Given an optional manager info instance, print out the logging hierarchy
    """
    bcolors = bgcolors(colors)

    tsize = tab_size
    if mgrinfo == None:
        mgrinfo = LoggerMgrInfo()
    for x in mgrinfo.loggers:
        print bcolors.OKBLUE + str(x) + bcolors.ENDC
        if x.handler_cnt > 0:
            for y in x.handlers:
                print bcolors.OKGREEN + ("\t{}".format(y)).expandtabs(tsize) + bcolors.ENDC
                if y.has_formatter:
                    print bcolors.WARNING + ("\t\t{}".format(y.formatter)).expandtabs(tsize)
                if y.filter_cnt > 0:
                    for z in y.filters:
                        print bcolors.FAIL + ("\t\t{}".format(z)).expandtabs(tsize) + bcolors.ENDC
        if x.filter_cnt > 0:
            for y in x.filters:
                print  bcolors.FAIL + ("\t{}".format(y)).expandtabs(tsize) + bcolors.ENDC
