# -*- coding: utf-8 -*-

# standard imports
import os
from Layer import LayerList
# import OGR
from osgeo import ogr, osr, gdal

from qgis.core import *

class Shp2Gpkg :

    def __init__(self, parent, file_dir, out_dir, cnt):
        self.file_dir = file_dir
        self.out_dir = out_dir
        self.crs_id = 5179
        self.iface = parent.iface
        self.parent = parent
        self.shpCnt = cnt

    def Folder2Gpkg(self):
        # 각 파일 포맷에 맞는 드라이버 초기화
        # shpDriver = ogr.GetDriverByName("ESRI Shapefile")
        gpkgDriver = ogr.GetDriverByName("GPKG")

        # 좌표계 정보 생성
        crs = osr.SpatialReference()
        crs.ImportFromEPSG(self.crs_id)

        # clear canvas
        # try:
        #     QgsMapLayerRegistry.instance().removeAllMapLayers()
        # except ZeroDivisionError as e:
        #     print(e)
        #     pass
        # print("START")

        # 대상 파일 있다면 지우고
        if os.path.isfile(self.out_dir):
            try:
                os.remove(self.out_dir)
            except ZeroDivisionError as e:
                print(e)
                print("대상 파일이 사용중이어 중단됩니다.")
                return

        # 대상 파일 만들기
        gpkg = gpkgDriver.CreateDataSource(self.out_dir)

        # 폴더내의 .shp파일을 찾아서 gpkg에 추가
        file_list = os.listdir(self.file_dir)
        crridx = 0
        self.parent.progressMainWork.setMinimum(0)
        self.parent.progressMainWork.setMaximum(self.shpCnt)
        for file_name in file_list:
            shp_nm = os.path.join(self.file_dir, file_name)
            ext = os.path.splitext(shp_nm)[-1]
            if ext == '.shp':
                # 원본 파일 열기
                # shp = shpDriver.Open(shp_nm, 0)
                crridx = crridx+1
                self.parent.progressMainWork.setValue(crridx)
                shp = gdal.OpenEx(shp_nm, gdal.OF_VECTOR, ["ESRI Shapefile"], ["ENCODING=UTF-8"])
                shpLayer = shp.GetLayer()
                layer_nm = self.getFileNM(file_name.replace('.shp', ''))
                if len(shpLayer) > 0 and layer_nm is not None:
                    # 원본 레이어 정보 얻기
                    geomType = shpLayer.GetGeomType()
                    layerDefinition = shpLayer.GetLayerDefn()

                    # 원본 레이어와 동일하게 대상 레이어 만들기
                    # layer_nm = self.getFileNM(file_name.replace('.shp', ''))
                    gpkgLayer = gpkg.CreateLayer(layer_nm.encode('utf-8'), crs, geom_type=geomType)
                    # self.parent.editLog.appendHtml(layer_nm)
                    for i in range(layerDefinition.GetFieldCount()):
                        fieldDefn = layerDefinition.GetFieldDefn(i)
                        gpkgLayer.CreateField(fieldDefn)

                    gpkgLayerDefn = gpkgLayer.GetLayerDefn()
                    shpCnt = len(shpLayer)
                    layerIdx = 0
                    self.parent.progressSubWork.setMinimum(0)
                    self.parent.progressSubWork.setMaximum(shpCnt)
                    # 원본 레이어의 객체 돌며
                    for shpFeature in shpLayer:
                        # 동일한 대상 객체 생성
                        gpkgFeature = ogr.Feature(gpkgLayerDefn)
                        for i in range(gpkgLayerDefn.GetFieldCount()):
                            gpkgFeature.SetField(gpkgLayerDefn.GetFieldDefn(i).GetNameRef(), shpFeature.GetField(i))
                        geom = shpFeature.GetGeometryRef()
                        gpkgFeature.SetGeometry(geom)
                        gpkgLayer.CreateFeature(gpkgFeature)
                        layerIdx = layerIdx+1
                        self.parent.progressSubWork.setValue(layerIdx)

                # 다 읽은 원본은 처음으로 포인터 돌리기
                shpLayer.ResetReading()

                # 파일 다 닫기
                # shp.Destroy()
                # print("COMPLETED")

            # 만들어진 GeoPackage를 QGIS에 불러오기
        gpkg.Destroy()
        gpkg_file = ogr.Open(self.out_dir)

        # for layer in gpkg_file:
        for layer in gpkg_file:
            layerName = unicode(layer.GetName().decode('utf-8'))
            # print(layerName)
            try:
                uri = u"{}|layername={}".format(self.out_dir, layerName)
                # print(uri)
                layer = self.iface.addVectorLayer(uri, None, "ogr")
            except ZeroDivisionError as e:
                print(e)
                layer = None

            if not layer:
                print u"Layer {} failed to load!".format(layerName)

    def getFileNM(self, layerid):
        layerKey = layerid.split("_")
        layerKey = LayerList(layerKey[0]).getLayerNM()
        if layerKey is not None:
            if layerid.find('_N') > 0:
                layerNm = layerKey.getLayerNM()['layerENM']+'_N'
            elif layerid.find('_R') > 0:
                layerNm = layerKey.getLayerNM()['layerENM'] + '_R'
            elif layerid.find('_PE') > 0:
                layerNm = layerKey.getLayerNM()['layerENM'] + '_PE'
            elif layerid.find('_GE') > 0:
                layerNm = layerKey.getLayerNM()['layerENM'] + '_GE'
            elif layerid.find('_PGE') > 0:
                layerNm = layerKey.getLayerNM()['layerENM'] + '_PGE'
            else:
                layerNm = layerKey['layerENM']
        else:
            layerNm = None
        return layerNm

