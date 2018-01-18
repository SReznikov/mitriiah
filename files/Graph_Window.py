# Space in which the rmsf figure is drawn
class GraphWindow(QtGui.QDialog):
    def __init__(self, x_a_res, y_a_rmsf):
        super(GraphWindow, self).__init__()

        self.setWindowTitle('RMSF plot')

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

        # use the selecter on graph
        cid = self.figure.canvas.mpl_connect('button_press_event', add_point_by_mouse)


    # plot the graph
    def redraw_graph(self):

        self.ax.clear() # discards the old graph

        self.ax.plot(x_a_res,y_a_rmsf, c='k') # plot the rmsf graph

        # plot every selected point
        for point in selected_points:
            self.ax.plot(point['x'],point['y'], c='r', marker='o')

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
            
            print('Saved atom list from Graph-Window')
            main_window.reply_log_object.append("Saved atom list from Graph-Window")

            saving_and_output()

        # quit the program shortcut
        if event.key() == QtCore.Qt.Key_Q:
            
            print('Hamster ran out!')

            app.quit()

    # close down all open windows when this one is closed -- is it needed??
    def closeEvent(self, event):
        app.quit()