#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Login, Administration (Account)

	Configuration Data Format
	{
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

default = {
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
		},
	]
}

class account(ml_config.base):
	""" Account """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "account.txt"), threadlock = None):
		""" init config """
		super(account, self).__init__(fpath, threadlock)
		self.tag = "account"
		self.default = default
		self.user_syntax = {
			"name": {'T':str, 'D':"", 'M':True, 'S':None},
			"group": {'T':str, 'D':"", 'M':True, 'S':None},
			"password": {'T':str, 'D':"", 'M':True, 'S': None}
		}
		self.users_syntax = {
			"*": {'T':dict, 'D':{}, 'M':False, 'S':self.user_syntax}
		}
		self.main_syntax = {
			"user": {'T':list, 'D':[], 'M':False, 'S':self.users_syntax}
		}
		self.helper = [(self.tag, [
			(ml_jcfg.N_("user"), {
				"[]": [
					(ml_jcfg.N_("name"), ml_jcfg.JcDomainName()),
					(ml_jcfg.N_("group"), ml_jcfg.JcSelect(opt=["admin", "monitor"], default="admin")),
					(ml_jcfg.N_("password"), ml_jcfg.JcDomainName())
				]
			})
		])]
	def do_set(self):
		""" real task """
		status = True
		admin_password = ""
		monitor_password = ""
		users = ml_func.sudo(["awk -F: '{print $1}' /etc/passwd"])
		if not users[0]:
			return (False, ["fail to read /etc/passwd"])
		# SLB users cannot duplicate or exist in system users
		for user in users[1].split():
			try:
				ret_uid = ml_func.sudo(["id -u", user])
				if ret_uid[0]:
					uid = int(ret_uid[1].strip())
				else:
					continue
			except Exception as e:
				continue
			if uid < 1000:
				for u in self.cfg["user"]:
					if u["name"] == user:
						return (False, ["not allow account name " + user])
		name_list = []
		for u in self.cfg["user"]:
			if u["name"] in name_list:
				return (False, ["detected duplicate account name " + u["name"]])
			name_list.append(u["name"])
		# admin and monitor accounts must exist and can not change group
		if "admin" not in name_list or "monitor" not in name_list:
			return (False, ["not allow to delete default accounts"])
		for u in self.cfg["user"]:
			if u["name"] == "admin":
				admin_password = u["password"]
				if u["group"] != "admin":
					return (False, ["not allow to change default group of admin"])
			if u["name"] == "monitor":
				monitor_password = u["password"]
				if u["group"] != "monitor":
					return (False, ["not allow to change default group of monitor"])
		# delete all SLB users (UID >= 1000)
		for user in users[1].split():
			if user == "admin" or user == "monitor":
				continue
			try:
				ret_uid = ml_func.sudo(["id -u", user])
				if ret_uid[0]:
					uid = int(ret_uid[1].strip())
				else:
					continue
			except Exception as e:
				continue
			if uid >= 1000:
				ret_del = ml_func.sudo(["userdel -r", user])
				if not ret_del[0]:
					status = False
		if not status:
			return (False, ["fail to delete users"])
		e = ml_func.sudo(["userdel -r", "monitor"])
		e = ml_func.sudo(["userdel -r", "admin"])
		# delete all SLB groups
		e = ml_func.sudo(["groupdel", "monitor"])
		e = ml_func.sudo(["groupdel", "admin"])
		# add SLB users and groups
		e = ml_func.sudo(["useradd -m", "admin", "-s /bin/ml_c_cli_command.py"])
		if not e[0]:
			return (False, ["fail to add admin"])
		e = ml_func.sudo(["echo admin:" + admin_password + "| chpasswd"])
		print "echo admin:" + admin_password + "| chpasswd"
		if not e[0]:
			return (False, ["fail to set admin password"])
		e = ml_func.sudo(["useradd -m", "monitor", "-s /bin/ml_c_cli_command.py"])
		if not e[0]:
			return (False, ["fail to add monitor"])
		e = ml_func.sudo(["echo monitor:" + monitor_password + "| chpasswd"])
		print "echo monitor:" + monitor_password + "| chpasswd"
		if not e[0]:
			return (False, ["fail to set monitor password"])
		for new_user in self.cfg["user"]:
			if new_user["name"] == "admin" or new_user["name"] == "monitor":
				continue
			ret_new = ml_func.sudo(["useradd -m", new_user["name"], "-G", new_user["group"], "-s /bin/ml_c_cli_command.py"])
			if ret_new[0]:
				ret_password = ml_func.sudo(["echo", new_user["name"] + ":" + new_user["password"], "| chpasswd"])
				if not ret_password[0]:
					status = False
			else:
				status = False
		if not status:
			return (False, ["fail to add users"])
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = account(threadlock = threadlock)
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
		obj = account(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
