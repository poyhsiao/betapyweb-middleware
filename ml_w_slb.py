#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
	Web Page - SLB

	Configuration Data Format
	{
		"ip": {
			"ipv4": [
				{
					"label": "one",
					"ip_address": ["10.1.1.4"]
				},
				{
					"label": "many",
					"ip_address": ["10.1.1.1", "10.1.1.2", "10.1.1.3", "10.1.1.4"]
				},
				{
					"label": "ANY",
					"ip_address": ["ANY"]
				}
			],
			"ipv6": [
				{
					"label": "one",
					"ip_address": ["2001::1"]
				},
				{
					"label": "many",
					"ip_address": ["2001::1", "2001::2", "2001::3", "2001::4"]
				},
				{
					"label": "ANY",
					"ip_address": ["ANY"]
				}
			]
		},
		"service_group": {
			"ipv4": [
				{
					"label": "group1_v4",
					"protocol": "TCP",
					"application_port": [
						80,
						443
					]
				}
			],
			"ipv6": [
				{
					"label": "group1_v6",
					"protocol": "TCP",
					"application_port": [
						80,
						443
					]
				}
			]
		},
		"real_server_group": {
			"ipv4": [
				{
					"label": "real1_v4",
					"ip_address": "10.1.1.1",
					"weight": 1,
					"health_check": "NA",
					"maintenance_mode": False
				},
				{
					"label": "real2_v4",
					"ip_address": "10.1.1.1",
					"weight": 1,
					"health_check": "HTTP_GET",
					"http_get": {
						"url": "/",
						"status_code": 200,
						"from_local_ip": "10.1.1.1",
						"to_remote_port": 80,
						"connection_timeout": 10,
						"delay_before_retry": 10
					},
					"maintenance_mode": False
				},
				{
					"label": "real3_v4",
					"ip_address": "10.1.1.1",
					"weight": 1,
					"health_check": "HTTPS_GET",
					"https_get": {
						"url": "/",
						"status_code": 200,
						"from_local_ip": "10.1.1.1",
						"to_remote_port": 80,
						"connection_timeout": 10,
						"delay_before_retry": 10
					},
					"maintenance_mode": False
				},
				{
					"label": "real4_v4",
					"ip_address": "10.1.1.1",
					"weight": 1,
					"health_check": "ICMP_CHECK",
					"icmp_check": {
						"timeout": 10
					},
					"maintenance_mode": False
				},
				...
			],
			"ipv6": [
				{
					"label": "real1_v6",
					"ip_address": "2001::1",
					"weight": 1,
					"health_check": "TCP_CHECK",
					"tcp_check": {
						"from_local_ip": "2001::2",
						"to_remote_ip": "2001::3",
						"connection_timeout": 10
					},
					"maintenance_mode": False
				},
				{
					"label": "real2_v6",
					"ip_address": "2001::1",
					"weight": 1,
					"health_check": "SMTP_CHECK",
					"smtp_check": {
						"helo_name": "",
						"from_local_ip": "2001::2",
						"to_remote_ip": "2001::3",
						"to_remote_port": 25,
						"connection_timeout": 10
					},
					"maintenance_mode": False
				},
				{
					"label": "real3_v6",
					"ip_address": "2001::1",
					"weight": 1,
					"health_check": "PATTERN_CHECK",
					"pattern_check": {
						"send": "GET / HTTP/1.0\r\n\r\n",
						"expect": "HTTP",
						"to_remote_ip": "2001::3",
						"to_remote_port": 80,
						"timeout": 10
					},
					"maintenance_mode": False
				},
				...
			]
		},
		"fallback_server": {
			"ipv4": [
				{
					"label": "fall1_v4",
					"ip_address": "10.1.1.1"
				},
				{
					"label": "NA",
					"ip_address": "NA"
				},
				...
			],
			"ipv6": [
				{
					"label": "fall1_v6",
					"ip_address": "2001::1"
				},
				{
					"label": "NA",
					"ip_address": "NA"
				},
				...
			]
		},
		"property": [
			{
				"label": "proper1",
				"forward_method": "NAT",
				"balance_mode": "Round-robin",
				"health_check_interval": 10,
				"persistence": 10,
				"ipv4_netmask": "255.255.255.0",
				"ipv6_prefix": 64
			},
			...
		],
		"policy": {
			"ipv4": [
				{
					"source_ip": "one",
					"destination_ip": "many",
					"service_group": "group1_v4",
					"action": "VIP",
					"real_server_group": "real1_v4",
					"fallback_server": "fall1_v4",
					"property": "proper1"
				},
				...
			],
			"ipv6": [
				{
					"source_ip": "one",
					"destination_ip": "many",
					"service_group": "group1_v6",
					"action": "Accept",
					"real_server_group": "",
					"fallback_server": "",
					"property": ""
				},
				...
			]
		}
	}
