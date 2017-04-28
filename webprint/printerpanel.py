import wx

from hm.wxx.grid.field import StringField, DateField
from hm.wxx.grid.schema import Schema
from hm.wxx.grid import DataGrid


class TaskGrid(DataGrid):
    def __init__(self, *args, **kwargs):
        DataGrid.__init__(
            self,
            Schema(
                (
                    StringField(
                        'Title',
                        label='文档标题',
                        dataobj_field='title',
                        display_width=65,
                        editable=False
                    ),
                    DateField(
                        'SubmitTime',
                        label='提交时间',
                        dataobj_field='submitTime',
                        format='%.19s',
                        display_width=130
                    )
                ),
                allow_row_move=False,
                allow_col_move=False
            ),
            *args, **kwargs
        )

        self.SetRowLabelSize(50)


class PrinterPanel(wx.Panel):
    def __init__(self, parent):
        wx.Panel.__init__(self, parent)

        sizer = wx.BoxSizer(wx.VERTICAL)

        self.btnPause = wx.Button(self, -1, '暂停打印')
        self.btnPurge = wx.Button(self, -1, '删除所有任务')

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.AddMany([
            (0, 0, 1),
            (self.btnPurge, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5),
            (self.btnPause, 0, wx.ALIGN_CENTER_VERTICAL | wx.ALL, 5),
        ])

        sizer.Add(TaskGrid(self), 1, wx.GROW | wx.ALL, 5)
        sizer.Add(hsizer, 0, wx.GROW)

        self.SetSizer(sizer)
        sizer.Fit(self)
