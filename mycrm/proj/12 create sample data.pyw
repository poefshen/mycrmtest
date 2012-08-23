# create sample data
def createSampleData():
    assetid = 1
    
    #query binds to assets
    query = QSqlQuery()
    query.prepare("INSERT INTO assets (name, categoryid, room) "
                  "VALUES (:name, :categoryid, :room)")
    room = QVariant("1203")    # room is a integer(1203)
    name,  category = ("HP4230s",  2)     # category is a integer
    query.bindValue(":name", QVariant(name))
    query.bindValue(":categoryid", QVariant(category))
    query.bindValue(":room", room)
    query.exec_()


    #logQuery binds to logs
    logQuery = QSqlQuery()
    logQuery.prepare("INSERT INTO logs (assetid, date, actionid) "
                     "VALUES (:assetid, :date, :actionid)") 
        #prepare + bindvalue will insert value to table "log"
    logQuery.bindValue(":assetid", QVariant(assetid)) # assetid = 1
    when = today.addDays(-random.randint(7, 1500))
    logQuery.bindValue(":date", QVariant(when))
    logQuery.bindValue(":actionid", QVariant(ACQUIRED)) #ACQUIRED = 1
    logQuery.exec_()
    

    logQuery.bindValue(":assetid", QVariant(assetid))
    when = when.addDays(random.randint(1, 1500))
    logQuery.bindValue(":date", QVariant(when))
    logQuery.bindValue(":actionid",
                            QVariant(random.choice((2, 4))))
    logQuery.exec_()
    
    # if you need to add more than one asset, you need to add:
    # assetid += 1
        
    QApplication.processEvents()
    
    
    # below is not data related, but just to display the inserted values in shell:
    print "Assets:"
    query.exec_("SELECT id, name, categoryid, room FROM assets "
                "ORDER by id")
    categoryQuery = QSqlQuery()
    while query.next():
        id = query.value(0).toInt()[0]
        name = unicode(query.value(1).toString())
        categoryid = query.value(2).toInt()[0]
        room = unicode(query.value(3).toString())
        categoryQuery.exec_(QString("SELECT name FROM categories "
                                    "WHERE id = %1").arg(categoryid))
        category = "%d" % categoryid
        if categoryQuery.next():
            category = unicode(categoryQuery.value(0).toString())
        print "%d: %s [%s] %s" % (id, name, category, room)
    QApplication.processEvents()

