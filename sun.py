from datetime import datetime, timedelta

import ephem

btown = ephem.Observer()
btown.pressure = 0

# standard horizon found in documentation
btown.horizon = '-0:34'

# bloomington lat and lon
btown.lat, btown.lon = '39.170637', '-86.556237'

# NOTE: all datetimes are UTC

def previous_setting(dt) :
  btown.date = dt.strftime("%Y/%m/%d %H:%M")
  
  setting = btown.previous_setting(ephem.Sun())
  return datetime.strptime(str(setting), '%Y/%m/%d %H:%M:%S')

def next_setting(dt) :
  btown.date = dt.strftime("%Y/%m/%d %H:%M")
  
  setting = btown.next_setting(ephem.Sun())
  return datetime.strptime(str(setting), '%Y/%m/%d %H:%M:%S')

def next_rising(dt) :
  btown.date = dt.strftime("%Y/%m/%d %H:%M")
  
  setting = btown.next_rising(ephem.Sun())
  return datetime.strptime(str(setting), '%Y/%m/%d %H:%M:%S')

def is_light(dt) :
  set = previous_setting(dt)
  rise = next_rising(dt)
  
  return rise - set > timedelta(hours = 24)

def is_dark(dt) :
  return not is_light(dt)

if __name__ == '__main__' :
  print is_light(datetime.utcnow())
  
  for i in range(24) :
    dt = datetime.utcnow() + timedelta(hours = i)
    print dt, is_light(dt)
