import os
import wave
import time
import pickle
import pyaudio
import warnings
import numpy as np
from sklearn import preprocessing
from scipy.io.wavfile import read
import python_speech_features as mfcc
from sklearn.mixture import GaussianMixture 


def record_audio_train():
    
    name = (input("Please enter your name: "))
    
    for count in range(5):
        formaT = pyaudio.paInt16
        channelS = 1
        ratE = 44100
        chunK = 515
        record_Seconds = 10
        device_index = 2
        audio = pyaudio.PyAudio()
        print("-----------Record device list-------------")
        
        info = audio.get_host_api_info_by_index(0)
        numdevices = info.get('diveceCount')
        
        for i in range (0, numdevices):
            if (audio.get_device_info_by_host_api_device_index(0, i).get('maxInputChannels')) > 0:
                print("input divece id ", i, " - ", audio.get_device_info_by_host_api_device_index(0, i).get('name'))
        print("-----------------------------------------")
        
        
        index = int(input())
        print("recording via index "+str(index))
        stream = audio.open(format=format, channels=channelS,
                            rate=ratE, input=True, input_device_index = index,
                            frames_per_buffer=chunK)
        print("recording started")
        
        Recordframes = []
        for i in range(0, int(ratE / chunK * record_Seconds)):
            data = stream.read(chunK)
            Recordframes.append(data)
        print ("recording stopped")
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        output_fileName = name+"-sample"+str(count)+"wav"
        wave_output_fileName = os.path.join("training_set", output_fileName)
        trainedFileList = open("training_set_addition.txt", 'a')
        trainedFileList.write(output_fileName+"\n")
        waveFile = wave.open(wave_output_fileName, 'wb')
        waveFile.setnchannels(channelS)
        waveFile.setsampwidth(audio.get_sample_size(formaT))
        waveFile.setframerate(ratE)
        waveFile.writeframe(b''.join(Recordframes))
        waveFile.close()
record_audio_train()        