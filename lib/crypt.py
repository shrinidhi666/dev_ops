#!/usr/bin/env python2.7
#-*- coding: utf-8 -*-
__author__ = "Shrinidhi Rao"
__license__ = "GPL"
__email__ = "shrinidhi666@gmail.com"

import sys
import os

sys.path.append(os.sep.join(os.path.abspath(__file__).split(os.sep)[:-2]))
import lib.constants
import lib.db_sqlite3
import lib.transport

from Crypto.PublicKey import RSA
from Crypto import Random

def generate_master():
  client = lib.transport.client()
  if(os.path.exists(lib.constants.master_private_key_file)):
    print("key file already present : {0}".format(lib.constants.master_private_key_file))
    f = open(lib.constants.master_private_key_file, "r")
    key = RSA.importKey(f.read())
    public_key = key.publickey().exportKey("PEM")

  else:
    if(not os.path.exists(lib.constants.configdir)):
      try:
        os.makedirs(lib.constants.configdir)
      except:
        print (sys.exc_info())
    random_generator = Random.new().read
    key = RSA.generate(2048, random_generator)
    private_key_file = open(lib.constants.master_private_key_file, "w")
    private_key_file.write(key.exportKey("PEM"))
    private_key_file.flush()
    private_key_file.close()
    public_key = key.publickey().exportKey("PEM")

  client.send(message={lib.constants.msg_keys.tasktype:lib.constants.tasktypes.key_register,
                       lib.constants.msg_keys.payload:public_key,

                         })
  print ("done writing private key")






if(__name__ == "__main__"):
  generate_master()