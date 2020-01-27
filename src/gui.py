#!/usr/bin/python
# -'''- coding: utf-8 -'''-

import sys
import time
import os
from datetime import datetime, timezone
import stations
from img_button import ImgButton
from stations import Station
from constants import *
from PySide2.QtCore import QSize, QUrl, QStringListModel, Slot, QModelIndex
from PySide2.QtWidgets import *
from PySide2.QtGui import *
from PySide2.QtMultimedia import *
from apscheduler.schedulers.background import BackgroundScheduler



class StationList(QListView):
    def __init__(self, items: list):
        super().__init__()
        self.stringListModel = QStringListModel()
        self.stringListModel.setStringList(items)
        self.setModel(self.stringListModel)
        self.setStyleSheet("font-size: 23px;")
        self.setSpacing(0)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        
class MainWidget(QWidget):
    def __init__(self):
        super().__init__()
        # Configure layout
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        #Color stuff
        self.setAutoFillBackground(True)
        background_pal = self.palette()
        background_pal.setColor(self.backgroundRole(), Color.DARK_GREY)
        self.setPalette(background_pal)

        #Add a play and pause button
        self.play_icon = ImgButton(QPixmap(os.path.join(RESOURCE_PATH,"play_normal.png")),QPixmap(os.path.join(RESOURCE_PATH,"play_hover.png")),QPixmap(os.path.join(RESOURCE_PATH,"play_pressed.png")))
        self.layout.addWidget(self.play_icon, 3, 0)
        self.pause_icon = ImgButton(QPixmap(os.path.join(RESOURCE_PATH,"pause_normal.png")),QPixmap(os.path.join(RESOURCE_PATH,"pause_hover.png")),QPixmap(os.path.join(RESOURCE_PATH,"pause_pressed.png")))
        self.layout.addWidget(self.pause_icon, 3, 3)
        #connect the play and pause buttons to their functionality
        self.play_icon.clicked.connect(lambda: self.play_selected())
        self.pause_icon.clicked.connect(lambda: self.pause())
        #Add label displaying the current channel playing
        self.stationLabel = QLabel(self)
        self.stationLabel.setStyleSheet("font-size: 20px; color: white;")
        self.layout.addWidget(self.stationLabel,3,1,1,2, Qt.AlignCenter)
        #Add label displaying current song
        self.songLabel = QLabel(self)
        self.songLabel.setStyleSheet("font-size: 15px; color: white;")
        self.layout.addWidget(self.songLabel,2,0,1,4,Qt.AlignCenter)

        #Create a dictionary containing radio station names and their urls
        self.channelDict = stations.get_sr_channel_dict()
        #Add QlistView that displays radio stations
        self.stationList = StationList([channel for channel in self.channelDict])
        self.layout.addWidget(self.stationList,0,0,1,4)

        #Media player
        self.player = QMediaPlayer()
        self.currentChannel = self.channelDict["P1"] #Set default station !was a url
        self.player.setVolume(100)

        #Bind Enter to play the selected station
        self.play_action = QAction("Play", self)
        self.play_action.setShortcut("Return")
        self.play_action.triggered.connect(self.play_selected)
        self.addAction(self.play_action)

        #Scheduler
        end_date = self.currentChannel.currentSongEndDate #TODO Write function
        #TODO Edit to good format for scheduler
        self.scheduler = BackgroundScheduler()
        #self.scheduler.add_job(lambda:, 'date',run_date=end_date,args=["Name"])
        self.scheduler.start()

    def update_current_song(self):

        song_info = stations.get_current_song_info(self.currentChannel.id)
        if song_info is not None:
            self.currentChannel.currentSongDesc = song_info[0] + " - " + song_info[1]
            millis = int(int(song_info[2].strip("/Date()"))/1000)+(3630)
            utc = datetime.utcfromtimestamp(millis)
            self.currentChannel.currentSongEndDate = utc
            self.songLabel.setText(self.currentChannel.currentSongDesc)
            self.scheduler.add_job(lambda: self.update_current_song(), 'date' ,run_date=utc)
        else:
            self.songLabel.setText("")
            self.currentChannel.currentSongEndDate = None #TODO update scheduler


    @Slot()
    def play_selected(self):
        self.currentChannel = self.channelDict[self.stationList.selectedIndexes()[0].data()]
        self.stationLabel.setText(self.currentChannel.name)
        #Display current
        song_info = stations.get_current_song_info(self.currentChannel.id)
        self.update_current_song()
        self.player.setMedia(QUrl(self.currentChannel.url))
        self.player.play()

    def pause(self):
        self.songLabel.setText("")
        self.player.pause()
    
    def set_current_song(self):
        self.currentSong = get_current_song_info(self.currentChannel);

class MainWindow(QMainWindow):
    """
    Main window of the application.
    """
    def __init__(self, centralWidget: QWidget):
        super().__init__()
        self.setWindowTitle("Radio")
        self.show()

        self.setCentralWidget(centralWidget)
        self.setFixedSize(400,500)
        self.setWindowIcon(QIcon("chari.png"))

if __name__ == "__main__":

    app = QApplication(sys.argv)
    widget = MainWidget()
    window = MainWindow(widget)
    window.show()
    sys.exit(app.exec_())

