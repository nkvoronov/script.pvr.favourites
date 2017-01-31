# -*- coding: utf-8 -*-

import os
import sys
import xbmc
import xbmcaddon
import xbmcgui

if sys.version_info < (2, 7):
    import simplejson
else:
    import json as simplejson

__author__ = 'YLLOW_DRAGON'
__scriptname__ = 'PVR favourites'
__scriptid__ = 'script.pvr.favourites'
__addon__ = xbmcaddon.Addon(__scriptid__)
__cwd__ = __addon__.getAddonInfo('path')
__common__ = sys.modules[globals()['__name__']]
__resources__ = xbmc.translatePath(os.path.join(__cwd__, 'resources'))
__resources_lib__ = xbmc.translatePath(os.path.join(__resources__, 'lib'))

debug = 'true'
logErorr = xbmc.LOGERROR

sys.path.append(__resources_lib__)

reload(sys)
sys.setdefaultencoding('utf-8')

def Lang(vcode):
    return __addon__.getLocalizedString(vcode)

def dbg_log(vsource, vtext, vlevel=xbmc.LOGNOTICE):
    if debug == 'false':
        return
    xbmc.log('## '+__scriptname__+' ## ' + vsource + ' ## ' + vtext, vlevel)

def json_response(vJsonQuery):
    json_query = xbmc.executeJSONRPC(vJsonQuery)
    json_query = unicode(json_query, 'utf-8', errors='ignore')
    return simplejson.loads(json_query)

def get_channels_json_response(vIsRadio):
    if str(vIsRadio) == '0':
        JsonQuery = '{ "jsonrpc": "2.0", "id": 0, "method": "PVR.GetChannels", "params": { "channelgroupid": "alltv", "properties": [ "thumbnail", "channeltype", "hidden", "locked",  "lastplayed" ] } }'
    else:
        JsonQuery = '{ "jsonrpc": "2.0", "id": 0, "method": "PVR.GetChannels", "params": { "channelgroupid": "allradio", "properties": [ "thumbnail", "channeltype", "hidden", "locked",  "lastplayed" ] } }'
    return json_response(JsonQuery)

def get_channel_details_json_response(vChannelID):
    JsonQuery = '{ "jsonrpc": "2.0", "id": 0, "method": "PVR.GetChannelDetails", "params": { "channelid": ' + vChannelID + ', "properties" : [ "broadcastnow" ] } }'
    return json_response(JsonQuery) 