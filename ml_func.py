#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Middleware Function
"""
import datetime
import fcntl
import json
import os.path
import subprocess
import time
# ours
import ml_jcfg
#import const
#import xtd_logd
import ml_log

log_workflow = False

def log_failure(cmd, err):
	text = str(datetime.datetime.now()) + " " 
	text += cmd + "\n"
	text += str(err) + "\n"
	fp = open(const.FAILURE_LOG, "a")
	fp.write(text)
	fp.close()

def sh(ocmd, stdout="", block=True):
	cmd = " ".join(ocmd)
	if log_workflow:
		#fp = open(const.WORKFLOW_LOG, "a")
		#fp.write(cmd + "\n")
		#fp.close()
		ml_log.log(__name__ + ": " + cmd)
	try:
		p = subprocess.Popen(cmd, shell=True,
			stdin = subprocess.PIPE,
			stdout = subprocess.PIPE,
			stderr = subprocess.PIPE,
			close_fds=True)
		if block:
			x = p.communicate()
			if 0 != p.returncode:
				#log_failure(cmd, x[0])
				ml_log.log(__name__ + ": " + cmd + str(x[0]))
				return (False, x[0])
		else:
			x = [""]
	except Exception as e:
		#log_failure(cmd, e)
		ml_log.log(__name__ + ": " + cmd + str(e))
		return (False, str(e))
	return (True, x[0])

def sudo(cmd, stdout = "", block=True):
	cmd.insert(0, "sudo")
	return sh(cmd, stdout, block)

def get_netpos_proxyarp(pos):
	rst = []
	e = sudo(["xtctl netpos", pos])
	lines = e[1].split("\n")
	i = 0
	for line in lines:
		i += 1
		if line == "PROXYARP":
			break	
	while lines[i] != "SUBNET":
		rst.extend(iprange2list(lines[i]))
		i += 1
	return rst
 
def get_netpos_addresses(pos):
	rst = []
	e = sudo(["xtctl netpos", pos])
	lines = e[1].split("\n")
	i = 0
	for line in lines:
		i += 1
		if line == "LOCALHOST":
			break	
	while lines[i] != "PROXYARP":
		rst.extend(iprange2list(lines[i]))
		i += 1
	return rst 

def num_of_set_bits(val):
	n = 0
	while val:
		n += (val & 1)
		val = val >> 1
	return n

def get_iface_mac(iface):
	try:
		f = open("/sys/class/net/" + iface + "/address")
		x = f.read().strip()
		f.close()
	except Exception as e:
		return (False, str(e))
	return (True, x)

def get_iface_mtu(iface):
	try:
		f = open("/sys/class/net/" + iface + "/mtu")
		x = f.read().strip()
		f.close()
	except Exception as e:
		return (False, str(e))
	return (True, int(x))

def get_arp_entry(addr, pos="all"):
	cmd = ["arp -n"]
	if pos != "all":
		cmd.append("-i "+ pos)
	cmd.append(addr)
	cmd.append("| grep -v incomplete | grep -v match")
	e = sudo(cmd)
	if not e[0]:
		return (False, "no valid entry about "+ addr)
	tmp = e[1].strip()
	return (True, e[1].split()[3])

def ip2int(ip):
	v = 0
	try:
		t = [int(i) for i in ip.split(".")]
		if len(t) != 4: return None
		for i in range(0,4):
			if 0 > t[i] or t[i] > 255: return None
			v += (t[i] << (24 - 8*i))
	except:
		return None
	return v

def int2ip(val):
	import struct
	import socket
	return socket.inet_ntop(socket.AF_INET, struct.pack("!I", val))

def iprange2list(iprange, kind="str"):
	tok = iprange.split("-")
	if len(tok) == 1:
		if kind == "int":
			return [ip2int(tok[0])]
		return tok
	start = ip2int(tok[0])
	end = ip2int(tok[1]) + 1
	if kind == "int":
		return range(start, end)
	return [int2ip(i) for i in range(start, end)]

def is_ip_in_subnet(ip, subnet):
	ipv = ip2int(ip)
	tok = subnet.split("/")
	maskv = ip2int(tok[1]) 
	subnetv = ip2int(tok[0]) & ip2int(tok[1]) 
	return (ipv & maskv) == subnetv

def cidr2ipboundary(cidr, kind="str"):
	"""get the 1st and last IP of given cidr as int or string"""
	tok = cidr.split("/")
	base = ip2int(tok[0])
	prefix = int(tok[1])
	fst = base + 1
	last = base + 2 ** (32 - prefix) - 2 
	if kind == "int":
		return (fst, last)
	return (int2ip(fst), int2ip(last))

def inverse_iprange(range_list, netmask):
	rst = []
	cidr = block2cidr(range_list[0].split("-")[0]+ "/"+ netmask)
	boundary = cidr2ipboundary(cidr, "int")
	pool = range(boundary[0], boundary[1] + 1)
	for r in range_list:
		tok = r.split("-") 
		start = ip2int(tok[0])
		end = ip2int(tok[-1])
		pool = [i for i in pool if i < start or i > end]
	
	rend = pool[0]
	lend = rend 
	for j in pool[1:]:
		if j != rend + 1:
			tmp = int2ip(lend)
			if lend != rend:
				tmp += "-" + int2ip(rend)
			rst.append(tmp)
			lend = j
		rend = j
	tmp = int2ip(lend)
	if lend != rend:
		tmp += "-" + int2ip(rend)
	rst.append(tmp)
	return rst

def block2cidr(block):
	"""net block (192.168.0.0/255.255.255.0) to cidr notation"""
	t = block.split("/")
	ip_val = ip2int(t[0])
	mask_val = ip2int(t[1])
	return int2ip(ip_val & mask_val) + "/" + str(num_of_set_bits(mask_val))

def ipv4mask2prefix(mask):
	m_val = ip2int(mask)
	p_val = num_of_set_bits(m_val)
	return str(p_val)

def load_json(fpath):
	try: 
		f = open(fpath, "r")
		data = json.load(f)
		f.close()
	except Exception as e:
		return (False, str(e))
	return (True, data)

def save_json(fpath, data):
	f = open(fpath, "w")
	json.dump(data, f, indent=4)
	f.close()

def lock(fpath):
	f = open(fpath, "w")
	try:
		fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
	except Exception as e:
		f.close()
		return (False, str(e))
	return (True, f)

def unlock(f):
	fcntl.flock(f, fcntl.LOCK_UN)
	f.close()

def wait_bootup():
	while not os.path.exists(const.BOOTUP_REPORT):
		print "System is booting up now"
		time.sleep(3)
	time.sleep(1) # wait xt_bootup.py to dump report
	return load_json(const.BOOTUP_REPORT)[1]

def reboot(msg):
	print msg
	e = sudo(["/sbin/reboot -d &"]) # wait 3 secs for returnning to UI
	if not e[0]:
		print e[1]
	return e

def kill_by_pid_f(pid_f):
	if not os.path.exists(pid_f):
		return (False, "no pid file")
	f = open(pid_f, "r")
	pid = f.read().strip()
	f.close()

	e = sudo(["kill", pid])
	if not e[0]:
		return (False, e[1])
	return (True, None)

def crontab_replace(job, run_at="* * * * *"):
	e = sh(["sed -i", "'\#"+ job+ "#d'", const.CRON_TAB])
	cmd = "echo '"+ run_at+ " "+ job+ "' >> "+ const.CRON_TAB 
	e = sudo(["sh -c \""+ cmd+ "\""])
	return sudo(["crontab", const.CRON_TAB])

def iptables_raw_change_policy(action):
	sudo(["iptables -t raw -P PREROUTING", action])
	sudo(["iptables -t raw -P OUTPUT", action])
	return (True, None)

def set_default_cfg(tag):
	if not os.path.exists(const.CFG_DIR+tag+".txt"):
		sudo(["cp "+const.MIDWARE_DIR+"factory_default/"+tag+".txt "+const.CFG_DIR])
		sudo(["chmod 666 "+const.CFG_DIR+tag+".txt"])
	return (True, None)
	
def xte_get(tag, helper, fname, fdir):
	e = jcfg.load_file(helper, fname, fdir)
	if not e[0]: return e
	return (True, e[1][tag])

def xte_set(tag, helper, data, callback, fname, fdir, user):
	ret = True
	emsg = []
	e = lock(const.APPLY_LOCK)
	if not e[0]:
		return (False, ["System locked"])
	lockf = e[1]

	e = callback(data)
	logmsg = "success"
	if not e[0]:
		logmsg = "failure"
		ret = False
		emsg.append(e[1])
		# load previous config and callback again
		e = jcfg.load_file(helper, fname, fdir)
		assert(e[0])
		e = callback(e[1][tag])
		assert(e[0])
	else:
		e = jcfg.save_file(helper, {tag: data}, fname, fdir)
		if not e[0]:
			ret = False
			emsg.append(e[1])
		
	if user is not None:
		logmsg = user+ " apply "+ tag+ ": " + logmsg
		xtd_logd.add_log(logmsg)

	unlock(lockf)
	return (ret, emsg)

if __name__ == "__main__":
	import unittest
	class MyTest(unittest.TestCase):
		def test_ip2int_1(self):
			self.assertEqual(ip2int("192.168.0.1"), 0xc0a80001)
		def test_int2ip_1(self):
			self.assertEqual(int2ip(0xc0a800FE), "192.168.0.254")
		def test_num_of_set_bits_1(self):
			self.assertEqual(
				num_of_set_bits(ip2int("255.255.192.0")), 18)
		def test_block2cidr_1(self):
			self.assertEqual(
				block2cidr("10.10.0.10/255.255.192.0"), 
				"10.10.0.0/18")
		def test_iprange2list_1(self):
			self.assertEqual(
				iprange2list("192.168.2.1"), 
				["192.168.2.1"])
		def test_iprange2list_2(self):
			self.assertEqual(
				iprange2list("192.168.2.1-192.168.2.3"), 
				["192.168.2.1", "192.168.2.2", "192.168.2.3"])
		def test_iprange2list_3(self):
			self.assertEqual(
				iprange2list("192.168.2.1-192.168.2.3", "int"), 
				[0xc0a80201, 0xc0a80202, 0xc0a80203])
		def test_cidr2ipboundary_1(self):
			self.assertEqual(
				cidr2ipboundary("192.168.0.0/24", "str"), 
				("192.168.0.1", "192.168.0.254"))
		def test_cidr2ipboundary_2(self):
			self.assertEqual(
				cidr2ipboundary("192.168.0.0/16", "str"), 
				("192.168.0.1", "192.168.255.254"))
		def test_cidr2ipboundary_3(self):
			self.assertEqual(
				cidr2ipboundary("192.168.0.0/18", "str"), 
				("192.168.0.1", "192.168.63.254"))
		def test_cidr2ipboundary_3(self):
			self.assertEqual(
				cidr2ipboundary("192.168.0.0/25", "str"), 
				("192.168.0.1", "192.168.0.126"))
		def test_inverse_iprange_1(self):
			self.assertEqual(inverse_iprange(["192.168.0.1"], "255.255.255.0"),  ["192.168.0.2-192.168.0.254"])
		def test_inverse_iprange_2(self):
			self.assertEqual(inverse_iprange(
			["192.168.0.3", "192.168.0.100"], "255.255.255.0"),  
			["192.168.0.1-192.168.0.2", 
			"192.168.0.4-192.168.0.99", 
			"192.168.0.101-192.168.0.254"])
		def test_inverse_iprange_3(self):
			self.assertEqual(inverse_iprange(
			["192.168.0.1"], "255.255.255.128"),  
			["192.168.0.2-192.168.0.126"])
		def test_inverse_iprange_4(self):
			self.assertEqual(inverse_iprange(
			["1.1.0.9-1.1.0.21", "1.1.0.253"], "255.255.255.0"),  
			["1.1.0.1-1.1.0.8", "1.1.0.22-1.1.0.252", "1.1.0.254"])
		def test_inverse_iprange_5(self):
			self.assertEqual(inverse_iprange(
			["1.1.0.1-1.1.0.253"], "255.255.255.0"),  
			["1.1.0.254"])
		def test_inverse_iprange_6(self):
			self.assertEqual(inverse_iprange(
			["1.1.0.1", "1.1.0.3"], "255.255.255.0"),  
			["1.1.0.2", "1.1.0.4-1.1.0.254"])
		def test_get_arp_entry_1(self):
			self.assertEqual(get_arp_entry("9.9.9.9"), 
				(False, "no valid entry about 9.9.9.9"))
		def test_get_arp_entry_2(self):
			"""Do ping before you run this function"""
			self.assertEqual(get_arp_entry("192.168.0.1"), 
				(True, "08:00:27:70:4d:ca"))
		def test_get_arp_entry_3(self):
			"""Do ping before you run this function"""
			self.assertEqual(get_arp_entry("192.168.0.66"), 
				(False, "no valid entry about 192.168.0.66"))
		def test_ipv4mask2prefix_1(self):
			self.assertEqual(ipv4mask2prefix("255.255.192.0"), "18")
		def test_ipv4mask2prefix_2(self):
			self.assertEqual(ipv4mask2prefix("255.0.0.0"), "8")
		def test_is_ip_in_subnet_1(self):
			self.assertEqual(is_ip_in_subnet("192.168.128.1", "192.168.128.0/255.255.192.0"), True)
		def test_is_ip_in_subnet_2(self):
			self.assertEqual(is_ip_in_subnet("192.168.128.0", "192.168.128.0/255.255.192.0"), True)
		def test_is_ip_in_subnet_3(self):
			self.assertEqual(is_ip_in_subnet("192.168.1.0", "192.168.128.0/255.255.192.0"), False)
	suite = unittest.makeSuite(MyTest, "test")
	suite = unittest.makeSuite(MyTest, "test")
	runner = unittest.TextTestRunner()
	runner.run(suite)
