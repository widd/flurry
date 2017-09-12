from twisted.internet import reactor
from twisted.internet.endpoints import TCP4ServerEndpoint

from flurry.auth.source import FlurryLoginFactory
from flurry.auth.example import ExampleAuthSource


def main():
	endpoint = TCP4ServerEndpoint(reactor, 7112)
	endpoint.listen(FlurryLoginFactory(ExampleAuthSource))


if __name__ == '__main__':
	from twisted.python import log
	import sys

	FlurryLoginFactory.debug = True

	log.startLogging(sys.stdout)
	main()
	reactor.run()
