# -*- coding: utf-8 -*1-
import os
import time
#ours
import const
import jcfg
import xt_func

TAG = "network"
ETHER_HELPER = [
	("clone-mac", jcfg.JcMac()),
	("mtu", jcfg.JcINT(default=-1)),
	("speed-duplex", jcfg.JcSelect(default='auto', opt=['auto', '10/half', '10/full', '100/half', '100/full', '1000/full']))
]
DMZLAN_HELPER = [
	("ethernet", ETHER_HELPER),
	("basic-subnet", {
		"[]": [
			("ip", jcfg.JcIpv4(a=True, r=True, default=None)),
			("mask", jcfg.JcIpv4Mask(default=None))
		]
	}),
	("static-route", {
		"[]": [
			("subnet", jcfg.JcIpv4(s=True, default=None)), 
			("gateway", jcfg.JcIpv4(a=True, default=None))
		]
	})
]
WAN_HELPER = [
	("ethernet", ETHER_HELPER),
	("enable", jcfg.JcBOOL()),
	("label", jcfg.JcName()),
	("downstream", jcfg.JcINT(default=512)),
	("upstream", jcfg.JcINT(default=512)),
	("type", jcfg.JcSelect(opt=['static', 'pppoe', 'dhcp'], default="n/a")),
	("static-mode", [
		#("_mandatory_if", "type=static"),
		("ip", {
			#"_mandatory": True,
			"[]": jcfg.JcIpv4(a=True, r=True, default=None)
		}),
		("mask", jcfg.JcIpv4Mask()),
		("gateway", jcfg.JcIpv4(a=True))
	]),
	("pppoe-mode", [
		#("_mandatory_if", "type=pppoe"),
		("username", jcfg.JcName()),
		("password", jcfg.JcPassword()),
		("service-name", jcfg.JcName()),
		("ip", jcfg.JcIpv4(a=True)),
		("daily-redial", jcfg.JcTimeString())
	]),
	("public-ip-passthrough", [
		("mask", jcfg.JcIpv4Mask()),
		("ip", {"[]": jcfg.JcIpv4(a=True, r=True, default=None)})
	])
]
HELPER = [("network", [
	("lan", DMZLAN_HELPER),
	("wan1", WAN_HELPER),
	("wan2", WAN_HELPER),
	("wan3", WAN_HELPER),
	("wan4", WAN_HELPER),
	("dmz", DMZLAN_HELPER)
])]
BMSTATD_CONF = const.XTCFG_DIR+"bmstatd.conf"
DYM_PID_PREFIX = "/var/run/dy_monitor-"
ARPENFORCED_CONF = const.XTCFG_DIR+"arpenforced.conf"
DO_PING = const.CFG_DIR+""

def _make_arpenforced_conf_for_wan(data, pos, rst):
	if data[pos]["enable"] == 1:
		queue = []
		if data[pos]["type"] == "static":
			for i in data[pos]["static-mode"]["ip"]:
				queue.append(i)
		if len(data[pos]["public-ip-passthrough"]["ip"]) > 0:
			for i in data[pos]["public-ip-passthrough"]["ip"]:
				queue.append(i)

		if len(queue) > 0:
			rst.append("oif "+ pos)
			for i in queue:
				rst.append("garp "+ i)
				rst.append("garp-alt "+ i)
				rst.append("poison "+ i)
				
			if os.path.exists(DO_PING):
				e = xt_func.get_arp_entry(data[pos]["static-mode"]["gateway"], pos)
				if not e[0]:
					dmac = "FF:FF:FF:FF:FF:FF"
				else:
					dmac = e[1]
				rst.append("dmac "+ dmac)
				for i in queue:
					rst.append("ping {} {}".format(i, data[pos]["static-mode"]["gateway"]))

	return (True, None)

def _make_arpenforced_conf_for_lan(data, rst):
	if len(data["lan"]["basic-subnet"]) >= 0:
		rst.append("oif lan")
		for i in data["lan"]["basic-subnet"]:
			rst.append("garp " + i["ip"])
			rst.append("garp-alt " + i["ip"])
			rst.append("poison " + i["ip"])

	return (True, None)

