# this is part 2, merge with 40
class MainForm(QDialog):

    def done(self, result=1):
        query = QSqlQuery()
        # if in log, the assetid is not in table asset.id:
        #   -> delete those rows from table logs
        query.exec_("DELETE FROM logs WHERE logs.assetid NOT IN"
                    "(SELECT id FROM assets)")
        #close dialog
        QDialog.done(self, 1)


# accept one argument - index
# if index is not valid, 
    def assetChanged(self, index):
        if index.isValid():
            # record: model's public function, will retrive the whole row if exists
            #   -> take an argument of row number 
            #   -> note that we can use column name "id" to retrive a db element
            #   -> record.value("columnName")
            # This is same as model.data(model.index(3, 4))
            # (3,4) is the related row/column number
            # Note: record.value("columnName") will return an QVariant
            record = self.assetModel.record(index.row())
            id = record.value("id").toInt()[0]
            # setFilter: if model is populated with data, same as where, to filter data
            #   -> if not populated, it will take effect after next select()
            # QString("xx %1").arg(xx) is a standard way
            self.logModel.setFilter(QString("assetid = %1").arg(id))
        else:
            self.logModel.setFilter("assetid = -1")
        self.logModel.reset() # workaround for Qt <= 4.3.3/SQLite bug
        self.logModel.select()
        self.logView.horizontalHeader().setVisible(
                self.logModel.rowCount() > 0)
        if PYQT_VERSION_STR < "4.1.0":
            self.logView.setColumnHidden(ID, True)
            self.logView.setColumnHidden(ASSETID, True)


    def addAsset(self):
    # save currentIndex of view in "row", if no index, set row to 0
    # !! view has currentIndex(), tells what data currently view is using
    #   -> normally it is a row in db for 
        row = self.assetView.currentIndex().row() \
            if self.assetView.currentIndex().isValid() else 0

# If the driver supports transactions, 
#   ->use transaction() to start a transaction, and commit() or rollback() to complete it. 
        QSqlDatabase.database().transaction()
        # insert a row in the model (not the db)
        self.assetModel.insertRow(row)
        # note the method how we define an index 
        #   -> would it be same as using the constant QIndex(xx, xx)
        index = self.assetModel.index(row, NAME) # name is constant, 1
        # !! setCurrentIndex: new method 
        # though we retrive a row, index is one record of db
        self.assetView.setCurrentIndex(index)

        assetid = 1
        query = QSqlQuery()
        query.exec_("SELECT MAX(id) FROM assets")
        # if max "assetid" exists, we retrive "id" from table"asset"
        #   -> means we add that record after the last line
        #   -> if the table is empty !! we set the asset id to "2"? 
        if query.next():
        # !! query will return several lines, and value(0) will return the first row
        #   -> then [0] will return the first record of that line
            assetid = query.value(0).toInt()[0] 
        query.prepare("INSERT INTO logs (assetid, date, actionid) "
                      "VALUES (:assetid, :date, :actionid)")
        query.bindValue(":assetid", QVariant(assetid + 1))
        query.bindValue(":date", QVariant(QDate.currentDate()))
        query.bindValue(":actionid", QVariant(ACQUIRED))
        query.exec_()
        # !! commit here (end of "transaction")
        QSqlDatabase.database().commit()
        # set index as "editing", and not changing index
        self.assetView.edit(index)


    def deleteAsset(self):
        # do nothing if no currentIndex
        index = self.assetView.currentIndex()
        if not index.isValid():
            return
        QSqlDatabase.database().transaction()
        # check above if any question
        record = self.assetModel.record(index.row())
        assetid = record.value(ID).toInt()[0]
        logrecords = 1
        # !! care about how we remove data from database 
        query = QSqlQuery(QString("SELECT COUNT(*) FROM logs "
                                  "WHERE assetid = %1").arg(assetid))
        # if there is log related to the asset to be deleted
        #   -> change "logrecord" to current id
        
        if query.next():
            logrecords = query.value(0).toInt()[0]
        # pop up window to confirm multi delete
        msg = QString("<font color=red>Delete</font><br><b>%1</b>"
                      "<br>from room %2") \
                      .arg(record.value(NAME).toString()) \
                      .arg(record.value(ROOM).toString())
        if logrecords > 1:
            msg += QString(", along with %1 log records") \
                   .arg(logrecords)
        msg += "?"
        if QMessageBox.question(self, "Delete Asset", msg,
                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            QSqlDatabase.database().rollback()
            return
        # delete multi logs (under that asset)
        query.exec_(QString("DELETE FROM logs WHERE assetid = %1") \
                    .arg(assetid))
        # then remove record in asset
        self.assetModel.removeRow(index.row())
        self.assetModel.submitAll()
        QSqlDatabase.database().commit()
        # !! refresh whats assetChanged for
        self.assetChanged(self.assetView.currentIndex())

# !! check later
    def addAction(self):
        index = self.assetView.currentIndex()
        if not index.isValid():
            return
        QSqlDatabase.database().transaction()
        record = self.assetModel.record(index.row())
        assetid = record.value(ID).toInt()[0]

        row = self.logModel.rowCount()
        self.logModel.insertRow(row)
        self.logModel.setData(self.logModel.index(row, ASSETID),
                              QVariant(assetid))
        self.logModel.setData(self.logModel.index(row, DATE),
                              QVariant(QDate.currentDate()))
        QSqlDatabase.database().commit()
        index = self.logModel.index(row, ACTIONID)
        self.logView.setCurrentIndex(index)
        self.logView.edit(index)

# !! check later 
    def deleteAction(self):
        index = self.logView.currentIndex()
        if not index.isValid():
            return
        record = self.logModel.record(index.row())
        action = record.value(ACTIONID).toString()
        if action == "Acquired":
            QMessageBox.information(self, "Delete Log",
                    "The 'Acquired' log record cannot be deleted.<br>"
                    "You could delete the entire asset instead.")
            return
        when = unicode(record.value(DATE).toString())
        if QMessageBox.question(self, "Delete Log",
                "Delete log<br>%s %s?" % (when, action),
                QMessageBox.Yes|QMessageBox.No) == QMessageBox.No:
            return
        self.logModel.removeRow(index.row())
        self.logModel.submitAll()

# !! check later 
    def editActions(self):
        form = ReferenceDataDlg("actions", "Action", self)
        form.exec_()

# !! check later 
    def editCategories(self):
        form = ReferenceDataDlg("categories", "Category", self)
        form.exec_()
