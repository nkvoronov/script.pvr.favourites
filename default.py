# -*- coding: utf-8 -*-

import sys
import os
import xbmc
import xbmcvfs
import xbmcaddon
sys.path.append(xbmcvfs.translatePath(os.path.join(xbmcaddon.Addon().getAddonInfo('path'), 'resources', 'lib')))
import action

if __name__ == '__main__':
    action.Main()