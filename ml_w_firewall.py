#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - firewall

	Configuration Data Format
	{
		'rule': [
			{
				'source': 'lan', 
				'destination': 'wan', 
				'service': 'tcp@80'
				'log': 0, 
				'action': 'accept', 
			}
		]
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg
from ml_jcfg import N_

class firewall(ml_config.base):
	""" firewall """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "firewall.txt"), threadlock = None):
		""" init config """
		super(firewall, self).__init__(fpath, threadlock)
		self.tag = "firewall"
		self.cfg = {
		}
		self.helper = [(self.tag, [
			(N_("rule"), {
				"[]": [
					(N_("source"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True), 'lan', 'wan', 'dmz', 'localhost', 'any', ml_jcfg.JcGroup(), ml_jcfg.JcFqdn()], default='any')),
					(N_("destination"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True), 'lan', 'wan', 'dmz', 'localhost', 'any', ml_jcfg.JcGroup(), ml_jcfg.JcFqdn()], default='any')),
					(N_("service"), ml_jcfg.JcSelect(opt=['any', ml_jcfg.JcL3Proto(), ml_jcfg.JcL4Proto(), ml_jcfg.JcGroup()], default='any')),
					(N_("action"), ml_jcfg.JcSelect(opt=['accept', 'deny'], default=None)),
					(N_("log"), ml_jcfg.JcBOOL(default=0))
				]
			})
		])]

	def do_set(self):
		""" real task """
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = firewall(threadlock = threadlock)
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
		obj = firewall(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
