###############################################################################################
# DS1820.py                                                                                   #
# Communication with DS1820                                                                   #
# (c) https://github.com/thomaspfeiffer-git May 2015                                          #
###############################################################################################


class DS1820:
   def __init__ (self, id):
      self.__id = id
   

   def read (self):
      pass



def read_sensor(path):
  value = "U"
  try:
    f = open(path, "r")
    line = f.readline()
    if re.match(r"([0-9a-f]{2} ){9}: crc=[0-9a-f]{2} YES", line):
      line = f.readline()
      m = re.match(r"([0-9a-f]{2} ){9}t=([+-]?[0-9]+)", line)
      if m:
        value = str(float(m.group(2)) / 1000.0)
    f.close()
  except (IOError), e:
    print time.strftime("%x %X"), "Error reading", path, ": ", e
  return value


