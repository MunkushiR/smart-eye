import streamlit as st
from PIL import Image
import os
import cv2
from backend.utils import *
from playsound import playsound
from matplotlib import pyplot as plt



def RUN():
    st.sidebar.title('Smart Eye')

    app_choice = st.sidebar.selectbox("Choose Mode",
                ["About", "Run Application"])
    
    if app_choice == 'About':
        about()

    elif app_choice == 'Run Application':
        application()

def about():
    about_path = os.path.join("frontend","README.md")
    f = open(about_path)
    code = f.read()
    st.markdown(code)

def application():
    picture = st.camera_input(label="Take Picture", disabled=False, key=1)

    while picture is not None:
        img = Image.open(picture)
        st.image(img, width= 250)
        with open(picture.name, 'wb') as name:
            name.write(picture.getbuffer())
        #print(name)

        max_val = 8
        max_pt = -1
        max_kp = 0

        orb_create = cv2.ORB_create()

        image = cv2.imread(picture.name)

        original = picture.name
        new = os.rename(original, 'new.jpg')

        new = new or 'new.jpg'
        
        test_image = read_img(new)

        original = resize_img(test_image, 0.4)

        #display('original', original)


        (kp1, des1) = orb_create.detectAndCompute(test_image, None)

        training_set = ['backend/files/50_01.jpg', 'backend/files/100_01.jpg', 'backend/files/200_01.jpg', 'backend/files/500_01.jpg','backend/files/1000_01.jpg']

        for i in range(0, len(training_set)):
            train_image = cv2.imread(training_set[i])

            (kp2, des2) = orb_create.detectAndCompute(train_image, None)

            
            bruteforce = cv2.BFMatcher()
            all_matches = bruteforce.knnMatch(des1, des2, k=2)

            good = []
            
            for (m, n) in all_matches:
                if m.distance < 0.789 * n.distance:
                    good.append([m])

            if len(good) > max_val:
                max_val = len(good)
                max_pt = i
                max_kp = kp2

            #print(i, ' ', training_set[i], ' ', len(good))

        if max_val != 8:
            #print(training_set[max_pt])
            #print('good matches ', max_val)

            train_image2 = cv2.imread(training_set[max_pt])
            img3 = cv2.drawMatchesKnn(test_image, kp1, train_image2, max_kp, good, 4)
            
            note = str(training_set[max_pt])[14:-7]
            #print('\nDetected denomination: Ksh. ', note)

            audio_file = 'backend/textToSpeech/{}.mp3'.format(note)
            #plt.imshow(img3), plt.show()
            playsound(audio_file)

        else:
            print('No Matches')
            playsound('nomatch.mp3')
        
        #st.write(type(new))
        os.remove(new)
        #os.remove('.camera*')
        
        picture = None
      

RUN()
