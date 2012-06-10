#!/usr/bin/env python

import subprocess

def timelapse_running() :
  cmd = 'ps -ef | grep timelapse.py'
  
  p = subprocess.Popen(
    'sudo ' + cmd,
    shell=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE,
  )
  
  (stdout, stderr) = p.communicate()
  ret = p.returncode
  
  for line in stdout.split('\n') :
    if not line : continue
    
    tokens = line.split(None, 7)
    
    if 'grep' not in tokens[7] :
      return True
  
  return False

if __name__ == '__main__' :
  print timelapse_running()

