#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Login
"""
import unittest
import os
import threading
import ml_w_login
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test Login """
	def setUp(self):
		""" setUp """

	def test_login_g01(self):
		""" login_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "login-g01.json"), os.path.join("running", "account.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "login-g01.jcfg"), os.path.join("running", "account.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_login.get("admin", "1234", threading.RLock())
		self.assertEqual(e, (True, None))

if __name__ == "__main__":
	unittest.main()
