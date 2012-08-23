class ReferenceDataDlg(QDialog):

    def __init__(self, table, title, parent=None):
        super(ReferenceDataDlg, self).__init__(parent)

        self.model = QSqlTableModel(self)
        self.model.setTable(table)
        self.model.setSort(NAME, Qt.AscendingOrder)
        self.model.setHeaderData(ID, Qt.Horizontal,
                QVariant("ID"))
        self.model.setHeaderData(NAME, Qt.Horizontal,
                QVariant("Name"))
        self.model.setHeaderData(DESCRIPTION, Qt.Horizontal,
                QVariant("Description"))
        self.model.select()

        self.view = QTableView()
        self.view.setModel(self.model)
        self.view.setSelectionMode(QTableView.SingleSelection)
        self.view.setSelectionBehavior(QTableView.SelectRows)
        self.view.setColumnHidden(ID, True)
        self.view.resizeColumnsToContents()

        addButton = QPushButton("&Add")
        deleteButton = QPushButton("&Delete")
        okButton = QPushButton("&OK")
        if not MAC:
            addButton.setFocusPolicy(Qt.NoFocus)
            deleteButton.setFocusPolicy(Qt.NoFocus)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(addButton)
        buttonLayout.addWidget(deleteButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(okButton)
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

        self.connect(addButton, SIGNAL("clicked()"), self.addRecord)
        self.connect(deleteButton, SIGNAL("clicked()"),
                     self.deleteRecord)
        self.connect(okButton, SIGNAL("clicked()"), self.accept)

        self.setWindowTitle(
                "Asset Manager - Edit %s Reference Data" % title)


    def addRecord(self):
        row = self.model.rowCount()
        self.model.insertRow(row)
        index = self.model.index(row, NAME)
        self.view.setCurrentIndex(index)
        self.view.edit(index)


    def deleteRecord(self):
        index = self.view.currentIndex()
        if not index.isValid():
            return
        #QSqlDatabase.database().transaction()
        record = self.model.record(index.row())
        id = record.value(ID).toInt()[0]
        table = self.model.tableName()
        query = QSqlQuery()
        if table == "actions":
            query.exec_(QString("SELECT COUNT(*) FROM logs "
                                "WHERE actionid = %1").arg(id))
        elif table == "categories":
            query.exec_(QString("SELECT COUNT(*) FROM assets "
                                "WHERE categoryid = %1").arg(id))
        count = 0
        if query.next():
            count = query.value(0).toInt()[0]
        if count:
            QMessageBox.information(self,
                    QString("Delete %1").arg(table),
                    QString("Cannot delete %1<br>"
                            "from the %2 table because it is used by "
                            "%3 records") \
                    .arg(record.value(NAME).toString())
                    .arg(table).arg(count))
            #QSqlDatabase.database().rollback()
            return
        self.model.removeRow(index.row())
        self.model.submitAll()
        #QSqlDatabase.database().commit()
