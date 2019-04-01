

class Cron():

    def __init__(self):

        from crontab import CronTab

        self.cron = CronTab('zanea')

    def add_cron(self,email):

        job = self.cron.new(command="python3 /home/zanea/Projets/job-market-analysis/test_cron.py '" + email + "'",comment=email)
        job.minute.every(1)
        self.cron.write()
        return True



instance = Cron()

instance.add_cron('anthony.93460...')