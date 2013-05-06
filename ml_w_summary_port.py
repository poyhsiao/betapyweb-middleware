#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - Summary Port

	Configuration Data Format
	{
		"port": [
			{
				"interface": "s0e1",
				"status": "1000/Full",
				"RX": {
					"packets": 2740,
					"bytes": 215697
				},
				"TX": {
					"packets": 112,
					"bytes": 84835
				}
			},
			....
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
	cfg = {"port":[]}
	try:
		interfaces = []
		# get all interfaces
		ret_pis = ml_func.sudo(["ifconfig -a -s"])
		if ret_pis[0]:
			pis = ret_pis[1].split("\n")
			if len(pis) > 1:
				pis.remove(pis[0])
				for pi in pis:
					m = re.match("(\w+) ", pi)
					if m:
						if m.group(1) != "lo":
							interfaces.append(m.group(1))
		else:
			return (False, ["Fail to get port"])
		for i in interfaces:
			port = {"interface":i}
			# get every interface's speed/duplex
			ret_pe = ml_func.sudo(["ethtool", i, "| grep Speed"])
			if ret_pe[0]:
				s = ret_pe[1].split()[1]
				m = re.match("(\d+)", s)
				if m:
					speed = m.group()
				else:
					speed = "Unknown" 
			else:
				return (False, ["Fail to get port speed of " + i])
			ret_pe = ml_func.sudo(["ethtool", i, "| grep Duplex"])
			if ret_pe[0]:
				duplex = ret_pe[1].split()[1]
			else:
				return (False, ["Fail to get port duplex of " + i])
			port.update({"status": speed + "/" + duplex})
			# get every interface's RX, TX, and "Down" status.
			port.update({"RX":{}, "TX":{}})
			ret_pi = ml_func.sudo(["ifconfig", i])
			if ret_pi[0]:
				raw = ret_pi[1].split("\n")
				m = re.search("UP", raw[0])
				if m is None:
					port.update({"status":"Down"})
				for r in raw:
					m = re.search("RX packets\s+(\d+)\s+bytes\s+(\d+)", r)
					if m:
						port["RX"].update({"packets":m.group(1)})
						port["RX"].update({"bytes":m.group(2)})
					m = re.search("TX packets\s+(\d+)\s+bytes\s+(\d+)", r)
					if m:
						port["TX"].update({"packets":m.group(1)})
						port["TX"].update({"bytes":m.group(2)})
			else:
				return (False, ["Fail to get port " + i])
			cfg["port"].append(port)
	except Exception as e:
		return (False, [str(e)])
	return (True, cfg)
