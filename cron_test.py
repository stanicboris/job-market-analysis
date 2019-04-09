from crontab import CronTab

cron = CronTab(user='zanea') 

job = cron.new(command="python test_cron.py 'argument de merde'", comment='email@adress')

job.minute.every(1)

cron.write()