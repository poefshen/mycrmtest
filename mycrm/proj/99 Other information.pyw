# I'm using "!!" to locate the items that is not clear to me

# Drop Old Tables
    query = QSqlQuery()
    query.exec_("DROP TABLE assets")
    query.exec_("DROP TABLE logs")
    query.exec_("DROP TABLE actions")
    query.exec_("DROP TABLE categories")
    QApplication.processEvents()
    
# Predefined Data:
import qrc_resources # remember to add pictuers
import os
import sys
import random
from PyQt4.QtCore import *

ID = 0 # These 5 lines are Predefined numbers (Name <-> Column in DB)
NAME = ASSETID = 1
CATEGORYID = DATE = DESCRIPTION = 2
ROOM = ACTIONID = 3
ACQUIRED = 1
