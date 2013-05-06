#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Counters

	Configuration Data Format
	{
		"vips": [
			{
				"vip": "192.168.200.200",
				"port": 443,
				"connections": 0,
				"inbound_packets": 0,
				"inbound_bytes": 0,
				"outbound_packets": 0,
				"outbound_bytes": 0,
				"rips": [
					{
						"rip": "192.168.200.200",
						"port": 443,
						"connections": 0,
						"inbound_packets": 0,
						"inbound_bytes": 0,
						"outbound_packets": 0,
						"outbound_bytes": 0
					},
					...
				]
			},
			...
		]
	}
"""
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
		rc0 = ml_func.sudo(["ipvsadm -ln --stats"])
		if not rc0[0]:
			return (False, ["ipvsadm fails"])
		data = rc0[1].split("\n")
		if "" in data:
			data.remove("")
		if len(data) <= 3:
			return (True, cfg)
		for line in data[3:]:
			tokens = line.split()
			if tokens[0] == "->":
				rip = {}
				if "]:" in tokens[1]:
					address = tokens[1].split("]:")[0].strip("[")
					port = tokens[1].split("]:")[1]
				else:
					address = tokens[1].split(":")[0]
					port = tokens[1].split(":")[1]
				rip.update({
					"rip": address,
					"port": port,
					"connections": tokens[2],
					"inbound_packets": tokens[3],
					"outbound_packets": tokens[4],
					"inbound_bytes": tokens[5],
					"outbound_bytes": tokens[6]
				})
				if "rips" in vip.keys():
					vip["rips"].append(rip)
				else:
					return (False, ["fail to parse rip from ipvsadm output"])
			else:
				if len(tokens) != 7:
					return (False, ["fail to parse vip from ipvsadm output"])
				vip = {}
				if "]:" in tokens[1]:
					address = tokens[1].split("]:")[0].strip("[")
					port = tokens[1].split("]:")[1]
				else:
					address = tokens[1].split(":")[0]
					port = tokens[1].split(":")[1]
				vip.update({
					"vip": address,
					"port": port,
					"connections": tokens[2],
					"inbound_packets": tokens[3],
					"outbound_packets": tokens[4],
					"inbound_bytes": tokens[5],
					"outbound_bytes": tokens[6],
					"rips": []
				})
				cfg["vips"].append(vip)
	except Exception as e:
		return (False, [str(e)])
	return (True, cfg)
