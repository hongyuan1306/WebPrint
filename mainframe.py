import wx
import wx.aui

from utils import enumeratePrinters
from printerpanel import PrinterPanel


class MainFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(
            self, None, -1, 'WebPrint', size=(1024, 768),
            style=wx.DEFAULT_FRAME_STYLE)

        self.SetMenuBar(self.MakeMenuBar())

        self.nb = wx.aui.AuiNotebook(self, style=wx.aui.AUI_NB_DEFAULT_STYLE |
                                     wx.aui.AUI_NB_CLOSE_ON_ALL_TABS)

        for printer in enumeratePrinters():
            self.nb.AddPage(PrinterPanel(self.nb), printer['name'])

        self.Centre(wx.BOTH)

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
