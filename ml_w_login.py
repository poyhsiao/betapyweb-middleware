#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Login

	Configuration Data Format from super class
"""
import ml_w_account

class login(ml_w_account.account):
	""" Login """
	def login(self, username = None, password = None):
		""" Check user name and return True or False """
		self.get()
		if username and isinstance(self.cfg, dict):
			if "user" in self.cfg.keys():
				for u in self.cfg["user"]:
					if u["name"] == username:
						if u["password"] == password:
							return (True, None)
		return (False, ["invalid user"])

def get(username = None, password = None, threadlock = None):
	"""
		Web UI calls get(user = "USER_NAME")
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = login(threadlock = threadlock)
		return obj.login(username, password)
	except Exception as e:
		return (False, [str(e)])
