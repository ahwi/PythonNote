import os
import cv2
import numpy as np

p = r"C:\Users\ahwi\02.note\03.python学习\02.note\code\opencv\doc\第2-7章notebook课件\图像操作"
filename = os.path.join(p, 'cat.jpg')
img = cv2.imread(filename)
print(img)
