from PyQt4 import QtCore, QtGui
import app as app



class ReplyLog(QtGui.QTextEdit):
    def __init__(self):
        super(ReplyLog, self).__init__()

        self.append(" Hello... hamster is running. To start right-click on the graph, or input a range. ")
        # print("min/max residue: %s, %s" % (app.min_res, app.max_res))
        # self.append("min/max residue: %s, %s" % (app.min_res, app.max_res))
        self.setReadOnly(True)

    # define the keyboard shortcuts
    # def keyPressEvent(self, event):

    #     super(ReplyLog, self).keyPressEvent(event)

    #     # key_shortcuts(event)

    #     # atom output shortcut
    #     if event.key() == QtCore.Qt.Key_P:
            
    #         print('Saved atom list')
    #         main_window.reply_log_object.append("Saved atom list")

    #         saving_and_output()

    #     # quit the program shortcut
    #     if event.key() == QtCore.Qt.Key_Q:
            
    #         print('Hamster ran out!')

    #         app.quit()

    #     if event.key() == QtCore.Qt.Key_S:
    #         save_variables()


    #     if event.key() == QtCore.Qt.Key_L:
    #         open_variables()

