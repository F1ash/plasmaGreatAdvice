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

class plasmaGreatAdvice(plasmascript.Applet):
	def __init__(self, parent = None):
		plasmascript.Applet.__init__(self, parent)

		self.kdehome = unicode(KGlobal.dirs().localkdedir()) + \
						'share/apps/plasma/plasmoids/plasmaGreatAdvice/contents/'
		self.Settings = QSettings('plasmaGreatAdvice', 'plasmaGreatAdvice')
		self.timeout = self.Settings.value('TimeOut', QVariant(10)).toInt()[0]

		self.adviceIcon = Plasma.IconWidget()
		if os.path.exists(self.kdehome + 'icons/advice.png') :
			self.adviceIcon.setIcon(self.kdehome + 'icons/advice.png')
		else :
			self.adviceIcon.setIcon(os.getcwd() + '/plasmaGreatAdvice/contents/icons/advice.png')
		self.adviceIcon.clicked.connect(self.show_n_hide)

	def init(self):
		self.layout = QGraphicsLinearLayout(self.applet)
		self.layout.setSpacing(0)
		self.layout.addItem(self.adviceIcon)

		self.setLayout(self.layout)

		self.setHasConfigurationInterface(True)

		self.Timer = QTimer()
		self.Timer.timeout.connect(self.showAdvice)
		self.Timer.start(self.timeout * 1000)

	def getNewText(self):
		fileName = randomString(24)
		Data = QStringList()
		if os.path.exists(self.kdehome + 'code/getText.sh') :
			Data.append(self.kdehome + 'code/getText.sh')
		else :
			Data.append(os.getcwd() + '/plasmaGreatAdvice/contents/code/getText.sh')
		Data.append(fileName)
		getAdsviceThread = QProcess()
		start = getAdsviceThread.startDetached('/bin/sh', Data)
		return fileName, start

	def showAdvice(self):
		if 'Control' in dir(self) : self.Control.close()
		fileName, start = self.getNewText()
		if start :
			time.sleep(3)
			try :
				with open("/dev/shm/" + fileName, 'rb') as f :
					data = f.read()
			except :
				data = 'error'
			self.Control = ControlWidget(QString().fromUtf8(data), self)
			self.Control.show()
			os.remove("/dev/shm/" + fileName)

	def show_n_hide(self):
		if 'Control' not in dir(self): return None
		if self.Control.isVisible() :
			self.Control.hide()
		else:
			#self.Control.move(self.popupPosition(self.Control.size()))
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
		self.timeout = self.Settings.value('TimeOut', QVariant(10)).toInt()[0]
		self.Timer.start(self.timeout * 1000)
		self.dialog.done(0)

	def configDenied(self):
		self.dialog.done(0)

	def __del__(self):
		self.Timer.stop()
		if 'Control' in dir(self) : self.Control.close()

class ControlWidget(Plasma.Dialog):
	def __init__(self, data, obj, parent = None):
		Plasma.Dialog.__init__(self, parent)
		
		self.layout = QGridLayout()

		self.advice = QLabel('<font color=red size=7><b>' + data + '</b></font>')
		self.layout.addWidget(self.advice, 0, 0)

		self.setLayout(self.layout)

class AppletSettings(QWidget):
	def __init__(self, obj = None, parent= None):
		QWidget.__init__(self, parent)

		self.prnt = parent
		self.Settings = obj.Settings

		timeOut = self.Settings.value('TimeOut', 10).toInt()[0]

		self.layout = QGridLayout()

		self.timeOutLabel = QLabel("Timeout checking (sec.):")
		self.layout.addWidget(self.timeOutLabel,0,0)
		self.timeOutBox = KIntSpinBox(10, 7200, 1, timeOut, self)
		self.timeOutBox.setMaximumWidth(75)
		self.layout.addWidget(self.timeOutBox, 0, 5)

		self.setLayout(self.layout)

	def refreshSettings(self, parent = None):
		self.Settings.setValue('TimeOut', str(self.timeOutBox.value()))
		self.Settings.sync()

	def eventClose(self, event):
		self.prnt.done(0)

def CreateApplet(parent):
	return plasmaGreatAdvice(parent)
