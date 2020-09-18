import signal
import sys
import time
import threading

def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print('Press Ctrl+C')
forever = threading.Event()
forever.wait()
while True:
    continue