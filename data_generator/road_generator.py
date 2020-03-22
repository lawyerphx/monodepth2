import math
import os
import cv2

#cut the images using given boxes
from PIL import Image

imgList = os.listdir("../roads/")
print(imgList)

def Ceil(x):
    return int(math.ceil(x))

def magnify(img, fac):
    x, y, _  = img.shape
    return cv2.resize(img, (Ceil(y*fac), Ceil(x*fac)), interpolation=cv2.INTER_CUBIC)

def shrink(img, fac):
    x, y, _  = img.shape
    return cv2.resize(img, (Ceil(y/fac), Ceil(x/fac)), interpolation=cv2.INTER_CUBIC)

def cuttosize(img):
    x, y, _ = img.shape
    print("shape = ", x, y)
    ys = (y - 640)//2
    return img[-192:, ys:ys+640]

if __name__ == '__main__':
    for name in imgList:
        try:
            img = cv2.imread("../roads/"+name)
            x0, y0, _ = img.shape
            print(name, x0, y0)
            img = cv2.resize(img, (1024, 320), interpolation=cv2.INTER_CUBIC)
            file_name, file_type = os.path.splitext(name)
            cv2.imwrite("./cutted/%s.jpg" % (file_name), img)

            cmd = "python ../test_simple.py --image_path ./cutted/%s.jpg --model_name mono+stereo_1024x320" % file_name
            info = os.system(cmd)

            img = cv2.imread("./cutted/%s_disp.jpeg" % file_name)
            img = cv2.resize(img, (y0, x0), interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            cv2.imwrite("./depth/%s.jpg" % (file_name), img)
        except IOError:
            print("one file was ignored")

#192 * 640