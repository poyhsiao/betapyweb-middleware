#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Rates

	Configuration Data Format
	{
		"vips": [
			{
				"vip": "192.168.200.200",
				"port": 443,
				"connections/sec": 0,
				"inbound_packets/sec": 0,
				"inbound_bytes/sec": 0,
				"outbound_packets/sec": 0,
				"outbound_bytes/sec": 0,
				"rips": [
					{
						"rip": "192.168.200.200",
						"port": 443,
						"connections/sec": 0,
						"inbound_packets/sec": 0,
						"inbound_bytes/sec": 0,
						"outbound_packets/sec": 0,
						"outbound_bytes/sec": 0
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
		rr0 = ml_func.sudo(["ipvsadm -ln --rate"])
		if not rr0[0]:
			return (False, ["ipvsadm fails"])
		data = rr0[1].split("\n")
		#print data
		if "" in data:
			#print "take null lines out"
			data.remove("")
		#print "pass d-zone"
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
					"connections/sec": tokens[2],
					"inbound_packets/sec": tokens[3],
					"outbound_packets/sec": tokens[4],
					"inbound_bytes/sec": tokens[5],
					"outbound_bytes/sec": tokens[6]
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
					"connections/sec": tokens[2],
					"inbound_packets/sec": tokens[3],
					"outbound_packets/sec": tokens[4],
					"inbound_bytes/sec": tokens[5],
					"outbound_bytes/sec": tokens[6],
					"rips": []
				})
				cfg["vips"].append(vip)
	except Exception as e:
		return (False, [str(e)])
	return (True, cfg)
