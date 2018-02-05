import socket
import time


class ClientError(Exception):
  pass


class Client:
  def __init__(self, host, port, timeout=None):
    self.socket = socket.create_connection((host, port), timeout)

  def send(self, msg):
    try:
      self.socket.sendall(msg.encode("utf8"))
    except socket.error as error:
      raise ClientError("Error sending data", error)

  def receive(self):
    try:
      answer = self.socket.recv(1024).decode("utf8")
    except socket.error as error:
      raise ClientError("Error receiving data", error)

    status, data = answer.split("\n", 1)
    data = data.strip()

    if status == 'error':
      raise ClientError(data)

    return data

  def put(self, key, value, timestamp=None):
    if not timestamp:
      timestamp = int(time.time())
    msg = "put {0} {1} {2}\n".format(key, str(value), str(timestamp))
    self.send(msg)
    self.receive()

  def get(self, key):
    data = {}
    msg = "get {0}\n".format(key)
    self.send(msg)
    answer = self.receive()

    if answer == '':
      return data

    items = [item.split() for item in answer.split('\n')]
    for key, metric, timestamp in items:
      if key not in data:
        data[key] = []
      data[key].append((int(timestamp), float(metric)))

    return data
