#!/usr/bin/env python
#-*- coding: UTF-8 -*- 
"""
	Boot Up Procedure
"""

def bootup():
	""" boot up procedure """
	# SAVE CONFIG:   copy running config to startup config
	# RELOAD CONFIG: copy startup config to running config
	# startup config always exists, running config exists only when
	# system up, bootup must RELOAD CONFIG.
	ret = True
	hw = {}
	report = {
	#	"license": xt_license.INVALID,
	#	"err": [],
	}
	#xt_func.sh(["chmod 777 /swlb/*"])
	#xt_func.sh(["chmod 666 /swlb/cfg/*"])

	#if is_new_machine():
	#	print "license:", xt_license.NEW
	#	report["license"] = xt_license.NEW
	#	return (True, report)
	#license = xt_license.get()[1]
	
	#eth0mac = xt_func.get_iface_mac("eth0")[1]
	#e = xt_license.validate(kind="system", bound=eth0mac, data=license)
	#if not e[0]:
	#	print "license:", e[1]
	#	report["license"] = e[1]
	#	return (False, report)

	#report["license"] = xt_license.GOOD

	#for (dev, pos, rtab, dum) in const.IFMAP:
	#	if dev.startswith("usb"): continue
	#	hw[pos] = {}
	#	e = xt_func.sh(["ip link set dev", dev, "down"])
	#	if not e[0]:
	#		ret = False
	#		report["err"].append(e[1])
	#	e = xt_func.sh(["ip link set dev", dev, "name", pos])
	#	if not e[0]:
	#		ret = False
	#		report["err"].append(e[1])
	#	e = xt_func.get_iface_mac(pos)
	#	if not e[0]:
	#		ret = False
	#		report["err"].append(e[1])
	#	hw[pos]["mac"] = e[1]
	#	e = xt_func.get_iface_mtu(pos)
	#	if not e[0]:
	#		ret = False
	#		report["err"].append(e[1])
	#	hw[pos]["mtu"] = e[1]
	#xt_func.save_json(const.HW_INFO, hw)

	#e = xt_func.sh(["modprobe dummy"])
	#if not e[0]:
	#	ret = False
	#	report["err"].append(e[1])
	#e = xt_func.sh(["ifconfig dummy0 up"])
	#if not e[0]:
	#	ret = False
	#	report["err"].append(e[1])
	#for (dev, pos, rtab, dum) in const.IFMAP:
	#	xt_func.sh(["ip rule add fwmark", rtab, "table", rtab]) 
	#	xt_func.sh(["ip addr add", dum+"/24", "brd + dev dummy0"])
	#xt_func.sh(["iptables -t nat -F"])
	#xt_func.sh(["iptables -t nat -A PREROUTING -j VSERVER"])
	#xt_func.sh(["iptables -t nat -A POSTROUTING -j WNAT"])
	#xt_func.sh(["iptables -F"])
	#xt_func.sh(["iptables -A PREROUTING -j NETPOS"])
	#xt_func.sh(["iptables -A PREROUTING -j IPGRP"])
	#xt_func.sh(["iptables -A PREROUTING -j SRVGRP"])
	#xt_func.sh(["iptables -A PREROUTING -j FIREWALL"])
	#xt_func.sh(["iptables -A PREROUTING -j SESSLIMIT"])
	#xt_func.sh(["iptables -A PREROUTING -j AUTOROUTE"])
	#xt_func.sh(["iptables -A PREROUTING -j TRAFFIC"])
	#xt_func.sh(["iptables -A POSTROUTING -j WSRC"])
	#xt_func.sh(["iptables -A INPUT -j LFILTER"])
	#xt_func.sh(["iptables -t mangle -F"])
	#xt_func.sh(["iptables -t mangle -A PREROUTING -j SRVGRP"])
	#xt_func.sh(["iptables -t mangle -A OUTPUT -j NETPOS"])
	#xt_func.sh(["iptables -t mangle -A OUTPUT -j IPGRP"])
	#xt_func.sh(["iptables -t mangle -A OUTPUT -j SRVGRP"])
	#xt_func.sh(["iptables -t mangle -A OUTPUT -j AUTOROUTE"])
	#xt_func.sh(["iptables -t mangle -A OUTPUT -j TRAFFIC"])

	#xt_func.sh(["ip addr flush dev lan"])
	#xt_func.sh(["ip addr add 192.168.0.1/24 brd + dev lan"])
	#xt_func.sh(["ip link set dev lan up"])

	#xt_func.sh(["mkdir -p /debug"])
	#xt_func.sh(["mount -t debugfs debugfs /debug"])
	#xt_func.sh(["modprobe linklog"])
	#xt_func.sh(["sysinfod"])
	#
	#xt_func.sh(["sysctl -w net.ipv4.ip_forward=1"])
	#xt_func.sh(["sysctl -w net.ipv4.conf.all.accept_redirects=1"])
	#xt_func.sh(["echo 2097152 > /proc/sys/net/core/rmem_max"])
	#xt_func.sh(["echo 799999 > /proc/sys/net/nf_conntrack_max"])
	#xt_func.sh(["echo 10240 > /proc/sys/net/ipv4/neigh/default/gc_thresh1"])
	#xt_func.sh(["echo 20480 > /proc/sys/net/ipv4/neigh/default/gc_thresh2"])
	#xt_func.sh(["echo 40960 > /proc/sys/net/ipv4/neigh/default/gc_thresh3"])

	#xt_func.sh(["rm -f", const.XTCFG_DIR + "*"])
	#prepare_cron_dir()
	#prepare_special_accounts()

	#e = xte_administration.bootup()
	#if not e[0]: 
	#	ret = False
	#	e[1].insert(0, "administration")
	#	report["err"].append(e[1])

	## Persistent daemons are not start/stop by xte_(event)s
	#e = xt_func.sh(["logd -d"])
	#if not e[0]: 
	#	ret = False
	#	e[1].insert(0, "logd")
	#	report["err"].append(e[1])

	#xt_func.iptables_raw_change_policy("DROP")
	#for x in const.MOD_LIST:
	#	page = __import__(x)	
	#	print page.__name__
	#	e = page.get()
	#	if not e[0]: 
	#		ret = False
	#		e[1].insert(0, page.TAG)
	#		report["err"].append(e[1])
	#	else:
	#		e = page.set(e[1], user=None)
	#		if not e[0]: 
	#			ret= False
	#			e[1].insert(0, page.TAG)
	#			report["err"].append(e[1])
	#xt_func.iptables_raw_change_policy("ACCEPT")
	print "all pages done"

	#xt_func.sh(["chmod 666 /swlb/xcfg/*"])
	return (ret, report)
	
if __name__ == "__main__":
	bootup()
