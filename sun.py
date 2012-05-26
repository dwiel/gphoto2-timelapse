from datetime import datetime, timedelta

import ephem
import pytz

### helpers
def utc_to_local(t, tz):
  return tz.fromutc(t).replace(tzinfo=None)
def local_to_utc(t, tz=None):
  try :
    if tz == None :
      return t.astimezone(pytz.utc).replace(tzinfo=None)
    else :
      return tz.localize(t).astimezone(pytz.utc).replace(tzinfo=None)
  except AttributeError, e :
    if t == None :
      raise AttributeError('t must not be None')
    else :
      raise e

tz = pytz.timezone('US/Eastern')

btown = ephem.Observer()
btown.pressure = 0
btown.horizon = '-0:34'
btown.lat, btown.lon = '39.170637', '-86.556237'

def previous_setting(dt) :
  btown.date = local_to_utc(dt, tz).strftime("%Y/%m/%d %H:%M")
  
  setting = btown.previous_setting(ephem.Sun())
  setting = datetime.strptime(str(setting), '%Y/%m/%d %H:%M:%S')
  return utc_to_local(setting, tz)

def next_setting(dt) :
  btown.date = local_to_utc(dt, tz).strftime("%Y/%m/%d %H:%M")
  
  setting = btown.next_setting(ephem.Sun())
  setting = datetime.strptime(str(setting), '%Y/%m/%d %H:%M:%S')
  return utc_to_local(setting, tz)

def next_rising(dt) :
  btown.date = local_to_utc(dt, tz).strftime("%Y/%m/%d %H:%M")
  
  setting = btown.next_rising(ephem.Sun())
  setting = datetime.strptime(str(setting), '%Y/%m/%d %H:%M:%S')
  return utc_to_local(setting, tz)

def is_light(dt) :
  set = previous_setting(dt)
  rise = next_rising(dt)
  
  return rise - set > timedelta(hours = 24)

def is_dark(dt) :
  return not is_light(dt)


if __name__ == '__main__' :
  print is_light(datetime.now())
  
  for i in range(24) :
    print is_light(datetime.now() + timedelta(hours = i))
