# -*- coding: utf-8 -*-
"""
/***************************************************************************
 ngii_tools
                                 A QGIS plugin
 shp2gpkg to QGIS
                             -------------------
        begin                : 2017-09-08
        copyright            : (C) 2017 by BJ Jang / Gaia3D
        email                : jangbi882@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load OnMapLoader class from file OnMapLoader.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .ngii_tools import NgiiTools
    return NgiiTools(iface)
