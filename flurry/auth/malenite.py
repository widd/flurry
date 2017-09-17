import hashlib
from datetime import datetime

import bcrypt
from alchimia import TWISTED_STRATEGY
from sqlalchemy import create_engine, MetaData, Table
from twisted.internet import reactor
from twisted.internet.defer import inlineCallbacks
from twisted.python import log

import flurry
from flurry.auth.source import AuthSource
from flurry.auth.xml import XMLProtocol
from flurry.util import messages

DB_USERNAME = ''
DB_PASSWORD = ''
DB_HOST = ''
DB_NAME = ''

STATIC_RNDK = ''


def malenite_hash(password, key=STATIC_RNDK):
	newHash = hashlib.md5(password).hexdigest().upper()
	newHash = newHash[::-1] + key + 'Y(02.>\'H}t":E1'
	return hashlib.md5(newHash).hexdigest()[::-1]

engine = create_engine(
	'mysql://%s:%s@%s/%s' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_NAME),
	reactor=reactor,
	strategy=TWISTED_STRATEGY
)

metadata = MetaData(bind=engine)

# Need to pull the underlying sync engine to autoload on startup with alchimia
penguins = Table('penguins', metadata, autoload_with=engine._engine)


class MaleniteAuthSource(AuthSource):
	def __init__(self):
		super(self.__class__, self).__init__(1)
		self.author = flurry.__author__
		self.xmlAuthed = False
		self.randomKey = STATIC_RNDK  # Malenite uses a static key.
		self.xmlHandler = XMLProtocol(self.randomKey)
		self.xmlHandler.finished.addCallback(self.authenticate)
		self.xmlHandler.finished.addErrback(self.xmlError)

	@inlineCallbacks
	def authenticate(self, (username, password, randomKey)):
		self.xmlAuthed = True
		del self.xmlHandler

		result = yield engine.execute(penguins.select(penguins.c.Username == username).limit(1))
		user = yield result.fetchone()

		if not user:
			self.sendError(messages.PENGUIN_NOT_FOUND)
		else:
			db_password = user[penguins.c.Password]

			if not bcrypt.checkpw(password, db_password):
				self.sendError(messages.INCORRECT_PASSWORD)
			else:
				if user[penguins.c.IsOnline] == 1:
					self.sendError(messages.LOGIN_FLOODING)
				else:
					ban_status = user[penguins.c.Banned]

					if ban_status == 'Permanent':
						self.sendError(messages.BANNED_FOREVER)
					elif ban_status != '-1':
						ts = datetime.utcfromtimestamp(int(ban_status))
						ban_time = ts - datetime.utcnow()
						if ban_time.seconds > 0:
							hours_left = max(1, int(ban_time.seconds // 3600))
							if hours_left == 1:
								self.sendError(messages.BAN_AN_HOUR)
							else:
								self.sendError(messages.BAN_DURATION(hours_left))
					else:
						log.msg('User %s authenticated from %s using %s' % (username, self.transport.getPeer(), self))
						login_key = malenite_hash(password)
						self.sendLine(messages.LOGIN_KEY(user[penguins.c.ID], login_key))

	def xmlError(self, error):
		log.msg(repr(error))
		self.transport.loseConnection()

	def sendError(self, error):
		self.sendLine(error)
		self.transport.loseConnection()

	def connectionMade(self):
		if not self.xmlAuthed:
			self.xmlHandler.makeConnection(self.transport)

	def lineReceived(self, line):
		super(self.__class__, self).lineReceived(line)
		if not self.xmlAuthed:
			self.xmlHandler.lineReceived(line)
