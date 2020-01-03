# -*- coding: utf-8 -*-

import sys
import os
import common
import xbmc
import xbmcgui

class SelectChannels(xbmcgui.WindowXMLDialog):

    def __init__(self, *args, **kwargs):
        try:
            xbmcgui.WindowXMLDialog.__init__(self)
            self.isRadio = kwargs.get("isradio")
            self.SkinPropery = kwargs.get("property")

            self.C_MAIN_HEADER=1
            self.C_MAIN_LIST1=3
            self.C_MAIN_LIST2=6
            self.C_MAIN_OK_BUTTON=5
            self.C_MAIN_CANCEL_BUTTON1=7
            self.C_MAIN_CANCEL_BUTTON2=99

        except Exception as e:
            common.dbg_log('SelectChannels::__init__', 'ERROR: (' + repr(e) + ')', common.logErorr)

    def onInit(self):
        try:
            try:
                self.ChannelList = self.getControl(self.C_MAIN_LIST2)
                self.getControl(self.C_MAIN_LIST1).setVisible(False)
            except:
                print_exc()
                self.ChannelList = self.getControl(self.C_MAIN_LIST1)

            self.getControl(self.C_MAIN_HEADER).setLabel(common.Lang(32000 + int(self.isRadio)))
            self.getControl(self.C_MAIN_CANCEL_BUTTON1).setLabel(common.Lang(32004))
            self.getControl(self.C_MAIN_OK_BUTTON).setVisible(False)

            lstItem = xbmcgui.ListItem(common.Lang(32002))
            lstItem.setLabel2(common.Lang(32003))
            lstItem.setIconImage('DefaultAddonNone.png')
            lstItem.setProperty('Thumbnail','')
            lstItem.setProperty('ChannelId','')
            lstItem.setProperty('Addon.Summary',common.Lang(32003))
            self.ChannelList.addItem(lstItem)

            channels_list = common.get_channels_json_response(self.isRadio)

            if 'result' in channels_list and 'channels' in channels_list['result'] and channels_list['result']['channels'] is not None:
                for item in channels_list['result']['channels']:
                    lstItem = xbmcgui.ListItem(item['label'])
                    if item['channeltype'] == 'tv':
                        lstItem.setLabel2(common.Lang(32005))
                    else:
                        lstItem.setLabel2(common.Lang(32006))
                    if item['thumbnail']:
                        lstItem.setIconImage(item['thumbnail'])
                        lstItem.setProperty('Thumbnail',item['thumbnail'])
                    else:
                        lstItem.setIconImage('DefaultTVShows.png')
                        lstItem.setProperty('Thumbnail','DefaultTVShows.png')
                    lstItem.setProperty('ChannelId',str(item['channelid']))
                    lstItem.setProperty('Addon.Summary',item['channeltype'])
                    self.ChannelList.addItem(lstItem)

            self.setFocus(self.ChannelList)

        except Exception as e:
            common.dbg_log('SelectChannels::onInit', 'ERROR: (' + repr(e) + ')', common.logErorr)

    def onAction(self, action):
        try:
            if action.getId() in (9, 10, 92, 216, 247, 257, 275, 61467, 61448,):
                self.close()
        except Exception as e:
            common.dbg_log('SelectChannels::onAction', 'ERROR: (' + repr(e) + ')', common.logErorr)

    def onClick(self, controlID):
        try:
            if controlID == self.C_MAIN_LIST1 or controlID == self.C_MAIN_LIST2:
                selectedPos = self.ChannelList.getSelectedPosition()
                if selectedPos > 0:
                    selectedItem = self.getControl(controlID).getSelectedItem()
                    strChannelName = selectedItem.getLabel()
                    strThumbnail = selectedItem.getProperty('Thumbnail')
                    strChannelId = selectedItem.getProperty('ChannelId')

                    xbmc.executebuiltin('Skin.SetString(%s,%s)' % ('%s.%s' % (self.SkinPropery, "ChannelId",), strChannelId,))
                    xbmc.executebuiltin('Skin.SetString(%s,%s)' % ('%s.%s' % (self.SkinPropery, "Label",), strChannelName,))
                    xbmc.executebuiltin('Skin.SetString(%s,%s)' % ('%s.%s' % (self.SkinPropery, "Icon",), strThumbnail,))
                    xbmc.sleep(300)
                    self.close()
                else:
                    xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % (self.SkinPropery, "ChannelId",))
                    xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % (self.SkinPropery, "Label",))
                    xbmc.executebuiltin('Skin.Reset(%s)' % '%s.%s' % (self.SkinPropery, "Icon",))
                    xbmc.sleep(300)
                    self.close()

            if controlID == self.C_MAIN_CANCEL_BUTTON1 or controlID == self.C_MAIN_CANCEL_BUTTON2:
                self.close()

        except Exception as e:
            common.dbg_log('SelectChannels::onClick', 'ERROR: (' + repr(e) + ')', common.logErorr)

    def onFocus(self, controlID):
        pass
