#!/usr/bin/env python3

# import faulthandler

# faulthandler.enable()
import sys
import os
import argparse
import atexit
import signal

# from PyQt4 import QtCore, QtGui
import re
import shelve

# from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

from matplotlib.backends.qt_compat import QtCore, QtGui, is_pyqt5
if is_pyqt5():
    from matplotlib.backends.backend_qt5agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
else:
    from matplotlib.backends.backend_qt4agg import (
        FigureCanvas, NavigationToolbar2QT as NavigationToolbar)



from matplotlib.figure import Figure

# import matplotlib
# matplotlib.use('TkAgg')
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg as FigureCanvas
# from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg as NavigationToolbar
# from matplotlib.figure import Figure





from graph_window import GraphWindow 
from main_gui_window import MainGuiWindow
from ranges import SelectedRangeList
from selected_points import SelectedPointsList
from selected_residues import SelectedResiduesList
from reply_log import ReplyLog

import app as app


choices=["*.xvg","*.txt","*.gro"] # accepted file extensions

# check if the file has an accepted extension
def CheckExt(choices):
    class Act(argparse.Action):
        def __call__(self,parser,namespace,fname,option_string=None):
            ext = os.path.splitext(fname)[1][1:]
            if ext not in choices:
                option_string = '({})'.format(option_string) if option_string else ''
                parser.error("file doesn't end with one of {}{}".format(choices,option_string))
            else:
                setattr(namespace,self.dest,fname)

    return Act


parser = argparse.ArgumentParser()

parser.add_argument("-r", "--rmsf", dest = 'rmsf_filename', default = "rmsf.xvg", help="rmsf file", action=CheckExt({'xvg','txt'}))
parser.add_argument("-c", "--coords", dest = 'my_gro_filename', default = "protein.gro", help=".gro file used for rmsf", action=CheckExt({'gro'}))

app.args = parser.parse_args()


# Open the rmsf.xvg file and assign residue and rmsf variables
with open(app.args.rmsf_filename) as rmsf:

    rmsf_lines = [line.strip() for line in rmsf if not line.startswith(('#', '@'))]

    for line in rmsf_lines:

        cols = line.split()

        if len(cols) == 2:
            app.x_a_res.append(float(cols[0]))
            app.y_a_rmsf.append(float(cols[1]))

# Open the given .gro file and assign needed variables (residue/atom values and names)
with open(app.args.my_gro_filename) as gro_file:

    for line in gro_file:
        
        cols = line.split()

        if len(cols) == 6: #number of cols in gro file. will depend if pre or post sim (6 or 9 cols)
            res_col = cols[0]

            match = re.match(r"([0-9]+)([a-zA-Z]+)", res_col, re.I)
            if match:
                items = match.groups()
                
                if len(items) == 2:
                    val_col = items[0]
                    res_col = items[1]

            app.gro_residue_val.append(int(items[0]))
            app.gro_residue_name.append(str(items[1]))
            app.gro_atom_name.append(str(cols[1]))
            app.gro_atom_number.append(int(cols[2]))

# class SystemTrayIcon(QtGui.QSystemTrayIcon):

#     def __init__(self, icon, parent=None):
#         QtGui.QSystemTrayIcon.__init__(self, icon, parent)
#         menu = QtGui.QMenu(parent)
#         exitAction = menu.addAction("Exit")
#         self.setContextMenu(menu)


#############

def main():


    app.qapp = QtGui.QApplication(sys.argv)

    app.main_window = MainGuiWindow()
    app.main_window.move(50, 60)
    app.main_window.resize(1500, 1000)
    app.main_window.setWindowTitle("mitriiah")
    app.main_window.setWindowIcon(QtGui.QIcon("kitty.png"))

    # w = QtGui.QWidget()
    # trayIcon = SystemTrayIcon(QtGui.QIcon("kitty.jpg"), w)

    # trayIcon.show()
    # app.main_window.setWindowIcon(QtGui.setPixmap("hamster.png"))

    # pic = QtGui.QLabel(app.main_window)
    # pic.setGeometry(10, 10, 400, 100)
    # #use full ABSOLUTE path to the image, not relative
    # pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/hamster.png"))


    # w = QtGui.QWidget()
    # w.resize(820, 240)
    # w.setWindowTitle("Hello World!")
    # w.setWindowIcon( QtGui.QIcon("hamster.png") )
    # w.show()

    app.main_window.show()
    app.main_window.raise_()

    sys.exit(app.qapp.exec_())


if __name__ == '__main__':
    main()



#############

# app = QtGui.QApplication(sys.argv)

# w = QtGui.QWidget()
# trayIcon = SystemTrayIcon(QtGui.QIcon("Example1.ico"), w)
# trayIcon.show()

# sys.exit(app.exec_())



# app = QtGui.QApplication(sys.argv)
# window = QtGui.QMainWindow()
# window.setGeometry(0, 0, 400, 200)


# pic = QtGui.QLabel(window)
# pic.setGeometry(10, 10, 400, 100)
# #use full ABSOLUTE path to the image, not relative
# pic.setPixmap(QtGui.QPixmap(os.getcwd() + "/logo.png"))

# window.show()
# sys.exit(app.exec_())



# class Application:
#     def __init__(self, app):
#         self.app.qapp = QtGui.QApplication(sys.argv)
#         self.app.main_window = MainGuiWindow()

#     def run(self):
#         timer = QTimer()
#         timer.start(500)
#         timer.timeout.connect(lambda: None)

#         self.app.main_window.move(50, 60)
#         self.app.main_window.resize(1500, 1000)
#         self.app.main_window.show()
#         self.app.main_window.raise_()
#         return self.app.qapp.exec_()

#     def cleanup(self):
#         self.gui.cleanup()

# def main():
#     app.qapp = Application(app)
#     atexit.register(cleanup, app.qapp)
#     sys.exit(app.qapp.run())


# main()

# def main():
#     # app = QApplication(sys.argv)
#     # app = QtGui.QApplication(sys.argv)
#     app.qapp = QtGui.QApplication(sys.argv)
#     # gui = Window()

#     # Rejestracja funkcji, która wywoła się z końcem aplikacji
#     atexit.register(cleanup, gui)

#     # Pozwala interpreterowi uruchomić się co 500 ms,
#     # dzięki czemu możemy przechwycić nadchodzące sygnały
#     # (w przeciwnym wypadku Qt będzie je blokować).
#     timer = QTimer()
#     timer.start(500)
#     timer.timeout.connect(lambda: None)

#     app.main_window = MainGuiWindow()
#     app.main_window.move(50, 60)
#     app.main_window.resize(1500, 1000)
#     app.main_window.show()
#     app.main_window.raise_()

#     sys.exit(app.qapp.exec_())




# # Obsługa SIGINT (ctrl-c)
# signal.signal(signal.SIGINT, interruptHandler)
# main()


