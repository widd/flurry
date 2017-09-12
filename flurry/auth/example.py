import string

from twisted.python import log

import flurry
from flurry.auth.source import AuthSource
from flurry.auth.xml import XMLProtocol
from flurry.util.strutil import rndk


class ExampleAuthSource(AuthSource):
	def __init__(self):
		super(self.__class__, self).__init__(1)
		self.author = flurry.__author__
		self.xmlAuthed = False
		self.randomKey = rndk(string.letters + string.digits + string.punctuation)
		self.xmlHandler = XMLProtocol(self.randomKey)
		self.xmlHandler.finished.addCallback(self.authenticate)
		self.xmlHandler.finished.addErrback(self.xmlError)

	def authenticate(self, (username, password, randomKey)):
		# They did it!
		# They got a flash policy (policy-request), checked version (verChk), and got their random key (rndK)
		self.xmlAuthed = True
		print "%s auth with password %s and rndk %s from %s" % (username, password, randomKey, self)
		# Let GC clean up the XML handler - we don't need it anymore.
		del self.xmlHandler
		# From here you can authenticate user credentials... perhaps check them against a database.
		# Note that you don't need to use the XMLProtocol class at all. Maybe you use some other login method. Who knows?

	def xmlError(self, error):
		log.msg(repr(error))
		self.transport.loseConnection()

	def connectionMade(self):
		self.xmlHandler.makeConnection(self.transport)

	def lineReceived(self, line):
		self.xmlHandler.lineReceived(line)
