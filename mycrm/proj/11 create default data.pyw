def createDefaultData():

    print "Populating tables..."
    # 
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Acquired', 'When installed')")
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Broken', 'When failed and unusable')")
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Repaired', 'When back in service')")
    query.exec_("INSERT INTO actions (name, description) "
                "VALUES ('Routine maintenance', "
                "'When tested, refilled, etc.')")
    query.exec_("INSERT INTO categories (name, description) VALUES "
                "('Computer Equipment', "
                "'Monitors, System Units, Peripherals, etc.')")
    query.exec_("INSERT INTO categories (name, description) VALUES "
                "('Furniture', 'Chairs, Tables, Desks, etc.')")
    query.exec_("INSERT INTO categories (name, description) VALUES "
                "('Electrical Equipment', 'Non-computer electricals')")
                
