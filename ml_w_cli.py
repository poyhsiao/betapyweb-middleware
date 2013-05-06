#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Administration (CLI)

	Configuration Data Format
	{
		"ssh": True,
		"telnet": False
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg
import ml_func

default = {
	"ssh": True,
	"telnet": False
}

class cli(ml_config.base):
	""" CLI """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "cli.txt"), threadlock = None):
		""" init config """
		super(cli, self).__init__(fpath, threadlock)
		self.tag = "cli"
		self.default = default
		self.main_syntax = {
			"ssh": {'T':bool, 'D':True, 'M':True, 'S':None}, 
			"telnet": {'T':bool, 'D':False, 'M':True, 'S':None}
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("ssh"), ml_jcfg.JcBOOL(default=1)),
			(ml_jcfg.N_("telnet"), ml_jcfg.JcBOOL(default=0))
		])]
	def do_set(self):
		""" real task """
		# ssh
		if self.cfg["ssh"]:
			e = ml_func.sudo(["/etc/rc.d/sshd restart"])
			if not e[0]:
				return e
		else:
			e = ml_func.sudo(["/etc/rc.d/sshd stop"])
			if not e[0]:
				return e
		# telnet
		if self.cfg["telnet"]:
			e = ml_func.sudo(["/etc/rc.d/xinetd restart"])
			if not e[0]:
				return e
		else:
			e = ml_func.sudo(["/etc/rc.d/xinetd stop"])
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
		obj = cli(threadlock = threadlock)
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
		obj = cli(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])

def start_sshd(user = None, threadlock = None):
	"""
		Web UI calls start_sshd()
		return
			(True, None)
			(False, list)
	"""
	e = ml_func.sudo(["/etc/rc.d/sshd restart"])
	if not e[0]:
		return e
	else:
		return (True, None)

def stop_sshd(user = None, threadlock = None):
	"""
		Web UI calls stop_sshd()
		return
			(True, None)
			(False, list)
	"""
	e = ml_func.sudo(["/etc/rc.d/sshd stop"])
	if not e[0]:
		return e
	else:
		return (True, None)

def start_telnetd(user = None, threadlock = None):
	"""
		Web UI calls start_telnetd()
		return
			(True, None)
			(False, list)
	"""
	e = ml_func.sudo(["/etc/rc.d/xinetd restart"])
	if not e[0]:
		return e
	else:
		return (True, None)

def stop_telnetd(user = None, threadlock = None):
	"""
		Web UI calls stop_telnetd()
		return
			(True, None)
			(False, list)
	"""
	e = ml_func.sudo(["/etc/rc.d/xinetd stop"])
	if not e[0]:
		return e
	else:
		return (True, None)
