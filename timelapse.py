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
import subprocess

import sun

# the time between photos
DELTA = timedelta(seconds = 20)

def log(message) :
  print datetime.utcnow(), message

def run(cmd) :
  reset_nikon()
  
  # try running the command once and if it fails, reset_nikon
  # and then try once more
  for i in range(2) :
    log("running %s" % cmd)
    
    p = subprocess.Popen(
      'sudo ' + cmd,
      shell=True,
      stdout=subprocess.PIPE,
      stderr=subprocess.PIPE,
    )
    stdout = p.communicate()[1]
    ret = p.returncode
    
    print 'stdout', stdout
    print 'end stdout'
    print 'ret', ret
    
    if ret == 0 :
      return ret, stdout
    elif ret == 1 :
      if 'No camera found' in stdout :
        print '#### no camera found'
        print 'TODO: reboot?'
        print 'TODO: reset power on camera via GP IO?'
        return ret, stdout
      else :
        # other error like tried to delete a file where there was none, etc
        return ret, stdout
    else :
      reset_nikon()
  
  return ret, stdout

def reset_nikon() :
  import os
  
  ret = os.popen('lsusb').read()
  for line in ret.split('\n') :
    if 'Nikon' not in line : continue
    
    return os.system("./usbreset /dev/bus/usb/%s/%s" % (line[4:7], line[15:18]))

def take_picture(filename = None) :
  if not filename :
    filename = datetime.utcnow().strftime("%Y%m%d-%H%M%S.jpg")
  
  log('taking picture')
  return run("gphoto2 --capture-image-and-download --filename %s" % filename)
  #return os.system("gphoto2 --capture-image-and-download")

def delete_picture() :
  log('deleting picture')
  
  ret, stdout = run("gphoto2 --delete-file=1 --folder=/store_00010001")
  if 'There are no files in folder' in stdout :
    ret, stdout = run("gphoto2 --delete-file=1 --folder=/store_00010001/DCIM/100NIKON")
    if 'There are no files in folder' in stdout :
      ret, stdout = run("gphoto2 --delete-file=1 --folder=/")
  
  return ret

def reset_settings() :
  log('reseting settings')
  run("gphoto2 --set-config /main/capturesettings/flashmode=1")
  run("gphoto2 --set-config /main/capturesettings/focusmode=0")

reset_settings()

while True :
  t = datetime.utcnow()
  
  # only take pictures when it is light out
  if sun.is_light(t) :
    reset_nikon()
    take_picture()
  
  # remove the picture from camera memory since there isn't much there
  reset_nikon()
  delete_picture()
  
  # wait for 1 minute
  # we can't just do sleep(5 * 60) because taking the picture takes time
  print datetime.utcnow(), 'waiting ...'
  while datetime.utcnow() < t + DELTA :
    time.sleep(1)
