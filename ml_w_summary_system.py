#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Summary System

	Configuration Data Format
	{
		"version": "1.0",
		"serial_number": "1111-2222-3333-4444",
		"uptime": "32 days, 8:14",
		"connections": 2843,
		"cpu_usage": 12.0
	}
"""
import re
import ml_system
import ml_func

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, cfg)
			(False, list)
	"""
	cfg = {}
	cfg.update({"version": ml_system.VERSION})
	cfg.update({"serial_number": ml_system.SERIAL_NUMBER})
	try:
		ut0 = ml_func.sudo(["uptime"])
		if ut0[0]:
			m = re.search("up .* user", ut0[1])
		else:
			return (False, ["Fail to get uptime"])
		if m:
			ut1 = m.group()
			m = re.search(".*,", ut1[3:-4])
		else:
			return (False, ["Fail to get uptime"])
		if m:
			ut2 = m.group()
			cfg.update({"uptime": ut2[:-1]})
		else:
			return (False, ["Fail to get uptime"])
		ret = ml_func.sudo(["cat /proc/sys/net/netfilter/nf_conntrack_count"])
		if ret[0]:
			cfg.update({"connections": int(ret[1])})
		else:
			cfg.update({"connections": 0})
		ups = ml_func.sudo(["ps -axo \%cpu="])
		if ups[0]:
			ua = 0.0
			for up in ups[1].split():
				ua += float(up)
			if ua > 100.0:
				ua = 100.0
			cfg.update({"cpu_usage": ua})
		else:
			return (False, ["Fail to get cpu usage"])
	except Exception as e:
		return (False, [str(e)])
	return (True, cfg)
