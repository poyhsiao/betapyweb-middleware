#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - Account
"""
import unittest
import os
import threading
import ml_w_account
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test Account """
	def setUp(self):
		""" setUp """

	def test_account_g01(self):
		""" account_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "account-g01.json"), os.path.join("running", "account.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "account-g01.jcfg"), os.path.join("running", "account.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_account.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"user": [
				{
					"name": "admin",
					"group": "admin",
					"password": "1234"
				},
				{
					"name": "monitor",
					"group": "monitor",
					"password": "5678"
				}
			]
		}))

class test_set(unittest.TestCase):
	""" Test Account """
	def setUp(self):
		""" setUp """

	def test_account_g02(self):
		""" account_g02 """
		account = {
			"user": [
				{
					"name": "admin",
					"group": "admin",
					"password": "1234"
				},
				{
					"name": "monitor",
					"group": "monitor",
					"password": "5678"
				}
			]
		}
		self.maxDiff = None
		e = ml_w_account.set(None, account)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "account.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"user": [{"password": "1234", "group": "admin", "name": "admin"}, {"password": "5678", "group": "monitor", "name": "monitor"}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['account {\n', '    user-array {\n', '        user { #1\n', '            name admin\n', '            password 1234\n', '        }\n', '        user { #2\n', '            name monitor\n', '            group monitor\n', '            password 5678\n', '        }\n', '    }\n', '}\n'])

	def test_account_g03(self):
		""" account_g03 """
		account = {
			"user": [
				{
					"name": "admin",
					"group": "admin",
					"password": "1234"
				},
				{
					"name": "monitor",
					"group": "monitor",
					"password": "5678"
				}
			]
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_account.set(None, account, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "account.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"user": [{"password": "1234", "group": "admin", "name": "admin"}, {"password": "5678", "group": "monitor", "name": "monitor"}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['account {\n', '    user-array {\n', '        user { #1\n', '            name admin\n', '            password 1234\n', '        }\n', '        user { #2\n', '            name monitor\n', '            group monitor\n', '            password 5678\n', '        }\n', '    }\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
