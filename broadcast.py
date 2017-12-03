MYPORT = 5000

import sys, time
import os
from socket import *

s = socket(AF_INET, SOCK_DGRAM)
s.bind(('', 0))
s.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)


while True:
    data = repr(time.time())
    data = data.encode('UTF-8')

    s.sendto(data, ('<broadcast>', MYPORT))
    time.sleep(2)
