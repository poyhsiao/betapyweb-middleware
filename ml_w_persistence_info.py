#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Persistence Info

	Configuration Data Format
	{
		"vips": [
			{
				"vip": "192.168.200.200",
				"persistent": 300,
				"netmask": 24,
				"prefix": 0,
				"rips": [
					{
						"rip": "192.168.200.200",
						"weight": 1,
						"persistent": 100,
						"active": 0,
						"inactive": 0
					},
					...
				]
			},
			{
				"vip": "2001::1",
				"persistent": 300,
				"netmask": 0,
				"prefix": 128,
				"rips": [
					{
						"rip": "2001::2",
						"weight": 1,
						"persistent": 100,
						"active": 0,
						"inactive": 0
					},
					...
				]
			},
			...
		]
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
	cfg = {"vips":[]}
	try:
		rp0 = ml_func.sudo(["ipvsadm -ln --persistent-conn"])
		if not rp0[0]:
			return (False, ["ipvsadm fails"])
		data = rp0[1].split("\n")
		if "" in data:
			data.remove("")
		if len(data) <= 3:
			return (True, cfg)
		for line in data[3:]:
			tokens = line.split()
			if tokens[0] == "->":
				if len(tokens) != 6:
					return (False, ["fail to parse rip from ipvsadm output"])
				rip = {}
				if "]:" in tokens[1]:
					address = tokens[1].split("]:")[0].strip("[")
				else:
					address = tokens[1].split(":")[0]
				rip.update({
					"rip": address,
					"weight": tokens[2],
					"persistent": tokens[3],
					"active": tokens[4],
					"inactive": tokens[5]
				})
				if "rips" in vip.keys():
					vip["rips"].append(rip)
				else:
					return (False, ["fail to parse rip from ipvsadm output"])
			else:
				if len(tokens) != 5:
					return (False, ["fail to parse vip from ipvsadm output"])
				vip = {}
				if "]:" in tokens[1]:
					address = tokens[1].split("]:")[0].strip("[")
					netmask = 0
					prefix = 64
				else:
					address = tokens[1].split(":")[0]
					netmask = 24
					prefix = 0
				vip.update({
					"vip": address,
					"persistent": tokens[4],
					"netmask": netmask,
					"prefix": prefix,
					"rips": []
				})
				cfg["vips"].append(vip)
	except Exception as e:
		return (False, [str(e)])
	return (True, cfg)
