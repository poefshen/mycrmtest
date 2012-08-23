def createable():

    print "Creating tables..."
    query.exec_("""CREATE TABLE actions (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(20) NOT NULL,
                description VARCHAR(40) NOT NULL)""")
    query.exec_("""CREATE TABLE categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(20) NOT NULL,
                description VARCHAR(40) NOT NULL)""")
    query.exec_("""CREATE TABLE assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name VARCHAR(40) NOT NULL,
                categoryid INTEGER NOT NULL,
                room VARCHAR(4) NOT NULL,
                FOREIGN KEY (categoryid) REFERENCES categories)""")
    query.exec_("""CREATE TABLE logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                assetid INTEGER NOT NULL,
                date DATE NOT NULL,
                actionid INTEGER NOT NULL,
                FOREIGN KEY (assetid) REFERENCES assets,
                FOREIGN KEY (actionid) REFERENCES actions)""")
    QApplication.processEvents()

