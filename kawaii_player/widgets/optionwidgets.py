import os
import datetime
from functools import partial
from PyQt5 import QtCore, QtWidgets, QtGui
from player_functions import write_files
from thread_modules import DiscoverServer

class SidebarWidget(QtWidgets.QListWidget):
    """
    Options Sidebar Widget
    """
    def __init__(self, parent, uiwidget, home_dir):
        super(SidebarWidget, self).__init__(parent)
        global ui, home
        ui = uiwidget
        home = home_dir

    def mouseMoveEvent(self, event): 
        self.setFocus()
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_O:
            ui.setPreOpt()
        elif event.key() == QtCore.Qt.Key_Down:
            nextr = self.currentRow() + 1
            if nextr == self.count():
                self.setCurrentRow(0)
            else:
                self.setCurrentRow(nextr)
        elif event.key() == QtCore.Qt.Key_Up:
            prev_r = self.currentRow() - 1
            if self.currentRow() == 0:
                self.setCurrentRow(self.count()-1)
            else:
                self.setCurrentRow(prev_r)
        elif event.key() == QtCore.Qt.Key_Right:
            if not ui.list1.isHidden():
                ui.list1.setFocus()
            elif not ui.scrollArea.isHidden():
                ui.scrollArea.setFocus()
            elif not ui.scrollArea1.isHidden():
                ui.scrollArea1.setFocus()
            elif not ui.list_poster.isHidden():
                ui.list_poster.setFocus()
            ui.dockWidget_3.hide()
        elif event.key() == QtCore.Qt.Key_Return:
            ui.newoptions('clicked')
            self.setFocus()
        elif event.key() == QtCore.Qt.Key_Left:
            if not ui.list2.isHidden():
                if ui.list2.currentItem():
                    index = ui.list2.currentRow()
                    ui.list2.setCurrentRow(index)
                ui.list2.setFocus()
            elif not ui.list1.isHidden():
                ui.list1.setFocus()
            elif not ui.scrollArea.isHidden():
                ui.scrollArea.setFocus()
            elif not ui.scrollArea1.isHidden():
                ui.scrollArea1.setFocus()
            elif not ui.list_poster.isHidden():
                ui.list_poster.setFocus()
            if ui.auto_hide_dock:
                ui.dockWidget_3.hide()
        elif event.key() == QtCore.Qt.Key_H:
            ui.setPreOpt()
        elif (event.modifiers() == QtCore.Qt.ControlModifier 
                and event.key() == QtCore.Qt.Key_D):
            site = ui.get_parameters_value(s='site')['site']
            if site.lower() == 'myserver':
                if not ui.discover_thread:
                    ui.discover_thread = DiscoverServer(ui, True)
                    ui.discover_thread.start()
                elif isinstance(ui.discover_thread, DiscoverServer):
                    if ui.discover_thread.isRunning():
                        ui.discover_server = False
                    else:
                        ui.discover_thread = DiscoverServer(ui, True)
                        ui.discover_thread.start()
        elif event.key() == QtCore.Qt.Key_Delete:
            param_dict = ui.get_parameters_value(s='site', b='bookmark')
            site = param_dict['site']
            bookmark = param_dict['bookmark']
            if site == "PlayLists":
                index = self.currentRow()
                item_r = self.item(index)
                if item_r:
                    item = str(self.currentItem().text())
                    if item != "Default":
                        file_pls = os.path.join(home, 'Playlists', item)
                        if os.path.exists(file_pls):
                            os.remove(file_pls)
                        self.takeItem(index)
                        del item_r
                        ui.list2.clear()
            if bookmark:
                index = self.currentRow()
                item_r = self.item(index)
                if item_r:
                    item = str(self.currentItem().text())
                    bookmark_array = [
                        'All', 'Watching', 'Completed', 'Incomplete', 
                        'Later', 'Interesting', 'Music-Videos'
                        ]
                    if item not in bookmark_array:
                        file_pls = os.path.join(home, 'Bookmark', item+'.txt')
                        if os.path.exists(file_pls):
                            os.remove(file_pls)
                        self.takeItem(index)
                        del item_r
                        ui.list1.clear()
                        ui.list2.clear()
        else:
            super(SidebarWidget, self).keyPressEvent(event)

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        history = menu.addAction("History")
        anime = menu.addAction("Animes")
        movie = menu.addAction("Movies")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == history:
            ui.setPreOpt()
        elif action == anime:
            category = "Animes"
            ui.set_parameters_value(catg=category)
        elif action == movie:
            category = "Movies"
            ui.set_parameters_value(catg=category)


