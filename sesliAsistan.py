from gtts import gTTS
import playsound
import speech_recognition as sr
import pyaudio
import os
import random
r=sr.Recognizer()
class SesliAsistan:
    def seslendirme(self,metin):
        metin_seslendirme=gTTS(text=metin,lang='tr')
        dosya=str(random.randint(0,1000000000))+".mp3"
        metin_seslendirme.save(dosya)
        playsound(dosya)
        os.remove(dosya)
    def mikrofon(self):
        with sr.Microphone() as kaynak:
            print('Sizi Dinliyorum...')
            listen=r.listen(kaynak)
            ses=""
            try:
                ses=r.recognize_google(listen,language='tr-TR')
            except sr.UnknownValueError:
                self.seslendirme('Anlasilmadi')
            return  ses

asistan=SesliAsistan()
while True:
    gelen_ses=asistan.mikrofon()
    if(gelen_ses!=""):
        print(gelen_ses)