class ReplyLog(QtGui.QTextEdit):
    def __init__(self):
        super(ReplyLog, self).__init__()

        self.append(" Hamster log:")
        self.setReadOnly(True)

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