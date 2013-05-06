#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - VLAN

	Configuration Data Format
	{
		"vconfig": [
			{
				"interface": "s0e2",
				"vlan_id": 10
			},
			...
		]
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg
import ml_func
import re

class vlan(ml_config.base):
	""" VLAN """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "vlan.txt"), threadlock = None):
		""" init config """
		super(vlan, self).__init__(fpath, threadlock)
		self.tag = "vlan"
		self.cfg = {}
		self.vconfig_syntax = {
			#"name": {'T':str, 'D':"", 'M':True, 'S':None},
			"interface": {'T':str, 'D':"s0e1", 'M':True, 'S':None},
			"vlan_id": {'T':int, 'D':2, 'M':True, 'S': None}
		}
		self.vconfigs_syntax = {
			"*": {'T':dict, 'D':{}, 'M':False, 'S':self.vconfig_syntax}
		}
		self.main_syntax = {
			"vconfig": {'T':list, 'D':[], 'M':False, 'S':self.vconfigs_syntax}
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("vconfig"), {
				"[]": [
					#(ml_jcfg.N_("name"), ml_jcfg.JcDomainName()),
					(ml_jcfg.N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2', 'eth0'], default='s0e1')),
					(ml_jcfg.N_("vlan_id"), ml_jcfg.JcINT(default=100))
				]
			})
		])]
	def do_set(self):
		""" real task """
		e = ml_func.sudo(["ip -o -0 addr show"], ["| grep @"])
		if e[0]:
			lines = e[1].split("\n")
			for line in lines:
				m = re.search(":.*@", line)
				if m:
					e = ml_func.sudo(["ip link delete dev", line[m.start()+2:m.end()-1]])
		for vconfig in self.cfg['vconfig']:
			e = ml_func.sudo(["ip link add link", vconfig["interface"], "name", vconfig["interface"] + "." + str(vconfig["vlan_id"]), "type vlan id", str(vconfig["vlan_id"])])
			if not e[0]:
				return e
			e = ml_func.sudo(["ip link set dev", vconfig["interface"] + "." + str(vconfig["vlan_id"]), "up"])
			if not e[0]:
				return e
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = vlan(threadlock = threadlock)
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
		obj = vlan(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
