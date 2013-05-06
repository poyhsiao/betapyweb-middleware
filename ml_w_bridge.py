#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Bridge

	Configuration Data Format
	{
		"br": [
			{
				"name": "s0b1",
				"interface": [
					"s0e1",
					"s0e2"
				],
				"STP": True,
				"hello_time": 5,
				"max_message_age": 5,
				"forward_delay": 5
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

class bridge(ml_config.base):
	""" Bridge """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "bridge.txt"), threadlock = None):
		""" init config """
		super(bridge, self).__init__(fpath, threadlock)
		self.tag = "bridge"
		self.cfg = {}
		self.interface_syntax = {
			"*": {'T':str, 'D':"s0e1", 'M':True, 'S':None}
		}
		self.br_syntax = {
			"name": {'T':str, 'D':"", 'M':True, 'S':None},
			"interface": {'T':list, 'D':[], 'M':True, 'S':self.interface_syntax},
			"STP": {'T':bool, 'D': True, 'M': True, 'S': None},
			"hello_time": {'T':int, 'D':2, 'M':True, 'S': None},
			"max_message_age": {'T':int, 'D':20, 'M':True, 'S': None},
			"forward_delay": {'T':int, 'D':15, 'M':True, 'S': None}
		}
		self.brs_syntax = {
			"*": {'T':dict, 'D':{}, 'M':False, 'S':self.br_syntax}
		}
		self.main_syntax = {
			"br": {'T':list, 'D':[], 'M':False, 'S':self.brs_syntax}
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("br"), {
				"[]": [
					(ml_jcfg.N_("name"), ml_jcfg.JcDomainName()),
					(ml_jcfg.N_("interface"), {
						"[]": ml_jcfg.JcSelect(opt=['s0e1', 's0e2', 'eth0'], default='s0e1')
					}),
					(ml_jcfg.N_("STP"), ml_jcfg.JcBOOL(default=1)),
					(ml_jcfg.N_("hello_time"), ml_jcfg.JcINT(default=2)),
					(ml_jcfg.N_("max_message_age"), ml_jcfg.JcINT(default=20)),
					(ml_jcfg.N_("forward_delay"), ml_jcfg.JcINT(default=15))
				]
			})
		])]
	def do_set(self):
		""" real task """
		status = True
		emsg = []
		content = ml_func.sudo(["brctl show"])
		if content[0]:
			lines = content[1].split("\n")
			lines.remove(lines[0])
			for line in lines:
				b = re.search(".*?\t", line)
				if b:
					ret = ml_func.sudo(["brctl delbr", line[0:b.end()-1]])
					if not ret[0]:
						return (False, ["Fail to delete bridges"])
		for br in self.cfg['br']:
			ret = ml_func.sudo(["brctl addbr", br["name"]])
			if not ret[0]:
				return (False, ["Fail to add bridge " + br["name"]])
			buf = ["brctl addif", br["name"]]
			for interface in br["interface"]:
				sbuf = buf[:]
				sbuf.append(interface)
				ret = ml_func.sudo(sbuf)
				if not ret[0]:
					return (False, ["Fail to add interface " + br["interface"] + " to bridge " + br["name"]])
			if br["STP"]:
				stp = "on"
			else:
				stp = "off"
			ret = ml_func.sudo(["brctl stp", br["name"], stp])
			if not ret[0]:
				status = False
				emsg.append("Fail to set STP mode")
			ret = ml_func.sudo(["brctl sethello", br["name"], str(br["hello_time"])])
			if not ret[0]:
				status = False
				emsg.append("Fail to set hello time")
			ret = ml_func.sudo(["brctl setmaxage", br["name"], str(br["max_message_age"])])
			if not ret[0]:
				status = False
				emsg.append("Fail to set max message age")
			ret = ml_func.sudo(["brctl setfd", br["name"], str(br["forward_delay"])])
			if not ret[0]:
				status = False
				emsg.append("Fail to set forward delay")
		if not status:
			return (False, emsg)
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = bridge(threadlock = threadlock)
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
		obj = bridge(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
