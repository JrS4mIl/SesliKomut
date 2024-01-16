import random
import time
from gtts import gTTS
from playsound import playsound
import speech_recognition as sr
import pyaudio
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
import  requests
from bs4 import  BeautifulSoup
r=sr.Recognizer()

class SesliAsistan:

    def seslendirme(self, metin):
        metin_seslendirme = gTTS(text=metin, lang="tr")
        dosya = str(random.randint(0, 10000000000)) + ".mp3"
        metin_seslendirme.save(dosya)
        playsound(dosya)
        os.remove(dosya)

    def mikrofon(self):
        with sr.Microphone() as kaynak:
            print("Sizi dinliyorum..")
            listen=r.listen(kaynak)
            ses=""
            try:
                ses=r.recognize_google(listen,language="tr-TR")
            except sr.UnknownValueError:
                self.seslendirme("ne dediğinizi anlayamadım")
            return ses

    def ses_karslik(self,gelen_Ses):
        if(gelen_Ses in "merhaba"):
            self.seslendirme("size de merhabalar")
        elif(gelen_Ses in "nasılsın"):
            self.seslendirme("iyiyim sizler nasılsınız")
        elif(gelen_Ses in "müzik aç" or gelen_Ses in "video aç"):

            try:
                self.seslendirme("ne açmamı istersiniz")
                cevap=self.mikrofon()

                url="https://www.youtube.com/results?search_query="+cevap
                tarayici=webdriver.Chrome()
                tarayici.get(url)

                ilk_video=tarayici.find_element(By.XPATH,"//*[@id='video-title']/yt-formatted-string").click()

                time.sleep(5)

                self.seslendirme("istediğiniz içerik bu mu ")
                gelen_komut=self.mikrofon()
                if(gelen_komut in "Hayır"):
                    sayac=2
                    tarayici.back()
                    while(sayac<5):
                        diger_videolar=tarayici.find_element(By.XPATH,"//*[@id='contents']/ytd-video-renderer[{}]".format(sayac)).click()
                        time.sleep(5)
                        self.seslendirme("istediğiniz içerik bu mu")
                        komut=self.mikrofon()
                        if(komut in "Evet"):
                            self.seslendirme("keyifli vakit geçirmeler...")
                            break
                        else:
                            self.seslendirme("o zaman diğer videolara bakalım")
                            tarayici.back()
                            sayac+=1
                else:
                    self.seslendirme("keyifli vakit geçirmeler...")

            except:
                self.seslendirme("bir hata meydana geldi.lütfen daha sonra tekrar deneyiniz")

        elif(gelen_Ses in "google aç" or gelen_Ses in "arama yap"):
            self.seslendirme("ne aramamı istersiniz")
            cevap=self.mikrofon()

            url="https://www.google.com/search?q="+cevap
            self.seslendirme("{} ile ilgili bulduğum içerikler bunlar".format(cevap))
            tarayici=webdriver.Chrome()
            tarayici.get(url)

            site=tarayici.find_element(By.XPATH,"//*[@id='rso']/div[1]/div/div/div/div/div/div/div[1]/a/h3").click()

            time.sleep(5)
            tarayici.quit()
        elif(gelen_Ses in 'hava durum'):
            self.seslendirme('Hangi sehrin hava durumunu istersiniz')
            cevap=self.mikrofon()
            url = f'https://havadurumu15gunluk.xyz/havadurumu/948/{cevap}-hava-durumu-15-gunluk.html'
            response = requests.get(url)
            if response.status_code == 200:
                print('Islem Basarili baba')
                soup = BeautifulSoup(response.text, 'html.parser')
                havaDurum = soup.find_all('tr')[1].text.strip()
                ##print(havaDurum)
                havaDurum = havaDurum.replace('Saatlik', "")
                print(havaDurum)
                gunduz_sicaklik = havaDurum[-6:-4]
                gece = havaDurum[-3:-1]
                print("Gece Sikcalik:" + gece)
                print("Gunduz Sicaklik:" + gunduz_sicaklik)
                havaDurum = havaDurum[6:-6].strip()

                gunler = ["Sal", "Car", "Per", "Cum", "Cmt", 'Pzr', 'Pzt']
                for i in gunler:
                    if i in havaDurum:
                        havaDurum = havaDurum.replace(i, "")
                print(havaDurum)




            else:
                print('hata')




    def uyanma_fonksiyonu(self,gelen_Ses):
        if(gelen_Ses in "hey siri"):
            self.seslendirme("dinliyorum...")
            ses=self.mikrofon()
            if(ses!=""):
                self.ses_karslik(ses)



asistan = SesliAsistan()

while True:
    gelen_Ses=asistan.mikrofon().lower()
    if(gelen_Ses!=""):
        print(gelen_Ses)
        asistan.uyanma_fonksiyonu(gelen_Ses)

