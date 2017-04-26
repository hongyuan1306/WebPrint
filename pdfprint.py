import ctypes
from ctypes.wintypes import BYTE, DWORD, LPCWSTR

import wx
import fitz


class PdfPrintout(wx.Printout):
    """
    Class encapsulating the functionality of printing out the document. The
    methods below over-ride those of the base class and supply document
    specific information to the printing framework that calls them internally.
    """
    def __init__(self, title, pdfdoc):
        """
        Pass in the instance of dpViewer to be printed.
        """
        wx.Printout.__init__(self, title)
        self.pdfdoc = pdfdoc

    def HasPage(self, pageno):
        """
        Report whether pageno exists.
        """
        if pageno <= self.pdfdoc.pageCount:
            return True
        else:
            return False

    def GetPageInfo(self):
        """
        Supply maximum range of pages and the range to be printed
        These are initial values passed to Printer dialog, where they
        can be amended by user.
        """
        maxnum = self.pdfdoc.pageCount
        return (1, maxnum, 1, maxnum)

    def OnPrintPage(self, page):
        """
        Provide the data for page by rendering the drawing commands
        to the printer DC, MuPDF returns the page content from an internally
        generated bitmap and sfac sets it to a high enough resolution that
        reduces anti-aliasing blur but keeps it small to minimise printing time
        """
        sfac = 4.0
        pageno = page - 1       # zero based
        page = self.pdfdoc.loadPage(pageno)

        width = page.bound().width
        height = page.bound().height

        self.FitThisSizeToPage(wx.Size(width * sfac, height * sfac))
        dc = self.GetDC()
        gc = wx.GraphicsContext.Create(dc)

        matrix = fitz.Matrix(sfac, sfac)
        try:
            pix = page.getPixmap(matrix=matrix)   # MUST be keyword arg(s)
            bmp = wx.Bitmap.FromBufferRGBA(pix.width, pix.height, pix.samples)
            gc.DrawBitmap(bmp, 0, 0, pix.width, pix.height)
        except (RuntimeError, MemoryError):
            pass

        return True


def printPdf(pdfFile):
    if isinstance(pdfFile, str):
        # a filename/path string, pass the name to fitz.open
        pdfdoc = fitz.open(pdfFile)
    else:
        # assume it is a file-like object, pass the stream content to
        # fitz.open and a '.pdf' extension in pathname to identify the
        # stream type
        if pdfFile.tell() > 0:     # not positioned at start
            pdfFile.seek(0)
        stream = bytearray(pdfFile.read())
        pdfdoc = fitz.open('fileobject.pdf', stream)
    printout = PdfPrintout('', pdfdoc)

    pdata = wx.PrintData()
    pdata.SetPrinterName('HP LaserJet')
    data = wx.PrintDialogData(pdata)

    printer = wx.Printer(data)
    if (not printer.Print(None, printout, True) and
            printer.GetLastError() == wx.PRINTER_ERROR):
        print('Printing failed')

    printout.Destroy()


def enumeratePrinters():
    # Use EnumPrintersW to list local printers with their names and
    # descriptions.

    winspool = ctypes.WinDLL('winspool.drv')  # for EnumPrintersW
    msvcrt = ctypes.cdll.msvcrt  # for malloc, free

    # Parameters: modify as you need. See MSDN for detail.
    PRINTER_ENUM_LOCAL = 2
    Name = None  # ignored for PRINTER_ENUM_LOCAL
    Level = 1  # or 2, 4, 5

    class PRINTER_INFO_1(ctypes.Structure):
        _fields_ = [
            ("Flags", DWORD),
            ("pDescription", LPCWSTR),
            ("pName", LPCWSTR),
            ("pComment", LPCWSTR),
        ]

    # Invoke once with a NULL pointer to get buffer size.
    info = ctypes.POINTER(BYTE)()
    pcbNeeded = DWORD(0)
    pcReturned = DWORD(0)  # the number of PRINTER_INFO_1 structures retrieved
    winspool.EnumPrintersW(
        PRINTER_ENUM_LOCAL, Name, Level,
        ctypes.byref(info), 0,
        ctypes.byref(pcbNeeded), ctypes.byref(pcReturned))

    bufsize = pcbNeeded.value
    buffer = msvcrt.malloc(bufsize)
    winspool.EnumPrintersW(PRINTER_ENUM_LOCAL, Name, Level, buffer, bufsize,
                           ctypes.byref(pcbNeeded), ctypes.byref(pcReturned))
    info = ctypes.cast(buffer, ctypes.POINTER(PRINTER_INFO_1))
    for i in range(pcReturned.value):
        print(info[i].pName, '=>', info[i].pDescription)
    msvcrt.free(buffer)


if __name__ == '__main__':
    app = wx.App()
    app.MainLoop()

    enumeratePrinters()
