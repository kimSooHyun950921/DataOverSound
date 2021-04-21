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
import struct


import soundEncode as se

class Server():
    def __init__(self):
        self.protocol = self.make_protocol()
        self.popped_protocol = list(self.protocol)

    def make_protocol(self):
        current_dt = str(datetime.datetime.now())
        print(current_dt)
        data_type = 'D'
        l_code ='DNLAB'
        data_size = len(current_dt.split('.')[0]) + len(l_code)

        protocol = 'a'#{"ctime":current_dt.split('.')[0],"lcodes":l_code}
        
        print(protocol)

        json_protocol = json.dumps(protocol)
        return json_protocol

    def wrapper(self):
        seq_num = 0
        data_size = len(bytearray(self.protocol,"utf-8"))
        print("DATASIZE",data_size)
        #reserved_data = 1
        send_packet = bytes('a')#struct.pack("hh",seq_num ,data_size)
        print(struct.unpack("hh",send_packet))
        print("packed_data_info",send_packet)
        se.send(send_packet)
        time.sleep(1.5)
        while len(self.popped_protocol) > 0:
            seq_num += 1
            send_word = self.make_msg()
            send_packet = struct.pack("h3s",seq_num, bytes(send_word,'utf-8'))
            print("packed_data",send_packet)

            se.send(send_packet)
            time.sleep(1.5)
        self.popped_protocol = list(self.make_protocol())

    def make_msg(self):
        send_word = None
        try:
            word_1 = self.popped_protocol.pop(0)
            send_word = word_1
            word_2 = self.popped_protocol.pop(0)
            send_word += word_2
            word_3 = self.popped_protocol.pop(0)
            send_word += word_3
#            word_4 = self.popped_protocol.pop(0)
#            send_word += word_4
            print("orinal_data : ",send_word)

            return send_word
        except IndexError:
            return send_word


    def main(self):
        self.wrapper()



if __name__ == '__main__':
    server = Server()
    server.main()
