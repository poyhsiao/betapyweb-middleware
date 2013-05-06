#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - DateTime
"""
import unittest
import os
import threading
import ml_w_date_time
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test DateTime """
	def setUp(self):
		""" setUp """

	def test_date_time_g01(self):
		""" date_time_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "date_time-g01.json"), os.path.join("running", "date_time.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "date_time-g01.jcfg"), os.path.join("running", "date_time.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_date_time.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			"time_zone": "Taipei",
			"time_server": "59.124.196.83",
			"date": "2013/02/04",
			"time": "13:10:00"
		}))

class test_set(unittest.TestCase):
	""" Test DateTime """
	def setUp(self):
		""" setUp """

	def test_date_time_g02(self):
		""" date_time_g02 """
		date_time = {
			"time_zone": "Taipei",
			"time_server": "59.124.196.83",
			"date": "2013/02/04",
			"time": "13:10:00"
		}
		self.maxDiff = None
		e = ml_w_date_time.set(None, date_time)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "date_time.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"date": "2013/02/04", "time_server": "59.124.196.83", "time_zone": "Taipei", "time": "13:10:00"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['date_time {\n', '    time_zone Taipei\n', '    time_server 59.124.196.83\n', '    date 2013/02/04\n', '    time 13:10:00\n', '}\n'])

	def test_date_time_g03(self):
		""" date_time_g03 """
		date_time = {
			"time_zone": "Taipei",
			"time_server": "59.124.196.83",
			"date": "2013/02/04",
			"time": "13:10:00"
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_date_time.set(None, date_time, threading.RLock())
		sl = {}
		for i in range(10):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(10):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "date_time.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"date": "2013/02/04", "time_server": "59.124.196.83", "time_zone": "Taipei", "time": "13:10:00"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['date_time {\n', '    time_zone Taipei\n', '    time_server 59.124.196.83\n', '    date 2013/02/04\n', '    time 13:10:00\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
