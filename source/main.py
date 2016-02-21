#!/usr/bin/env python3

from concurrent import futures
from admin import run_autodiscover_server
from led import *
import yaml
import os

RFLED_CONFIG_PATH = os.getenv('RFLED_CONFIG_PATH', 'config.yml')

with open(RFLED_CONFIG_PATH, 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

executor = futures.ThreadPoolExecutor(max_workers=len(cfg['interfaces'])+1)

# Start milight bridge threads
for iface in cfg['interfaces']:
    executor.submit(run_milight_bridge, iface["ip"], iface["serial"], cfg)

# Start autodiscovery thread if needed
if(cfg['autodiscover']):
    executor.submit(run_autodiscover_server, cfg);