class FilterTitleList(QtWidgets.QListWidget):
    """
    Filter Titlelist Widget
    """
    def __init__(self, parent, uiwidget, home_dir):
        super(FilterTitleList, self).__init__(parent)
        global ui, home
        ui = uiwidget
        home = home_dir

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down:
            nextr = self.currentRow() + 1
            if nextr == self.count():
                ui.go_page.setFocus()
            else:
                self.setCurrentRow(nextr)
        elif event.key() == QtCore.Qt.Key_Up:
            prev_r = self.currentRow() - 1
            if self.currentRow() == 0:
                ui.go_page.setFocus()
            else:
                self.setCurrentRow(prev_r)
        elif event.key() == QtCore.Qt.Key_Return:
            ui.search_list4_options()

    def contextMenuEvent(self, event):
        menu = QtWidgets.QMenu(self)
        hd = menu.addAction("Hide Search Table")
        sideBar = menu.addAction("Show Sidebar")
        history = menu.addAction("Show History")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == hd:
            self.hide()
        elif action == sideBar:
            if ui.dockWidget_3.isHidden():
                ui.dockWidget_3.show()
                ui.btn1.setFocus()
            else:
                ui.dockWidget_3.hide()
                ui.list1.setFocus()
        elif action == history:
            ui.setPreOpt()


class FilterPlaylist(QtWidgets.QListWidget):
    """
    Filter Playlist Widget
    """
    def __init__(self, parent, uiwidget, home_dir, logr):
        super(FilterPlaylist, self).__init__(parent)
        global ui, home, logger
        ui = uiwidget
        home = home_dir
        logger = logr

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down:
            nextr = self.currentRow() + 1
            if nextr == self.count():
                ui.goto_epn_filter_txt.setFocus()
            else:
                self.setCurrentRow(nextr)
        elif event.key() == QtCore.Qt.Key_Up:
            prev_r = self.currentRow() - 1
            if self.currentRow() == 0:
                ui.goto_epn_filter_txt.setFocus()
            else:
                self.setCurrentRow(prev_r)
        elif event.key() == QtCore.Qt.Key_Return:
            ui.search_list5_options()
        elif event.key() == QtCore.Qt.Key_Q:
            site = ui.get_parameters_value(s='site')['site']
            if (site == "Music" or site == "Video" or site == "Local" 
                    or site == "PlayLists" or site == "None"):
                file_path = os.path.join(home, 'Playlists', 'Queue')
                if not os.path.exists(file_path):
                    f = open(file_path, 'w')
                    f.close()
                if not ui.queue_url_list:
                    ui.list6.clear()
                indx = self.currentRow()
                item = self.item(indx)
                if item:
                    tmp = str(self.currentItem().text())
                    tmp1 = tmp.split(':')[0]
                    r = int(tmp1)
                    ui.queue_url_list.append(ui.epn_arr_list[r])
                    ui.list6.addItem(ui.epn_arr_list[r].split('	')[0])
                    logger.info(ui.queue_url_list)
                    write_files(file_path, ui.epn_arr_list[r], line_by_line=True)


class QueueListWidget(QtWidgets.QListWidget):
    """
    Queue Widget List
    """
    def __init__(self, parent, uiwidget, home_dir):
        super(QueueListWidget, self).__init__(parent)
        global ui, home
        ui = uiwidget
        home = home_dir

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Down:
            nextr = self.currentRow() + 1
            if nextr == self.count():
                self.setCurrentRow(0)
            else:
                self.setCurrentRow(nextr)
        elif event.key() == QtCore.Qt.Key_Up:
            prev_r = self.currentRow() - 1
            if self.currentRow() == 0:
                self.setCurrentRow(self.count()-1)
            else:
                self.setCurrentRow(prev_r)
        elif event.key() == QtCore.Qt.Key_PageUp:
            r = self.currentRow()
            if r > 0:
                r1 = r - 1
                if not ui.video_local_stream:
                    ui.queue_url_list[r], ui.queue_url_list[r1] = ui.queue_url_list[r1], ui.queue_url_list[r]
                item = self.item(r)
                txt = item.text()
                self.takeItem(r)
                del item
                self.insertItem(r1, txt)
                self.setCurrentRow(r1)
        elif event.key() == QtCore.Qt.Key_PageDown:
            r = self.currentRow()
            if r < self.count()-1 and r >= 0:
                r1 = r + 1
                if not ui.video_local_stream:
                    ui.queue_url_list[r], ui.queue_url_list[r1] = ui.queue_url_list[r1], ui.queue_url_list[r]
                item = self.item(r)
                txt = item.text()
                self.takeItem(r)
                del item
                self.insertItem(r1, txt)
                self.setCurrentRow(r1)
        elif event.key() == QtCore.Qt.Key_Return:
            r = self.currentRow()
            if self.item(r):
                ui.queueList_return_pressed(r)
        elif event.key() == QtCore.Qt.Key_Delete:
            r = self.currentRow()
            if self.item(r):
                item = self.item(r)
                self.takeItem(r)
                del item
                if not ui.video_local_stream:
                    del ui.queue_url_list[r]

