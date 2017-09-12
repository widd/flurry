from twisted.internet.protocol import ServerFactory
from twisted.protocols.basic import LineReceiver
from twisted.python import log

from flurry import BANNER, DESC

# State values for reuse in AuthSource implementations that mimic the vanilla login flow.
VERSION_CHECK, RANDOM_KEY, LOGIN = range(3)


class AuthSource(LineReceiver, object):
	# Delimiter can be changed in the case of extreme login overhauls, but you probably don't need to touch it.
	delimiter = '\0'
	version = None
	author = None

	def __init__(self, version):
		self.version = version

	def rawDataReceived(self, data):
		pass

	def lineReceived(self, line):
		if FlurryLoginFactory.debug:
			log.msg(line)

	def __repr__(self):
		return "%s (Version: %s/Author: %s)" % (self.__class__.__name__, self.version, self.author)


class FlurryLoginFactory(ServerFactory):
	protocol = None
	debug = False

	def __init__(self, authSource):
		self.protocol = authSource
		log.msg("Using %s" % authSource.__name__)
		print BANNER
		print DESC
