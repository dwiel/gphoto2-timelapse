from datetime import datetime, timedelta
import os
import time

def log(message) :
  print datetime.now(), message

def run(cmd) :
  log("running %s" % cmd)
  return os.system(cmd)

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
  take_picture()
  
  # remove the picture from camera memory since there isn't much there
  delete_picture()
  
  # wait for 1 minute
  # we can't just do sleep(5 * 60) because taking the picture takes time
  print datetime.now(), 'waiting ...'
  while datetime.now() < t + timedelta(seconds = 20) :
    time.sleep(1)
