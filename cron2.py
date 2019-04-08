

class Cron():

    def __init__(self):

        from crontab import CronTab

        self.cron = CronTab('zanea')

    def add_cron(self):

        job = self.cron.new(command="echo 'peokpokpok' > bla.log")
        job.minute.every(1)
        self.cron.write()
        return True



instance = Cron()

instance.add_cron()