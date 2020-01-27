
from PySide2.QtCore import QSize
from PySide2.QtWidgets import *
from PySide2.QtGui import *

class ImgButton(QAbstractButton):
    """Image Button able to display different images for when pressed or hovered"""
    def __init__(self, pixmap, pixmap_hover, pixmap_pressed, parent=None):
        super(ImgButton, self).__init__(parent)
        self.pixmap = pixmap
        self.pixmap_hover = pixmap_hover
        self.pixmap_pressed = pixmap_pressed

        self.pressed.connect(self.update)
        self.released.connect(self.update)

    def paintEvent(self, event):
        pix = self.pixmap_hover if self.underMouse() else self.pixmap
        if self.isDown():
            pix = self.pixmap_pressed

        painter = QPainter(self)
        painter.drawPixmap(event.rect(), pix)

    def enterEvent(self, event):
        self.update()

    def leaveEvent(self, event):
        self.update()

    def sizeHint(self):
        return QSize(100, 100)