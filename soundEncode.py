import sys
import wave
import struct
from io import StringIO

import alsaaudio
import colorama
import numpy as np
import pyaudio

from reedsolo import RSCodec, ReedSolomonError
from termcolor import cprint
from pyfiglet import figlet_format


HANDSHAKE_START_HZ = 8200
HANDSHAKE_END_HZ = 8200 + 1024

START_HZ = 1024
STEP_HZ = 256
BITS = 4

FEC_BYTES = 4



def sound_generate(stream, freq):
    print(freq)
    sample_rate = 44100
    duration  = float(0.38)
    sample = np.arange(duration * sample_rate)
    increment = 2 * np.pi * sample *freq
    increment = increment/sample_rate
    samples = np.sin(increment).astype(np.float32)
    stream.write(samples)

def divide_by_tone(each_data):
    data = list()
    #print("each_data:",each_data)
    data.append(each_data >> 4)
    data.append(each_data & 15)
    out = 0
    bit_left = each_data
    return data

def to_freq(step):
    return START_HZ + step * STEP_HZ

def sound_code(fec_payload):
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=44100,
                    output = True)

    start_flag =True
    for each_data in fec_payload:
        if start_flag:
            freq = HANDSHAKE_START_HZ
            sound_generate(stream, freq)
            start_flag = False
        data = divide_by_tone(each_data)
        for tone in data:
            freq = to_freq(tone)
            sound_generate(stream, freq)
    freq = HANDSHAKE_END_HZ
    sound_generate(stream, freq)
    sound_generate(stream, freq)
    #print(freq)

def play_Sound(msg):
    byte_array = msg#.encode("utf-8")
    rs = RSCodec(FEC_BYTES)
    fec_payload = bytearray(rs.encode(byte_array))
    #print(rs.decode(fec_payload))
    sound_code(fec_payload)

def send(input_msg):
    play_Sound(input_msg)


if __name__ == '__main__':
    size = 0
    input_msg = input("input:")
    #seq_num = input("seq:")
    send(input_msg)
