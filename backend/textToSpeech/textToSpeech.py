import gtts
from playsound import playsound

currency = ["fifty kenyan shillings","one hundred kenyan shillings", "two hundred kenyan shillings",
            "five hundred kenyan shillings", "one thousand kenyan shillings"]

for i in currency:
    tts = gtts.gTTS(i)
    tts.save("{}.mp3".format(i))
    playsound("{}.mp3".format(i))
    print(i)