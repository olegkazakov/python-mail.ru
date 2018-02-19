import asyncio

server_storage = {}

class ClientServerProtocol(asyncio.Protocol):

  def connection_made(self, transport):
    self.transport = transport

  def data_received(self, data):
    resp = self.process_data(data.decode())
    self.transport.write(resp.encode())

  def process_data(self, data):
    action, payload = data.split(' ', 1)
    res = 'error\nwrong command\n\n'
    if action in ('get', 'put'):
      res = getattr(self, action)(payload)

    return res

  def put(self, data):
    key, value, timestamp = data.split()
    if key not in server_storage:
      server_storage[key] = {}
    server_storage[key].update({timestamp: value})

    return 'ok\n\n'

  def add_to_res(self, res, key, values):
    if values:
      for timestamp, value in sorted(values.items()):
        res += '{} {} {}\n'.format(key, value, timestamp)

    return res

  def get(self, data):
    key = data.strip()
    res = 'ok\n'
    if key == '*':
      for key, values in server_storage.items():
        res = self.add_to_res(res, key, values)
    else:
      values = server_storage.get(key)
      res = self.add_to_res(res, key, values)

    return res + '\n'

def run_server(host, port):
  loop = asyncio.get_event_loop()
  coro = loop.create_server(
    ClientServerProtocol,
    host, port
  )

  server = loop.run_until_complete(coro)

  try:
    loop.run_forever()
  except KeyboardInterrupt:
    pass

  server.close()
  loop.run_until_complete(server.wait_closed())
  loop.close()
