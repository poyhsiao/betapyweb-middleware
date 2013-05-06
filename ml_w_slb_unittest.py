#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	unittest - SLB
"""
import unittest
import os
import threading
import ml_w_slb
import ml_system
import shutil

class test_get(unittest.TestCase):
	""" Test SLB """
	def setUp(self):
		""" setUp """

	def test_slb_g01(self):
		""" slb_g01 """
		if "json" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "slb-g01.json"), os.path.join("running", "slb.txt"))
		if "jcfg" == ml_system.CFG_TYPE:
			shutil.copyfile(os.path.join("unittest", "slb-g01.jcfg"), os.path.join("running", "slb.txt"))
		if "pickle" == ml_system.CFG_TYPE:
			return
		self.maxDiff = None
		e = ml_w_slb.get(None, threading.RLock())
		self.assertEqual(e, (True, {'service_group': {'ipv4': [{'protocol': 'TCP', 'application_port': [80, 443], 'label': 'group1_v4'}], 'ipv6': [{'protocol': 'TCP', 'application_port': [80, 443], 'label': 'group1_v6'}]}, 'policy': {'ipv4': [{'service_group': 'group1_v4', 'destination_ip': 'many', 'fallback_server': 'fall1_v4', 'action': 'VIP', 'property': 'proper1', 'source_ip': 'one', 'real_server_group': 'real1_v4'}], 'ipv6': [{'service_group': 'group1_v6', 'destination_ip': 'many', 'fallback_server': '', 'action': 'Accept', 'property': '', 'source_ip': 'one', 'real_server_group': ''}]}, 'ip': {'ipv4': [{'ip_address': ['10.1.1.4'], 'label': 'one'}, {'ip_address': ['10.1.1.1', '10.1.1.2', '10.1.1.3', '10.1.1.4'], 'label': 'many'}], 'ipv6': [{'ip_address': ['2001::1'], 'label': 'one'}, {'ip_address': ['2001::1', '2001::2', '2001::3', '2001::4'], 'label': 'many'}]}, 'real_server_group': {'ipv4': [{'health_check': 'NA', 'weight': 1, 'maintenance_mode': False, 'label': 'real1_v4', 'tcp_check': {'to_remote_ip': '0.0.0.0', 'from_local_ip': '0.0.0.0', 'connection_timeout': 10}, 'https_get': {'delay_before_retry': 10, 'from_local_ip': '0.0.0.0', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}, 'pattern_check': {'to_remote_ip': '0.0.0.0', 'send': '', 'to_remote_port': 80, 'expect': '', 'timeout': 10}, 'smtp_check': {'to_remote_ip': '0.0.0.0', 'from_local_ip': '0.0.0.0', 'connection_timeout': 10, 'to_remote_port': 80, 'helo_name': ''}, 'icmp_check': {'timeout': 10}, 'ip_address': '10.1.1.1', 'http_get': {'delay_before_retry': 10, 'from_local_ip': '0.0.0.0', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}}, {'health_check': 'HTTP_GET', 'weight': 1, 'maintenance_mode': False, 'label': 'real2_v4', 'tcp_check': {'to_remote_ip': '0.0.0.0', 'from_local_ip': '0.0.0.0', 'connection_timeout': 10}, 'https_get': {'delay_before_retry': 10, 'from_local_ip': '0.0.0.0', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}, 'pattern_check': {'to_remote_ip': '0.0.0.0', 'send': '', 'to_remote_port': 80, 'expect': '', 'timeout': 10}, 'smtp_check': {'to_remote_ip': '0.0.0.0', 'from_local_ip': '0.0.0.0', 'connection_timeout': 10, 'to_remote_port': 80, 'helo_name': ''}, 'icmp_check': {'timeout': 10}, 'ip_address': '10.1.1.1', 'http_get': {'delay_before_retry': 10, 'from_local_ip': '10.1.1.1', 'url': '/', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}}, {'health_check': 'HTTPS_GET', 'weight': 1, 'maintenance_mode': False, 'label': 'real3_v4', 'tcp_check': {'to_remote_ip': '0.0.0.0', 'from_local_ip': '0.0.0.0', 'connection_timeout': 10}, 'https_get': {'delay_before_retry': 10, 'from_local_ip': '10.1.1.1', 'url': '/', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}, 'pattern_check': {'to_remote_ip': '0.0.0.0', 'send': '', 'to_remote_port': 80, 'expect': '', 'timeout': 10}, 'smtp_check': {'to_remote_ip': '0.0.0.0', 'from_local_ip': '0.0.0.0', 'connection_timeout': 10, 'to_remote_port': 80, 'helo_name': ''}, 'icmp_check': {'timeout': 10}, 'ip_address': '10.1.1.1', 'http_get': {'delay_before_retry': 10, 'from_local_ip': '0.0.0.0', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}}, {'health_check': 'ICMP_CHECK', 'weight': 1, 'maintenance_mode': False, 'label': 'real4_v4', 'tcp_check': {'to_remote_ip': '0.0.0.0', 'from_local_ip': '0.0.0.0', 'connection_timeout': 10}, 'https_get': {'delay_before_retry': 10, 'from_local_ip': '0.0.0.0', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}, 'pattern_check': {'to_remote_ip': '0.0.0.0', 'send': '', 'to_remote_port': 80, 'expect': '', 'timeout': 10}, 'smtp_check': {'to_remote_ip': '0.0.0.0', 'from_local_ip': '0.0.0.0', 'connection_timeout': 10, 'to_remote_port': 80, 'helo_name': ''}, 'icmp_check': {'timeout': 10}, 'ip_address': '10.1.1.1', 'http_get': {'delay_before_retry': 10, 'from_local_ip': '0.0.0.0', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}}], 'ipv6': [{'health_check': 'NA', 'weight': 1, 'maintenance_mode': False, 'label': 'real1_v6', 'tcp_check': {'to_remote_ip': '::', 'from_local_ip': '2001::2', 'connection_timeout': 10}, 'https_get': {'delay_before_retry': 10, 'from_local_ip': '::', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}, 'pattern_check': {'to_remote_ip': '::', 'send': '', 'to_remote_port': 80, 'expect': '', 'timeout': 10}, 'smtp_check': {'to_remote_ip': '::', 'from_local_ip': '::', 'connection_timeout': 10, 'to_remote_port': 80, 'helo_name': ''}, 'icmp_check': {'timeout': 10}, 'ip_address': '2001::1', 'http_get': {'delay_before_retry': 10, 'from_local_ip': '::', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}}, {'health_check': 'NA', 'weight': 1, 'maintenance_mode': False, 'label': 'real2_v6', 'tcp_check': {'to_remote_ip': '::', 'from_local_ip': '::', 'connection_timeout': 10}, 'https_get': {'delay_before_retry': 10, 'from_local_ip': '::', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}, 'pattern_check': {'to_remote_ip': '::', 'send': '', 'to_remote_port': 80, 'expect': '', 'timeout': 10}, 'smtp_check': {'to_remote_ip': '::', 'from_local_ip': '2001::2', 'connection_timeout': 10, 'to_remote_port': 25, 'helo_name': ''}, 'icmp_check': {'timeout': 10}, 'ip_address': '2001::1', 'http_get': {'delay_before_retry': 10, 'from_local_ip': '::', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}}, {'health_check': 'NA', 'weight': 1, 'maintenance_mode': False, 'label': 'real3_v6', 'tcp_check': {'to_remote_ip': '::', 'from_local_ip': '::', 'connection_timeout': 10}, 'https_get': {'delay_before_retry': 10, 'from_local_ip': '::', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}, 'pattern_check': {'to_remote_ip': '::', 'send': '', 'to_remote_port': 80, 'expect': 'HTTP', 'timeout': 10}, 'smtp_check': {'to_remote_ip': '::', 'from_local_ip': '::', 'connection_timeout': 10, 'to_remote_port': 80, 'helo_name': ''}, 'icmp_check': {'timeout': 10}, 'ip_address': '2001::1', 'http_get': {'delay_before_retry': 10, 'from_local_ip': '::', 'url': '', 'status_code': 200, 'connection_timeout': 10, 'to_remote_port': 80}}]}, 'fallback_server': {'ipv4': [{'ip_address': '10.1.1.1', 'label': 'fall1_v4'}], 'ipv6': [{'ip_address': '2001::1', 'label': 'fall1_v6'}]}}))

class test_set(unittest.TestCase):
	""" Test SLB """
	def setUp(self):
		""" setUp """

	def test_slb_g02(self):
		""" slb_g02 """
		slb = {
			"ip": {
				"ipv4": [
					{
						"label": "one",
						"ip_address": ["10.1.1.4"]
					},
					{
						"label": "many",
						"ip_address": ["10.1.1.1", "10.1.1.2", "10.1.1.3", "10.1.1.4"]
					}
				],
				"ipv6": [
					{
						"label": "one",
						"ip_address": ["2001::1"]
					},
					{
						"label": "many",
						"ip_address": ["2001::1", "2001::2", "2001::3", "2001::4"]
					}
				]
			},
			"service_group": {
				"ipv4": [
					{
						"label": "group1_v4",
						"protocol": "TCP",
						"application_port": [
							80,
							443
						]
					}
				],
				"ipv6": [
					{
						"label": "group1_v6",
						"protocol": "TCP",
						"application_port": [
							80,
							443
						]
					}
				]
			},
			"real_server_group": {
				"ipv4": [
					{
						"label": "real1_v4",
						"ip_address": "10.1.1.1",
						"weight": 1,
						"health_check": "NA",
						"maintenance_mode": False
					},
					{
						"label": "real2_v4",
						"ip_address": "10.1.1.1",
						"weight": 1,
						"health_check": "HTTP_GET",
						"http_get": {
							"url": "/",
							"status_code": 200,
							"from_local_ip": "10.1.1.1",
							"to_remote_port": 80,
							"connection_timeout": 10,
							"delay_before_retry": 10
						},
						"maintenance_mode": False
					},
					{
						"label": "real3_v4",
						"ip_address": "10.1.1.1",
						"weight": 1,
						"health_check": "HTTPS_GET",
						"https_get": {
							"url": "/",
							"status_code": 200,
							"from_local_ip": "10.1.1.1",
							"to_remote_port": 80,
							"connection_timeout": 10,
							"delay_before_retry": 10
						},
						"maintenance_mode": False
					},
					{
						"label": "real4_v4",
						"ip_address": "10.1.1.1",
						"weight": 1,
						"health_check": "ICMP_CHECK",
						"icmp_check": {
							"timeout": 10
						},
						"maintenance_mode": False
					},
				],
				"ipv6": [
					{
						"label": "real1_v6",
						"ip_address": "2001::1",
						"weight": 1,
						"health_check": "TCP_CHECK",
						"tcp_check": {
							"from_local_ip": "2001::2",
							"to_remote_ip": "2001::3",
							"connection_timeout": 10
						},
						"maintenance_mode": False
					},
					{
						"label": "real2_v6",
						"ip_address": "2001::1",
						"weight": 1,
						"health_check": "SMTP_CHECK",
						"smtp_check": {
							"helo_name": "",
							"from_local_ip": "2001::2",
							"to_remote_ip": "2001::3",
							"to_remote_port": 25,
							"connection_timeout": 10
						},
						"maintenance_mode": False
					},
					{
						"label": "real3_v6",
						"ip_address": "2001::1",
						"weight": 1,
						"health_check": "PATTERN_CHECK",
						"pattern_check": {
							"send": "",
							"expect": "HTTP",
							"to_remote_ip": "2001::3",
							"to_remote_port": 80,
							"timeout": 10
						},
						"maintenance_mode": False
					},
				]
			},
			"fallback_server": {
				"ipv4": [
					{
						"label": "fall1_v4",
						"ip_address": "10.1.1.1"
					}
				],
				"ipv6": [
					{
						"label": "fall1_v6",
						"ip_address": "2001::1"
					}
				]
			},
			"property": [
				{
					"label": "proper1",
					"forward_method": "NAT",
					"balance_mode": "Round-robin",
					"health_check_interval": 10,
					"persistence": 10,
					"ipv4_netmask": "255.255.255.0",
					"ipv6_prefix": 64
				}
			],
			"policy": {
				"ipv4": [
					{
						"source_ip": "one",
						"destination_ip": "many",
						"service_group": "group1_v4",
						"action": "VIP",
						"real_server_group": "real1_v4",
						"fallback_server": "fall1_v4",
						"property": "proper1"
					},
				],
				"ipv6": [
					{
						"source_ip": "one",
						"destination_ip": "many",
						"service_group": "group1_v6",
						"action": "Accept",
						"real_server_group": "",
						"fallback_server": "",
						"property": ""
					},
				]
			}
		}
		self.maxDiff = None
		e = ml_w_slb.set(None, slb)
		self.assertTrue(e[0], e[1])
		f = open(os.path.join("running", "slb.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"slb-server-1": "", "slb-server-2": "9.8.7.6", "domain-name": "test.domain.org", "hostname": "test.host"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['slb {\n', '    ip {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                label one\n', '                ip_address-array {\n', '                    ip_address 10.1.1.4 #1\n', '                }\n', '            }\n', '            ipv4 { #2\n', '                label many\n', '                ip_address-array {\n', '                    ip_address 10.1.1.1 #1\n', '                    ip_address 10.1.1.2 #2\n', '                    ip_address 10.1.1.3 #3\n', '                    ip_address 10.1.1.4 #4\n', '                }\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                label one\n', '                ip_address-array {\n', '                    ip_address 2001::1 #1\n', '                }\n', '            }\n', '            ipv6 { #2\n', '                label many\n', '                ip_address-array {\n', '                    ip_address 2001::1 #1\n', '                    ip_address 2001::2 #2\n', '                    ip_address 2001::3 #3\n', '                    ip_address 2001::4 #4\n', '                }\n', '            }\n', '        }\n', '    }\n', '    service_group {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                label group1_v4\n', '                protocol TCP\n', '                application_port-array {\n', '                    application_port 80 #1\n', '                    application_port 443 #2\n', '                }\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                label group1_v6\n', '                protocol TCP\n', '                application_port-array {\n', '                    application_port 80 #1\n', '                    application_port 443 #2\n', '                }\n', '            }\n', '        }\n', '    }\n', '    real_server_group {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                label real1_v4\n', '                ip_address 10.1.1.1\n', '            }\n', '            ipv4 { #2\n', '                label real2_v4\n', '                ip_address 10.1.1.1\n', '                health_check HTTP_GET\n', '                http_get {\n', '                    url /\n', '                    from_local_ip 10.1.1.1\n', '                }\n', '            }\n', '            ipv4 { #3\n', '                label real3_v4\n', '                ip_address 10.1.1.1\n', '                health_check HTTPS_GET\n', '                https_get {\n', '                    url /\n', '                    from_local_ip 10.1.1.1\n', '                }\n', '            }\n', '            ipv4 { #4\n', '                label real4_v4\n', '                ip_address 10.1.1.1\n', '                health_check ICMP_CHECK\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                label real1_v6\n', '                ip_address 2001::1\n', '                tcp_check {\n', '                    from_local_ip 2001::2\n', '                }\n', '            }\n', '            ipv6 { #2\n', '                label real2_v6\n', '                ip_address 2001::1\n', '                smtp_check {\n', '                    from_local_ip 2001::2\n', '                    to_remote_port 25\n', '                }\n', '            }\n', '            ipv6 { #3\n', '                label real3_v6\n', '                ip_address 2001::1\n', '                pattern_check {\n', '                    expect HTTP\n', '                }\n', '            }\n', '        }\n', '    }\n', '    fallback_server {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                label fall1_v4\n', '                ip_address 10.1.1.1\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                label fall1_v6\n', '                ip_address 2001::1\n', '            }\n', '        }\n', '    }\n', '    policy {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                source_ip one\n', '                destination_ip many\n', '                service_group group1_v4\n', '                real_server_group real1_v4\n', '                fallback_server fall1_v4\n', '                property proper1\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                source_ip one\n', '                destination_ip many\n', '                service_group group1_v6\n', '                action Accept\n', '            }\n', '        }\n', '    }\n', '}\n'])

	def test_slb_g03(self):
		""" slb_g03 """
		slb = {
			"ip": {
				"ipv4": [
					{
						"label": "one",
						"ip_address": ["10.1.1.4"]
					},
					{
						"label": "many",
						"ip_address": ["10.1.1.1", "10.1.1.2", "10.1.1.3", "10.1.1.4"]
					}
				],
				"ipv6": [
					{
						"label": "one",
						"ip_address": ["2001::1"]
					},
					{
						"label": "many",
						"ip_address": ["2001::1", "2001::2", "2001::3", "2001::4"]
					}
				]
			},
			"service_group": {
				"ipv4": [
					{
						"label": "group1_v4",
						"protocol": "TCP",
						"application_port": [
							80,
							443
						]
					}
				],
				"ipv6": [
					{
						"label": "group1_v6",
						"protocol": "TCP",
						"application_port": [
							80,
							443
						]
					}
				]
			},
			"real_server_group": {
				"ipv4": [
					{
						"label": "real1_v4",
						"ip_address": "10.1.1.1",
						"weight": 1,
						"health_check": "NA",
						"maintenance_mode": False
					},
					{
						"label": "real2_v4",
						"ip_address": "10.1.1.1",
						"weight": 1,
						"health_check": "HTTP_GET",
						"http_get": {
							"url": "/",
							"status_code": 200,
							"from_local_ip": "10.1.1.1",
							"to_remote_port": 80,
							"connection_timeout": 10,
							"delay_before_retry": 10
						},
						"maintenance_mode": False
					},
					{
						"label": "real3_v4",
						"ip_address": "10.1.1.1",
						"weight": 1,
						"health_check": "HTTPS_GET",
						"https_get": {
							"url": "/",
							"status_code": 200,
							"from_local_ip": "10.1.1.1",
							"to_remote_port": 80,
							"connection_timeout": 10,
							"delay_before_retry": 10
						},
						"maintenance_mode": False
					},
					{
						"label": "real4_v4",
						"ip_address": "10.1.1.1",
						"weight": 1,
						"health_check": "ICMP_CHECK",
						"icmp_check": {
							"timeout": 10
						},
						"maintenance_mode": False
					},
				],
				"ipv6": [
					{
						"label": "real1_v6",
						"ip_address": "2001::1",
						"weight": 1,
						"health_check": "TCP_CHECK",
						"tcp_check": {
							"from_local_ip": "2001::2",
							"to_remote_ip": "2001::3",
							"connection_timeout": 10
						},
						"maintenance_mode": False
					},
					{
						"label": "real2_v6",
						"ip_address": "2001::1",
						"weight": 1,
						"health_check": "SMTP_CHECK",
						"smtp_check": {
							"helo_name": "",
							"from_local_ip": "2001::2",
							"to_remote_ip": "2001::3",
							"to_remote_port": 25,
							"connection_timeout": 10
						},
						"maintenance_mode": False
					},
					{
						"label": "real3_v6",
						"ip_address": "2001::1",
						"weight": 1,
						"health_check": "PATTERN_CHECK",
						"pattern_check": {
							"send": "",
							"expect": "HTTP",
							"to_remote_ip": "2001::3",
							"to_remote_port": 80,
							"timeout": 10
						},
						"maintenance_mode": False
					},
				]
			},
			"fallback_server": {
				"ipv4": [
					{
						"label": "fall1_v4",
						"ip_address": "10.1.1.1"
					}
				],
				"ipv6": [
					{
						"label": "fall1_v6",
						"ip_address": "2001::1"
					}
				]
			},
			"property": [
				{
					"label": "proper1",
					"forward_method": "NAT",
					"balance_mode": "Round-robin",
					"health_check_interval": 10,
					"persistence": 10,
					"ipv4_netmask": "255.255.255.0",
					"ipv6_prefix": 64
				},
			],
			"policy": {
				"ipv4": [
					{
						"source_ip": "one",
						"destination_ip": "many",
						"service_group": "group1_v4",
						"action": "VIP",
						"real_server_group": "real1_v4",
						"fallback_server": "fall1_v4",
						"property": "proper1"
					},
				],
				"ipv6": [
					{
						"source_ip": "one",
						"destination_ip": "many",
						"service_group": "group1_v6",
						"action": "Accept",
						"real_server_group": "",
						"fallback_server": "",
						"property": ""
					},
				]
			}
		}
		class SetThread(threading.Thread):
			def run(self):
				e = ml_w_slb.set(None, slb, threading.RLock())
		sl = {}
		for i in range(100):
			sl.update({i:SetThread()})
			sl[i].setDaemon(True)
			sl[i].start()
		for i in range(100):
			sl[i].join()
		self.maxDiff = None
		f = open(os.path.join("running", "slb.txt"), "r")
		e = f.readlines()
		f.close()
		if "json" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['{"slb-server-1": "", "slb-server-2": "9.8.7.6", "domain-name": "test.domain.org", "hostname": "test.host"}'])
		if "jcfg" == ml_system.CFG_TYPE:
			self.assertEqual(e, ['slb {\n', '    ip {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                label one\n', '                ip_address-array {\n', '                    ip_address 10.1.1.4 #1\n', '                }\n', '            }\n', '            ipv4 { #2\n', '                label many\n', '                ip_address-array {\n', '                    ip_address 10.1.1.1 #1\n', '                    ip_address 10.1.1.2 #2\n', '                    ip_address 10.1.1.3 #3\n', '                    ip_address 10.1.1.4 #4\n', '                }\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                label one\n', '                ip_address-array {\n', '                    ip_address 2001::1 #1\n', '                }\n', '            }\n', '            ipv6 { #2\n', '                label many\n', '                ip_address-array {\n', '                    ip_address 2001::1 #1\n', '                    ip_address 2001::2 #2\n', '                    ip_address 2001::3 #3\n', '                    ip_address 2001::4 #4\n', '                }\n', '            }\n', '        }\n', '    }\n', '    service_group {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                label group1_v4\n', '                protocol TCP\n', '                application_port-array {\n', '                    application_port 80 #1\n', '                    application_port 443 #2\n', '                }\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                label group1_v6\n', '                protocol TCP\n', '                application_port-array {\n', '                    application_port 80 #1\n', '                    application_port 443 #2\n', '                }\n', '            }\n', '        }\n', '    }\n', '    real_server_group {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                label real1_v4\n', '                ip_address 10.1.1.1\n', '            }\n', '            ipv4 { #2\n', '                label real2_v4\n', '                ip_address 10.1.1.1\n', '                health_check HTTP_GET\n', '                http_get {\n', '                    url /\n', '                    from_local_ip 10.1.1.1\n', '                }\n', '            }\n', '            ipv4 { #3\n', '                label real3_v4\n', '                ip_address 10.1.1.1\n', '                health_check HTTPS_GET\n', '                https_get {\n', '                    url /\n', '                    from_local_ip 10.1.1.1\n', '                }\n', '            }\n', '            ipv4 { #4\n', '                label real4_v4\n', '                ip_address 10.1.1.1\n', '                health_check ICMP_CHECK\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                label real1_v6\n', '                ip_address 2001::1\n', '                tcp_check {\n', '                    from_local_ip 2001::2\n', '                }\n', '            }\n', '            ipv6 { #2\n', '                label real2_v6\n', '                ip_address 2001::1\n', '                smtp_check {\n', '                    from_local_ip 2001::2\n', '                    to_remote_port 25\n', '                }\n', '            }\n', '            ipv6 { #3\n', '                label real3_v6\n', '                ip_address 2001::1\n', '                pattern_check {\n', '                    expect HTTP\n', '                }\n', '            }\n', '        }\n', '    }\n', '    fallback_server {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                label fall1_v4\n', '                ip_address 10.1.1.1\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                label fall1_v6\n', '                ip_address 2001::1\n', '            }\n', '        }\n', '    }\n', '    policy {\n', '        ipv4-array {\n', '            ipv4 { #1\n', '                source_ip one\n', '                destination_ip many\n', '                service_group group1_v4\n', '                real_server_group real1_v4\n', '                fallback_server fall1_v4\n', '                property proper1\n', '            }\n', '        }\n', '        ipv6-array {\n', '            ipv6 { #1\n', '                source_ip one\n', '                destination_ip many\n', '                service_group group1_v6\n', '                action Accept\n', '            }\n', '        }\n', '    }\n', '}\n'])

if __name__ == "__main__":
	unittest.main()