def _make_arpenforced_conf_for_dmz(data, rst):
	for pos in const.ALL_WANS:
		if data[pos]["type"] != "static" or len(data[pos]["public-ip-passthrough"]["ip"]) == 0:
			continue
		rst.append("oif dmz")
		complements = xt_func.inverse_iprange(
			data[pos]["public-ip-passthrough"]["ip"], 
			data[pos]["static-mode"]["mask"])
		for i in complements:
			rst.append("garp "+ i)
			rst.append("garp-alt "+ i)
			rst.append("poison "+ i)

	return (True, None)

def do_arpenforce(data=None):
	if data is None:
		data = get()[1]
	rst = []

	for pos in const.ALL_WANS:
		_make_arpenforced_conf_for_wan(data, pos, rst)
	_make_arpenforced_conf_for_lan(data, rst)
	_make_arpenforced_conf_for_dmz(data, rst)

	f = open(ARPENFORCED_CONF, "w")
	for l in rst:
		f.write(l + "\n")
	f.close()

	return xt_func.sudo(["arpenforced", ARPENFORCED_CONF])

def _set_public_ip_passthrough(data):
	"""proxyarpd reads data from netpos, call this after netpos is done"""
	ret = True
	emsg = []
	
	for pos in const.ALL_WANS:
		if len(data[pos]["public-ip-passthrough"]["ip"]) == 0:
			continue
		e = xt_func.sudo(["proxyarpd -d -i", pos])
		if not e[0]:
			ret = False
			emsg.append(e[1])

	e = xt_func.sudo(["proxyarpd -d -i dmz"])
	if not e[0]:
		ret = False
		emsg.append(e[1])

	return (ret, emsg)

def _set_hardware(data, hw):
	ret = True
	emsg = []
	for pos in const.ALL_POS:
		newmac = hw[pos]["mac"]
		if data[pos]["ethernet"]["clone-mac"] != "":
			newmac = data[pos]["ethernet"]["clone-mac"]
		e = xt_func.sudo(["ip link set dev", pos, "address", newmac])
		if not e[0]: 
			ret = False
			emsg.append(e[1])
		newmtu = hw[pos]["mtu"]
		if data[pos]["ethernet"]["mtu"] != -1:
			newmtu = data[pos]["ethernet"]["mtu"]
		e = xt_func.sudo(["ip link set dev", pos, "mtu", str(newmtu)])
		if not e[0]: 
			ret = False
			emsg.append(e[1])
		newstatus = "on"
		if data[pos]["ethernet"]["speed-duplex"] != "auto":
			tok = data[pos]["ethernet"]["speed-duplex"].split("/")
			newstatus = "off speed {} duplex {}".format(
				tok[0], tok[1].lower())
		e = xt_func.sudo(["ethtool -s", pos, "autoneg", newstatus]);
		if not e[0]: 
			ret = False
			emsg.append(e[1])

	return (ret, emsg)

def _set_bandwidth_limit(data):
	ret = True
	emsg = []
	json = []

	for pos in const.ALL_WANS:
		json.append(
			[pos, data[pos]["downstream"], data[pos]["upstream"]])

	xt_func.save_json(BMSTATD_CONF, json)
	e = xt_func.sudo(["bmstatd -d -f", BMSTATD_CONF])
	if not e[0]: 
		ret = False
		emsg.append(e[1])

	return (ret, emsg)

