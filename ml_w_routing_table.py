#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Routing Table

	Configuration Data Format
	{
		"ipv4": [
			{
				"destination": "192.168.0.0",
				"prefix": 24,
				"gateway": "192.168.0.254",
				"interface": "s0e1"
			},
			...
		],
		"ipv6": [
			{
				"destination": "2001::",
				"prefix": 64,
				"gateway": "2001::2001",
				"interface": "s0e1"
			},
			...
		]
	}
"""
import os
import ml_system
import ml_config
import ml_check
import ml_jcfg
from ml_jcfg import N_
import ml_func

class routing_table(ml_config.base):
	""" Routing Table """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "routing_table.txt"), threadlock = None):
		""" init config """
		super(routing_table, self).__init__(fpath, threadlock)
		self.tag = "routing_table"
		self.cfg = {}
		self.ipv4_syntax = {
			"destination": {'T':str, 'D':"192.168.0.0", 'M':True, 'S': None, 'V': [ml_check.validate_ipv4]},
			"prefix": {'T':int, 'D':24, 'M':True, 'S': None, 'V': [ml_check.validate_ipv4_prefix]},
			"gateway": {'T':str, 'D':"192.168.0.254", 'M':True, 'S': None, 'V': [ml_check.validate_ipv4]},
			"interface": {'T': str, 'D': "s0e1", 'M': True, 'S': None}
		}
		self.ipv6_syntax = {
			"destination": {'T':str, 'D':"2001::", 'M':True, 'S': None, 'V': [ml_check.validate_ipv6]},
			"prefix": {'T':int, 'D':64, 'M':True, 'S': None, 'V': [ml_check.validate_ipv6_prefix]},
			"gateway": {'T':str, 'D':"2001::2001", 'M':True, 'S': None, 'V': [ml_check.validate_ipv6]},
			"interface": {'T': str, 'D': "s0e1", 'M': True, 'S': None}
		}
		self.ipv4s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':False, 'S':self.ipv4_syntax}
		}
		self.ipv6s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':False, 'S':self.ipv6_syntax}
		}
		self.main_syntax = {
			"ipv4": {'T':list, 'D':[], 'M':False, 'S':self.ipv4s_syntax},
			"ipv6": {'T':list, 'D':[], 'M':False, 'S':self.ipv6s_syntax}
		}
		self.helper = [(self.tag, [
			(N_("ipv4"), {
				"[]": [
					(N_("destination"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True)])),
					(N_("prefix"), ml_jcfg.JcINT(default=24)),
					(N_("gateway"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True)])),
					(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e1'))
				]
			}),
			(N_("ipv6"), {
				"[]": [
					(N_("destination"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)),
					(N_("prefix"), ml_jcfg.JcINT(default=64)),
					(N_("gateway"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)),
					(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e1'))
				]
			})
		])]
	def do_set(self):
		""" real task """
		status = True
		emsg = []
		#ml_func.sudo(["ip route flush table ", table])
		ml_func.sudo(["ip route flush cache"])
		for ip in self.cfg["ipv4"] + self.cfg['ipv6']:
			e = ml_func.sudo(["ip link set dev ", ip["interface"], " up"])
			if not e[0]:
				status = False
				emsg.append(e[1])
			e = ml_func.sudo(["ip route add ", ip["destination"] + "/" + str(ip["prefix"]), " dev ", ip["interface"], " via ", ip["gateway"]])
			if not e[0]:
				status = False
				emsg.append(e[1])
		if not status:
			return (False, emsg)
		else:
			return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = routing_table(threadlock = threadlock)
		return obj.get()
	except Exception as e:
		return (False, [str(e)])

def set(user = None, cfg = {}, threadlock = None):
	"""
		Web UI calls set()
		return
			(True, None)
			(False, list)
	"""
	try:
		obj = routing_table(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
