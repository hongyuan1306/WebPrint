========
WebPrint
========

Current Status
--------------

The project is currently suspended as its usefulness has lower priority.

Printing a PDF file using PyMuPDF to a given Windows printer is tested and
technically working. Database and websocket server are **not** implemented. As
a whole the code is not useable.


Introduction
------------

WebPrint is a printer server which allows web applications to send print jobs
using javascript, with the following features:

 * it runs on the Windows platform and exposes the Windows printers to web
   applications
 * it uses WAMP protocol over secure WebSocket (wss://) to communicate with the
   client web applications
 * it only accepts PDF files for printing
 * print tasks are cached first on the local file system, with a sqlite database
   for keeping track of the metadata. Unprinted tasks can be resumed when
   WebPrint is restarted
 * Multiple clients can connect to the server simultaneously


Dependencies
------------

 * Python 3.5 (this is the version in which the project is developed)
 * wxPython Phoenix (for GUI)
 * hm.wxx (for DataGrid)
 * PyMuPDF (as the PDF rendering engine)
 * sqlalchemy (the ORM)
 * autobahn (for WebSocket server support)
