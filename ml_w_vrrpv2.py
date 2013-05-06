#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - VRRPv2

	Configuration Data Format
	{
		"group": [
			{
				"group-name": "VG_1",
				"instance": [
					{
						"instance-name": "VI_1",
						"interface": "s0e1",
						"additional_track_interface": [
							{
								"interface": "s0e2"
							},
							...
						],
						"sync-interface": "s0e1",
						"delay-gratuitous-arp": 5,
						"virtual-router-id": 1,
						"priority": 1,
						"advertisement-interval": 10,
						"ipv4_vip": [
							{
								"ipv4": "192.168.1.1",
								"netmask": "255.255.255.0",
								"interface": "s0e1"
							},
							...
						],
						"ipv4_vr": [
							{
								"destination-ipv4": "192.168.1.1",
								"netmask": "255.255.255.0",
								"gateway": "192.168.1.1",
								"interface": "s0e1"
							},
							...
						],
						"ipv6_vip": [
							{
								"ipv6": "2001::1",
								"prefix": 64,
								"interface": "s0e1"
							},
							...
						],
						"ipv6_vr": [
							{
								"destination-ipv6": "2001::1",
								"prefix": 64,
								"gateway": "2001::1",
								"interface": "s0e1"
							},
							...
						],
						"preempt": True
					},
					...
				]
			},
			...
		]
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg
from ml_jcfg import N_
import ml_func
import ml_check

class vrrpv2(ml_config.base):
	""" VRRPv2 """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "vrrpv2.txt"), threadlock = None):
		""" init config """
		super(vrrpv2, self).__init__(fpath, threadlock)
		self.tag = "vrrpv2"
		self.cfg = {}
		self.ipv4_vip_syntax = {
			"ipv4": {'T': str, 'D': "192.168.1.1", 'M': True, 'S': None, 'V': [ml_check.validate_ipv4]},  # TO_DO: use WAN IP
			"netmask": {'T': str, 'D': "255.255.255.0", 'M': True, 'S': None, 'V': [ml_check.validate_ipv4_netmask]},
			"interface": {'T': str, 'D': "s0e1", 'M': True, 'S': None},
		}
		self.ipv4_vips_syntax = {
			"*": {'T': dict, 'D': {}, 'M': True, 'S': self.ipv4_vip_syntax},
		}
		self.ipv4_vr_syntax = {
			"destination-ipv4": {'T': str, 'D': "192.168.1.1", 'M': True, 'S': None, 'V': [ml_check.validate_ipv4]},
			"netmask": {'T': str, 'D': "255.255.255.0", 'M': True, 'S': None, 'V': [ml_check.validate_ipv4_netmask]},
			"gateway": {'T': str, 'D': "192.168.1.1", 'M': True, 'S': None, 'V': [ml_check.validate_ipv4]},
			"interface": {'T': str, 'D': "s0e1", 'M': True, 'S': None},
		}
		self.ipv4_vrs_syntax = {
			"*": {'T': dict, 'D': {}, 'M': True, 'S': self.ipv4_vr_syntax}
		}
		self.ipv6_vip_syntax = {
			"ipv6": {'T': str, 'D': "2001::1", 'M': True, 'S': None, 'V': [ml_check.validate_ipv6]},  # TO_DO: use WAN IP
			"prefix": {'T': int, 'D': 64, 'M': True, 'S': None, 'V': [ml_check.validate_ipv6_prefix]},
			"interface": {'T': str, 'D': "s0e1", 'M': True, 'S': None}
		}
		self.ipv6_vips_syntax = {
			"*": {'T': dict, 'D': {}, 'M': True, 'S': self.ipv6_vip_syntax}
		}
		self.ipv6_vr_syntax = {
			"destination-ipv6": {'T': str, 'D': "2001::1", 'M': True, 'S': None, 'V': [ml_check.validate_ipv6]},
			"prefix": {'T': int, 'D': 64, 'M': True, 'S': None, 'V': [ml_check.validate_ipv6_prefix]},
			"gateway": {'T': str, 'D': "2001::1", 'M': True, 'S': None, 'V': [ml_check.validate_ipv6]},
			"interface": {'T': str, 'D': "s0e1", 'M': True, 'S': None}
		}
		self.ipv6_vrs_syntax = {
			"*": {'T': dict, 'D': {}, 'M': True, 'S': self.ipv6_vr_syntax}
		}
		self.additional_track_interface_syntax = {
			"interface": {'T': str, 'D': "s0e1", 'M': True, 'S': None}
		}
		self.additional_track_interfaces_syntax = {
			"*": {'T': dict, 'D': {}, 'M': False, 'S': self.additional_track_interface_syntax}
		}
		self.instance_syntax = {
			"instance-name": {'T': str, 'D': "VI_1", 'M': True, 'S': None},
			"interface": {'T': str, 'D': "s0e1", 'M': True, 'S': None},
			"additional_track_interface": {'T': list, 'D': [], 'M': False, 'S': self.additional_track_interfaces_syntax},
			"sync-interface": {'T': str, 'D': "s0e1", 'M': True, 'S': None},
			"delay-gratuitous-arp": {'T': int, 'D': 5, 'M': False, 'S': None},
			"virtual-router-id": {'T': int, 'D': 1, 'M': True, 'S': None},
			"priority": {'T': int, 'D': 100, 'M': True, 'S': None},
			"advertisement-interval": {'T': int, 'D': 1, 'M': True, 'S': None},
			"ipv4_vip": {'T': list, 'D': [], 'M': False, 'S': self.ipv4_vips_syntax},
			"ipv4_vr": {'T': list, 'D': [], 'M': False, 'S': self.ipv4_vrs_syntax},
			"ipv6_vip": {'T': list, 'D': [], 'M': False, 'S': self.ipv6_vips_syntax},
			"ipv6_vr": {'T': list, 'D': [], 'M': False, 'S': self.ipv6_vrs_syntax},
			"preempt": {'T': bool, 'D': True, 'M': True, 'S': None}
		}
		self.instances_syntax = {
			"*": {'T': dict, 'D': {}, 'M': False, 'S': self.instance_syntax}
		}
		self.group_syntax = {
			"group-name": {'T':str, 'D': "VG_1", 'M': True, 'S': None},
			"instance": {'T': list, 'D': [], 'M': False, 'S': self.instances_syntax}
		}
		self.groups_syntax = {
			"*": {'T': dict, 'D': {}, 'M': False, 'S': self.group_syntax}
		}
		self.main_syntax = {
			"group": {'T': list, 'D': [], 'M': True, 'S': self.groups_syntax}
		}
		self.helper = [(self.tag, [
			(N_("group"), {
				"[]": [
					(N_("group-name"), ml_jcfg.JcDomainName()),
					(N_("instance"), {
						"[]": [
							(N_("instance-name"), ml_jcfg.JcDomainName()),
							(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e1')),
							(N_("additional_track_interface"), {
								"[]": [
									(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e2')),
								]
							}),
							(N_("sync-interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e1')),
							(N_("delay-gratuitous-arp"), ml_jcfg.JcINT(default=0)),
							(N_("virtual-router-id"), ml_jcfg.JcINT(default=1)),
							(N_("priority"), ml_jcfg.JcINT(default=1)),
							(N_("advertisement-interval"), ml_jcfg.JcINT(default=0)),
							(N_("ipv4_vip"), {
								"[]": [
									(N_("ipv4"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True)])),
									(N_("netmask"), ml_jcfg.JcIpv4Mask()),
									(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e1'))
								]
							}),
							(N_("ipv4_vr"), {
								"[]": [
									(N_("destination-ipv4"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True)])),
									(N_("netmask"), ml_jcfg.JcIpv4Mask()),
									(N_("gateway"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True)])),
									(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e1')),
								]
							}),
							(N_("ipv6_vip"), {
								"[]": [
									(N_("ipv6"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)),
									(N_("prefix"), ml_jcfg.JcINT(default=64)),
									(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e1'))
								]
							}),
							(N_("ipv6_vr"), {
								"[]": [
									(N_("destination-ipv6"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)),
									(N_("prefix"), ml_jcfg.JcINT(default=64)),
									(N_("gateway"), ml_jcfg.JcSTR(regex='^[\\x20-\\x7F ]{0,255}$', default='', sensitive=False)),
									(N_("interface"), ml_jcfg.JcSelect(opt=['s0e1', 's0e2'], default='s0e1')),
								]
							}),
							(N_("preempt"), ml_jcfg.JcBOOL(default=1))
						]
					})
				]
			})
		])]

	def do_set(self):
		""" real task """
		# generate conf file content
		gbuf = ""
		ibuf = ""
		if self.cfg.has_key("group"):
			for group in self.cfg["group"]:
				if group.has_key("group-name"):
					gbuf += "{0}vrrp_sync_group %s {{\n".format(" "*0) % (group["group-name"])
					gbuf += "{0}group {{\n".format(" "*4)
					if group.has_key("instance"):
						for instance in group["instance"]:
							if instance.has_key("instance-name"):
								gbuf += "{0}%s\n".format(" "*8) % (instance["instance-name"])
								ibuf += "{0}vrrp_instance %s {{\n".format(" "*0) % (instance["instance-name"])
								if instance.has_key("priority") and 255 == instance["priority"]:
									ibuf += "{0}state %s\n".format(" "*4) % ("MASTER")
								else:
									ibuf += "{0}state %s\n".format(" "*4) % ("BACKUP")
								if instance.has_key("interface"):
									ibuf += "{0}interface %s\n".format(" "*4) % (instance["interface"])
								if instance.has_key("additional_track_interface"):
									ibuf += "{0}track_interface {{\n".format(" "*4)
									for track in instance["additional_track_interface"]:
										if track.has_key("interface"):
											ibuf += "{0}%s\n".format(" "*8) % (track["interface"])
									ibuf += "{0}}}\n".format(" "*4)
								if instance.has_key("delay-gratuitous-arp"):
									ibuf += "{0}garp_master_delay %d\n".format(" "*4) % (instance["delay-gratuitous-arp"])
								if instance.has_key("virtual-router-id"):
									ibuf += "{0}virtual_router_id %d\n".format(" "*4) % (instance["virtual-router-id"])
								if instance.has_key("priority"):
									ibuf += "{0}priority %d\n".format(" "*4) % (instance["priority"])
								if instance.has_key("advertisement-interval"):
									ibuf += "{0}advert_int %d\n".format(" "*4) % (instance["advertisement-interval"])
								if instance.has_key("ipv4_vip") or instance.has_key("ipv6_vip"):
									ibuf += "{0}virtual_ipaddress {{\n".format(" "*4)
								if instance.has_key("ipv4_vip"):
									for ipv4_vip in instance["ipv4_vip"]:
										if ipv4_vip.has_key("ipv4"):
											ibuf += "{0}%s\n".format(" "*8) % (ipv4_vip["ipv4"])
								if instance.has_key("ipv6_vip"):
									for ipv6_vip in instance["ipv6_vip"]:
										if ipv6_vip.has_key("ipv6"):
											ibuf += "{0}%s\n".format(" "*8) % (ipv6_vip["ipv6"])
								if instance.has_key("ipv4_vip") or instance.has_key("ipv6_vip"):
									ibuf += "{0}}}\n".format(" "*4)
								if instance.has_key("preempt"):
									if not instance["preempt"]:
										ibuf += "{0}nopreempt\n".format(" "*4)
								#ibuf += "{0}preempt_delay %d\n".format(" "*4) % (300)
								ibuf += "{0}}}\n".format(" "*0)
					gbuf += "{0}}}\n".format(" "*4)
					gbuf += "{0}}}\n".format(" "*0)
		# update conf file
		try:
			file = open("keepalived.conf", "w")
			file.write(gbuf)
			file.write(ibuf)
			file.close()
		except Exception as e:
			return (False, [str(e)])
		# reload service
		try:
			ml_func.sudo(["/etc/rc.d/keepalived restart"])
		except Exception as e:
			return (False, [str(e)])

		return (True, None)
 
def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = vrrpv2(threadlock = threadlock)
		return obj.get()
	except Exception as e:
		return (False, [str(e)])

def set(user = None, cfg = {}, threadlock = None):
	"""
		Web UI calls set()
		return
			(True, None)
			(False, list)
	"""
	try:
		obj = vrrpv2(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])
