import re
# ours
import const
import xt_func

TAG="summary"

def _get_pos_connection_time(pos):
	import os
	import time
	fname = "/tmp/dy_monitor-" + pos + ".record"
	if pos == "lan" or pos == "dmz" or not os.path.exists(fname):
		return "N/A"

	f = open(fname, "r")
	line = f.readline().strip()
	f.close()
	start_sec = int(line) 
	now_sec = int(time.time())
	delta = now_sec - start_sec

	return _calc_uptime(delta)

def _get_pos_status(pos):
	e = xt_func.sh(["ip link show up | grep", pos])
	if e[0] is False:
		return "Down"

	raw = xt_func.sh(["ethtool", pos, "| egrep 'Speed|Duplex'"])[1].split()
	m = re.match("(\d+)", raw[1])
	if m is None:
		return "Unknown"
	return m.group(1) + "/" + raw[3]

def _get_summary_traffic():
	data = {}
	import time
	while True:
		e = xt_func.load_json(const.BM_RECORD)
		if e[0]: break
		time.sleep(1)
	
	for i in e[1]:
		data[i[0]] = {
			"rx": round((i[1] * 8.0)/const.KILO, 2),
			"tx": round((i[2] * 8.0)/const.KILO, 2)
		}

	return data

def _get_summary_detection():
	data = {}
	raw = xt_func.sudo(["xtctl", "autoroute", "stat"])[1]
	for i in range(0,4):
		pos = "wan" + str(i+1)
		if raw[i] == "0":
			data[pos] = "bad"
		else:
			data[pos] = "good"
	data["dmz"] = "N/A"
	data["lan"] = "N/A"
	
	return data

def _get_pos_summary(pos):
	data = {
		"status": _get_pos_status(pos),
		"connection-time": _get_pos_connection_time(pos),
	}

	return data

def _calc_uptime(raw):
	days = raw / 86400
	raw = raw % 86400
	hours = raw / 3600
	raw = raw % 3600
	mins = raw / 60
	secs = raw % 60

	rst = "{:02d}:{:02d}:{:02d}".format(hours, mins, secs)
	if days > 0:
		rst = "{} days {}".format(days, rst)
	return rst

def reconnect_dynamic_wan(pos):
	import xte_network
	return xte_network.reconnect_dynamic_wan(pos)

def _get_cpu_usage():
	str = xt_func.sudo(["cat", "/var/tmp/cpu.tmp"])[1].split("\n")
	return int(round(float(str[0])))
	
def _get_wan_address(pos):
	addrs = xt_func.get_netpos_addresses(pos)
	if len(addrs) == 0 : return "N/A"	
	return addrs[0]
	
def get(fname=TAG+".txt", fdir=const.CFG_DIR):
	import xte_network
	version_j = xt_func.load_json(const.CFG_DIR+"version.json")[1]
	license_j = xt_func.load_json(const.CFG_DIR+"license.json")[1]
	traffic = _get_summary_traffic()
	detection = _get_summary_detection()
	txt = xt_func.sh(["cat", "/proc/uptime"])[1]
	up_secs = int(txt.split(".")[0]) #Tuncate to integer
	network_c = xte_network.get()[1]

	data = {
		"version": version_j["version"],
		"sn": license_j["sn"],
		"uptime": _calc_uptime(up_secs),
		"connections":xt_func.sudo(["cat", "/proc/sys/net/netfilter/nf_conntrack_count"])[1],
		"cpu":_get_cpu_usage(),
	}
	for pos in const.ALL_POS:
		data[pos] = _get_pos_summary(pos)
		data[pos]["ip"] = _get_wan_address(pos)
		data[pos]["detection"] = detection[pos]
		data[pos]["rx"] = traffic[pos]["rx"]
		data[pos]["tx"] = traffic[pos]["tx"]
		if pos == "lan" or pos == "dmz":
			data[pos]["label"] = "N/A"
		else:
			data[pos]["label"] = network_c[pos]["label"]
	return (True, data)	

