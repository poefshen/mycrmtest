# addtional knowledget:

    floors = range(1, 12) + range(14, 28)
    monitors = (('17" LCD Monitor', 1),
                ('20" LCD Monitor', 1),
                ('21" LCD Monitor', 1),
                ('21" CRT Monitor', 1),
                ('24" CRT Monitor', 1))

random.choice(floors)
random.randint(1, 62)
random.choice(monitors)
random.randint(7, 1500)

today = QDate.currentDate()
when = today.addDays(-random.randint(7, 1500))

filename = os.path.join(os.path.dirname(os.__file__), "assets.db")
# set path+file 
