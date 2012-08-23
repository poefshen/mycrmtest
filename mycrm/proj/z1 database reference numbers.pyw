# Constants

ID = 0
NAME = ASSETID = 1
CATEGORYID = DATE = DESCRIPTION = 2
ROOM = ACTIONID = 3

ACQUIRED = 1


# table details
# "id" is default, there is no need to set related values
actions - id / 1.name / 2.description
categories - id / 1.name / 2.description
assets - id / 1.name / 2.categoryid(ref categories) / 3.room / 
logs - id / 1.assetid (ref assets)/ 2.date / 3.actionid (ref actions) 
