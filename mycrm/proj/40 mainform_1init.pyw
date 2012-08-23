class MainForm(QDialog):

# simplest form of init
    def __init__(self):
        super(MainForm, self).__init__()
# it seems after below "asset" will delegate a table
#    db = QSqlDatabase.addDatabase("QSQLITE")
#    db.setDatabaseName(filename)
#    db.open()

#init model(with foreign key), set table, set relation
# using real table names for setTable, QSqlrelation
# using column id for setRelation/setSort/setHeaderData
# summary: using everything inside model is using id instead of real db column name

        self.assetModel = QSqlRelationalTableModel(self)
        self.assetModel.setTable("assets")
        self.assetModel.setRelation(CATEGORYID,
                QSqlRelation("categories", "id", "name"))
        self.assetModel.setSort(ROOM, Qt.AscendingOrder)
        self.assetModel.setHeaderData(ID, Qt.Horizontal,
                QVariant("ID")) #literal, not predefined constant
        self.assetModel.setHeaderData(NAME, Qt.Horizontal,
                QVariant("Name"))
        self.assetModel.setHeaderData(CATEGORYID, Qt.Horizontal,
                QVariant("Category"))
        self.assetModel.setHeaderData(ROOM, Qt.Horizontal,
                QVariant("Room"))
        # this is really populate model with data
        self.assetModel.select()

# view: need to set model (source of data)
#   -> and delegate (how to present each data to view, and retrive from it)
        self.assetView = QTableView()
        self.assetView.setModel(self.assetModel)
        self.assetView.setItemDelegate(AssetDelegate(self))
# for view, we can set selection mode/behavior, and resize
        self.assetView.setSelectionMode(QTableView.SingleSelection)
        self.assetView.setSelectionBehavior(QTableView.SelectRows)
        self.assetView.setColumnHidden(ID, True)
        self.assetView.resizeColumnsToContents()
        assetLabel = QLabel("A&ssets")
        assetLabel.setBuddy(self.assetView)

        self.logModel = QSqlRelationalTableModel(self)
        self.logModel.setTable("logs")
        self.logModel.setRelation(ACTIONID,
                QSqlRelation("actions", "id", "name"))
        self.logModel.setSort(DATE, Qt.AscendingOrder)
        self.logModel.setHeaderData(DATE, Qt.Horizontal,
                QVariant("Date"))
        self.logModel.setHeaderData(ACTIONID, Qt.Horizontal,
                QVariant("Action"))
        self.logModel.select()

# same as above
        self.logView = QTableView()
        self.logView.setModel(self.logModel)
        self.logView.setItemDelegate(LogDelegate(self))
        self.logView.setSelectionMode(QTableView.SingleSelection)
        self.logView.setSelectionBehavior(QTableView.SelectRows)
# but we set hide column, and xxstretch(strech the last column as much as possible)
        self.logView.setColumnHidden(ID, True)
        self.logView.setColumnHidden(ASSETID, True)
        self.logView.resizeColumnsToContents()
        self.logView.horizontalHeader().setStretchLastSection(True)
        logLabel = QLabel("&Logs")
        logLabel.setBuddy(self.logView)


# create buttons
        addAssetButton = QPushButton("&Add Asset")
        deleteAssetButton = QPushButton("&Delete Asset")
        addActionButton = QPushButton("Add A&ction")
        deleteActionButton = QPushButton("Delete Ac&tion")
        editActionsButton = QPushButton("&Edit Actions...")
        editCategoriesButton = QPushButton("Ed&it Categories...")
        quitButton = QPushButton("&Quit")
        for button in (addAssetButton, deleteAssetButton,
                addActionButton, deleteActionButton,
                editActionsButton, editCategoriesButton, quitButton):
            if MAC:
                button.setDefault(False)
                button.setAutoDefault(False)

            else:
                # so this kind of represent and iteration will modify the buttons ?
                button.setFocusPolicy(Qt.NoFocus)

# set layout
        dataLayout = QVBoxLayout()
        dataLayout.addWidget(assetLabel)
        dataLayout.addWidget(self.assetView, 1)
        dataLayout.addWidget(logLabel)
        dataLayout.addWidget(self.logView)
        buttonLayout = QVBoxLayout()
        buttonLayout.addWidget(addAssetButton)
        buttonLayout.addWidget(deleteAssetButton)
        buttonLayout.addWidget(addActionButton)
        buttonLayout.addWidget(deleteActionButton)
        buttonLayout.addWidget(editActionsButton)
        buttonLayout.addWidget(editCategoriesButton)
        buttonLayout.addStretch()
        buttonLayout.addWidget(quitButton)
        layout = QHBoxLayout()
        layout.addLayout(dataLayout, 1)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)

# set connections:

# std pyqt conn, asset changed can accept 0-2 arguments
#   -> as there are 2 in SIGNAL
        self.connect(self.assetView.selectionModel(),
                SIGNAL("currentRowChanged(QModelIndex,QModelIndex)"),
                self.assetChanged)

# normal conn: button clicked to event 
        self.connect(addAssetButton, SIGNAL("clicked()"),
                     self.addAsset)
        self.connect(deleteAssetButton, SIGNAL("clicked()"),
                     self.deleteAsset)
        self.connect(addActionButton, SIGNAL("clicked()"),
                     self.addAction)
        self.connect(deleteActionButton, SIGNAL("clicked()"),
                     self.deleteAction)
        self.connect(editActionsButton, SIGNAL("clicked()"),
                     self.editActions)
        self.connect(editCategoriesButton, SIGNAL("clicked()"),
                     self.editCategories)
    # !! check what is self.done
        self.connect(quitButton, SIGNAL("clicked()"), self.done)

# !!check what is assetChanged
        self.assetChanged(self.assetView.currentIndex())
        self.setMinimumWidth(650)
        self.setWindowTitle("Asset Manager")