class MyToolTip(QtWidgets.QToolTip):
    
    def __init__(self, uiwidget):
        super(MyToolTip).__init__()
        global ui
        ui = uiwidget
        
class MySlider(QtWidgets.QSlider):

    def __init__(self, parent, uiwidget, home_dir):
        super(MySlider, self).__init__(parent)
        global home, ui
        ui = uiwidget
        home = home_dir
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        version = QtCore.QT_VERSION_STR
        self.version = tuple([int(i) for i in version.split('.')])
        if self.version >= (5, 9, 0):
            self.tooltip = MyToolTip(ui)
        else:
            self.tooltip = None
        self.parent = parent
        
    def mouseMoveEvent(self, event): 
        t = self.minimum() + ((self.maximum()-self.minimum()) * event.x()) / self.width()
        if ui.player_val == "mplayer":
            l=str((datetime.timedelta(milliseconds=t)))
        elif ui.player_val == "mpv":
            l=str((datetime.timedelta(seconds=t)))
        else:
            l = str(0)
        if '.' in l:
            l = l.split('.')[0]
        if self.tooltip is None:
            self.setToolTip(l)
        else:
            point = QtCore.QPoint(self.parent.x()+event.x(), self.parent.y()+self.parent.height())
            rect = QtCore.QRect(self.parent.x(), self.parent.y(), self.parent.width(), self.parent.height())
            self.tooltip.showText(point, l, self, rect, 1000)
        
    def mousePressEvent(self, event):
        old_val = int(self.value())
        t = ((event.x() - self.x())/self.width())
        t = int(t*ui.mplayerLength)
        new_val = t
        if ui.player_val == 'mplayer':
            print(old_val, new_val, int((new_val-old_val)/1000))
        else:
            print(old_val, new_val, int(new_val-old_val))
        if ui.mpvplayer_val.processId() > 0:
            if ui.player_val == "mpv":
                var = bytes('\n '+"seek "+str(new_val)+" absolute"+' \n', 'utf-8')
                ui.mpvplayer_val.write(var)
            elif ui.player_val =="mplayer":
                seek_val = int((new_val-old_val)/1000)
                var = bytes('\n '+"seek "+str(seek_val)+' \n', 'utf-8')
                ui.mpvplayer_val.write(var)


class VolumeSlider(QtWidgets.QSlider):

    def __init__(self, parent, uiwidget, mainwidget):
        super(VolumeSlider, self).__init__(parent)
        global ui, MainWindow
        MainWindow = mainwidget
        ui = uiwidget
        self.parent = parent
        self.setOrientation(QtCore.Qt.Horizontal)
        self.setRange(0, 100)
        self.setMouseTracking(True)
        self.valueChanged.connect(self.adjust_volume)
        self.pressed = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        
    def mouseMoveEvent(self, event):
        if ui.frame1.isHidden():
            ui.frame1.show()
        pos = int((event.x()/self.width())*100)
        
    def mousePressEvent(self, event):
        self.pressed = True
        pos = int((event.x()/self.width())*100)
        self.setValue(pos)
    
    def mouseReleaseEvent(self, event):
        self.pressed = True
        pos = int((event.x()/self.width())*100)
        self.setValue(pos)
    
    def keyPressEvent(self, event):
        if event.key() in [QtCore.Qt.Key_Right, QtCore.Qt.Key_Left]:
            self.pressed = False
            if event.key() == QtCore.Qt.Key_Right:
                self.setValue(self.value() + 1)
            else:
                self.setValue(self.value() - 1)
            ui.seek_to_vol_val(self.value(), action='dragged')
            ui.player_volume = str(self.value())
            
    def adjust_volume(self, val):
        self.parent.volume_text.setPlaceholderText('{}'.format(val))
        if self.pressed:
            ui.player_volume = str(val)
            if ui.mpvplayer_val.processId() > 0:
                ui.seek_to_vol_val(val, action='pressed')
                ui.logger.debug(val)
                
