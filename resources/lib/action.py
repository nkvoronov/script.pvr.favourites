# -*- coding: utf-8 -*-

import sys
import os
import xbmc
import xbmcgui
import xbmcaddon
import xbmcvfs
from datetime import datetime
import time
from xml.dom.minidom import parse
import gui
import common

class Main:
    def __init__(self):
        try:
            self._parse_argv()
            if self.ACTION == 'select':
                ShowDialog(self.ISRADIO, self.PROPERTY)
            elif self.ACTION == 'play':
                self._play_channels(self.CHANNELID)
            else:
                found, settings = self._read_file()
                self._set_properties(settings)
        except Exception, e:
            common.dbg_log('Main::__init__', 'ERROR: (' + repr(e) + ')', common.logErorr)

    def _parse_argv(self):
        try:
            try:
                params = dict(arg.split("=") for arg in sys.argv[ 1 ].split("&"))
            except:
                params = {}
            self.ACTION = params.get("action", "")
            self.PROPERTY = params.get("property", "")
            self.ISRADIO = params.get("isradio", 0)
            self.CHANNELID = params.get("channelid", 0)
        except Exception, e:
            common.dbg_log('Main::_parse_argv', 'ERROR: (' + repr(e) + ')', common.logErorr)

    def _read_file(self):
        try:
            self.settings_file = xbmc.translatePath('special://profile/addon_data/'+xbmc.getSkinDir()+'/settings.xml').decode("utf-8")
            if xbmcvfs.exists(self.settings_file):
                found = True
                self.doc = parse(self.settings_file)
                settings = self.doc.documentElement.getElementsByTagName('setting')
            else:
                found = False
                settings = []
            return found, settings
        except Exception, e:
            common.dbg_log('Main::_read_file', 'ERROR: (' + repr(e) + ')', common.logErorr)

    def _play_channels(self, vChannelID):
        try:
             xbmc.executeJSONRPC('{ "jsonrpc": "2.0", "id": 0, "method": "Player.Open", "params": { "item": { "channelid": ' + vChannelID + ' } } }')
        except Exception, e:
            common.dbg_log('Main::_play_channels', 'ERROR: (' + repr(e) + ')', common.logErorr)

    def _get_strTime(self, vDTstr):
        try:
            try:
                utcDate = datetime.strptime(vDTstr, '%Y-%m-%d %H:%M:%S')
            except TypeError:
                utcDate = datetime(*(time.strptime(vDTstr, '%Y-%m-%d %H:%M:%S')[0:6]))

            epoch = time.mktime(utcDate.timetuple())
            offset = datetime.fromtimestamp(epoch) - datetime.utcfromtimestamp(epoch)

            localDate = utcDate + offset

            timeStr = localDate.strftime('%H:%M')
            if timeStr[0] == '0':
                timeStr = timeStr[1:]
            return timeStr
        except Exception, e:
            common.dbg_log('Main::_get_strTime', 'ERROR: (' + repr(e) + ')', common.logErorr)

    def _set_properties(self, listing):
        try:
            self.WINDOW = xbmcgui.Window(10000)
            for count, setting in enumerate(listing):
                name = setting.attributes[ 'id' ].nodeValue
                aname = name.split('.')
                try:
                    value = setting.childNodes [ 0 ].nodeValue
                except:
                    value = ""
                if name.startswith('Channel') and name.endswith('.ChannelId') and value:
                    strTitle = ''
                    strStartTime = xbmc.getInfoLabel('System.Time(h:mm)')
                    strEndTime = xbmc.getInfoLabel('System.Time(h:mm)')

                    channel_details = common.get_channel_details_json_response(value)

                    if channel_details.has_key('result') and channel_details['result'].has_key('channeldetails') and channel_details['result']['channeldetails'].has_key('broadcastnow') and channel_details['result']['channeldetails']['broadcastnow'] is not None:
                        strTitle = channel_details['result']['channeldetails']['broadcastnow']['title']
                        strStartTime = self._get_strTime(channel_details['result']['channeldetails']['broadcastnow']['starttime'])
                        strEndTime = self._get_strTime(channel_details['result']['channeldetails']['broadcastnow']['endtime'])

                    self.WINDOW.setProperty(aname[0]+'.'+aname[1]+'.StartTime' , strStartTime)
                    self.WINDOW.setProperty(aname[0]+'.'+aname[1]+'.EndTime' , strEndTime)
                    self.WINDOW.setProperty(aname[0]+'.'+aname[1]+'.Title' , strTitle)
        except Exception, e:
            common.dbg_log('Main::_set_properties', 'ERROR: (' + repr(e) + ')', common.logErorr)

def ShowDialog(vRadio, vProperty):
    try:
        dlg = gui.SelectChannels('DialogSelect.xml',xbmcaddon.Addon().getAddonInfo('path').decode('utf-8'), isradio=vRadio, property=vProperty)
        dlg.doModal()
        del dlg
    except Exception, e:
        common.dbg_log('ShowDialog', 'ERROR: (' + repr(e) + ')', common.logErorr)
