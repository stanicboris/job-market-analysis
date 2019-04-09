from crontab import CronTab

cron = CronTab(user='zanea') 

job = cron.new(command="python test_cron.py 'coucou'", comment='email@adress')

job.minute.every(1) 

cron.write()