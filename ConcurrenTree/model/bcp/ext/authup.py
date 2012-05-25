from extension import *

class AuthUP(Extension):
	def __init__(self, auth, onlogin):
		'''
			auth - a ConcurrenTree.model.auth object
			onlogin(conn, username, docs) - callback
		'''
		Extension.__init__(self, "auth_u/p", {
			"login":self.login_attempt
		}, bound=True)
		self.auth = auth
		self.onlogin = onlogin

	def login_attempt(self, conn, obj):
		self.require(conn, "username", obj)
		self.require(conn, "password", obj)

		username = obj["username"]
		password = obj["password"]

		try:
			self.auth.load(username, password)
			self.auth.verify(username, password)
		except ValueError:
			self.error(conn, 302, "Bad Authorization Attempt")

		self.login_success(conn, username, self.auth[username])

	def login_success(self, conn, username, docs):
		print "Successful login by ", repr(username)
		self.onlogin(conn, username, docs)
