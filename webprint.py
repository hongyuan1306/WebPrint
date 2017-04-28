import wx
import wx.lib.mixins.inspection

from sqlalchemy import create_engine

from webprint.model import meta
from webprint.mainframe import MainFrame


def setupDB():
    engine = create_engine('sqlite:///:memory:', echo=True)
    meta.bind = engine


class WebPrintApp(wx.App, wx.lib.mixins.inspection.InspectionMixin):
    def OnInit(self):
        MainFrame().Show()
        return True


if __name__ == '__main__':
    setupDB()

    app = WebPrintApp()
    app.MainLoop()
