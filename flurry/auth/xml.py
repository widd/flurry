from twisted.internet.defer import Deferred
from twisted.protocols.basic import LineReceiver

from flurry.auth.source import VERSION_CHECK, RANDOM_KEY, LOGIN
from flurry.util.strutil import strbet


class XMLProtocol(LineReceiver):
	delimiter = '\0'

	def __init__(self, randomKey):
		self.randomKey = randomKey
		self.finished = Deferred()
		self.state = VERSION_CHECK

	def lineReceived(self, line):
		if '<policy-file-request/>' in line:
			self.sendLine("<cross-domain-policy><allow-access-from domain='*' to-ports='*'/></cross-domain-policy>")
		elif self.state == VERSION_CHECK and 'verChk' in line:
			self.sendLine("<msg t='sys'><body action='apiOK' r='0'></body></msg>")
			self.state = RANDOM_KEY
		elif self.state == RANDOM_KEY and "<body action='rndK'" in line:
			self.sendLine("<msg t='sys'><body action='rndK' r='-1'><k>%s</k></body></msg>" % self.randomKey)
			self.state = LOGIN
		elif self.state == LOGIN and "<msg t='sys'><body action='login' r='0'>" in line:
			username = strbet(line, '<nick><![CDATA[', ']]')
			password = strbet(line, '<pword><![CDATA[', ']]')
			if username or not password:
				self.finished.errback(Exception('Missing username or password in CDATA!'))
				return

			self.finished.callback((username, password, self.randomKey))
		else:
			self.finished.errback(Exception('Unknown message/state: %s' % line))
			return

	def rawDataReceived(self, data):
		pass
