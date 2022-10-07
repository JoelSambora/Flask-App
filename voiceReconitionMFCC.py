import speech_recognition as sr
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from sklearn import preprocessing
from python_speech_features import mfcc, logfbank

#Agora, leia o arquivo de áudio armazenado.
# Ele retornará dois valores - a frequência de amostragem
# e o sinal de áudio. Forneça o caminho do arquivo de áudio
# onde ele está armazenado.

frequency, audio = wavfile.read("congratulations.wav")

#aqui estamos coletando as primeiras 15.000 amostras para análise.
audio = audio[:15000]

#técnicas do MFCC e execute o seguinte comando para extrair os recursos do MFCC −

featuresMfcc = mfcc(audio, frequency)

#Agora, imprima os parâmetros MFCC, conforme mostrado −

print('nMFCC:nNumber of windows =', featuresMfcc.shape[0])
print('Length of each feature =', featuresMfcc.shape[1])

#Agora, plote e visualize os recursos do MFCC usando os comandos abaixo −

featuresMfcc = featuresMfcc.T
plt.matshow(featuresMfcc)
plt.title('MFCC')

#Nesta etapa, trabalhamos com os recursos do banco de filtros conforme mostrado −
#Extraia os recursos do banco de filtros −

filterbankFeatures = logfbank(audio, frequency)


#Agora, imprima os parâmetros do banco de filtros.

print('nFilter bank:nNumber of windows =', filterbankFeatures.shape[0])
print('Length of each feature =', filterbankFeatures.shape[1])

#Agora, plote e visualize os recursos do banco de filtros.

filterbankFeatures = filterbankFeatures.T

print('teste = ',filterbankFeatures)
plt.matshow(filterbankFeatures)
plt.title('Filter bank')
plt.show()

def calculate_delta(array):
    """Calculate and returns the delta of given feature vector matrix"""

    rows,cols = array.shape
    deltas = np.zeros((rows,20))
    N = 2
    for i in range(rows):
        index = []
        j = 1
        while j <= N:
            if i-j < 0:
              first =0
            else:
              first = i-j
            if i+j > rows-1:
                second = rows-1
            else:
                second = i+j 
            index.append((second,first))
            j+=1
        deltas[i] = ( array[index[0][0]]-array[index[0][1]] + (2 * (array[index[1][0]]-array[index[1][1]])) ) / 10
    return deltas

def extract_features(audio,rate):
    """extract 20 dim mfcc features from an audio, performs CMS and combines 
    delta to make it 40 dim feature vector"""    
    
    mfcc_feature = mfcc.mfcc(audio,rate, 0.025, 0.01,20,nfft = 1200, appendEnergy = True)    
    mfcc_feature = preprocessing.scale(mfcc_feature)
    delta = calculate_delta(mfcc_feature)
    combined = np.hstack((mfcc_feature,delta)) 
    return combined

extract_features(audio,15000)