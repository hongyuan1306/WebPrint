import asyncio
import threading
from autobahn.asyncio.websocket import WebSocketServerFactory

import wx
import wx.aui
import wx.adv

from .utils import enumeratePrinters
from .printerpanel import PrinterPanel
from .server import MyServerProtocol


class AppTaskBarIcon(wx.adv.TaskBarIcon):
    def __init__(self, frame):
        wx.adv.TaskBarIcon.__init__(self)

        icon = wx.Icon('./webprint.ico', wx.BITMAP_TYPE_ICO)
        self.SetIcon(icon, 'WebPrint')
        self.frame = frame

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarActivate)

    def OnTaskBarActivate(self, evt):
        if self.frame.IsIconized():
            self.frame.Iconize(False)
        if not self.frame.IsShown():
            self.frame.Show(True)
        self.frame.Raise()


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, None, -1, 'WebPrint', size=(1024, 768),
            style=wx.DEFAULT_FRAME_STYLE)

        self.SetMenuBar(self.MakeMenuBar())
        self.trayIcon = AppTaskBarIcon(self)

        # hide to frame to implement minize to system tray
        self.Bind(wx.EVT_CLOSE, self.OnWindowClose)

        bookStyle = wx.aui.AUI_NB_DEFAULT_STYLE
        bookStyle &= ~(wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
        self.nb = wx.aui.AuiNotebook(self, style=bookStyle)

        for printer in enumeratePrinters():
            self.nb.AddPage(PrinterPanel(self.nb), printer['name'])

        self.Centre(wx.BOTH)
        self.StartServer()

    def StartServer(self):
        def sever_thread(loop):
            asyncio.set_event_loop(loop)

            factory = WebSocketServerFactory('ws://127.0.0.1:9000')
            factory.protocol = MyServerProtocol

            coro = loop.create_server(factory, '0.0.0.0', 9000)
            server = loop.run_until_complete(coro)
            try:
                loop.run_forever()
            finally:
                print('Stopping server')
                server.close()
                loop.close()

        loop = asyncio.get_event_loop()
        t = threading.Thread(target=sever_thread, args=(loop,))
        t.start()
        self.serverThread = t

    def OnExit(self, evt):
        if self.trayIcon is not None:
            self.trayIcon.Destroy()
        self.serverThread.join(timeout=0.1)
        print('sever thread exit')
        self.Destroy()

    def OnWindowClose(self, evt):
        self.Hide()

    def MakeMenuBar(self):
        mb = wx.MenuBar()

        menu1 = wx.Menu()

        item = wx.MenuItem(menu1, -1, '退出')
        IDM_EXIT = menu1.Append(item)
        mb.Append(menu1, '主菜单')

        self.Bind(wx.EVT_MENU, self.OnExit, IDM_EXIT)

        menu2 = wx.Menu()
        IDM_CHG_PASS = menu2.Append(-1, '更改密码')
        mb.Append(menu2, '工具')

        self.Bind(wx.EVT_MENU, self.dummy, IDM_CHG_PASS)

        return mb

    def dummy(self):
        pass
