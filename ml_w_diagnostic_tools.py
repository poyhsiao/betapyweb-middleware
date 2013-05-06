#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Diagnostic Tools
"""
import ml_func
import ml_check
import ml_w_ip_address

def start_arping(user = None, threadlock = None):
	"""
		Web UI calls start_arping()
		return
			(True, None)
			(False, list)
	"""
	e = ml_w_ip_address.get()
	if e[0]:
		for i in e[1]["ip"]:
			for p in i["ipv4"]:
				target = p["ipv4_address"]
				ml_func.sudo(["arping -U -c 10", target], block=True)
	return (True, None)

def stop_arping(user = None, threadlock = None):
	"""
		Web UI calls stop_arping()
		return
			(True, None)
			(False, list)
	"""
	ml_func.sudo(["killall arping"], block=True)
	return (True, None)

def start_ping(user = None, target = None, threadlock = None):
	"""
		Web UI calls start_ping()
		return
			(True, str)
			(False, list)
	"""
	if target is None:
		return (False, ["invalid target"])
	if ml_check.validate_ipv4(target):
		e = ml_func.sudo(["ping -W 3 -c 10", target], block=True)
	elif ml_check.validate_ipv6(target):
		e = ml_func.sudo(["ping6 -W 3 -c 10", target], block=True)
	else:
		return (False, ["invalid target"])
	return e

def stop_ping(user = None, threadlock = None):
	"""
		Web UI calls stop_ping()
		return
			(True, None)
			(False, list)
	"""
	ml_func.sudo(["killall ping"], block=True)
	ml_func.sudo(["killall ping6"], block=True)
	return (True, None)

def start_traceroute(user = None, target = None, threadlock = None):
	"""
		Web UI calls start_traceroute()
		return
			(True, str)
			(False, list)
	"""
	if target is None:
		return (False, ["invalid target"])
	e = ml_func.sudo(["traceroute -n", target], block=True)
	return e

def stop_traceroute(user = None, threadlock = None):
	"""
		Web UI calls stop_traceroute()
		return
			(True, None)
			(False, list)
	"""
	ml_func.sudo(["killall traceroute"], block=True)
	return (True, None)
