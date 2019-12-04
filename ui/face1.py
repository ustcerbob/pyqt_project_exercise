from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import sys
from PyQt5.QtWidgets import QApplication, QWidget
from service import face_service
import service.camera as camera


class Ui_self(QWidget):
    def __init__(self, parent=None):
        super(Ui_self, self).__init__(parent)
        self.timer_camera = QtCore.QTimer()  # 定时器
        self.setupUi()
        self.retranslateUi()
        self.cap = cv2.VideoCapture()  # 准备获取图像
        self.CAM_NUM = 0

        self.slot_init()  # 设置槽函数
        self.open_camera()  # 打开窗口即打开摄像头

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(509, 389)
        self.pushButton = QtWidgets.QPushButton(self)
        self.pushButton.setGeometry(QtCore.QRect(30, 100, 56, 17))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 180, 141, 171))
        self.label.setObjectName("label")
        self.label_face = QtWidgets.QLabel(self)
        self.label_face.setGeometry(QtCore.QRect(220, 30, 231, 321))
        self.label_face.setObjectName("label_face")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(30, 20, 41, 9))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(30, 60, 41, 9))
        self.label_4.setObjectName("label_4")
        self.label_msg = QtWidgets.QLabel(self)
        self.label_msg.setGeometry(QtCore.QRect(30, 150, 41, 9))
        self.label_msg.setObjectName("label_msg")
        self.lineEdit = QtWidgets.QLineEdit(self)
        self.lineEdit.setGeometry(QtCore.QRect(60, 10, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self)
        self.lineEdit_2.setGeometry(QtCore.QRect(60, 50, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_2 = QtWidgets.QPushButton(self)
        self.pushButton_2.setGeometry(QtCore.QRect(90, 100, 56, 17))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.setWindowTitle(_translate("self", "MainWindow"))
        self.pushButton.setText(_translate("self", "注册人脸"))
        self.label.setText(_translate("self", "显示图片"))
        self.label_face.setText(_translate("self", "显示摄像头动态图像"))
        self.label_3.setText(_translate("self", "学号"))
        self.label_4.setText(_translate("self", "姓名"))
        self.label_msg.setText(_translate("self", ""))
        self.pushButton_2.setText(_translate("self", "人脸识别"))

    def slot_init(self):
        # 设置槽函数
        # self.pushButton_open.clicked.connect(self.button_open_camera_click)
        self.timer_camera.timeout.connect(self.show_camera)
        # self.pushButton_close.clicked.connect(self.closeEvent)
        self.pushButton.clicked.connect(self.register_face)
        self.pushButton_2.clicked.connect(self.face_detect)

    def open_camera(self):
        if self.timer_camera.isActive() == False:
            # flag = self.cap.open(self.CAM_NUM)
            flag = self.cap.open(self.CAM_NUM)
            print(flag)
            print("摄像头开启")
            if flag == False:
                msg = QtWidgets.QMessageBox.warning(
                    self, u"Warning", u"请检测相机与电脑是否连接正确",
                    buttons=QtWidgets.QMessageBox.Ok,
                    defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                print("定时器开启")
                self.timer_camera.start(30)

    # 定时器执行显示动态图片
    def show_camera(self):
        flag, self.image = self.cap.read()
        # print("读取图片")
        self.image = cv2.flip(self.image, 1)  # 左右翻转
        show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)

        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.label_face.setPixmap(QtGui.QPixmap.fromImage(showImage))
        self.label_face.setScaledContents(True)

    def save_and_show_static_img(self):
        # 保存图片
        cv2.imwrite(camera.default_img_name, self.image)

        # cv2.putText(self.image, 'The picture have saved !',
        #             (int(self.image.shape[1]/2-130), int(self.image.shape[0]/2)),
        #             cv2.FONT_HERSHEY_SCRIPT_COMPLEX,
        #             1.0, (255, 0, 0), 1)
        #
        # #self.timer_camera.stop()
        #
        # show = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)  # 左右翻转
        #
        # showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)

        # self.label_face.setPixmap(QtGui.QPixmap.fromImage(showImage))
        #
        # self.label_face.setScaledContents(True)

        # 左侧框显示人脸图片

        jpg = QtGui.QPixmap(camera.default_img_name).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)

    # 注册人脸
    def register_face(self):
        self.save_and_show_static_img()
        # 用此图片进行人脸注册
        userId = self.lineEdit.text()
        user_info = self.lineEdit_2.text()

        if not userId or not user_info:
            QtWidgets.QMessageBox.warning(
                self, "Warning", "请填写完整的个人信息",
                buttons=QtWidgets.QMessageBox.Ok,
                defaultButton=QtWidgets.QMessageBox.Ok)
            return
        code = face_service.face_register_to_db(userId, user_info)
        if code == 0:
            msg = '人脸注册成功！请点击人脸识别！'
        else:
            msg = '人脸注册失败，请对准摄像头重试！'
        self.label_msg.setText(msg)

        self.label_msg.adjustSize()

    def face_detect(self):
        self.save_and_show_static_img()

        jpg = QtGui.QPixmap(camera.default_img_name).scaled(self.label.width(), self.label.height())
        self.label.setPixmap(jpg)
        code, user_info = face_service.face_search_welcome()
        if code == 0:
            msg = "欢迎" + user_info + "同学！"
        else:
            msg = '人脸识别失败，请对准摄像头重试！'
        self.label_msg.setText(msg)

        self.label_msg.adjustSize()


if __name__ == '__main__':
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    ui = Ui_self()

    ui.show()
    exit(app.exec_())
