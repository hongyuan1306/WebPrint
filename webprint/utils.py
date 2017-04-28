import ctypes
from ctypes.wintypes import BYTE, DWORD, LPCWSTR


def enumeratePrinters():
    """ Use EnumPrintersW to list local printers with their names and
    descriptions."""

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

    printers = [{
        'name': info[i].pName,
        'description': info[i].pDescription
    } for i in range(pcReturned.value)]

    msvcrt.free(buffer)
    return printers
