#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - IP Address
"""
import unittest
import os
import threading
import ml_w_ip_address
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test DNS """
	def setUp(self):
		""" setUp """

	def test_ip_address_g01(self):
		""" ip_address_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "ip_address-g01.json"), os.path.join("running", "ip_address.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "ip_address-g01.jcfg"), os.path.join("running", "ip_address.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_ip_address.get(None, threading.RLock())
		self.assertEqual(e, (True, {
			'ip': [{
				'interface': 's0e2', 
				'ipv4': [
					{'ipv4_address': '192.168.10.1', 'ipv4_prefix': 16}, 
					{'ipv4_address': '192.168.10.2', 'ipv4_prefix': 16}, 
					{'ipv4_address': '192.168.10.3', 'ipv4_prefix': 16}
				], 
				'ipv6': [
					{'ipv6_prefix': 32, 'ipv6_address': '2001::1'}, 
					{'ipv6_prefix': 32, 'ipv6_address': '2001::2'}
				]
			}]
		}))

class test_set(unittest.TestCase):
	""" Test DNS """
	def setUp(self):
		""" setUp """

	def test_ip_address_g02(self):
		""" ip_address_g02 """
		ip_address = {
			'ip': [{
				'interface': 's0e2', 
				'ipv4': [
					{'ipv4_address': '192.168.10.1', 'ipv4_prefix': 16}, 
					{'ipv4_address': '192.168.10.2', 'ipv4_prefix': 16}, 
					{'ipv4_address': '192.168.10.3', 'ipv4_prefix': 16}
				], 
				'ipv6': [
					{'ipv6_prefix': 32, 'ipv6_address': '2001::1'}, 
					{'ipv6_prefix': 32, 'ipv6_address': '2001::2'}
				]
			}]
		}
		self.maxDiff = None
		e = ml_w_ip_address.set(None, ip_address)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "ip_address.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"ip": [{"interface": "s0e2", "ipv4": [{"ipv4_address": "192.168.10.1", "ipv4_prefix": 16}, {"ipv4_address": "192.168.10.2", "ipv4_prefix": 16}, {"ipv4_address": "192.168.10.3", "ipv4_prefix": 16}], "ipv6": [{"ipv6_prefix": 32, "ipv6_address": "2001::1"}, {"ipv6_prefix": 32, "ipv6_address": "2001::2"}]}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['ip_address {\n', '    ip-array {\n', '        ip { #1\n', '            interface s0e2\n', '            ipv4-array {\n', '                ipv4 { #1\n', '                    ipv4_address 192.168.10.1\n', '                    ipv4_prefix 16\n', '                }\n', '                ipv4 { #2\n', '                    ipv4_address 192.168.10.2\n', '                    ipv4_prefix 16\n', '                }\n', '                ipv4 { #3\n', '                    ipv4_address 192.168.10.3\n', '                    ipv4_prefix 16\n', '                }\n', '            }\n', '            ipv6-array {\n', '                ipv6 { #1\n', '                    ipv6_address 2001::1\n', '                    ipv6_prefix 32\n', '                }\n', '                ipv6 { #2\n', '                    ipv6_address 2001::2\n', '                    ipv6_prefix 32\n', '                }\n', '            }\n', '        }\n', '    }\n', '}\n'])

	def test_ip_address_g03(self):
		""" ip_address_g03 """
		ip_address = {
			'ip': [{
				'interface': 's0e2', 
				'ipv4': [
					{'ipv4_address': '192.168.10.1', 'ipv4_prefix': 16}, 
					{'ipv4_address': '192.168.10.2', 'ipv4_prefix': 16}, 
					{'ipv4_address': '192.168.10.3', 'ipv4_prefix': 16}
				], 
				'ipv6': [
					{'ipv6_prefix': 32, 'ipv6_address': '2001::1'}, 
					{'ipv6_prefix': 32, 'ipv6_address': '2001::2'}
				]
			}]
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_ip_address.set(None, ip_address, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "ip_address.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"ip": [{"interface": "s0e2", "ipv4": [{"ipv4_address": "192.168.10.1", "ipv4_prefix": 16}, {"ipv4_address": "192.168.10.2", "ipv4_prefix": 16}, {"ipv4_address": "192.168.10.3", "ipv4_prefix": 16}], "ipv6": [{"ipv6_prefix": 32, "ipv6_address": "2001::1"}, {"ipv6_prefix": 32, "ipv6_address": "2001::2"}]}]}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['ip_address {\n', '    ip-array {\n', '        ip { #1\n', '            interface s0e2\n', '            ipv4-array {\n', '                ipv4 { #1\n', '                    ipv4_address 192.168.10.1\n', '                    ipv4_prefix 16\n', '                }\n', '                ipv4 { #2\n', '                    ipv4_address 192.168.10.2\n', '                    ipv4_prefix 16\n', '                }\n', '                ipv4 { #3\n', '                    ipv4_address 192.168.10.3\n', '                    ipv4_prefix 16\n', '                }\n', '            }\n', '            ipv6-array {\n', '                ipv6 { #1\n', '                    ipv6_address 2001::1\n', '                    ipv6_prefix 32\n', '                }\n', '                ipv6 { #2\n', '                    ipv6_address 2001::2\n', '                    ipv6_prefix 32\n', '                }\n', '            }\n', '        }\n', '    }\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
