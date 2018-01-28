from argparse import ArgumentParser
import os
import tempfile
import json

storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
parser = ArgumentParser()
parser.add_argument("--key", default=None)
parser.add_argument("--val", default=None)

def read_storage():
  if not os.path.exists(storage_path):
    return {}

  with open(storage_path, 'r') as f:
    data = f.read()
    return json.loads(data) if data else {}

def write_storage(storage):
  with open(storage_path, 'w') as f:
    f.write(json.dumps(storage))

def update_value(key, value):
  storage = read_storage()
  if key in storage:
    storage[key].append(value)
  else:
    storage[key] = [value]

  write_storage(storage)

def get_value(key):
  storage = read_storage()
  return storage.get(key)

def main():
  args = parser.parse_args()

  if args.key is None:
    return None

  if args.val is None:
    print(get_value(args.key))
    return None

  update_value(args.key, args.val)

if __name__ == '__main__':
  main()
