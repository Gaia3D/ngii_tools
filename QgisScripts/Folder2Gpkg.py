# -*- coding: utf-8 -*-

# standard imports
import sys, os, qgis.gui
# sys.path.append('D:\Source\\ngii_tools\QgisScripts')
from LayerList import LayerList

# import OGR
from osgeo import ogr, osr, gdal

from qgis.core import *

try:
    iface
except:
    import qgis.gui
    iface = qgis.gui.QgisInterface


CRS_ID = 5179
# FILE_DIR = "D:\Setup\NgiiData"
FILE_DIR = "D:\encode_shp"
OUT_FILE = r"D:\temp\ngii.gpkg"


def main():
    # 각 파일 포맷에 맞는 드라이버 초기화
    shpDriver = ogr.GetDriverByName("ESRI Shapefile")
    gpkgDriver = ogr.GetDriverByName("GPKG")

    # 좌표계 정보 생성
    crs = osr.SpatialReference()
    crs.ImportFromEPSG(CRS_ID)

    # clear canvas
    try:
        QgsMapLayerRegistry.instance().removeAllMapLayers()
    except:
        pass

    print("START")

    # 대상 파일 있다면 지우고
    if os.path.isfile(OUT_FILE):
        try:
            os.remove(OUT_FILE)
        except ZeroDivisionError as e:
            print(e)
            print("대상 파일이 사용중이어 중단됩니다.")
            return

    # 대상 파일 만들기
    gpkg = gpkgDriver.CreateDataSource(OUT_FILE)

    #폴더내의 .shp파일을 찾아서 gpkg에 추가
    file_list = os.listdir(FILE_DIR)
    for file_name in file_list:
        shp_nm = os.path.join(FILE_DIR, file_name)
        ext = os.path.splitext(shp_nm)[-1]
        if ext == '.shp':
            # 원본 파일 열기
            # shp = shpDriver.Open(shp_nm, 0)
            shp = gdal.OpenEx(shp_nm, gdal.OF_VECTOR, ["ESRI Shapefile"], ["ENCODING=UTF-8"])
            shpLayer = shp.GetLayer()

            # 원본 레이어 정보 얻기
            geomType = shpLayer.GetGeomType()
            layerDefinition = shpLayer.GetLayerDefn()

            # 원본 레이어와 동일하게 대상 레이어 만들기
            layer_nm = LayerList.getLayerNM(file_name.replace('.shp',''))['layerENM']
            gpkgLayer = gpkg.CreateLayer(layer_nm.encode('utf-8'), crs, geom_type=geomType)

            for i in range(layerDefinition.GetFieldCount()):
                fieldDefn = layerDefinition.GetFieldDefn(i)
                gpkgLayer.CreateField(fieldDefn)

            gpkgLayerDefn = gpkgLayer.GetLayerDefn()

            # 원본 레이어의 객체 돌며
            for shpFeature in shpLayer:
                # 동일한 대상 객체 생성
                gpkgFeature = ogr.Feature(gpkgLayerDefn)
                for i in range(gpkgLayerDefn.GetFieldCount()):
                    gpkgFeature.SetField(gpkgLayerDefn.GetFieldDefn(i).GetNameRef(), shpFeature.GetField(i))
                geom = shpFeature.GetGeometryRef()
                gpkgFeature.SetGeometry(geom)
                gpkgLayer.CreateFeature(gpkgFeature)

                # 진행상황 표시
                # print ".",

            # 다 읽은 원본은 처음으로 포인터 돌리기
            shpLayer.ResetReading()

            # 파일 다 닫기
            # shp.Destroy()
            print("COMPLETED")


        # 만들어진 GeoPackage를 QGIS에 불러오기
    gpkg.Destroy()
    gpkg_file = ogr.Open(OUT_FILE)

    # for layer in gpkg_file:
    for layer in gpkg_file:
        layerName = unicode(layer.GetName().decode('utf-8'))
        # print(layerName)
        try:
            uri = u"{}|layername={}".format(OUT_FILE, layerName)
            # print(uri)
            layer = iface.addVectorLayer(uri, None, "ogr")
        except ZeroDivisionError as e:
            print(e)
            layer = None

        if not layer:
            print u"Layer {} failed to load!".format(layerName)


###################
# RUN Main function
if __name__ == '__console__':
    main()

if __name__ == '__main__':
    main()