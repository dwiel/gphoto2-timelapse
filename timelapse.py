"""
NOTE: many settings in here are specific to the NIKON3000 and will need to be 
tweaked for other cameras

TODO:
* slow down interval at night
* do an image diff between the past few images to see how fast things are
  changing.  If they are changing slowly, slow down the interval
"""

from datetime import datetime, timedelta
import os
import time

import sun

# the time between photos
DELTA = timedelta(seconds = 20)

def log(message) :
  print datetime.now(), message

def run(cmd) :
  log("running %s" % cmd)
  ret = os.system(cmd)
  print 'ret', ret

def reset_nikon() :
  import os
  
  ret = os.popen('lsusb').read()
  for line in ret.split('\n') :
    if 'Nikon' not in line : continue
    
    return os.system("./usbreset /dev/bus/usb/%s/%s" % (line[4:7], line[15:18]))

def take_picture(filename = None) :
  if not filename :
    filename = datetime.now().strftime("%Y%m%d-%H%M%S.jpg")
  
  log('taking picture')
  return run("gphoto2 --capture-image-and-download --filename %s" % filename)
  #return os.system("gphoto2 --capture-image-and-download")

def delete_picture() :
  log('deleting picture')
  return run("gphoto2 --delete-file=1 --folder=/store_00010001/DCIM/100NIKON")

def reset_settings() :
  log('reseting settings')
  run("gphoto2 --set-config /main/capturesettings/flashmode=1")
  run("gphoto2 --set-config /main/capturesettings/focusmode=0")

reset_settings()

while True :
  t = datetime.now()
  
  # only take pictures when it is light out
  if sun.is_light(t) :
    reset_nikon()
    take_picture()
  
  # remove the picture from camera memory since there isn't much there
  reset_nikon()
  delete_picture()
  
  # wait for 1 minute
  # we can't just do sleep(5 * 60) because taking the picture takes time
  print datetime.now(), 'waiting ...'
  while datetime.now() < t + DELTA :
    time.sleep(1)
