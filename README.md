# Flurry
Login daemon for small flightless birds.

# AuthSource
The `AuthSource` class is a simple wrapper around Twisted's `LineReceiver`. It is intentionally left open ended so that various database schemas and login methods can be implemented. However, Flurry offers an `XMLProtocol` class that handles the CP client's initial XML handshake and login, leaving you with the job of validating the credentials and telling the client your response. Check out `ExampleAuthSource` in `flurry/auth/example.py` to see how it works.

# Installation/Use
You can clone the repository and use pip to install the dependencies (a la `pip install -r requirements.txt`). By default it does not come with any sort of DBMS dependencies, only Twisted (and its respective dependencies). If you use an `AuthSource` that uses other packages, make sure to install them.

You can edit `runFlurry.py` to suit your needs. It uses the `ExampleAuthSource` on port `7112` and simply prints the user data it receives. Executing it will start the server in all of its shiny glory.

# Docs?
I'm writing them okay calm down GEEZ
