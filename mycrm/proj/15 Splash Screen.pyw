# this is part of the Main GUI
    create = not QFile.exists(filename) # This is related to splash screen

    splash = None

    if create:
        app.setOverrideCursor(QCursor(Qt.WaitCursor))
        splash = QLabel()
        pixmap = QPixmap(":/assetmanagersplash.png")
        splash.setPixmap(pixmap)
        splash.setMask(pixmap.createHeuristicMask())
        splash.setWindowFlags(Qt.SplashScreen)
        rect = app.desktop().availableGeometry()
        splash.move((rect.width() - pixmap.width()) / 2,
                    (rect.height() - pixmap.height()) / 2)
        splash.show()
        app.processEvents()
        createFakeData()

    form = MainForm()
    form.show()
    
    if create:
        splash.close()
        app.processEvents()
        app.restoreOverrideCursor()

