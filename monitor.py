import argparse
import datetime
import json
import platform
import pprint
import socket
import time
import uuid
from datetime import timedelta
from itertools import chain

import psutil

from sender import Sender

# parse args
parser = argparse.ArgumentParser(description='Monitoring script to send system info to a tracking server')
parser.add_argument('-d', '--dest', default='http://localhost:8080/', help='API Endpoint for Monitoring Data (Defaults to http://localhost:8080/)')
parser.add_argument('-i', '--interval', default=5, type=int, help='Interval between checks (Seconds. Defaults to 5 seconds)')
parser.add_argument('-a', '--attempts', default=30, type=int, help='Attempts to send data when sending failes (Defaults to 30)')
parser.add_argument('-t', '--timeout', default=60, type=int, help='Timeout between resend attempts (Seconds. Defaults to 60. If attempts is reached script will die)')
args = parser.parse_args()

# Factor in sleep for bandwidth checking
if args.interval >= 2:
    args.interval -= 2

def main():
    # Hostname Info
    hostname = socket.gethostname()

    # CPU Info
    cpu_count = psutil.cpu_count()
    cpu_usage = psutil.cpu_percent(interval=1)

    # Memory Info
    memory_stats = psutil.virtual_memory()
    memory_total = memory_stats.total / 1e+6
    memory_used = memory_stats.used / 1e+6
    memory_used_percent = memory_stats.percent

    # Disk Info
    disk_info = psutil.disk_usage('/')
    storage_total = (disk_info.total) / 1e+6
    storage_used = (disk_info.used) / 1e+6
    storage_used_percent = disk_info.percent

    # Platform Info
    system = {
        "name" : platform.system(),
        "version" : platform.release(),
        "os" : platform.freedesktop_os_release()["PRETTY_NAME"]
    }

    # Time Info
    timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S+00:00")
    uptime = timedelta(seconds=int(time.time() - psutil.boot_time()))

    # System UUID
    sys_uuid = uuid.getnode()

    # Set Machine Info
    machine = {
    	"hostname" : hostname,
		"uuid" : sys_uuid,
        "system" : system,
        "uptime" : str(uptime),
    	"cpu_count" : cpu_count,
    	"cpu_usage" : cpu_usage,
    	"memory_total" : memory_total,
    	"memory_used" : memory_used,
    	"memory_used_percent" : memory_used_percent,
    	"storage_total" : storage_total,
    	"storage_used" : storage_used,
    	"storage_used_percent" : storage_used_percent,
        "timestamp" : timestamp
    }

    data = json.dumps(machine)
    send_data(data)



def send_data(data):
    username = "data"
    s = Sender(data)
    s.send_msg(data)


if __name__ == "__main__":
    while True:
        main()
        time.sleep(args.interval)