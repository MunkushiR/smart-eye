import cv2
from utils import *
from playsound import playsound
from matplotlib import pyplot as plt

max_val = 8
max_pt = -1
max_kp = 0
#algorith for detecting and describing local features in the im
orb_create = cv2.ORB_create()


test_image = read_img('files/100_01.jpg')
test_image = read_img('../new.jpg')


original = resize_img(test_image, 0.4)
display('original', original)

(kp1, des1) = orb_create.detectAndCompute(test_image, None)

training_set = ['files/50_01.jpg', 'files/100_01.jpg', 'files/200_01.jpg', 'files/500_01.jpg','files/1000_01.jpg']

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

	print(i, ' ', training_set[i], ' ', len(good))

if max_val != 8:
	print(training_set[max_pt])
	print('good matches ', max_val)

	train_image2 = cv2.imread(training_set[max_pt])
	img3 = cv2.drawMatchesKnn(test_image, kp1, train_image2, max_kp, good, 4)
	
	note = str(training_set[max_pt])[6:-7]
	print('\nDetected denomination: Ksh. ', note)

	audio_file = 'textToSpeech/{}.mp3'.format(note)
	(plt.imshow(img3), plt.show())
	playsound(audio_file)

else:
	print('No Matches')