def _set_dmzlan_ifup_address_and_route(data, pos):
	ret = True
	emsg = []

	# Always ifups dmz
	e = xt_func.sudo(["ip link set dev", pos, "up"])
	if not e[0]: 
		ret = False
		emsg.append(e[1])

	for i in data["basic-subnet"]:
		ip_range = xt_func.iprange2list(i["ip"])
		inet = xt_func.block2cidr(ip_range[0]+ "/"+ i["mask"]) 
		for ip in ip_range:
			e = xt_func.sudo(["ip addr add", ip+ "/"+ i["mask"], "brd + dev", pos])
			if not e[0]: 
				ret = False
				emsg.append(e[1])
		e = xt_func.sudo(["ip route add", inet, "dev", pos, "src", ip_range[0], "table", const.RTAB[pos]])

	for i in data["static-route"]:
		e = xt_func.sudo(["ip route add", i["subnet"], "via", i["gateway"], "dev", pos, "table", const.RTAB[pos]])
		if not e[0]: 
			ret = False
			emsg.append(e[1])

	return (ret, emsg)

def _set_static_wan_ifup_address_and_route(data, pos):
	ret = True
	emsg = []

	if data["enable"] != 1: return (ret, [pos, "disabled"])

	e = xt_func.sudo(["ip link set dev", pos, "up"])
	if not e[0]: 
		ret = False
		emsg.append(e[1])

	# static supports only one subnet
	fst_ip = data["static-mode"]["ip"][0].split("-")[0]
	inet = xt_func.block2cidr(fst_ip + "/" + data["static-mode"]["mask"]) 
	for i in data["static-mode"]["ip"]:
		ip_range = xt_func.iprange2list(i)
		for ip in ip_range:
			e = xt_func.sudo(["ip addr add", ip+ "/"+ data["static-mode"]["mask"], "brd + dev", pos])
			if not e[0]: 
				ret = False
				emsg.append(e[1])
	e = xt_func.sudo(["ip route add default via", data["static-mode"]["gateway"], "dev", pos, "table", const.RTAB[pos]])
	e = xt_func.sudo(["ip route append default via", data["static-mode"]["gateway"], "dev", pos])

	if len(data["public-ip-passthrough"]["ip"]) > 0:
		#Copy addresses to DMZ for public-ip-passthrough
		for ip in ip_range:
			e = xt_func.sudo(["ip addr add", ip+ "/"+ data["static-mode"]["mask"], "brd + dev dmz"])
			if not e[0]: 
				ret = False
				emsg.append(e[1])
		#Don't forget route tables 
		e = xt_func.sudo(["ip route del", inet, "dev dmz"])
		e = xt_func.sudo(["ip route add", inet, "src", fst_ip, "dev dmz table", const.RTAB["dmz"]])

	return (ret, emsg)

def _set_dynamic_wan_ifup_address_and_route(data, pos):
	if data["enable"] != 1: return (True, [pos, "disabled"])

	cmd = ["dy_monitor -d -i", pos, "-t"]
	cmd.append(data["type"])
	if data["type"] == "pppoe":
		cmd.append("-u "+ data["pppoe-mode"]["username"])
		cmd.append("-p "+ data["pppoe-mode"]["password"])
		if data["pppoe-mode"]["service-name"] != "":
			cmd.append("-s "+ data["pppoe-mode"]["service-name"])
		if data["pppoe-mode"]["daily-redial"] != "":
			cmd.append("-r "+ data["pppoe-mode"]["daily-redial"])
		if data["pppoe-mode"]["ip"] != "":
			cmd.append("-a "+ data["pppoe-mode"]["ip"])
		if data["public-ip-passthrough"]["mask"] != "":
			cmd.append("-m "+ xt_func.ipv4mask2prefix(data["public-ip-passthrough"]["mask"]))

	return xt_func.sudo(cmd)

def _set_ifup_address_and_route(data):
	ret = True
	emsg = []

	#set WLHD:good for default
	arg = ""
	for pos in const.ALL_WANS:
		if data[pos]["type"] == "static" and data[pos]["enable"] == 1:
			arg += "1"
		else:
			arg += "0"
	e = xt_func.sudo(["xtctl autoroute stat", arg])
	if not e[0]: 
		ret = False
		emsg.append(e[1])

	#Make sure DMZ is before WANs
	for pos in const.ALL_POS:
		if pos == "dmz" or pos == "lan":
			e = _set_dmzlan_ifup_address_and_route(data[pos], pos)
		elif data[pos]["type"] == "static":
			e = _set_static_wan_ifup_address_and_route(data[pos], pos)
		else: #pppoe or dhcp
			e = _set_dynamic_wan_ifup_address_and_route(data[pos], pos)
		if not e[0]: 
			ret = False
			emsg.append(e[1])

	return (ret, emsg)