"""
import os
import ml_system
import ml_config
import ml_jcfg
import ml_func
import ml_check

default = {
}

class slb(ml_config.base):
	""" SLB """
	def __init__(self, fpath = os.path.join(ml_system.CFG_PATH, "slb.txt"), threadlock = None):
		""" init config """
		super(slb, self).__init__(fpath, threadlock)
		self.tag = "slb"
		self.default = default
		self._ipv4s_syntax = {
			"*": {'T':str, 'D':"", 'M':False, 'S':None, 'V': [ml_check.validate_ipv4, ml_check.validate_ANY]}
		}
		self._ipv6s_syntax = {
			"*": {'T':str, 'D':"", 'M':False, 'S':None, 'V': [ml_check.validate_ipv6, ml_check.validate_ANY]}
		}
		self.ipv4_syntax = {
			"label": {'T':str, 'D':"", 'M':True, 'S':None},
			"ip_address": {'T':list, 'D':[], 'M':True, 'S':self._ipv4s_syntax}
		}
		self.ipv6_syntax = {
			"label": {'T':str, 'D':"", 'M':True, 'S':None},
			"ip_address": {'T':list, 'D':[], 'M':True, 'S':self._ipv6s_syntax}
		}
		self.ipv4s_syntax = {
			"*": {'T': dict, 'D': {}, 'M': True, 'S': self.ipv4_syntax},
		}
		self.ipv6s_syntax = {
			"*": {'T': dict, 'D': {}, 'M': True, 'S': self.ipv6_syntax},
		}
		self.ip_syntax = {
			"ipv4": {'T':list, 'D':[], 'M':False, 'S':self.ipv4s_syntax},
			"ipv6": {'T':list, 'D':[], 'M':False, 'S':self.ipv6s_syntax}
		}
		self.service_group_ip_application_port_syntax = {
			"*": {'T':int, 'D':80, 'M':True, 'S':None}
		}
		self.service_group_ip_syntax = {
			"label": {'T':str, 'D':"", 'M':True, 'S':None},
			"protocol": {'T':str, 'D':"", 'M':True, 'S':None},
			"application_port": {'T':list, 'D':[], 'M':True, 'S':self.service_group_ip_application_port_syntax}
		}
		self.service_group_ips_syntax = {
			"*": {'T':dict, 'D':{}, 'M':True, 'S':self.service_group_ip_syntax}
		}
		self.service_group_syntax = {
			"ipv4": {'T':list, 'D':[], 'M':False, 'S':self.service_group_ips_syntax},
			"ipv6": {'T':list, 'D':[], 'M':False, 'S':self.service_group_ips_syntax}
		}
		self.real_server_group_ipv4_http_get_syntax = {
			"url": {'T':str, 'D':"", 'M':True, 'S':None},
			"status_code": {'T':int, 'D':200, 'M':True, 'S':None},
			"from_local_ip": {'T':str, 'D':"0.0.0.0", 'M':True, 'S':None, 'V': [ml_check.validate_ipv4]},
			"to_remote_port": {'T':int, 'D':80, 'M':True, 'S':None},
			"connection_timeout": {'T':int, 'D':10, 'M':True, 'S':None},
			"delay_before_retry": {'T':int, 'D':10, 'M':True, 'S':None}
		}
		self.real_server_group_ipv6_http_get_syntax = {
			"url": {'T':str, 'D':"", 'M':True, 'S':None},
			"status_code": {'T':int, 'D':200, 'M':True, 'S':None},
			"from_local_ip": {'T':str, 'D':"::", 'M':True, 'S':None, 'V': [ml_check.validate_ipv6]},
			"to_remote_port": {'T':int, 'D':80, 'M':True, 'S':None},
			"connection_timeout": {'T':int, 'D':10, 'M':True, 'S':None},
			"delay_before_retry": {'T':int, 'D':10, 'M':True, 'S':None}
		}
		self.real_server_group_ip_icmp_check_syntax = {
			"timeout": {'T':int, 'D':10, 'M':True, 'S':None}
		}
		self.real_server_group_ipv4_tcp_check_syntax = {
			"from_local_ip": {'T':str, 'D':"0.0.0.0", 'M':True, 'S':None, 'V': [ml_check.validate_ipv4]},
			"to_remote_port": {'T':int, 'D':80, 'M':True, 'S':None},
			"connection_timeout": {'T':int, 'D':10, 'M':True, 'S':None}
		}
		self.real_server_group_ipv6_tcp_check_syntax = {
			"from_local_ip": {'T':str, 'D':"::", 'M':True, 'S':None, 'V': [ml_check.validate_ipv6]},
			"to_remote_port": {'T':int, 'D':80, 'M':True, 'S':None},
			"connection_timeout": {'T':int, 'D':10, 'M':True, 'S':None}
		}
		self.real_server_group_ipv4_smtp_check_syntax = {
			"helo_name": {'T':str, 'D':"", 'M':True, 'S':None},
			"from_local_ip": {'T':str, 'D':"0.0.0.0", 'M':True, 'S':None, 'V': [ml_check.validate_ipv4]},
			"to_remote_ip": {'T':str, 'D':"0.0.0.0", 'M':True, 'S':None, 'V': [ml_check.validate_ipv4]},
			"to_remote_port": {'T':int, 'D':25, 'M':True, 'S':None},
			"connection_timeout": {'T':int, 'D':10, 'M':True, 'S':None}
		}
		self.real_server_group_ipv6_smtp_check_syntax = {
			"helo_name": {'T':str, 'D':"", 'M':True, 'S':None},
			"from_local_ip": {'T':str, 'D':"::", 'M':True, 'S':None, 'V': [ml_check.validate_ipv6]},
			"to_remote_ip": {'T':str, 'D':"::", 'M':True, 'S':None, 'V': [ml_check.validate_ipv6]},
			"to_remote_port": {'T':int, 'D':25, 'M':True, 'S':None},
			"connection_timeout": {'T':int, 'D':10, 'M':True, 'S':None}
		}
		self.real_server_group_ipv4_pattern_check_syntax = {
			"send": {'T':str, 'D':"GET / HTTP/1.0\r\n\r\n", 'M':True, 'S':None},
			"expect": {'T':str, 'D':"HTTP", 'M':True, 'S':None},
			"to_remote_ip": {'T':str, 'D':"0.0.0.0", 'M':True, 'S':None, 'V': [ml_check.validate_ipv4]},
			"to_remote_port": {'T':int, 'D':80, 'M':True, 'S':None},
			"timeout": {'T':int, 'D':10, 'M':True, 'S':None}
		}
		self.real_server_group_ipv6_pattern_check_syntax = {
			"send": {'T':str, 'D':"GET / HTTP/1.0\r\n\r\n", 'M':True, 'S':None},
			"expect": {'T':str, 'D':"HTTP", 'M':True, 'S':None},
			"to_remote_ip": {'T':str, 'D':"::", 'M':True, 'S':None, 'V': [ml_check.validate_ipv6]},
			"to_remote_port": {'T':int, 'D':80, 'M':True, 'S':None},
			"timeout": {'T':int, 'D':10, 'M':True, 'S':None}
		}
		self.real_server_group_ipv4_syntax = {
			"label": {'T':str, 'D':"", 'M':True, 'S':None},
			"ip_address": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv4]},
			"weight": {'T':int, 'D':1, 'M':True, 'S':None},
			"health_check": {'T':str, 'D':"NA", 'M':True, 'S':None},
			"http_get": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv4_http_get_syntax},
			"https_get": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv4_http_get_syntax},
			"icmp_check": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ip_icmp_check_syntax},
			"tcp_check": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv4_tcp_check_syntax},
			"smtp_check": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv4_smtp_check_syntax},
			"pattern_check": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv4_pattern_check_syntax},
			"maintenance_mode": {'T':bool, 'D':False, 'M':True, 'S':None}
		}
		self.real_server_group_ipv6_syntax = {
			"label": {'T':str, 'D':"", 'M':True, 'S':None},
			"ip_address": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv6]},
			"weight": {'T':int, 'D':1, 'M':True, 'S':None},
			"health_check": {'T':str, 'D':"NA", 'M':True, 'S':None},
			"http_get": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv6_http_get_syntax},
			"https_get": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv6_http_get_syntax},
			"icmp_check": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ip_icmp_check_syntax},
			"tcp_check": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv6_tcp_check_syntax},
			"smtp_check": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv6_smtp_check_syntax},
			"pattern_check": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_ipv6_pattern_check_syntax},
			"maintenance_mode": {'T':bool, 'D':False, 'M':True, 'S':None}
		}
		self.real_server_group_ipv4s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':True, 'S':self.real_server_group_ipv4_syntax}
		}
		self.real_server_group_ipv6s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':True, 'S':self.real_server_group_ipv6_syntax}
		}
		self.real_server_group_syntax = {
			"ipv4": {'T':list, 'D':[], 'M':False, 'S':self.real_server_group_ipv4s_syntax},
			"ipv6": {'T':list, 'D':[], 'M':False, 'S':self.real_server_group_ipv6s_syntax}
		}
		self.fallback_server_ipv4_syntax = {
			"label": {'T':str, 'D':"", 'M':True, 'S':None},
			"ip_address": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv4, ml_check.validate_NA]}
		}
		self.fallback_server_ipv6_syntax = {
			"label": {'T':str, 'D':"", 'M':True, 'S':None},
			"ip_address": {'T':str, 'D':"", 'M':False, 'S':None, 'V':[ml_check.validate_ipv6, ml_check.validate_NA]}
		}
		self.fallback_server_ipv4s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':True, 'S':self.fallback_server_ipv4_syntax}
		}
		self.fallback_server_ipv6s_syntax = {
			"*": {'T':dict, 'D':{}, 'M':True, 'S':self.fallback_server_ipv6_syntax}
		}
		self.fallback_server_syntax = {
			"ipv4": {'T':list, 'D':[], 'M':False, 'S':self.fallback_server_ipv4s_syntax},
			"ipv6": {'T':list, 'D':[], 'M':False, 'S':self.fallback_server_ipv6s_syntax}
		}
		self.property_syntax = {
			"label": {'T':str, 'D':"", 'M':True, 'S':None},
			"forward_method": {'T':str, 'D':"NAT", 'M':True, 'S':None},
			"balance_mode": {'T':str, 'D':"Round-robin", 'M':True, 'S':None},
			"health_check_interval": {'T':int, 'D':10, 'M':True, 'S':None},
			"persistence": {'T':int, 'D':10, 'M':True, 'S':None},
			"ipv4_netmask": {'T': str, 'D': "255.255.255.0", 'M': True, 'S': None, 'V': [ml_check.validate_ipv4_netmask]},
			"ipv6_prefix": {'T': int, 'D': 64, 'M': True, 'S': None, 'V': [ml_check.validate_ipv6_prefix]}
		}
		self.properties_syntax = {
			"*": {'T':dict, 'D':{}, 'M':True, 'S':self.property_syntax}
		}
		self.policy_ip_syntax = {
			"source_ip": {'T':str, 'D':"", 'M':True, 'S':None},
			"destination_ip": {'T':str, 'D':"", 'M':True, 'S':None},
			"service_group": {'T':str, 'D':"", 'M':True, 'S':None},
			"action": {'T':str, 'D':"", 'M':True, 'S':None},
			"real_server_group": {'T':str, 'D':"", 'M':True, 'S':None},
			"fallback_server": {'T':str, 'D':"", 'M':True, 'S':None},
			"property": {'T':str, 'D':"", 'M':True, 'S':None}
		}
		self.policy_ips_syntax = {
			"*": {'T':dict, 'D':{}, 'M':True, 'S':self.policy_ip_syntax}
		}
		self.policy_syntax = {
			"ipv4": {'T':list, 'D':[], 'M':False, 'S':self.policy_ips_syntax},
			"ipv6": {'T':list, 'D':[], 'M':False, 'S':self.policy_ips_syntax}
		}
		self.main_syntax = {
			"ip": {'T':dict, 'D':{}, 'M':False, 'S':self.ip_syntax}, 
			"service_group": {'T':dict, 'D':{}, 'M':False, 'S':self.service_group_syntax}, 
			"real_server_group": {'T':dict, 'D':{}, 'M':False, 'S':self.real_server_group_syntax}, 
			"fallback_server": {'T':dict, 'D':{}, 'M':False, 'S':self.fallback_server_syntax}, 
			"property": {'T':list, 'D':[], 'M':False, 'S':self.properties_syntax},
			"policy": {'T':dict, 'D':{}, 'M':False, 'S':self.policy_syntax}
		}
		self.ip_helper = [
			(ml_jcfg.N_("ipv4"), {
				"[]": [
					(ml_jcfg.N_("label"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("ip_address"), {"[]": ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True), "ANY"])})
				]
			}),
			(ml_jcfg.N_("ipv6"), {
				"[]": [
					(ml_jcfg.N_("label"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("ip_address"), {"[]": ml_jcfg.JcSelect(opt=[ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False), "ANY"])})
				]
			})
		]
		self.service_group_helper = [
			(ml_jcfg.N_("ipv4"), {
				"[]": [
					(ml_jcfg.N_("label"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("protocol"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("application_port"), {"[]": ml_jcfg.JcINT(default=65535)})
				]
			}),
			(ml_jcfg.N_("ipv6"), {
				"[]": [
					(ml_jcfg.N_("label"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("protocol"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("application_port"), {"[]": ml_jcfg.JcINT(default=65535)})
				]
			})
		]
		self.ipv4_http_get_helper = [
			(ml_jcfg.N_("url"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("status_code"), ml_jcfg.JcINT(default=200)),
			(ml_jcfg.N_("from_local_ip"), ml_jcfg.JcIpv4(a=True, r=True, s=True, default="0.0.0.0")),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("connection_timeout"), ml_jcfg.JcINT(default=10)),
			(ml_jcfg.N_("delay_before_retry"), ml_jcfg.JcINT(default=10))
		]
		self.ipv6_http_get_helper = [
			(ml_jcfg.N_("url"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("status_code"), ml_jcfg.JcINT(default=200)),
			(ml_jcfg.N_("from_local_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="::", sensitive=False)),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("connection_timeout"), ml_jcfg.JcINT(default=10)),
			(ml_jcfg.N_("delay_before_retry"), ml_jcfg.JcINT(default=10))
		]
		self.ipv4_https_get_helper = [
			(ml_jcfg.N_("url"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("status_code"), ml_jcfg.JcINT(default=200)),
			(ml_jcfg.N_("from_local_ip"), ml_jcfg.JcIpv4(a=True, r=True, s=True, default="0.0.0.0")),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("connection_timeout"), ml_jcfg.JcINT(default=10)),
			(ml_jcfg.N_("delay_before_retry"), ml_jcfg.JcINT(default=10))
		]
		self.ipv6_https_get_helper = [
			(ml_jcfg.N_("url"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("status_code"), ml_jcfg.JcINT(default=200)),
			(ml_jcfg.N_("from_local_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="::", sensitive=False)),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("connection_timeout"), ml_jcfg.JcINT(default=10)),
			(ml_jcfg.N_("delay_before_retry"), ml_jcfg.JcINT(default=10))
		]
		self.icmp_check_helper = [
			(ml_jcfg.N_("timeout"), ml_jcfg.JcINT(default=10))
		]
		self.ipv4_tcp_check_helper = [
			(ml_jcfg.N_("from_local_ip"), ml_jcfg.JcIpv4(a=True, r=True, s=True, default="0.0.0.0")),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("connection_timeout"), ml_jcfg.JcINT(default=10))
		]
		self.ipv6_tcp_check_helper = [
			(ml_jcfg.N_("from_local_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="::", sensitive=False)),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("connection_timeout"), ml_jcfg.JcINT(default=10))
		]
		self.ipv4_smtp_check_helper = [
			(ml_jcfg.N_("helo_name"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("from_local_ip"), ml_jcfg.JcIpv4(a=True, r=True, s=True, default="0.0.0.0")),
			(ml_jcfg.N_("from_remote_ip"), ml_jcfg.JcIpv4(a=True, r=True, s=True, default="0.0.0.0")),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("connection_timeout"), ml_jcfg.JcINT(default=10))
		]
		self.ipv6_smtp_check_helper = [
			(ml_jcfg.N_("helo_name"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("from_local_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="::", sensitive=False)),
			(ml_jcfg.N_("from_remote_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="::", sensitive=False)),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("connection_timeout"), ml_jcfg.JcINT(default=10))
		]
		self.ipv4_pattern_check_helper = [
			(ml_jcfg.N_("send"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("expect"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("from_remote_ip"), ml_jcfg.JcIpv4(a=True, r=True, s=True, default="0.0.0.0")),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("timeout"), ml_jcfg.JcINT(default=10))
		]
		self.ipv6_pattern_check_helper = [
			(ml_jcfg.N_("send"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("expect"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=True)),
			(ml_jcfg.N_("from_remote_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="::", sensitive=False)),
			(ml_jcfg.N_("to_remote_port"), ml_jcfg.JcINT(default=80)),
			(ml_jcfg.N_("timeout"), ml_jcfg.JcINT(default=10))
		]
		self.real_server_group_helper = [
			(ml_jcfg.N_("ipv4"), {
				"[]": [
					(ml_jcfg.N_("label"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("ip_address"), ml_jcfg.JcIpv4(a=True, r=True, s=True)),
					(ml_jcfg.N_("weight"), ml_jcfg.JcINT(default=1)),
					(ml_jcfg.N_("health_check"), ml_jcfg.JcSelect(opt=["NA", "HTTP_GET", "HTTPS_GET", "ICMP_CHECK", "TCP_CHECK", "SMTP_CHECK", "PATTERN_CHECK"], default="NA")),
					(ml_jcfg.N_("http_get"), self.ipv4_http_get_helper),
					(ml_jcfg.N_("https_get"), self.ipv4_https_get_helper),
					(ml_jcfg.N_("icmp_check"), self.icmp_check_helper),
					(ml_jcfg.N_("tcp_check"), self.ipv4_tcp_check_helper),
					(ml_jcfg.N_("smtp_check"), self.ipv4_smtp_check_helper),
					(ml_jcfg.N_("pattern_check"), self.ipv4_pattern_check_helper),
					(ml_jcfg.N_("maintenance_mode"), ml_jcfg.JcBOOL(default=0))
				]
			}),
			(ml_jcfg.N_("ipv6"), {
				"[]": [
					(ml_jcfg.N_("label"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("ip_address"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("weight"), ml_jcfg.JcINT(default=1)),
					(ml_jcfg.N_("health_check"), ml_jcfg.JcSelect(opt=["NA", "HTTP_GET", "HTTPS_GET", "ICMP_CHECK", "TCP_CHECK", "SMTP_CHECK", "PATTERN_CHECK"], default="NA")),
					(ml_jcfg.N_("http_get"), self.ipv6_http_get_helper),
					(ml_jcfg.N_("https_get"), self.ipv6_https_get_helper),
					(ml_jcfg.N_("icmp_check"), self.icmp_check_helper),
					(ml_jcfg.N_("tcp_check"), self.ipv6_tcp_check_helper),
					(ml_jcfg.N_("smtp_check"), self.ipv6_smtp_check_helper),
					(ml_jcfg.N_("pattern_check"), self.ipv6_pattern_check_helper),
					(ml_jcfg.N_("maintenance_mode"), ml_jcfg.JcBOOL(default=0))
				]
			})
		]
		self.fallback_server_helper = [
			(ml_jcfg.N_("ipv4"), {
				"[]": [
					(ml_jcfg.N_("label"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("ip_address"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcIpv4(a=True, r=True, s=True), "NA"]))
				]
			}),
			(ml_jcfg.N_("ipv6"), {
				"[]": [
					(ml_jcfg.N_("label"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("ip_address"), ml_jcfg.JcSelect(opt=[ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False), "NA"]))
				]
			})
		]
		self.policy_helper = [
			(ml_jcfg.N_("ipv4"), {
				"[]": [
					(ml_jcfg.N_("source_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("destination_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("service_group"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("action"), ml_jcfg.JcSelect(opt=["Accept", "Deny", "VIP"], default="VIP")),
					(ml_jcfg.N_("real_server_group"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("fallback_server"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("property"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False))
				]
			}),
			(ml_jcfg.N_("ipv6"), {
				"[]": [
					(ml_jcfg.N_("source_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("destination_ip"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("service_group"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("action"), ml_jcfg.JcSelect(opt=["Accept", "Deny", "VIP"], default="VIP")),
					(ml_jcfg.N_("real_server_group"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("fallback_server"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("property"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False))
				]
			})
		]
		self.helper = [(self.tag, [
			(ml_jcfg.N_("ip"), self.ip_helper),
			(ml_jcfg.N_("service_group"), self.service_group_helper),
			(ml_jcfg.N_("real_server_group"), self.real_server_group_helper),
			(ml_jcfg.N_("fallback_server"), self.fallback_server_helper),
			(ml_jcfg.N_("property"), {
				"[]": [
					(ml_jcfg.N_("label"), ml_jcfg.JcSTR(regex="^[\\x20-\\x7F ]{0,255}$", default="", sensitive=False)),
					(ml_jcfg.N_("forward_method"), ml_jcfg.JcSelect(opt=["NAT", "Route", "Transparent"], default="NAT")),
					(ml_jcfg.N_("balance_mode"), ml_jcfg.JcSelect(opt=["Round-robin", "Weighted Least Connections", "Weighted Round-robin", "Least Connection", "Locality Based Least Connection", "Locality Based Least Connection with Replication", "Destination Hash", "Source Hash", "Shortest Expect Delay", "Never Queue"], default="Round-robin")),
					(ml_jcfg.N_("health_check_interval"), ml_jcfg.JcINT(default=10)),
					(ml_jcfg.N_("persistence"), ml_jcfg.JcINT(default=10)),
					(ml_jcfg.N_("ipv4_netmask"), ml_jcfg.JcIpv4Mask()),
					(ml_jcfg.N_("ipv6_prefix"), ml_jcfg.JcINT(default=64))
				]
			}),
			(ml_jcfg.N_("policy"), self.policy_helper)
		])]
	def do_set(self):
		""" real task """
		mark = 1
		sbuf = ""
		ml_func.sudo(["/sbin/iptables -t filter -F FORWARD"])
		ml_func.sudo(["/sbin/ip6tables -t filter -F FORWARD"])
		ml_func.sudo(["/sbin/iptables -t mangle -F PREROUTING"])
		ml_func.sudo(["/sbin/ip6tables -t mangle -F PREROUTING"])
		# check fields
		if self.cfg.has_key("policy"):
			if self.cfg["policy"].has_key("ipv4"):
				for policy in self.cfg["policy"]["ipv4"]:
					if label_get(policy["source_ip"], self.cfg["ip"]["ipv4"]) == None:
						return (False, ["source ip - " + policy["source_ip"] + " does not exist"])
					if label_get(policy["destination_ip"], self.cfg["ip"]["ipv4"]) == None:
						return (False, ["destination ip - " + policy["destination_ip"] + " does not exist"])
					if label_get(policy["service_group"], self.cfg["service_group"]["ipv4"]) == None:
						return (False, ["service group - " + policy["service_group"] + " does not exist"])
					if policy["action"] == "VIP":
						if label_get(policy["real_server_group"], self.cfg["real_server_group"]["ipv4"]) == None:
							return (False, ["real server group - " + policy["real_server_group"] + " does not exist"])
						if label_get(policy["fallback_server"], self.cfg["fallback_server"]["ipv4"]) == None:
							return (False, ["fallback server - " + policy["fallback_server"] + " does not exist"])
						if label_get(policy["property"], self.cfg["property"]) == None:
							return (False, ["property - " + policy["property"] + " does not exist"])
						# add firewall mark
						src = ""
						for s in label_get(policy["source_ip"], self.cfg["ip"]["ipv4"])["ip_address"]:
							if s != "ANY" and s != "":
								src = " -s " + s
							dst = ""
							for d in label_get(policy["destination_ip"], self.cfg["ip"]["ipv4"])["ip_address"]:
								if d != "ANY" and d != "":
									dst = " -d " + d
								service = label_get(policy["service_group"], self.cfg["service_group"]["ipv4"])
								protocol = ""
								if service["protocol"] == "TCP":
									protocol = " -p tcp "
								elif service["protocol"] == "UDP":
									protocol = " -p udp "
								elif service["protocol"] == "BOTH":
									protocol = ""
								else:
									return (False, ["unknown protocol - " + service["protocol"]])
								port = ""
								if len(service["application_port"]) > 0:
									port = " -m multiport --dports "
									for p in service["application_port"]:
										try:
											port += str(p) + ","
										except Exception as e:
											return (False, [str(e)])
									port = port[:-1]
								ml_func.sudo(["/sbin/iptables -t mangle -A PREROUTING", src, dst, protocol, port, "-j MARK --set-mark " + str(mark)])
						# add keepalived
						sbuf += "{0}virtual_server fwmark %d {{\n".format(" "*0) % (mark)
						proper = label_get(policy["property"], self.cfg["property"])
						if proper["health_check_interval"] >= 0:
							sbuf += "{0}delay_loop %d\n".format(" "*4) % (proper["health_check_interval"])
						if bm_get(proper["balance_mode"]) == None:
							return (False, ["unknown balance mode - " + proper["balance_mode"]])
						sbuf += "{0}lb_algo %s\n".format(" "*4) % (bm_get(proper["balance_mode"]))
						if fm_get(proper["forward_method"]) == None:
							return (False, ["unknown forward method - " + proper["forward_method"]])
						sbuf += "{0}lb_kind %s\n".format(" "*4) % (fm_get(proper["forward_method"]))
						if proper["persistence"] >= 0:
							sbuf += "{0}persistence_timeout %d\n".format(" "*4) % (proper["persistence"])
						sbuf += "{0}persistence_granularity %s\n".format(" "*4) % (proper["ipv4_netmask"])
						if policy["fallback_server"] != "NA":
							sbuf += "{0}sorry_server %s 0\n".format(" "*4) % (label_get(policy["fallback_server"], self.cfg["fallback_server"]["ipv4"])["ip_address"])
						real_server = label_get(policy["real_server_group"], self.cfg["real_server_group"]["ipv4"])
						sbuf += "{0}real_server %s 0 {{\n".format(" "*4) % (real_server["ip_address"])
						if real_server["maintenance_mode"]:
							sbuf += "{0}weight 0\n".format(" "*8)
						elif real_server["weight"] >= 0:
							sbuf += "{0}weight %d\n".format(" "*8) % (real_server["weight"])
						if real_server["health_check"] != "NA":
							ret = hc_get(real_server)
							if ret[0]:
								for s in ret[1]:
									sbuf += "{0}%s\n".format(" "*8) % (s)
							else:
								return ret
						sbuf += "{0}}}\n".format(" "*4)
						sbuf += "{0}}}\n".format(" "*0)
					elif policy["action"] == "Accept" or policy["action"] == "Deny":
						src = ""
						for s in label_get(policy["source_ip"], self.cfg["ip"]["ipv4"])["ip_address"]:
							if s != "ANY" and s != "":
								src = " -s " + s
							dst = ""
							for d in label_get(policy["destination_ip"], self.cfg["ip"]["ipv4"])["ip_address"]:
								if d != "ANY" and d != "":
									dst = " -d " + d
								service = label_get(policy["service_group"], self.cfg["service_group"]["ipv4"])
								protocol = ""
								if service["protocol"] == "TCP":
									protocol = " -p tcp "
								elif service["protocol"] == "UDP":
									protocol = " -p udp "
								elif service["protocol"] == "BOTH":
									return (False, ["not support protocol - " + service["protocol"]])
								else:
									return (False, ["unknown protocol - " + service["protocol"]])
								port = ""
								if len(service["application_port"]) > 0:
									port = " -m multiport --dports "
									for p in service["application_port"]:
										try:
											port += str(p) + ","
										except Exception as e:
											return (False, [str(e)])
									port = port[:-1]
								if policy["action"] == "Accept":
									action = "-j ACCEPT"
								elif policy["action"] == "Deny":
									action = "-j DROP"
								ml_func.sudo(["/sbin/iptables -t filter -I FORWARD", src, dst, protocol, port, action])
					else:
						return (False, ["unknown policy action - " + policy["action"]])
					mark += 1
			if self.cfg["policy"].has_key("ipv6"):
				for policy in self.cfg["policy"]["ipv6"]:
					if label_get(policy["source_ip"], self.cfg["ip"]["ipv6"]) == None:
						return (False, ["source ip - " + policy["source_ip"] + " does not exist"])
					if label_get(policy["destination_ip"], self.cfg["ip"]["ipv6"]) == None:
						return (False, ["destination ip - " + policy["destination_ip"] + " does not exist"])
					if label_get(policy["service_group"], self.cfg["service_group"]["ipv6"]) == None:
						return (False, ["service group - " + policy["service_group"] + " does not exist"])
					if policy["action"] == "VIP":
						if label_get(policy["real_server_group"], self.cfg["real_server_group"]["ipv6"]) == None:
							return (False, ["real server group - " + policy["real_server_group"] + " does not exist"])
						if label_get(policy["fallback_server"], self.cfg["fallback_server"]["ipv6"]) == None:
							return (False, ["fallback server - " + policy["fallback_server"] + " does not exist"])
						if label_get(policy["property"], self.cfg["property"]) == None:
							return (False, ["property - " + policy["property"] + " does not exist"])
						# add firewall mark
						src = ""
						for s in label_get(policy["source_ip"], self.cfg["ip"]["ipv6"])["ip_address"]:
							if s != "ANY" and s != "":
								src = " -s " + s
							dst = ""
							for d in label_get(policy["destination_ip"], self.cfg["ip"]["ipv6"])["ip_address"]:
								if d != "ANY" and d != "":
									dst = " -d " + d
								service = label_get(policy["service_group"], self.cfg["service_group"]["ipv6"])
								protocol = ""
								if service["protocol"] == "TCP":
									protocol = " -p tcp "
								elif service["protocol"] == "UDP":
									protocol = " -p udp "
								elif service["protocol"] == "BOTH":
									protocol = ""
								else:
									return (False, ["unknown protocol - " + service["protocol"]])
								port = ""
								if len(service["application_port"]) > 0:
									port = " -m multiport --dports "
									for p in service["application_port"]:
										try:
											port += str(p) + ","
										except Exception as e:
											return (False, [str(e)])
									port = port[:-1]
								ml_func.sudo(["/sbin/ip6tables -t mangle -A PREROUTING", src, dst, protocol, port, "-j MARK --set-mark " + str(mark)])
						# add keepalived
						sbuf += "{0}virtual_server fwmark %d {{\n".format(" "*0) % (mark)
						proper = label_get(policy["property"], self.cfg["property"])
						if proper["health_check_interval"] >= 0:
							sbuf += "{0}delay_loop %d\n".format(" "*4) % (proper["health_check_interval"])
						if bm_get(proper["balance_mode"]) == None:
							return (False, ["unknown balance mode - " + proper["balance_mode"]])
						sbuf += "{0}lb_algo %s\n".format(" "*4) % (bm_get(proper["balance_mode"]))
						if fm_get(proper["forward_method"]) == None:
							return (False, ["unknown forward method - " + proper["forward_method"]])
						sbuf += "{0}lb_kind %s\n".format(" "*4) % (fm_get(proper["forward_method"]))
						if proper["persistence"] >= 0:
							sbuf += "{0}persistence_timeout %d\n".format(" "*4) % (proper["persistence"])
						sbuf += "{0}persistence_granularity %s\n".format(" "*4) % (proper["ipv6_prefix"])
						if policy["fallback_server"] != "NA":
							sbuf += "{0}sorry_server %s 0\n".format(" "*4) % (label_get(policy["fallback_server"], self.cfg["fallback_server"]["ipv6"])["ip_address"])
						real_server = label_get(policy["real_server_group"], self.cfg["real_server_group"]["ipv6"])
						sbuf += "{0}real_server %s 0 {{\n".format(" "*4) % (real_server["ip_address"])
						if real_server["maintenance_mode"]:
							sbuf += "{0}weight 0\n".format(" "*8)
						elif real_server["weight"] >= 0:
							sbuf += "{0}weight %d\n".format(" "*8) % (real_server["weight"])
						if real_server["health_check"] != "NA":
							ret = hc_get(real_server)
							if ret[0]:
								for s in ret[1]:
									sbuf += "{0}%s\n".format(" "*8) % (s)
							else:
								return ret
						sbuf += "{0}}}\n".format(" "*4)
						sbuf += "{0}}}\n".format(" "*0)
					elif policy["action"] == "Accept" or policy["action"] == "Deny":
						src = ""
						for s in label_get(policy["source_ip"], self.cfg["ip"]["ipv6"])["ip_address"]:
							if s != "ANY" and s != "":
								src = " -s " + s
							dst = ""
							for d in label_get(policy["destination_ip"], self.cfg["ip"]["ipv6"])["ip_address"]:
								if d != "ANY" and d != "":
									dst = " -d " + d
								service = label_get(policy["service_group"], self.cfg["service_group"]["ipv6"])
								protocol = ""
								if service["protocol"] == "TCP":
									protocol = " -p tcp "
								elif service["protocol"] == "UDP":
									protocol = " -p udp "
								elif service["protocol"] == "BOTH":
									return (False, ["not support protocol - " + service["protocol"]])
								else:
									return (False, ["unknown protocol - " + service["protocol"]])
								port = ""
								if len(service["application_port"]) > 0:
									port = " -m multiport --dports "
									for p in service["application_port"]:
										try:
											port += str(p) + ","
										except Exception as e:
											return (False, [str(e)])
									port = port[:-1]
								if policy["action"] == "Accept":
									action = "-j ACCEPT"
								elif policy["action"] == "Deny":
									action = "-j DROP"
								ml_func.sudo(["/sbin/ip6tables -t filter -I FORWARD", src, dst, protocol, port, action])
					else:
						return (False, ["unknown policy action - " + policy["action"]])
					mark += 1
		# update conf file
		try:
			file = open("running/slb.conf", "w")
			file.write(sbuf)
			file.close()
		except Exception as e:
			return (False, [str(e)])
		# reload service
		return (True, None)

def get(user = None, threadlock = None):
	"""
		Web UI calls get()
		return
			(True, dict)
			(False, list)
	"""
	try:
		obj = slb(threadlock = threadlock)
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
		obj = slb(threadlock = threadlock)
		return obj.set(cfg)
	except Exception as e:
		return (False, [str(e)])

def label_get(label, data):
	""" search data and return the first label object """
	if isinstance(data, list):
		for obj in data:
			if isinstance(obj, dict):
				if obj.has_key("label"):
					if obj["label"] == label:
						return obj
	return None

def bm_get(ui):
	""" convert UI balance method to keepalived lb_algo """
	if ui == "Round-robin":
		return "rr"
	elif ui == "Weighted Round-robin":
		return "wrr"
	elif ui == "Least Connection":
		return "lc"
	elif ui == "Weighted Least Connections":
		return "wlc"
	elif ui == "Locality Based Least Connection":
		return "lblc"
	elif ui == "Locality Based Least Connection with Replication":
		return "lblcr"
	elif ui == "Source Hash":
		return "sh"
	elif ui == "Destination Hash":
		return "dh"
	elif ui == "Shortest Expect Delay":
		return "sed"
	elif ui == "Never Queue":
		return "nq"
	else:
		return None

def fm_get(ui):
	""" convert UI forward method to keepalived lb_kind """
	if ui == "NAT":
		return "NAT"
	elif ui == "Route":
		return "DR"
	elif ui == "Transparent":
		return None
	else:
		return None

def hc_get(rs):
	"""
		generate keepalived health check from real server
		return
			(True, list of keepalived health check block strings)
			(False, list)
	"""
	sl = []
	if rs["health_check"] == "HTTP_GET":
		httpget = rs["http_get"]
		sl.append("HTTP_GET {")
		sl.append("{0}url {{".format(" "*4))
		sl.append("{0}path %s".format(" "*8) % (httpget["url"]))
		sl.append("{0}status_code %d".format(" "*8) % (httpget["status_code"]))
		sl.append("{0}}}".format(" "*4))
		sl.append("{0}bindto %s".format(" "*4) % (httpget["from_local_ip"]))
		sl.append("{0}connect_port %d".format(" "*4) % (httpget["to_remote_port"]))
		sl.append("{0}connect_timeout %d".format(" "*4) % (httpget["connection_timeout"]))
		sl.append("{0}delay_before_retry %d".format(" "*4) % (httpget["delay_before_retry"]))
		sl.append("}")
	elif rs["health_check"] == "HTTPS_GET":
		httpsget = rs["https_get"]
		sl.append("SSL_GET {")
		sl.append("{0}url {{".format(" "*4))
		sl.append("{0}path %s".format(" "*8) % (httpsget["url"]))
		sl.append("{0}status_code %d".format(" "*8) % (httpsget["status_code"]))
		sl.append("{0}}}".format(" "*4))
		sl.append("{0}bindto %s".format(" "*4) % (httpsget["from_local_ip"]))
		sl.append("{0}connect_port %d".format(" "*4) % (httpsget["to_remote_port"]))
		sl.append("{0}connect_timeout %d".format(" "*4) % (httpsget["connection_timeout"]))
		sl.append("{0}delay_before_retry %d".format(" "*4) % (httpsget["delay_before_retry"]))
		sl.append("}")
	elif rs["health_check"] == "TCP_CHECK":
		tcpcheck = rs["tcp_check"]
		sl.append("TCP_CHECK {")
		sl.append("{0}bindto %s".format(" "*4) % (tcpcheck["from_local_ip"]))
		sl.append("{0}connect_port %d".format(" "*4) % (tcpcheck["to_remote_port"]))
		sl.append("{0}connect_timeout %d".format(" "*4) % (tcpcheck["connection_timeout"]))
		sl.append("}")
	elif rs["health_check"] == "SMTP_CHECK":
		smtpcheck = rs["smtp_check"]
		sl.append("SMTP_CHECK {")
		sl.append("{0}host {{".format(" "*4))
		sl.append("{0}connect_ip %s".format(" "*8) % (smtpcheck["to_remote_ip"]))
		sl.append("{0}connect_port %d".format(" "*8) % (smtpcheck["to_remote_port"]))
		sl.append("{0}bindto %s".format(" "*8) % (smtpcheck["from_local_ip"]))
		sl.append("{0}}}".format(" "*4))
		sl.append("{0}connect_timeout %d".format(" "*4) % (smtpcheck["connection_timeout"]))
		if smtpcheck["helo_name"] != None and smtpcheck["helo_name"] != "":
			sl.append("{0}helo_name %s".format(" "*4) % (smtpcheck["helo_name"]))
		sl.append("}")
	elif rs["health_check"] == "ICMP_CHECK":
		icmpcheck = rs["icmp_check"]
		sl.append("MISC_CHECK {")
		sl.append("{0}misc_path \"ping -w 1 %s; exit $?\"".format(" "*4) % (rs["ip_address"]))
		sl.append("{0}misc_timeout %d".format(" "*4) % (icmpcheck["timeout"]))
		sl.append("}")
	elif rs["health_check"] == "PATTERN_CHECK":
		patterncheck = rs["pattern_check"]
		sl.append("MISC_CHECK {")
		sl.append("{0}misc_path \"echo -en \'%s\' | nc -n %s %d | grep \'%s\'; exit $?\"".format(" "*4) % (patterncheck["send"], patterncheck["to_remote_ip"], patterncheck["to_remote_port"], patterncheck["expect"]))
		sl.append("{0}misc_timeout %d".format(" "*4) % (patterncheck["timeout"]))
		sl.append("}")
	else:
		return (False, ["unknown health check - " + rs["health_check"]])
	return (True, sl)
