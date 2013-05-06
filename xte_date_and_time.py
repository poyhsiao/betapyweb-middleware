# -*- coding: utf-8 -*1-
import datetime
#ours
import const
import jcfg
import tz
import xt_func
import xtd_logd
from jcfg import N_

TAG="time"
HELPER = [("time", [
	(N_("time-zone"), jcfg.JcTimeZone(opt=tz.TZ, default=None)),
	(N_("time-server"), jcfg.JcSelect(opt=[jcfg.JcIpv4(a=True), jcfg.JcDomainName()], default=""))
])]

def _set(data):
	ret = True
	emsg = []
	tzcode = tz.TZ[data["time-zone"]]
	e = xt_func.sh(["echo '"+ tzcode+ "'", "| sudo tee /etc/TZ"])
	if not e[0]:
		ret = False
		emsg.append(e[1])

	f = open(const.CRON_SH["ntpd"], "w")
	f.write("#!/bin/sh\n")
	if data["time-server"] != "":
		f.write("sleep 30\n")
		f.write("ntpd -qnNp "+ data["time-server"]+ "\n")
		f.write("hwclock -w\n")
	f.close()

	e = xt_func.sudo([const.CRON_SH["ntpd"]], block=False)
	if not e[0]:
		ret = False
		emsg.append(e[1])

	d = datetime.datetime.today()
	run_at = str(d.second) + " * * * *"
	e = xt_func.crontab_replace(const.CRON_SH["ntpd"], run_at)
	if not e[0]:
		ret = False
		emsg.append(e[1])

	return (ret, emsg)

def get(fname=TAG+".txt", fdir=const.CFG_DIR):
	e = xt_func.xte_get(TAG, HELPER, fname, fdir)
	if e[0]:
		# dynamic entries are not in configuratio
		e[1]["date"] = datetime.datetime.strftime(datetime.datetime.now(), "%Y %m %d %H %M %S").split()
	return e

def importing(fname=TAG+".txt", fdir=const.CFG_DIR):
	return (True, None)

def set_datetime(data, user):
	ret = (True, None)
	xtd_logd.add_log(user + " apply " + TAG)
	timestr = ".".join(data[0:3]) + "-" + ":".join(data[3:6])
	e = xt_func.sudo(["date -s", timestr])
	if not e[0]:
		ret = (False, N_("See failure.log"))
	e = xt_func.sudo(["hwclock -w"])
	if not e[0]:
		ret = (False, N_("See failure.log"))
	return ret	

def set(data, user, fname=TAG+".txt", fdir=const.CFG_DIR):
	e = validate(data)
	if not e[0]:
		return e
	return xt_func.xte_set(TAG, HELPER, data, _set, fname, fdir, user)

def export(fname=TAG+".txt", fdir=const.CFG_DIR):
	return jcfg.export_file(HELPER, fname, fdir)

def validate(data):
	if "date" in data:
		del data["date"]
	return jcfg.validate_jcfg(HELPER, {TAG: data})
