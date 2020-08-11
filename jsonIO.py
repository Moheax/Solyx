import json
import os
import logging
from random import randint

class JsonIO():
  def __init__(self):
    self.logger = logging.getLogger('solyx')

  def _read_json(self, file):
    with open(file, encoding='utf-8', mode="r") as f:
      data = json.load(f)
    return data
  
  def _write_json(self, file, data):
    with open(file, encoding='utf-8', mode="w") as f:
      json.dump(data, f, indent=4,sort_keys=True,
                separators=(',',' : '))
    return data

  def verify_json(self, file):
    try:
      self._read_json(file)
      return True
    except FileNotFoundError:
      return False
    except json.decoder.JSONDecodeError:
      return False

  def save(self, file, data):
    rnd = randint(10000, 99999)
    path = os.path.splitext(file)[0]
    tmp = "{}-{}.tmp".format(path, rnd)
    self._write_json(tmp, data)
    try:
      self._read_json(tmp)
    except json.decoder.JSONDecodeError:
      self.logger.exception("JsonIO.save() failed for file: {}".format(file))
      return False
    os.replace(tmp, file)
    return True

  def load(self, file):
    try:
      data = self._read_json(file)
      return data
    except Exception:
      self.logger.exception("JsonIO.load() failed for file: {}".format(file))
      return False
