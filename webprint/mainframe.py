import wx
import wx.aui
import wx.adv

from .utils import enumeratePrinters
from .printerpanel import PrinterPanel


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

        self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        bookStyle = wx.aui.AUI_NB_DEFAULT_STYLE
        bookStyle &= ~(wx.aui.AUI_NB_CLOSE_ON_ACTIVE_TAB)
        self.nb = wx.aui.AuiNotebook(self, style=bookStyle)

        for printer in enumeratePrinters():
            self.nb.AddPage(PrinterPanel(self.nb), printer['name'])

        self.Centre(wx.BOTH)

    def OnCloseWindow(self, evt):
        if self.trayIcon is not None:
            self.trayIcon.Destroy()
        self.Destroy()

    def MakeMenuBar(self):
        mb = wx.MenuBar()

        menu1 = wx.Menu()
        IDM_SALES_ORDER = menu1.Append(-1, '销售订单')
        IDM_PURCHASE_ORDER = menu1.Append(-1, '采购订货')

        item = wx.MenuItem(menu1, -1, '物流管理')
        IDM_LOGISTICS = menu1.Append(item)

        menu1.AppendSeparator()
        mb.Append(menu1, '主菜单(&M)')

        self.Bind(wx.EVT_MENU, self.dummy, IDM_SALES_ORDER)
        self.Bind(wx.EVT_MENU, self.dummy, IDM_PURCHASE_ORDER)
        self.Bind(wx.EVT_MENU, self.dummy, IDM_LOGISTICS)

        menu2 = wx.Menu()
        IDM_CHG_PASS = menu2.Append(-1, '更改密码')
        IDM_CANCEL_INVOICE = menu2.Append(-1, '发票作废')
        mb.Append(menu2, '工具(&T)')

        self.Bind(wx.EVT_MENU, self.dummy, IDM_CHG_PASS)
        self.Bind(wx.EVT_MENU, self.dummy, IDM_CANCEL_INVOICE)

        return mb

    def dummy(self):
        pass
