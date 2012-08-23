class LogDelegate(QSqlRelationalDelegate):

# same format as asset delegate for every method
    def __init__(self, parent=None):
        super(LogDelegate, self).__init__(parent)

# when column() is DATE we will change alignment
    def paint(self, painter, option, index):
        myoption = QStyleOptionViewItem(option)
        if index.column() == DATE:
            myoption.displayAlignment |= Qt.AlignRight|Qt.AlignVCenter
        QSqlRelationalDelegate.paint(self, painter, myoption, index)

# when actionid is CQUIRED, it will be readonl 
# when method "createEditor" returns nothing, it will be read only
    def createEditor(self, parent, option, index):
        if index.column() == ACTIONID and \
           index.model().data(index, Qt.DisplayRole).toInt()[0] == \
           ACQUIRED: # Acquired is read-only
            return
# when column is date, we will use QDateEdit, and set some properties
# by default, we just pass the option(we don't need to change type here)
#   -> and use default. 
        if index.column() == DATE:
            editor = QDateEdit(parent)
            editor.setMaximumDate(QDate.currentDate())
            editor.setDisplayFormat("yyyy-MM-dd")
            if PYQT_VERSION_STR >= "4.1.0":
                editor.setCalendarPopup(True)
            editor.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return editor
        else:
            return QSqlRelationalDelegate.createEditor(self, parent,
                                                       option, index)

# only change when type is DATE(default is string)
    def setEditorData(self, editor, index):
        if index.column() == DATE:
            date = index.model().data(index, Qt.DisplayRole).toDate()
            editor.setDate(date)
        else:
            QSqlRelationalDelegate.setEditorData(self, editor, index)

# set data in the model, the data is from editor's data
    def setModelData(self, editor, model, index):
        if index.column() == DATE:
            model.setData(index, QVariant(editor.date()))
        else:
            QSqlRelationalDelegate.setModelData(self, editor, model,
                                                index)
