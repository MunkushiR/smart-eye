#To run app run : streamlit run main2.py


import streamlit as st
from backend.utils import *
import cv2
from playsound import playsound
import gtts
from PIL import Image
import random

def RUN():
    st.sidebar.title("Smart Eye")
    app_choice = st.sidebar.selectbox("Choose Mode",
                    ["About","Run Application"])

    if app_choice == "About":
        about()

    if app_choice == "Run Application":
        application()

def about():
    about_path = "frontend/README.md"
    f = open(about_path)
    code = f.read()
    st.markdown(code)

def application():
    picture = st.camera_input(label="Take a picture", disabled=False)

    max_val = 8
    max_pt = -1
    max_kp = 0

    orb = cv2.ORB_create()

    if picture:
        img1 = Image.open(picture)
        img1.save('new.jpg')
        img = read_img('new.jpg')
        #img = read_img('backend/files/100_01.jpg')
        original = resize_img(img, 0.4)
        #display('original', original)
        st.image(picture, caption="Image Taken")

        (kp1, des1) = orb.detectAndCompute(img, None)

        training_set = ['backend/files/50_test.jpg', 'backend/files/100_01.jpg', 'backend/files/200_01.jpg', 'backend/files/500_01.jpg','backend/files/1000_01.jpg']

        for i in range(0, len(training_set)):
            #Training Model
            train_img = cv2.imread(training_set[i])

            (kp2, des2) = orb.detectAndCompute(img, None)

            #Brute Force Matching
            bf = cv2.BFMatcher()
            all_matches = bf.knnMatch(des1, des2, k=2)

            good = []

            #Formulation of an arbituary number and appending matches to good[] list
            for (m, n) in all_matches:
                if m.distance < 0.789 * n.distance:
                    good.append([m])

            if len(good) > max_val:
                max_val = len(good)
                max_pt = i
                max_kp = kp2

            #st.markdown(i, ' ', training_set[i], ' ', len(good))
            

        if max_val != 8:
            print(training_set[max_pt])
            print('good matches ', max_val)
            train_img = cv2.imread(training_set[max_pt])
            img2 = cv2.drawMatchesKnn(img, kp1, train_img,max_kp, good, 4)
            #display('image', img2)

            note = str(training_set[max_pt])[14:-9]
            print(note)

            note1 = str('Detected denomination: Ksh. '+ note)

            audio_file = 'backend/textToSpeech/{}.mp3'.format(note)

            playsound(audio_file)

            st.markdown(note1)
            
            if st.button("Re-Run"):
                application()

        else:
            no_match = gtts.gTTS("no match found, try again")
            no_match.save('nomatch.mp3')
            no_match_display = str("No match found")
            playsound('nomatch.mp3')
            st.markdown(no_match_display)

            st.button('Re-Run', on_click=application())
            
            
RUN()           