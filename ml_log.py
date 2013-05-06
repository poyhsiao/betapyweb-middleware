#!/usr/bin/env python
#-*- coding: UTF-8 -*-
"""
  Logging
"""

import logging
import ml_system

if "CRITICAL" == ml_system.LOG_LEVEL:	l = logging.CRITICAL
if "ERROR"    == ml_system.LOG_LEVEL:	l = logging.ERROR
if "WARNING"  == ml_system.LOG_LEVEL:	l = logging.WARNING
if "INFO"     == ml_system.LOG_LEVEL:	l = logging.INFO
if "DEBUG"    == ml_system.LOG_LEVEL:	l = logging.DEBUG
logging.basicConfig(filename=ml_system.LOG_FILE, level=l)

def log(msg=""):
	""" middleware log function """
	logging.debug(msg)
