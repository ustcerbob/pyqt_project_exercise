import cv2

default_folder_path = '../ui/'
# default_folder_path = 'D:\\img_from_camera\\'
default_img_name = '1.png'


class Camera(object):
    def __init__(self):
        self.cap = cv2.VideoCapture()  # 准备获取图像
        self.CAM_NUM = 0

    def open(self):
        return self.cap.open(self.CAM_NUM)

    def read_img(self):
        flag, self.image = self.cap.read()
        # print("读取图片")
        self.image = cv2.flip(self.image, 1)  # 左右翻转
        show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        return show




