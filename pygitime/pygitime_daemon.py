import daemon
from pygitime import start_tracking_time


with daemon.DaemonContext():
    start_tracking_time()