def _set_netpos(data):
	ret = True
	emsg = []

	for pos in const.ALL_POS:
		fname = const.XTCFG_DIR+ "netpos-"+ pos+ ".txt"
		xcfg = {
			"LOCALHOST": [], "PROXYARP": [], 
			"SUBNET": [], "ROUTE": [], "GATEWAY": []
		}
		if pos == "lan" or pos == "dmz":
			for i in data[pos]['basic-subnet']:
				xcfg["LOCALHOST"].append(i["ip"])
				ip1 = i["ip"].split("-")[0]
				cidr = xt_func.block2cidr(ip1 + "/" + i["mask"])
				xcfg["SUBNET"].append(cidr)
			xcfg["ROUTE"] = [xt_func.block2cidr(i["subnet"]) for i in data[pos]['static-route']]
			xcfg["GATEWAY"] = [i["gateway"] for i in data[pos]['static-route']]
		elif data[pos]["enable"] == 1:
			if data[pos]["type"] == "static":
				# dy_monitord charges PPPoE and DHCP types
				for i in data[pos]["static-mode"]["ip"]:
					xcfg["LOCALHOST"].append(i)
				ip1 = data[pos]["static-mode"]["ip"][0].split("-")[0]
				cidr = xt_func.block2cidr(ip1 + "/" + data[pos]["static-mode"]["mask"])
				xcfg["SUBNET"].append(cidr)
			xcfg["PROXYARP"] = [i for i in data[pos]['public-ip-passthrough']["ip"]]
		f = open(fname, "w")
		for i in ["LOCALHOST", "PROXYARP", "SUBNET", "ROUTE", "GATEWAY"]:
			f.write(i + "\n");
			for j in xcfg[i]:
				f.write(j + "\n");
		f.close()
		e = xt_func.sudo(["xtctl netpos", pos, fname]); 
		if not e[0]: 
			ret = False
			emsg.append(e[1])

	return (ret, emsg)

def _set(data):
	hw = xt_func.load_json(const.HW_INFO)[1]
	ret = True
	emsg = []
	xt_func.sudo(["killall bmstatd"])
	xt_func.sudo(["killall proxyarpd"])
	xt_func.sudo(["killall dy_monitor"])
	time.sleep(4) # dy_monitor needs 3 sec to end itself
	for (dev, pos, rtab, dum) in const.IFMAP:
		xt_func.sudo(["ip link set dev", pos, "down"])
		xt_func.sudo(["ip addr flush dev", pos])
		xt_func.sudo(["ip route flush table", rtab])
	xt_func.sudo(["ip route flush cache"])

	e = _set_hardware(data, hw)
	if not e[0]:
		ret = False
		emsg.append(e[1])

	e = _set_ifup_address_and_route(data)
	if not e[0]:
		ret = False
		emsg.append(e[1])

	e = _set_netpos(data) 
	if not e[0]: 
		ret = False
		emsg.append(e[1])

	e = _set_public_ip_passthrough(data)
	if not e[0]: 
		ret = False
		emsg.append(e[1])

	e = _set_bandwidth_limit(data) 
	if not e[0]: 
		ret = False
		emsg.append(e[1])

	e = do_arpenforce(data)
	if not e[0]: 
		ret = False
		emsg.append(e[1])

	return (ret, emsg)

def reconnect_dynamic_wan(pos):
	e = get()
	if e[0] is False:
		return e

	data = e[1]

	if data[pos]["enable"] != 1:
		return (False, [pos, "is disabled"])

	if data[pos]["type"] != "dhcp" and data[pos]["type"] != "pppoe":
		return (False, [pos, "is not dynamic"])

	f = open(DYM_PID_PREFIX + pos, "r")
	oldpid = f.readline().strip()
	f.close()

	e = xt_func.sudo(["kill", oldpid])
	if not e[0]:
		return e

	return _set_dynamic_wan_ifup_address_and_route(data[pos], pos)

