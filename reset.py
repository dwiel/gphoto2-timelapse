import os

ret = os.popen('lsusb').read()
for line in ret.split('\n') :
  if 'Nikon' not in line : continue

  os.system("./usbreset /dev/bus/usb/%s/%s" % (line[4:7], line[15:18]))
