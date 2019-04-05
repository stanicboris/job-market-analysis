

class Cron():

    def __init__(self):

        from crontab import CronTab

        self.cron = CronTab('zanea')

    def add_cron(self,email,locations,metiers):

        job = self.cron.new(command="python3 /home/zanea/Projets/job-market-analysis/run_test.py " + locations + metiers  + email,comment=email)
        job.days.every(1)
        self.cron.write()
        return True



instance = Cron()

instance.add_cron('anthony.93460@gmail.com','paris','jardinier')