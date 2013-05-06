# -*- coding: utf-8 -*1-
import re
#ours
import const
import jcfg
import xt_func
import xte_network
from jcfg import N_

PING_SH_FILE="/tmp/diagnostic_ping.sh"
PING_RST_FILE="/tmp/diagnostic_ping.result"
PING_DONE_FILE="/tmp/diagnostic_ping.done"
TRACERT_SH_FILE="/tmp/diagnostic_traceroute.sh"
TRACERT_RST_FILE="/tmp/diagnostic_traceroute.result"
TRACERT_DONE_FILE="/tmp/diagnostic_traceroute.done"

def do_arpenforce():
	import xte_network
	return xte_network.do_arpenforce()

def _do_arping_detect(pos):
	clist = []
	addrs = xt_func.get_netpos_addresses(pos)
	proxys = xt_func.get_netpos_proxyarp(pos)
	
	for ip in proxys:
		addrs.append(ip)
	
	for ip in addrs:
		e = xt_func.sudo(["arping -D -w 1 -I", pos, ip, "| grep Unicast"])
		if e[0]:
			tok = e[1].split()
			mac = tok[4][1:-2].split(":")
			mac_s = []
			for i in mac:
				if len(i) == 1:
					mac_s.append("0" + i)
				else:
					mac_s.append(i)
			mac = ":".join(mac_s)
			clist.append((ip, pos, mac))
	return clist	

def do_ip_conflict_test():
	clist = []
	data = xte_network.get()[1]
	for pos in const.ALL_WANS:
		if data[pos]["enable"] != 1:
			continue
		if data[pos]["type"] == "static" or data[pos]["type"] == "dhcp":
			clist.extend(_do_arping_detect(pos))

	for pos in const.ALL_NOTWANS:
		clist.extend(_do_arping_detect(pos))

	if len(clist) > 0:
		return (True, clist)
	return (False, clist)

def poll_result(rst_f, done_f):
	import os
	done = os.path.exists(done_f)
	lines = []
	if os.path.exists(rst_f):
		f = open(rst_f, "r")
		lines = f.readlines()
		f.close()

	return (done, lines)

def kill_cmd(cmd):
	e = xt_func.sh(["ps | grep '"+ cmd+ "' | grep -v grep"])
	if not e[0]:
		return (False, [N_("nothing to kill")])

	tok = e[1].strip().split()
	e = xt_func.sudo(["kill", tok[0]])
	if not e[0]:
		return e

	return (True, [N_("kill"), tok[0]])

def start_ping(pos, target):
	dum = const.DUM_IP[pos]
	xt_func.sudo(["rm -f", PING_DONE_FILE, PING_RST_FILE])
	f = open(PING_SH_FILE, "w")
	f.write("#!/bin/sh\n")
	f.write("ping -W 3 -c 50 -I "+ dum+ " "+ target+ " >"+ PING_RST_FILE+ " 2>&1\n")
	f.write("touch "+ PING_DONE_FILE + "\n")
	f.close()
	e = xt_func.sh(["sh", PING_SH_FILE], block=False)
	return e

def poll_ping_result():
	return poll_result(PING_RST_FILE, PING_DONE_FILE)

def kill_ping():
	return kill_cmd("busybox ping")

def start_traceroute(pos, target):
	dum = const.DUM_IP[pos]
	xt_func.sudo(["rm -f", TRACERT_DONE_FILE, TRACERT_RST_FILE])
	f = open(TRACERT_SH_FILE, "w")
	f.write("#!/bin/sh\n")
	f.write("sudo traceroute -ns "+ dum+ " "+ target+ " >"+ TRACERT_RST_FILE+ " 2>&1\n")
	f.write("touch "+ TRACERT_DONE_FILE + "\n")
	f.close()
	e = xt_func.sh(["sh", TRACERT_SH_FILE], block=False)
	return e

def poll_traceroute_result():
	return poll_result(TRACERT_RST_FILE, TRACERT_DONE_FILE)

def kill_traceroute():
	return kill_cmd("sudo traceroute")	
