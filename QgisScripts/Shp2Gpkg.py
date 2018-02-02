# -*- coding: utf-8 -*-

# standard imports
import sys, os

# import OGR
from osgeo import ogr, gdal, osr

from qgis.core import *
try:
    iface
except:
    import qgis.gui
    iface = qgis.gui.QgisInterface

CRS_ID = 5179
SRC_FILE = r"C:\Temp\GpkgSample\BLD01000.shp"
OUT_FILE = r"C:\Temp\GpkgSample\ngii8.gpkg"
LAYER_NAME = "BLD_Building"


def main():
    os.environ['SHAPE_ENCODING'] = "CP949"
    gdal.SetConfigOption("SHAPE_ENCODING", "CP949")
    gdal.SetConfigOption("ENCODING", "CP949")

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
        except:
            print(u"대상 파일이 사용중이어 중단됩니다.")
            return

    # 대상 파일 만들기
    gpkg = gpkgDriver.CreateDataSource(OUT_FILE)


    # 원본 파일 열기
    # shp = shpDriver.Open(SRC_FILE, 0)
    # shp = gdal.OpenEx(SRC_FILE, gdal.OF_VECTOR)
    shp = gdal.OpenEx(SRC_FILE, gdal.OF_VECTOR, ["ESRI Shapefile"], ["SHAPE_ENCODING=CP949","ENCODING=CP949"])
    shpLayer = shp.GetLayer()

    # 원본 레이어 정보 얻기
    geomType = shpLayer.GetGeomType()
    layerDefinition = shpLayer.GetLayerDefn()

    # 원본 레이어와 동일하게 대상 레이어 만들기
    gpkgLayer = gpkg.CreateLayer(LAYER_NAME.encode('utf-8'), crs, geom_type=geomType)

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
        print ".",

    # 다 읽은 원본은 처음으로 포인터 돌리기
    shpLayer.ResetReading()

    # 파일 다 닫기
    # shp.Destroy()
    gpkg.Destroy()


    # 만들어진 GeoPackage를 QGIS에 불러오기
    gpkg = ogr.Open(OUT_FILE)

    for layer in gpkg:
        for layer in gpkg:
            layerName = unicode(layer.GetName().decode('utf-8'))

            try:
                uri = u"{}|layername={}".format(OUT_FILE, layerName)
                layer = iface.addVectorLayer(uri, None, "ogr")
                try:
                    layer.setName(layerName)
                except:
                    layer.setLayerName(layerName)
            except:
                layer = None

            if not layer:
                print u"Layer {} failed to load!".format(layerName)


    print("COMPLETED")

###################
# RUN Main function
if __name__ == '__console__':
    main()

if __name__ == '__main__':
    main()