class QProgressBarCustom(QtWidgets.QProgressBar):
    
    def __init__(self, parent, gui):
        super(QProgressBarCustom, self).__init__(parent)
        self.gui = gui
        
    def mouseReleaseEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            if self.gui.video_local_stream:
                if self.gui.torrent_frame.isHidden():
                    self.gui.torrent_frame.show()
                    self.gui.label_torrent_stop.setToolTip('Stop Torrent')
                    self.gui.label_down_speed.show()
                    self.gui.label_up_speed.show()
                    if self.gui.torrent_download_limit == 0:
                        down_rate = '\u221E' + ' K'
                    else:
                        down_rate = str(int(self.gui.torrent_download_limit/1024))+'K'
                    if self.gui.torrent_upload_limit == 0:
                        up_rate = '\u221E' + ' K'
                    else:
                        up_rate = str(int(self.gui.torrent_upload_limit/1024))+'K'
                    down = '\u2193 RATE: ' +down_rate
                    up = '\u2191 RATE:' +up_rate
                    self.gui.label_down_speed.setPlaceholderText(down)
                    self.gui.label_up_speed.setPlaceholderText(up)
                else:
                    self.gui.torrent_frame.hide()
            else:
                if self.gui.torrent_frame.isHidden():
                    self.gui.torrent_frame.show()
                    self.gui.label_down_speed.hide()
                    self.gui.label_up_speed.hide()
                    self.gui.label_torrent_stop.setToolTip('Stop Current Download')
                else:
                    self.gui.torrent_frame.hide()

class QLineCustom(QtWidgets.QLineEdit):
    
    def __init__(self, parent, ui_widget):
        super(QLineCustom, self).__init__(parent)
        global ui
        ui = ui_widget
        
    def keyPressEvent(self, event):
        if self.objectName() == 'go_page':
            if event.key() == QtCore.Qt.Key_Down:
                ui.list4.show()
                ui.list4.setFocus()
                self.show()
            elif event.key() == QtCore.Qt.Key_Up:
                ui.list4.show()
                ui.list4.setFocus()
                self.show()
            else:
                super(QLineCustom, self).keyPressEvent(event)
        elif self.objectName() == 'label_search':
            if event.key() in [QtCore.Qt.Key_Down, QtCore.Qt.Key_Return]:
                if not ui.list_poster.isHidden():
                    ui.list_poster.setFocus()
                elif not ui.scrollArea.isHidden():
                    ui.scrollArea.setFocus()
                elif not ui.scrollArea1.isHidden():
                    ui.scrollArea1.setFocus()
            else:
                super(QLineCustom, self).keyPressEvent(event)


class QLineCustomSearch(QtWidgets.QLineEdit):
    
    def __init__(self, parent, ui_widget):
        super(QLineCustomSearch, self).__init__(parent)
        global ui
        ui = ui_widget
    
    def go_to_target(self):
        if ui.focus_widget == ui.list1:
            ui.list1.setFocus()
            if ui.view_mode == 'thumbnail':
                ui.tab_6.setFocus()
                ui.take_to_thumbnail(mode='title', focus=True)
            elif ui.view_mode == 'thumbnail_light':
                ui.tab_6.setFocus()
                ui.list_poster.setFocus()
        elif ui.focus_widget == ui.list2:
            ui.list2.setFocus()
            if not ui.tab_6.isHidden():
                ui.tab_6.setFocus()
                ui.take_to_thumbnail(mode='epn', focus=True)
        
    def keyPressEvent(self, event):
        print("down")
        if event.key() == QtCore.Qt.Key_Down:
            self.go_to_target()
            self.hide()
        elif event.key() == QtCore.Qt.Key_Up:
            self.hide()
        elif event.key() == QtCore.Qt.Key_Return:
            self.go_to_target()
            self.hide()
        else:
            super(QLineCustomSearch, self).keyPressEvent(event)

class QLineCustomEpn(QtWidgets.QLineEdit):
    
    def __init__(self, parent, ui_widget):
        super(QLineCustomEpn, self).__init__(parent)
        global ui
        ui = ui_widget
        
    def keyPressEvent(self, event):
        
        if (event.type()==QtCore.QEvent.KeyPress) and (event.key() == QtCore.Qt.Key_Down):
            print("Down")
            ui.list5.setFocus()
        elif event.key() == QtCore.Qt.Key_Up:
            ui.list5.setFocus()
        super(QLineCustomEpn, self).keyPressEvent(event)


