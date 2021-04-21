import sys
import wave

from io import StringIO

import alsaaudio
import colorama
import numpy as np
import pyaudio

from reedsolo import RSCodec, ReedSolomonError
from termcolor import cprint

import datetime
import json
import time


import soundEncode as se

class Server():
    def __init__(self):
        pass

    def make_protocol(self):
        current_dt = str(datetime.datetime.now())
        print(current_dt)
        data_type = 'D'
        l_code ='DNLAB'
        data_size = len(current_dt) + len(l_code)

        protocol = {"type":data_type,"f_size":data_size,"data":{"ctime":current_dt,"l_code":l_code}}
        print(protocol)

        json_protocol = json.dumps(protocol)
        return json_protocol


    def send_msg(self):
        json_list = list(self.make_protocol())
        while True:
            send_word = None
            try:
                word_1 = json_list.pop(0)
                send_word = word_1
                word_2 = json_list.pop(0)
                send_word += word_2
                word_3 = json_list.pop(0)
                send_word += word_3
                se.send(send_word)
                time.sleep(1.5)
                send_word = None
            except IndexError:
                se.send(send_word)
                time.sleep(1.5)

                se.send("FIN")
                break
    def main(self):
        self.send_msg()



if __name__ == '__main__':
    server = Server()
    server.main()
