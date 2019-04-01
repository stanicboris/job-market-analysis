from crontab import CronTab

cron = CronTab(user='username') 

job = cron.new(command="python test_test.py", comment='email@adress')

job.minute.every(1)

cron.write()