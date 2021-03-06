# -*- coding: utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyKDE4.kdecore import KGlobal
from PyKDE4.kdeui import KPageDialog, KDialog, KIntSpinBox
from PyKDE4.plasma import Plasma
from PyKDE4 import plasmascript
import os.path, os, string, random, time

char_set = string.ascii_letters + string.digits

def randomString(j = 1):
	return ''.join(random.sample(char_set, j))

def pid_exists(pid, sig):
	try:
		os.kill(pid, sig)
		return True
	except OSError, err:
		return False

class plasmaGreatAdvice(plasmascript.Applet):
	def __init__(self, parent = None):
		plasmascript.Applet.__init__(self, parent)

		self.kdehome = '/usr/share/kde4/apps/plasma/plasmoids/kde-plasma-motivator/contents/'
		self.Settings = QSettings('kde-plasma-motivator', 'kde-plasma-motivator')
		self.initVar()

		if os.path.exists(self.kdehome + 'icons/advice.png') :
			self.iconPath = self.kdehome + 'icons/advice.png'
		else :
			self.iconPath = os.getcwd() + '/kde-plasma-motivator/contents/icons/advice.png'

	def initVar(self):
		self.timeout = self.Settings.value('TimeOut', 300).toInt()[0]
		self.autoclose = self.Settings.value('AutoClose', 3).toInt()[0]
		self.popup = self.Settings.value('PopUp', 1).toInt()[0]
		self.iconText = self.Settings.value('IconText', 1).toInt()[0]
		self.popupColor = self.Settings.value('PopUpColor', 'red').toString()
		self.iconTextColor = self.Settings.value('IconTextColor', 'blue').toString()

	def initLayout(self):
		if 'layout' in dir(self) :
			count = self.layout.count()
			for i in xrange(count) :
				item = self.layout.itemAt(count -1 - i)
				self.layout.removeAt(count -1 - i)
				item = None
		self.adviceIcon = Plasma.IconWidget()
		self.adviceIcon.setIcon(self.iconPath)
		if bool(self.popup) : self.adviceIcon.clicked.connect(self.show_n_hide)
		if self.applet.formFactor() == Plasma.Horizontal :
			self.adviceIcon.setOrientation(Qt.Horizontal)
			self.layout.setOrientation(Qt.Horizontal)
			self.layout.addItem(self.adviceIcon)
		else :
			self.adviceIcon.setOrientation(Qt.Vertical)
			self.layout.setOrientation(Qt.Vertical)
			if bool(self.popup) : self.layout.addItem(self.adviceIcon)
			if bool(self.iconText) :
				self.adviceLabel = Plasma.Label()
				self.adviceLabel.setScaledContents(True)
				self.adviceLabel.setAlignment(Qt.AlignCenter)
				self.layout.addItem(self.adviceLabel)
		self.adviceIcon.setTextBackgroundColor(QColor(self.iconTextColor))

		self.layout.setAlignment(self.adviceIcon, Qt.AlignLeft)
		self.setLayout(self.layout)

	def init(self):
		self.layout = QGraphicsLinearLayout(self.applet)
		self.layout.setSpacing(0)
		self.initLayout()
		self.setHasConfigurationInterface(True)

		Plasma.ToolTipManager.self().setContent( \
				self.applet, \
				Plasma.ToolTipContent( \
								'Great Advice\nMotivator', \
								QString(''), \
								QIcon(self.iconPath) ) )

		self.onceTimer = QTimer()
		self.onceTimer.timeout.connect(self.showAdvice)
		self.onceTimer.setSingleShot(True)
		self.onceTimer.start()
		self.Timer = QTimer()
		self.Timer.timeout.connect(self.showAdvice)
		self.Timer.start(self.timeout * 1000)

	def getNewText(self):
		fileName = randomString(24)
		Data = QStringList()
		if os.path.exists(self.kdehome + 'code/getText.sh') :
			Data.append(self.kdehome + 'code/getText.sh')
		else :
			Data.append(os.getcwd() + '/kde-plasma-motivator/contents/code/getText.sh')
		Data.append(fileName)
		getAdsviceThread = QProcess()
		start, pid = getAdsviceThread.startDetached('/bin/sh', Data, os.getcwd())
		return fileName, start, pid

	def preparedData(self):
		if 'Control' in dir(self) : self.Control.close()
		fileName, start, pid = self.getNewText()
		if start :
			i = 0
			while pid_exists(pid, 0):
				time.sleep(0.1)
				i += 1
				''' inhibits connect '''
				if i > 100 : pid_exists(pid, 9)
			if os.path.exists("/dev/shm/" + fileName) :
				with open("/dev/shm/" + fileName, 'rb') as f :
					data = f.read()
				os.remove("/dev/shm/" + fileName)
				""" text is absent, may be no connect """
				if data == '' : data = 'Проверь коннект, ёпта! (Авт.)'
				""" brocken text, may be low connect """
				if data.startswith('<span class=') : data = 'Смени блять провайдера! (Авт.)'
			else :
				data = 'WARNING: Getting Advice Error'
		else :
			data = 'WARNING: Bad command for getting Advice'
		return data

	def showAdvice(self):
		data = self.preparedData()
		#print data
		text = QString().fromUtf8(data)
		if bool(self.popup) :
			self.adviceIcon.setIcon(self.iconPath)
			self.Control = ControlWidget(text, self.autoclose, self, self.popupColor)
			self.Control.show()
		elif not bool(self.popup) and not bool(self.iconText) :
			self.adviceIcon.setIcon(self.iconPath)
		else :
			self.adviceIcon.setIcon('')
		if self.applet.formFactor() == Plasma.Horizontal :
			if bool(self.iconText) :
				self.adviceIcon.setText(text)
			else:
				self.adviceIcon.setText('')
		else :
			if bool(self.iconText) :
				text__ = str(data).replace(',', ', ')
				text_ = text__.replace('  ', ' ')
				text = QString().fromUtf8(text_.replace(' ', '\n'))
				self.adviceLabel.setText(text)
			else:
				pass

	def show_n_hide(self):
		if 'Control' not in dir(self): return None
		if self.Control.isVisible() :
			self.Control.hide()
		else:
			self.Control.move(self.popupPosition(self.Control.size()))
			self.Control.show()

	def createConfigurationInterface(self, parent):
		self.appletSettings = AppletSettings(self, parent)
		parent.addPage(self.appletSettings, "Settings")
		self.connect(parent, SIGNAL("okClicked()"), self.configAccepted)
		self.connect(parent, SIGNAL("cancelClicked()"), self.configDenied)

	def showConfigurationInterface(self):
		self.dialog = KPageDialog()
		self.dialog.setModal(True)
		self.dialog.setFaceType(KPageDialog.List)
		self.dialog.setButtons( KDialog.ButtonCode(KDialog.Ok | KDialog.Cancel) )
		self.createConfigurationInterface(self.dialog)
		self.dialog.move(self.popupPosition(self.dialog.sizeHint()))
		self.dialog.exec_()

	def configAccepted(self):
		self.Timer.stop()
		self.appletSettings.refreshSettings(self)
		self.initVar()
		self.initLayout()
		self.Timer.start(self.timeout * 1000)
		self.dialog.done(0)

	def configDenied(self):
		self.dialog.done(0)

	def __del__(self):
		self.Timer.stop()
		if 'Control' in dir(self) : self.Control.close()