class QLabelFloat(QtWidgets.QLabel):

    def __init(self, parent=None):
        QLabel.__init__(self, parent)
        
    def set_globals(self, uiwidget, home_dir):
        global ui, home
        ui = uiwidget
        home = home_dir
        
    def mouseMoveEvent(self, event):
        if ui.float_timer.isActive():
            ui.float_timer.stop()
        if ui.new_tray_widget.cover_mode.text() == ui.player_buttons['up']:
            wid_height = int(ui.float_window.height()/3)
        else:
            wid_height = int(ui.float_window.height())
        ui.new_tray_widget.setMaximumHeight(wid_height)
        ui.new_tray_widget.show()
        ui.float_timer.start(1000)
        print('float')
        
    def mouseEnterEvent(self, event):
        print('Enter Float')


class SelectButton(QtWidgets.QComboBox):
    
    def __init__(self, parent, ui_widget):
        super(SelectButton, self).__init__(parent)
        global ui
        ui = ui_widget
        
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Right:
            if not ui.list1.isHidden():
                ui.list1.setFocus()
            elif not ui.scrollArea.isHidden():
                ui.scrollArea.setFocus()
            elif not ui.scrollArea1.isHidden():
                ui.scrollArea1.setFocus()
            elif not ui.list_poster.isHidden():
                ui.list_poster.setFocus()
            if ui.auto_hide_dock:
                ui.dockWidget_3.hide()
        elif event.key() == QtCore.Qt.Key_Left:
            if self.currentText() == 'Addons':
                ui.btnAddon.setFocus()
            else:
                ui.list3.setFocus()
        else:
            super(SelectButton, self).keyPressEvent(event)

class GSBCSlider(QtWidgets.QSlider):

    def __init__(self, parent, uiwidget, name):
        super(GSBCSlider, self).__init__(parent)
        global ui
        self.parent = parent
        ui = uiwidget
        self.setObjectName(name)
        self.setOrientation(QtCore.Qt.Horizontal)
        if name == 'zoom':
            self.setRange(-200, 200)
        elif name == 'speed':
            self.setRange(-100, 400)
        else:
            self.setRange(-100, 100)
        self.setTickInterval(5)
        self.setValue(0)
        self.setMouseTracking(True)
        self.valueChanged.connect(self.adjust_gsbc_values)
        self.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.setTickPosition(QtWidgets.QSlider.TicksAbove)
        
    def adjust_gsbc_values(self, val):
        name = self.objectName()
        if name == 'zoom':
            label_value = eval('self.parent.{}_value'.format(name))
            zoom_val = 0.01* val
            label_value.setPlaceholderText(str(zoom_val))
            cmd = '\n set video-zoom {} \n'.format(zoom_val)
            if ui.mpvplayer_val.processId() > 0:
                ui.mpvplayer_val.write(bytes(cmd, 'utf-8'))
        elif name == 'speed':
            label_value = eval('self.parent.{}_value'.format(name))
            speed_val = 1 + 0.01* val
            label_value.setPlaceholderText(str(speed_val))
            cmd = '\n set speed {} \n'.format(speed_val)
            if ui.mpvplayer_val.processId() > 0:
                ui.mpvplayer_val.write(bytes(cmd, 'utf-8'))
        else:
            label_value = eval('self.parent.{}_value'.format(name))
            label_value.setPlaceholderText(str(val))
            cmd = '\n set {} {} \n'.format(name, val)
            if ui.mpvplayer_val.processId() > 0:
                ui.mpvplayer_val.write(bytes(cmd, 'utf-8'))
            ui.gsbc_dict.update({name:val})
        
