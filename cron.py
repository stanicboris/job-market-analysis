

class Cron():

    def __init__(self):

        from crontab import CronTab

        self.cron = CronTab('zanea') 

    def add_cron(self,locations,metiers,email):

        job = self.cron.new(command="python3 /usr/local/bin/ipython /home/zanea/Projets/job-market-analysis/run_test.py " + "'" + locations + "' '" + metiers  + "' '" + email + "'" + " > /home/zanea/Projets/job-market-analysis/cron.log 2>&1" , comment=email)
        job.hour.every(4)
        self.cron.write()
        return True 



instance = Cron()

instance.add_cron('[Paris,Nantes,Bordeaux,Toulouse,Lyon]','Data Scientist, Data Analyst, Data Engineer, Business intelligence','anthony.93460@gmail.com')