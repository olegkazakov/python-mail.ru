class FileReader:
  def __init__(self, filename):
    self._filename = filename

  def read(self):
    try:
      with open(self._filename) as f:
        return f.read()
    except IOError:
      return ''
