import speech_recognition as sr
import pyaudio
#om Recognizer classe na biblioteca SpeechRecognition. 
# O objetivo principal de um Recognizer classe é, naturalmente, reconhecer a fala.
# Criando um Recognizer instância é fácil
#
recognizer = sr.Recognizer()

#O uso do limite de energia melhorará o reconhecimento de fala ao trabalhar com dados de áudio. 
# Se os valores forem superioresao limiar de energia = 300, são considerados como fala,
# mas se os valores forem inferiores, são considerados silenciosos.
recognizer.energy_threshold = 300

#obter áudio do microfone
def takecommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening....")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
     print("Recognizing....")
     query = r.recognize_google(audio, language='pt')
     print(f"user said: {query}\n")
     
     #gravar áudio dito em um arquivo WAV
     with open("microphone-results.wav", "wb") as f:
      f.write(audio.get_wav_data())

    except Exception as e:
      print(e)
      return "None"
    return query
  
takecommand() 


#Código de processamento de áudio
audio_file = sr.AudioFile("microphone-results.wav")
type(audio_file)

#Então, vamos convertê-lo em áudio para dados de áudio com a ajuda de um registro.
with audio_file as source:
   audio_file = recognizer.record(source,duration = 5.0)
   result = recognizer.recognize_google(audio_data = audio_file)
print(result)
