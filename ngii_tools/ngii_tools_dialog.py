# -*- coding: utf-8 -*-
"""
/***************************************************************************
NgiiToolsDialog
                                 A QGIS plugin
 shp2gpkg to QGIS
                             -------------------
        begin                : 2017-09-08
        git sha              : $Format:%H$
        copyright            : (C) 2017 by BJ Jang / Gaia3D
        email                : jangbi882@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtGui, uic
from qgis.core import *

import ConfigParser
import os

from QgisScriptss import Convert


# import OGR
from osgeo import ogr, gdal, osr
gdal.UseExceptions()

def force_gui_update():
    QgsApplication.processEvents(QEventLoop.ExcludeUserInputEvents)

def addTableItem(parent, layer_list):
    parent.setRowCount(len(layer_list))
    layerCnt = 0
    for layernm in layer_list :
        # 아이템 생성
        item_shp = QtGui.QTableWidgetItem(layernm.split("_")[0])
        item_chk = QtGui.QTableWidgetItem(u"√")
        # 수직 수평 가운데 정렬
        item_shp.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        item_chk.setTextAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        # 자바스크립트처럼 .연산자로 한번에 못씀. 폰트설정
        chk_font = QtGui.QFont()
        chk_font.setBold(True)
        item_chk.setFont(chk_font)
        parent.setItem(layerCnt, 0, item_shp )
        if layernm.find('_N') > 0:
            parent.setItem(layerCnt, 2, item_chk)
        elif layernm.find('_R') > 0:
            parent.setItem(layerCnt, 3, item_chk)
        elif layernm.find('_PE') > 0:
            parent.setItem(layerCnt, 4, item_chk)
        elif layernm.find('_GE') > 0:
            parent.setItem(layerCnt, 5, item_chk)
        elif layernm.find('_PGE') > 0:
            parent.setItem(layerCnt, 6, item_chk)
        else :
           parent.setItem(layerCnt, 1, item_chk)
        layerCnt = layerCnt+1

#ui 파일 로드
FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'ngii_tools_dialog_base.ui'))

#########################
# Define User Exception
#########################
class StoppedByUserException(Exception):
    def __init__(self, message = ""):
        # Call the base class constructor with the parameters it needs
        super(StoppedByUserException, self).__init__(message)

#########################
# MAIN CLASS
#########################
class NgiiToolsDialog(QtGui.QDialog, FORM_CLASS):
    # iface = None
    # shpPath = None
    # gpkgPath = None
    # layerCnt = None

    def __init__(self, iface, parent=None):
        """Constructor."""
        super(NgiiToolsDialog, self).__init__(parent)
        self.shpPath = os.path.join(QgsApplication.qgisSettingsDirPath())
        self.gpkgPath = os.path.join(QgsApplication.qgisSettingsDirPath())
        self.configFile = os.path.join(QgsApplication.qgisSettingsDirPath(), 'ngii_tools.ini')
        self.setupUi(self)
        self.iface = iface
        self._connect_action()
        self.readConfig()
        self.edtSrcFile.setFocus()
        self.order(u"변환할 SHP파일이 있는 폴더를 선택해주세요.")
        self.flag = False
        # 그리드 사이즈 조절
        self.tableLayer.resizeColumnsToContents()
        self.header = self.tableLayer.horizontalHeader()
        self.header.setResizeMode(0, QtGui.QHeaderView.Stretch)
        # self.btnStart.setEnabled(True)

    def tr(self, message):
        return QCoreApplication.translate('NgiiToolsDialog', message)

    def error(self, msg):
        self.editLog.clear()
        self.editLog.appendHtml(u'<font color="red"><b>{}</b></font>'.format(msg))

    def info(self, msg):
        if not self.enableInfo:
            return
        self.editLog.appendPlainText(msg)

    def debug(self, msg):
        if not self.enableDebug:
            return
        self.editLog.appendHtml(u'<font color="gray">{}</font>'.format(msg))

    def order(self, msg):
        self.editLog.clear()
        self.editLog.appendHtml(u'<font color="blue"><b>{}</b></font>'.format(msg))

    # 이벤트 연결
    def _connect_action(self):
        self.connect(self.btnSrcFile, SIGNAL("clicked()"), self._on_click_btnSrcFile)
        self.connect(self.btnTgtFile, SIGNAL("clicked()"), self._on_click_btnTgtFile)
        self.connect(self.btnStart, SIGNAL("clicked()"), self._on_click_btnStart)
        # self.connect(self.btnStop, SIGNAL("clicked()"), self._on_click_btnStop)

    # 설정값 저장
    def writeConfig(self):
        conf = ConfigParser.SafeConfigParser()
        conf.add_section('LastFile')
        conf.set("LastFile", "shp", self.shpPath)
        conf.set("LastFile", "gpkg", self.gpkgPath)
        fp = open(self.configFile, "w")
        conf.write(fp)
        fp.close()

    # 설정값 읽기
    def readConfig(self):
        try:
            conf = ConfigParser.SafeConfigParser()
            conf.read(self.configFile)
            conf.set("LastFile", "shp", os.path.dirname(__file__))
            conf.set("LastFile", "gpkg", os.path.dirname(__file__))
            try:
                self.shpPath = conf.get("LastFile", "shp")
            except ConfigParser.NoSectionError:
                self.shpPath = os.path.expanduser("~")
            try:
                self.gpkgPath = conf.get("LastFile", "gpkg")
            except ConfigParser.NoSectionError:
                self.gpkgPath = os.path.expanduser("~")
        except Exception as e:
            self.error(unicode(e))

    def _on_click_btnSrcFile(self):
        qfd = QFileDialog()
        title = self.tr("Open SHP folder")
        shpPath = os.path.dirname(self.shpPath)
        path = QFileDialog.getExistingDirectory(qfd, caption=title, directory=shpPath)
        self.tableLayer.clearContents()
        if not path:
            return
        self.shpPath = path
        self.edtSrcFile.setText(self.shpPath)
        self.writeConfig()

        # 선택한 디렉토리에서 shp 파일을 읽어 리스트로 보여준다.
        file_list = os.listdir(self.shpPath)
        shp_list = []
        for file_name in file_list:
            shp_nm = os.path.join(self.shpPath, file_name)
            ext = os.path.splitext(shp_nm)[-1]
            if ext == '.shp':
                shp_list.append(file_name.replace('.shp', ''))

        if len(shp_list) == 0:
            self.btnStart.setEnabled(False)
            self.error(u"변활할 SHP 파일이 없습니다. 다시 선택해주세요.")
            self.tableLayer.clearContents()
        else :
            if not self.flag:
                self.order(u"GPKG 파일을 저장할 폴더를 선택해주세요.")
            else:
                self.order(u"변환 시작 버튼을 선택해주세요.")
            self.layerCnt = len(shp_list)
            addTableItem(self.tableLayer, shp_list)
            self.btnStart.setEnabled(True)

    def _on_click_btnTgtFile(self):
        qfd = QFileDialog()
        title = self.tr("Open GPKG folder")
        gpkgPath = os.path.dirname(self.gpkgPath)
        path = QFileDialog.getExistingDirectory(qfd, caption=title, directory=gpkgPath)

        if not path:
            return
        self.gpkgPath = path
        self.edtTgtFile.setText(self.gpkgPath)
        self.writeConfig()
        self.btnStart.setEnabled(True)
        self.flag = True
        self.order(u"변환 시작 버튼을 선택해주세요.")

    def _on_click_btnStart(self):
        self.order(u"SHP 파일을 GPKG 파일로 변환을 시작합니다.")
        self.iface.newProject()
        force_gui_update()
        Convert.Shp2Gpkg(self, self.shpPath, self.gpkgPath + "\\ngii.gpkg", self.layerCnt).Folder2Gpkg()
        self.order(u"SHP 파일을 GPKG 파일로 변환이 완료되었습니다.")






