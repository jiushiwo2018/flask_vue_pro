# -*- coding: utf-8 -*-

# from PyQt5.QtWidgets import QApplication
# from PyQt5.QtWebEngineWidgets import QWebEngineView
# from PyQt5.QtCore import QUrl
from PyQt5.uic.Compiler.qtproxies import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

def startWeb():
    from flask_vue_jquery_deskapp.app import app
    app.run()

def main(argv):
    qtapp = QtWidgets.QApplication(argv)
    from threading import Thread
    webapp = Thread(target=startWeb)
    webapp.daemon = True
    webapp.start()
    view = QWebEngineView()
    view.setWindowTitle('DeskApp')
    port = 5000
    view.setUrl( QUrl("http://localhost:{}/".format(port)))
    view.show()

    return qtapp.exec_()

import sys
if __name__ == '__main__':
    main(sys.argv)