from datetime import datetime


def now() -> str:
  '''
    returns 24 hour format -> 'HH:MM'
  '''
  h = datetime.now().hour
  m = datetime.now().minute
  return str(h).zfill(2) + ':' + str(m).zfill(2)

def hour() -> int:
  '''
    returns 24 hour format as int
  '''
  return datetime.now().hour

def minute() -> int:
  '''
    returns minutes as int
  '''
  return datetime.now().minute

def second() -> int:
  '''
    returns seconds as int
  '''
  return datetime.now().second

def total_seconds():
    t = datetime.now()
    return (t.now().hour*3600) + (t.now().minute*60) + (t.now().second)
