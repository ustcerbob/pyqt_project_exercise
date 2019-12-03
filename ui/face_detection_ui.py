import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import *
from service import face_service


class picture(QWidget):
    def __init__(self):
        super(picture, self).__init__()

        self.resize(600, 800)
        self.setWindowTitle("label显示图片")

        self.label = QLabel(self)
        self.label.setText("   显示图片")
        self.label.setFixedSize(300, 500)
        self.label.move(160, 200)

        self.label.setStyleSheet("QLabel{background:white;}"
                                 "QLabel{color:rgb(0,0,0,70);font-size:20px;font-weight:bold;font-family:宋体;}"
                                 )
        self.userId_label = QLabel(self)
        self.userId_label.setText("学号：")
        self.userId_label.move(10,30)
        self.userId_edit = QLineEdit(self)
        self.userId_edit.move(160,30)

        self.user_info_label = QLabel(self)
        self.user_info_label.setText("姓名：")
        self.user_info_label.move(10, 70)
        self.user_info_edit = QLineEdit(self)
        self.user_info_edit.move(160, 70)

        btn_save_img = QPushButton(self)
        btn_save_img.setText('注册人脸')
        btn_save_img.move(10, 110)
        btn_save_img.clicked.connect(self.register_face)

        btn_face_detect = QPushButton(self)
        btn_face_detect.setText('人脸识别')
        btn_face_detect.move(160, 110)
        btn_face_detect.clicked.connect(self.face_detect)

        self.msg = QLabel(self)
        self.msg.move(10,150)

    def register_face(self):
        userId = self.userId_edit.text()
        user_info = self.user_info_edit.text()
        print(userId,user_info)
        face_service.face_register_to_db(userId, user_info)
        imgName = 'D:\\1.jpg'
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        self.msg.setText("人脸注册成功！")
        self.msg.adjustSize()

    def face_detect(self):
        code, user_info = face_service.face_search_welcome()


        imgName = 'D:\\1.jpg'
        jpg = QtGui.QPixmap(imgName).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        if code == 0:
            self.msg.setText("欢迎"+user_info+"同学！")
            self.msg.adjustSize()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    my = picture()
    my.show()
    sys.exit(app.exec_())