def cli_show():
	for pos in const.ALL_POS:
		print "[{}]".format(pos)
		e = xt_func.sudo(["xtctl netpos", pos])
		if not e[0]:
			print "No such device"
			continue
		lines = e[1].split("\n")
		if pos == "lan" or pos == "dmz":
			data = {"l": [], "s": []}
			for l in lines:
				l = l.strip()
				if l == "LOCALHOST":
					flag = "l"
					continue
				elif l == "PROXYARP":
					flag = "p"
					continue
				elif l == "SUBNET":
					flag = "s"
					continue
				elif l == "ROUTE":
					break
				if flag == "l" or flag == "s":
					data[flag].append(l)
			for i in range(0, len(data["l"])):
				print "ip:{}, subnet:{}".format(data["l"][i], data["s"][i])
		else:
			data = []
			subnet = None
			for l in lines:
				l = l.strip()
				if l == "LOCALHOST":
					flag = "l"
					continue
				elif l == "PROXYARP":
					flag = "p"
					continue
				elif l == "SUBNET":
					flag = "s"
					continue
				elif l == "ROUTE":
					break
				if flag == "l":
					data.append(l)
				elif flag == "s":
					subnet = l
			for i in data:
				print "ip:{},".format(i)
			if subnet is not None:
				print "subnet:{}".format(subnet)


def export(fname=TAG+".txt", fdir=const.CFG_DIR):
	return jcfg.export_file(HELPER, fname, fdir)

def get(fname=TAG+".txt", fdir=const.CFG_DIR):
	return xt_func.xte_get(TAG, HELPER, fname, fdir)

def importing(fname=TAG+".txt", fdir=const.CFG_DIR):
	return (True, None)

def set(data, user, fname=TAG+".txt", fdir=const.CFG_DIR):
	e = validate(data)
	if e[0]:
		if user is not None: # None means 'called when bootup'
			xt_func.iptables_raw_change_policy("DROP")
		e = xt_func.xte_set(TAG, HELPER, data, _set, fname, fdir, user)
		if user is not None:
			xt_func.iptables_raw_change_policy("ACCEPT")
	return e

def validate(data):
	x = jcfg.JcPassword()
	for pos in const.ALL_WANS:
		data[pos]["pppoe-mode"]["password"] = x.encrypt(data[pos]["pppoe-mode"]["password"]) 
	e = jcfg.validate_jcfg(HELPER, {TAG: data})
	if not e[0]:
		return e
	for pos in const.ALL_WANS:
		data[pos]["pppoe-mode"]["password"] = x.decrypt(data[pos]["pppoe-mode"]["password"]) 
		if data[pos]["enable"] != 1:
			continue
		if data[pos]["type"] == "static":
			if len(data[pos]["static-mode"]["ip"]) == 0:
				return (False, ["network", pos, "static-mode", "ip", "can't be empty"])
			if data[pos]["static-mode"]["mask"] == "":
				return (False, ["network", pos, "static-mode", "mask", "can't be empty"])
			if data[pos]["static-mode"]["gateway"] == "":
				return (False, ["network", pos, "static-mode", "gateway", "can't be empty"])
		elif data[pos]["type"] == "pppoe":
			if data[pos]["pppoe-mode"]["username"] == "":
				return (False, ["network", pos, "pppoe-mode", "username", "can't be empty"])
			if data[pos]["pppoe-mode"]["password"] == "":
				return (False, ["network", pos, "pppoe-mode", "password", "can't be empty"])
		elif data[pos]["type"] == "dhcp":
			pass
		else:
			return (False, ["network", pos, "type", data[pos]["type"], jcfg.SEMERR_INVAL_VAL])
	return (True, None)
