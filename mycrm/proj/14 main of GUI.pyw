
def main():
    app = QApplication(sys.argv)

# Create DB
    filename = os.path.join(os.path.dirname(os.__file__), "assets.db")
    create = not QFile.exists(filename) # This is related to splash screen
    # If the data file does not exist, it will use splash screen to indicate the creating process
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName(filename)
    if not db.open():
        QMessageBox.warning(None, "Asset Manager",
            QString("Database Error: %1").arg(db.lastError().text()))
        sys.exit(1)

    splash = None
#ignore Splash Part1

    form = MainForm()
    form.show() 
# ignore Splash Part2
    app.exec_()
    del form # why need to close form, is there auto del feature?
    del db # this only deletes the connection


main()
