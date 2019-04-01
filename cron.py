from crontab import CronTab

cron = CronTab(user=True)
job = cron.new('python3 /home/zanea/Projets/job-market-analysis/test_cron.py')
job.minute.every(1)
cron.write()





