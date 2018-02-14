# -*- coding: utf-8 -*-

def getLayerNM(layerId):
    layer_list = {
        "ARB01000" : {
            "layerKNM" : "시도구역경계",
            "layerENM" : "ARB_SiDoAreaBoundary",
            "layerPNM" : "TN_CTPRVN_BNDRY"
        },
        "ARB02000" : {
            "layerKNM": "시군구구역경계",
            "layerENM": "ARB_SiGunGuAreaBoundary",
            "layerPNM": "TN_SIGNGU_BNDRY"
        },
        "ARB03000" : {
            "layerKNM": "읍면동구역경계",
            "layerENM": "ARB_EupMyeonDongAreaBoundary",
            "layerPNM": "TN_EMD_BNDRY"
        },
        "ARB04000" : {
            "layerKNM": "시설구역경계",
            "layerENM": "ARB_FacilityAreaBoundary",
            "layerPNM": "TN_FCLTY_ZONE_BNDRY"
        },
        "TRN01000" : {
             "layerKNM": "차도중심선",
             "layerENM": "TRN_RoadwayCenterLine",
             "layerPNM": "TN_RODWAY_CTLN"
        },
        "TRN02000" : {
            "layerKNM": "차도경계면",
            "layerENM": "TRN_RoadwayArea",
            "layerPNM": "TN_RODWAY_BNDRY"
        },
        "TRN03000" : {
            "layerKNM": "보도중심선",
            "layerENM": "TRN_SidewalkCenterline",
            "layerPNM": "TN_FTPTH_CTLN"
        },
        "TRN04000" : {
            "layerKNM": "보도경계면",
            "layerENM": "TRN_SidewalkArea",
            "layerPNM": "TN_FTPTH_BNDRY"
        },
        "TRN05000" : {
            "layerKNM": "자전거도로중심선",
            "layerENM": "TRN_BikewayCenterline",
            "layerPNM": "TN_BCYCL_CTLN"
        },
        "TRN06000" : {
            "layerKNM": "면형도로시설",
            "layerENM": "TRN_PolygonRoadFacility",
            "layerPNM": "TN_ARRFC"
        },
        "TRN07000" : {
            "layerKNM": "선형도로시설",
            "layerENM": "TRN_LineRoadFacility",
            "layerPNM": "TN_LNRFC"
        },
        "TRN08000" : {
            "layerKNM": "점형도로시설",
            "layerENM": "TRN_PointRoadFacility",
            "layerPNM": "TN_PTRFC"
        },
        "TRN09000" : {
            "layerKNM": "철도중심선",
            "layerENM": "TRN_RailroadCenterline",
            "layerPNM": "TN_RLROAD_CTLN"
        },
        "TRN10000" : {
            "layerKNM": "철도경계면",
            "layerENM": "TRN_RailroadArea",
            "layerPNM": "TN_RLROAD_BNDRY"
        },
        "TRN11000" : {
            "layerKNM": "면형철도시설",
            "layerENM": "TRN_PolygonRailFacility",
            "layerPNM": "TN_ARRFC"
        },
        "TRN12000" : {
            "layerKNM": "점형철도시설",
            "layerENM": "TRN_PointRailFacility",
            "layerPNM": "TN_PTRFC"
        },
        "TRN13000" : {
            "layerKNM": "면형공항시설",
            "layerENM": "TRN_PolygonAirportFacility",
            "layerPNM": "TN_ARAFC"
        },
        "TRN14000" : {
            "layerKNM": "선형공항시설",
            "layerENM": "TRN_LineAirportFacility",
            "layerPNM": "TN_LNAFC"
        },
        "TRN15000" : {
            "layerKNM": "점형공항시설",
            "layerENM": "TRN_PointAirportFacility",
            "layerPNM": "TN_PTAFC"
        },
        "TRN16000" : {
            "layerKNM": "면형항만시설",
            "layerENM": "TRN_PolygonPortFacility",
            "layerPNM": "TN_ARHFC"
        },
        "TRN17000" : {
            "layerKNM": "점형항만시설",
            "layerENM": "TRN_PointPortFacility",
            "layerPNM": "TN_PTHFC"
        },
        "BLD01000" : {
            "layerKNM": "건물",
            "layerENM": "BLD_Building",
            "layerPNM": "TN_BULD"
        },
        "BLD02000" : {
            "layerKNM": "건물부속시설",
            "layerENM": "BLD_BuildingAttachment",
            "layerPNM": "TN_BULD_ADCLS"
        },
        "BLD03000" : {
            "layerKNM": "면형구조시설",
            "layerENM": "BLD_PolygonStructure",
            "layerPNM": "TN_ARSFC"
        },
        "BLD04000" : {
            "layerKNM": "선형구조시설",
            "layerENM": "BLD_LineStructure",
            "layerPNM": "TN_LNSFC"
        },
        "BLD05000" : {
            "layerKNM": "점형구조시설",
            "layerENM": "BLD_PointStructure",
            "layerPNM": "TN_PTSFC"
        },
        "TPG01000" : {
            "layerKNM": "등고선",
            "layerENM": "TPG_Contour",
            "layerPNM": "TN_CTRLN"
        },
        "TPG02000" : {
            "layerKNM": "해안선",
            "layerENM": "TPG_Coastline",
            "layerPNM": "TN_SHORLINE"
        },
        "TPG03000" : {
            "layerKNM": "표고점",
            "layerENM": "TPG_ElevationPoint",
            "layerPNM": "TN_ALPT"
        },
        "TPG04000" : {
            "layerKNM": "면형지형",
            "layerENM": "TPG_PointTopography",
            "layerPNM": "TN_ARPGR"
        },
        "TPG05000" : {
            "layerKNM": "선형지형",
            "layerENM": "TPG_LineTopography",
            "layerPNM": "TN_LNPGR"
        },
        "TPG06000" : {
            "layerKNM": "점형지형",
            "layerENM": "TPG_PolygonTopography",
            "layerPNM": "TN_PTPGR"
        },
        "WTR01000" : {
            "layerKNM": "하천경계",
            "layerENM": "WTR_RiverArea",
            "layerPNM": "TN_RIVER_BNDRY"
        },
        "WTR02000" : {
            "layerKNM": "실폭하천",
            "layerENM": "WTR_ActualRiver",
            "layerPNM": "TN_RIVER_BT"
        },
        "WTR03000" : {
            "layerKNM": "하천중심선",
            "layerENM": "WTR_RiverCenterline",
            "layerPNM": "TN_RIVER_CTLN"
        },
        "WTR04000" : {
            "layerKNM": "호소",
            "layerENM": "WTR_Lake",
            "layerPNM": "TN_LKMH"
        },
        "WTR05000" : {
            "layerKNM": "수로시설",
            "layerENM": "WTR_WaterwayFacility",
            "layerPNM": "TN_WTCORS_FCLTY"
        },
        "VGT01000" : {
            "layerKNM": "경지경계",
            "layerENM": "VGT_ArableLandAreaBoundary",
            "layerPNM": "TN_FMLND_BNDRY"
        },
        "VGT02000" : {
            "layerKNM": "산지경계",
            "layerENM": "VGT_ForestAreaBoundary",
            "layerPNM": "TN_MTC_BNDRY"
        },
        "POI01000" : {
            "layerKNM": "관심지점",
            "layerENM": "POI_Name",
            "layerPNM": "TN_POI"
        },
        "GRD01000" : {
            "layerKNM": "통계격자",
            "layerENM": "GRD_StatisticsGrid",
            "layerPNM": "TN_STATS_GRID"
        },
        "GRF02000" : {
            "layerKNM": "도곽인덱스",
            "layerENM": "GRD_MapIndex",
            "layerPNM": "TN_MAPDMC_INDX"
        }
    }
    return layer_list[layerId]



#
# ###################
# # RUN Main function
# if __name__ == '__console__':
#     getLayerNM()
#
# if __name__ == '__main__':
#     print(getLayerNM('ARB01000')['layerKNM'])