class ExtraToolBar(QtWidgets.QFrame):
    
    def __init__(self, parent, uiwidget):
        super(ExtraToolBar, self).__init__(parent)
        global ui, MainWindow
        ui = uiwidget
        MainWindow = parent
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.setFrameShadow(QtWidgets.QFrame.Raised)
        self.setObjectName("frame_extra_toolbar")
        self.layout = QtWidgets.QVBoxLayout(self)
        self.layout.setObjectName("extra_toolbar_layout")
        self.playlist_hide = False
        self.hide()
        
        self.gsbc_layout = QtWidgets.QGridLayout(self)
        self.gsbc_layout.setObjectName('gsbc_layout')
        self.layout.insertLayout(1, self.gsbc_layout)
        self.brightness_slider = GSBCSlider(self, uiwidget, 'brightness')
        self.contrast_slider = GSBCSlider(self, uiwidget, 'contrast')
        self.saturation_slider = GSBCSlider(self, uiwidget, 'saturation')
        self.gamma_slider = GSBCSlider(self, uiwidget, 'gamma')
        self.hue_slider = GSBCSlider(self, uiwidget, 'hue')
        self.zoom_slider = GSBCSlider(self, uiwidget, 'zoom')
        self.speed_slider = GSBCSlider(self, uiwidget, 'speed')
        
        self.brightness_label = QtWidgets.QLabel(self)
        self.brightness_label.setText('Brightness')
        self.brightness_value = QtWidgets.QLineEdit(self)
        
        self.contrast_label = QtWidgets.QLabel(self)
        self.contrast_label.setText('Contrast')
        self.contrast_value = QtWidgets.QLineEdit(self)
        
        self.saturation_label = QtWidgets.QLabel(self)
        self.saturation_label.setText('Saturation')
        self.saturation_value = QtWidgets.QLineEdit(self)
        
        self.gamma_label = QtWidgets.QLabel(self)
        self.gamma_label.setText('Gamma')
        self.gamma_value = QtWidgets.QLineEdit(self)
        
        self.hue_label = QtWidgets.QLabel(self)
        self.hue_label.setText('Hue')
        self.hue_value = QtWidgets.QLineEdit(self)
        
        self.zoom_label = QtWidgets.QLabel(self)
        self.zoom_label.setText('Zoom')
        self.zoom_value = QtWidgets.QLineEdit(self)
        
        self.speed_label = QtWidgets.QLabel(self)
        self.speed_label.setText('Speed')
        self.speed_value = QtWidgets.QLineEdit(self)
        self.speed_value.setPlaceholderText('1.0')
        
        slider_list = [
            self.contrast_slider, self.brightness_slider,
            self.gamma_slider, self.saturation_slider, 
            self.hue_slider, self.zoom_slider, self.speed_slider
            ]
        for index, slider in enumerate(slider_list):
            label = eval("self.{}_label".format(slider.objectName()))
            label_value = eval("self.{}_value".format(slider.objectName()))
            label_value.setMaximumWidth(32)
            label_value.setPlaceholderText(str(slider.value()))
            label_value.returnPressed.connect(partial(self.gsbc_entered, label_value, slider))
            self.gsbc_layout.addWidget(label, index, 0, 1, 1)
            self.gsbc_layout.addWidget(slider, index, 1, 1, 3)
            self.gsbc_layout.addWidget(label_value, index, 5, 1, 1)
        
        self.buttons_layout = QtWidgets.QGridLayout(self)
        self.buttons_layout.setObjectName('buttons_layout')
        self.layout.insertLayout(2, self.buttons_layout)
        
        self.btn_aspect_label = QtWidgets.QLabel(self)
        self.btn_aspect_label.setText('Aspect\nRatio')
        self.buttons_layout.addWidget(self.btn_aspect_label, 0, 0, 2, 1)
        
        self.btn_aspect_original = QtWidgets.QPushButton(self)
        self.btn_aspect_original.setText('Original')
        self.btn_aspect_original.clicked.connect(partial(self.change_aspect, 'original'))
        self.buttons_layout.addWidget(self.btn_aspect_original, 0, 1, 1, 2)
        
        self.btn_aspect_disable = QtWidgets.QPushButton(self)
        self.btn_aspect_disable.setText('Disable')
        self.btn_aspect_disable.clicked.connect(partial(self.change_aspect, 'disable'))
        self.buttons_layout.addWidget(self.btn_aspect_disable, 0, 3, 1, 1)
        
        self.btn_aspect_4_3 = QtWidgets.QPushButton(self)
        self.btn_aspect_4_3.setText('4:3')
        self.btn_aspect_4_3.clicked.connect(partial(self.change_aspect, '4:3'))
        self.buttons_layout.addWidget(self.btn_aspect_4_3, 1, 1, 1, 1)
        
        self.btn_aspect_16_9 = QtWidgets.QPushButton(self)
        self.btn_aspect_16_9.setText('16:9')
        self.btn_aspect_16_9.clicked.connect(partial(self.change_aspect, '16:9'))
        self.buttons_layout.addWidget(self.btn_aspect_16_9, 1, 2, 1, 1)
        
        self.btn_aspect_235 = QtWidgets.QPushButton(self)
        self.btn_aspect_235.setText('2.35:1')
        self.btn_aspect_235.clicked.connect(partial(self.change_aspect, '2.35:1'))
        self.buttons_layout.addWidget(self.btn_aspect_235, 1, 3, 1, 1)
        
        self.btn_scr_label = QtWidgets.QLabel(self)
        self.btn_scr_label.setText('Screenshot')
        self.buttons_layout.addWidget(self.btn_scr_label, 2, 0, 1, 1)
        
        self.btn_scr_1 = QtWidgets.QPushButton(self)
        self.btn_scr_1.setText('1')
        self.btn_scr_1.clicked.connect(partial(self.execute_command, 'async screenshot'))
        self.buttons_layout.addWidget(self.btn_scr_1, 2, 1, 1, 1)
        self.btn_scr_1.setToolTip("Take Screenshot with subtitle")
        
        self.btn_scr_2 = QtWidgets.QPushButton(self)
        self.btn_scr_2.setText('2')
        self.btn_scr_2.clicked.connect(partial(self.execute_command, 'async screenshot video'))
        self.buttons_layout.addWidget(self.btn_scr_2, 2, 2, 1, 1)
        self.btn_scr_2.setToolTip("Take Screenshot without subtitle")
        
        self.btn_scr_3 = QtWidgets.QPushButton(self)
        self.btn_scr_3.setText('3')
        self.btn_scr_3.clicked.connect(partial(self.execute_command, 'async screenshot window'))
        self.buttons_layout.addWidget(self.btn_scr_3, 2, 3, 1, 1)
        self.btn_scr_3.setToolTip("Take Screenshot with window")
        """
        self.btn_speed_half = QtWidgets.QPushButton(self)
        self.btn_speed_half.setText('0.5x')
        self.btn_speed_half.clicked.connect(partial(self.adjust_speed, '0.5'))
        self.buttons_layout.addWidget(self.btn_speed_half, 3, 0, 1, 1)
        self.btn_speed_half.setToolTip('Half Speed')
        
        self.btn_speed_reset = QtWidgets.QPushButton(self)
        self.btn_speed_reset.setText('1x')
        self.btn_speed_reset.clicked.connect(partial(self.adjust_speed, '1.0'))
        self.buttons_layout.addWidget(self.btn_speed_reset, 3, 1, 1, 1)
        self.btn_speed_reset.setToolTip('Original Speed')
        
        self.btn_speed_did = QtWidgets.QPushButton(self)
        self.btn_speed_did.setText('1.5x')
        self.btn_speed_did.clicked.connect(partial(self.adjust_speed, '1.5'))
        self.buttons_layout.addWidget(self.btn_speed_did, 3, 2, 1, 1)
        self.btn_speed_did.setToolTip('Multiply speed by 1.5')
        
        self.btn_speed_twice = QtWidgets.QPushButton(self)
        self.btn_speed_twice.setText('2x')
        self.btn_speed_twice.clicked.connect(partial(self.adjust_speed, '2.0'))
        self.buttons_layout.addWidget(self.btn_speed_twice, 3, 3, 1, 1)
        self.btn_speed_twice.setToolTip('Multiply speed by 2')
        """
        self.btn_sub_minus = QtWidgets.QPushButton(self)
        self.btn_sub_minus.setText('Sub-')
        self.btn_sub_minus.clicked.connect(partial(self.execute_command, 'add sub-delay -0.1'))
        self.buttons_layout.addWidget(self.btn_sub_minus, 4, 0, 1, 1)
        self.btn_sub_minus.setToolTip('Add Subtitle Delay of -0.1s')
        
        self.btn_sub_plus = QtWidgets.QPushButton(self)
        self.btn_sub_plus.setText('Sub+')
        self.btn_sub_plus.clicked.connect(partial(self.execute_command, 'add sub-delay +0.1'))
        self.buttons_layout.addWidget(self.btn_sub_plus, 4, 1, 1, 1)
        self.btn_sub_plus.setToolTip('Add Subtitle Delay of +0.1s')
        
        self.btn_aud_minus = QtWidgets.QPushButton(self)
        self.btn_aud_minus.setText('A-')
        self.btn_aud_minus.clicked.connect(partial(self.execute_command, 'add audio-delay -0.1'))
        self.buttons_layout.addWidget(self.btn_aud_minus, 4, 2, 1, 1)
        self.btn_aud_minus.setToolTip('Add Audio Delay of -0.1s')
        
        self.btn_aud_plus = QtWidgets.QPushButton(self)
        self.btn_aud_plus.setText('A+')
        self.btn_aud_plus.clicked.connect(partial(self.execute_command, 'add audio-delay +0.1'))
        self.buttons_layout.addWidget(self.btn_aud_plus, 4, 3, 1, 1)
        self.btn_aud_plus.setToolTip('Add Audio Delay of +0.1s')
        
        self.btn_chapter_minus = QtWidgets.QPushButton(self)
        self.btn_chapter_minus.setText('Chapter-')
        self.btn_chapter_minus.clicked.connect(partial(self.add_chapter, '-'))
        self.buttons_layout.addWidget(self.btn_chapter_minus, 5, 0, 1, 2)
        
        self.btn_chapter_plus = QtWidgets.QPushButton(self)
        self.btn_chapter_plus.setText('Chapter+')
        self.btn_chapter_plus.clicked.connect(partial(self.add_chapter, '+'))
        self.buttons_layout.addWidget(self.btn_chapter_plus, 5, 2, 1, 2)
        
        self.btn_show_stat = QtWidgets.QPushButton(self)
        self.btn_show_stat.setText('Show Stats')
        self.btn_show_stat.clicked.connect(partial(self.execute_command, 'script-binding stats/display-stats-toggle'))
        self.buttons_layout.addWidget(self.btn_show_stat, 6, 0, 1, 2)
        
        self.btn_external_sub = QtWidgets.QPushButton(self)
        self.btn_external_sub.setText('External Subtitle')
        self.btn_external_sub.clicked.connect(partial(self.execute_command, 'external-subtitle'))
        self.buttons_layout.addWidget(self.btn_external_sub, 6, 2, 1, 2)
        
        self.volume_layout = QtWidgets.QGridLayout(self)
        self.volume_layout.setObjectName('volume_layout')
        self.layout.insertLayout(3, self.volume_layout)
        
        self.volume_label = QtWidgets.QLabel(self)
        self.volume_label.setText('Volume')
        self.volume_layout.addWidget(self.volume_label, 0, 0, 1, 1)
        self.slider_volume = VolumeSlider(self, uiwidget, MainWindow)
        self.slider_volume.setObjectName("slider_volume")
        self.volume_layout.addWidget(self.slider_volume, 0, 1, 1, 3)
        self.volume_text = QtWidgets.QLineEdit(self)
        self.volume_text.returnPressed.connect(self.volume_entered)
        self.volume_layout.addWidget(self.volume_text, 0, 5, 1, 1)
        self.volume_text.setMaximumWidth(32)
        
        self.speed_value.setPlaceholderText('1.0')
        self.speed_value.setToolTip('Default Original Speed 1.0')
    
    def change_aspect(self, val):
        if val == '2.35:1':
            key = '3'
        elif val == 'disable':
            key = '4'
        elif val == '16:9':
            key = '1'
        elif val == '4:3':
            key = '2'
        else:
            key = '0'
        ui.tab_5.change_aspect_ratio(key=key)
    
    def execute_command(self, msg):
        if msg == 'external-subtitle':
            ui.tab_5.load_external_sub()
        else:
            msg = bytes('\n {} \n'.format(msg), 'utf-8')
            ui.mpvplayer_val.write(msg)
        
    def add_chapter(self, val):
        if val == '-':
            msg = bytes('\n add chapter -1 \n', 'utf-8')
        else:
            msg = bytes('\n add chapter 1 \n', 'utf-8')
        ui.mpvplayer_val.write(msg)
        
    def adjust_speed(self, val):
        msg = None
        if val == '1.0':
            msg = bytes('\n set speed 1.0 \n', 'utf-8')
        else:
            msg = bytes('\n multiply speed {} \n'.format(val), 'utf-8')
        if msg:
            ui.mpvplayer_val.write(msg)
            
    def volume_entered(self):
        txt = self.volume_text.text()
        self.volume_text.clear()
        if txt.isnumeric():
            self.slider_volume.setValue(int(txt))
        
    def gsbc_entered(self, label, slider):
        value = label.text()
        label.clear()
        try:
            if slider.objectName() == 'zoom':
                label.setPlaceholderText(value)
                value = float(value)*100
                slider.setValue(int(value))
            if slider.objectName() == 'speed':
                label.setPlaceholderText(value)
                value = float(value)*100 - 100
                slider.setValue(int(value))
            else:
                slider.setValue(int(value))
                label.setPlaceholderText(value)
        except Exception as err:
            logger.error(err)
            slider.setValue(0)
            label.setPlaceholderText('0')
