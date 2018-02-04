import os
import tempfile

class File:
  def __init__(self, filename):
    self.filename = filename

  def write(self, data):
    print(self.filename)
    with open(self.filename, 'w') as f:
      return f.write(data)

  def read(self):
    with open(self.filename, 'r') as f:
      return f.read()

  def __str__(self):
    return self.filename

  def __getitem__(self, item):
    with open(self.filename, 'r') as f:
      data = f.readlines()
      return data[item]

  def __add__(self, other):
    with open(self.filename, 'r') as f, open(other.filename, 'r') as f2:
      content = f.read() + f2.read()
      new_file = File(os.path.join(tempfile.gettempdir(), 'new'))
      new_file.write(content)
      return new_file
