from PyQt4 import QtCore, QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

import matplotlib.patches as patches

# from matplotlib.backends.qt_compat import QtCore, QtGui, is_pyqt5
# if is_pyqt5():
#     from matplotlib.backends.backend_qt5agg import (
#         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)
# else:
#     from matplotlib.backends.backend_qt4agg import (
#         FigureCanvas, NavigationToolbar2QT as NavigationToolbar)


# from matplotlib.figure import Figure


from reply_log import ReplyLog
import app as app


# Space in which the rmsf figure is drawn
class GraphWindow(QtGui.QDialog):
    def __init__(self, x_a_res, y_a_rmsf):
        super(GraphWindow, self).__init__()

        self.main()
  
        self.redraw_graph()

    # set the drawing space
    def main(self):
        # a figure instance to plot on
        self.figure = Figure(figsize = (5,4))

        # this is the Canvas Widget that displays the `figure`. it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget. it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)
        
        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        self.setLayout(layout)

        # create an axis
        ax = self.figure.add_subplot(111)
        self.ax = ax

        ax.set_ylim(bottom = 0)

        # use the selecter on graph
        cid = self.figure.canvas.mpl_connect('button_press_event', app.add_point_by_mouse)
        
        self.redraw_graph()

    
    # plot the graph
    def redraw_graph(self):

        self.ax.clear() # discards the old graph

        # self.ax.plot(app.x_a_res,app.y_a_rmsf, c='k') # plot the rmsf graph


        self.ax.plot(app.chain_list["chain%s" % app.chain_num]["rmsf_data"]["x_a_res"],app.chain_list["chain%s" % app.chain_num]["rmsf_data"]["y_a_rmsf"], c='k')

        self.ax.set_ylim(bottom = 0)


        # plot every selected point
        for point in app.selected_points:
            self.ax.plot(point['x'],point['y'], c='r', marker='o')




        # plot every range
        for range_name, range_list in app.ranges_list.items():

            x = app.ranges_list[range_name]['from_val']
            w = (app.ranges_list[range_name]['to_val']) - (app.ranges_list[range_name]['from_val'])
            # t = (max(app.y_a_rmsf)) + 0.25
            t = (max(app.chain_list["chain%s" % app.chain_num]["rmsf_data"]["y_a_rmsf"])) + 0.25
            

            self.ax.add_patch(patches.Rectangle((x, -0.1), w, t, alpha = 0.2, facecolor = '#ffaa00'))

            # for index, val in enumerate(app.x_a_res):
            for index, val in enumerate(app.chain_list["chain%s" % app.chain_num]["rmsf_data"]["x_a_res"]):
                
                if val == x:
                    # y = app.y_a_rmsf[index]
                    y = app.chain_list["chain%s" % app.chain_num]["rmsf_data"]["y_a_rmsf"][index]
                    

                    if w == 0:
                        self.ax.plot(app.ranges_list[range_name]['from_val'],y, c='#ffaa00', marker='o')

        self.ax.set_title("RMSF")    
        self.ax.set_xlabel('Residue number')
        self.ax.set_ylabel('rmsf (nm)')

        # refresh canvas
        self.canvas.draw()

    # define the keyboard shortcuts
    def keyPressEvent(self, event):

        super(GraphWindow, self).keyPressEvent(event)

        # atom output shortcut
        if event.key() == QtCore.Qt.Key_P:
            
            print('Saved atom list')
            app.main_window.reply_log_object.append("Saved atom list")

            app.saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')


            app.qapp.quit()

        if event.key() == QtCore.Qt.Key_S:
            app.save_variables()


        if event.key() == QtCore.Qt.Key_L:
            app.open_variables()


    # close down all open windows when this one is closed -- is it needed??
    def closeEvent(self, event):
        app.qapp.quit()