class ControlWidget(Plasma.Dialog):
	def __init__(self, data, autoClose, obj, color, parent = None):
		Plasma.Dialog.__init__(self, parent)
		
		self.layout = QGridLayout()

		self.advice = QLabel('<font color=' + color + ' size=7><b>' + data + '</b></font>')
		self.layout.addWidget(self.advice, 0, 0)

		self.setLayout(self.layout)

		self.timer = QTimer()
		self.timer.setSingleShot(True)
		self.timer.timeout.connect(self.hide)
		self.timer.start(autoClose * 1000)

class AppletSettings(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.prnt = parent
		self.Settings = obj.Settings
		colorNames = QColor().colorNames()

		timeOut = self.Settings.value('TimeOut', 300).toInt()[0]
		autoClose = self.Settings.value('AutoClose', 3).toInt()[0]
		popup = self.Settings.value('PopUp', 1).toInt()[0]
		iconText = self.Settings.value('IconText', 1).toInt()[0]
		popupColor = self.Settings.value('PopUpColor', 'red').toString()
		iconTextColor = self.Settings.value('IconTextColor', 'blue').toString()

		self.layout = QGridLayout()

		self.timeOutLabel = QLabel("Timeout checking (sec.):")
		self.layout.addWidget(self.timeOutLabel, 0, 0)
		self.timeOutBox = KIntSpinBox(10, 7200, 1, timeOut, self)
		self.timeOutBox.setMaximumWidth(75)
		self.layout.addWidget(self.timeOutBox, 0, 5)

		self.autoCloseLabel = QLabel("Advice auto close (sec.):")
		self.layout.addWidget(self.autoCloseLabel, 1, 0)
		self.autoCloseBox = KIntSpinBox(1, 7200, 1, autoClose, self)
		self.autoCloseBox.setMaximumWidth(75)
		self.layout.addWidget(self.autoCloseBox, 1, 5)

		self.popupLabel = QLabel("Show pop-up advice:")
		self.layout.addWidget(self.popupLabel, 2, 0)
		self.popupBox = QCheckBox()
		if popup == 0 :
			self.popupBox.setCheckState(Qt.Unchecked)
		else :
			self.popupBox.setCheckState(Qt.Checked)
		self.popupBox.setMaximumWidth(75)
		self.layout.addWidget(self.popupBox, 2, 5)

		self.popupColorLabel = QLabel("Pop-up color:")
		self.layout.addWidget(self.popupColorLabel, 3, 0)
		self.popupColorBox = QComboBox()
		self.popupColorBox.setMaximumWidth(150)
		self.popupColorBox.addItems(colorNames)
		self.popupColorBox.setCurrentIndex(self.popupColorBox.findText(popupColor))
		self.layout.addWidget(self.popupColorBox, 3, 5)

		self.iconTextLabel = QLabel("Show advice in Icon:")
		self.layout.addWidget(self.iconTextLabel, 4, 0)
		self.iconTextBox = QCheckBox()
		if iconText == 0 :
			self.iconTextBox.setCheckState(Qt.Unchecked)
		else :
			self.iconTextBox.setCheckState(Qt.Checked)
		self.iconTextBox.setMaximumWidth(75)
		self.layout.addWidget(self.iconTextBox, 4, 5)

		self.iconTextColorLabel = QLabel("IconText color:")
		self.layout.addWidget(self.iconTextColorLabel, 5, 0)
		self.iconTextColorBox = QComboBox()
		self.iconTextColorBox.setMaximumWidth(150)
		self.iconTextColorBox.addItems(colorNames)
		self.iconTextColorBox.setCurrentIndex(self.iconTextColorBox.findText(iconTextColor))
		self.layout.addWidget(self.iconTextColorBox, 5, 5)

		self.setLayout(self.layout)

	def refreshSettings(self, parent = None):
		self.Settings.setValue('TimeOut', str(self.timeOutBox.value()))
		self.Settings.setValue('AutoClose', str(self.autoCloseBox.value()))
		self.Settings.setValue('PopUp', self.popupBox.checkState()/2)
		self.Settings.setValue('IconText', self.iconTextBox.checkState()/2)
		self.Settings.setValue('PopUpColor', self.popupColorBox.currentText())
		self.Settings.setValue('IconTextColor', self.iconTextColorBox.currentText())
		self.Settings.sync()

	def eventClose(self, event):
		self.prnt.done(0)

def CreateApplet(parent):
	return plasmaGreatAdvice(parent)
