# -*- coding: utf-8 -*-

from flask import Flask
from flaskext.mysql import MySQL
from flask import request
from flask.ext.cors import CORS, cross_origin
import json


app = Flask(__name__)
mysql = MySQL()

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'devrank'

mysql.init_app(app)
cors = CORS(app)


@app.route('/init')
def init():
	cursor = mysql.connect().cursor()
	cursor.execute("SELECT `job_title` FROM `rank_candidate` WHERE `job_title`<>' ' GROUP BY `job_title` ")
	job_title = list(cursor.fetchall())
	return json.dumps({"job_title": job_title})


@app.route('/search')
def search():
	cursor = mysql.connect().cursor()

	salary = request.args.get('salary')
	special = request.args.get('special')

	# Среднее количетво предложений на кандидата
	cursor.execute("SELECT COUNT(rank_poke.recruiter_id) FROM rank_candidate LEFT JOIN rank_poke ON rank_candidate.id=rank_poke.candidate_id WHERE `salary_min` BETWEEN 0 AND {0} AND rank_candidate.job_title='{1}' GROUP BY rank_poke.recruiter_id".format(salary, special))
	recruiter_jobs = cursor.fetchall()

	cursor.execute("SELECT COUNT(*) FROM rank_candidate WHERE `salary_min` BETWEEN 0 AND {0} AND rank_candidate.job_title='{1}'".format(salary, special))
	candidate_count = cursor.fetchone()[0]
	sum_jobs_procent_deals = 0.0
	sum_jobs = sum([item[0] for item in recruiter_jobs])
	
	if candidate_count:
		sum_jobs_procent_deals = float(sum_jobs / candidate_count)
	else:
		sum_jobs_procent_deals = 0

	stats_candidate_deals = [candidate_count, sum_jobs_procent_deals]

	# ТОП наиболее активных работодателей на Джинне
	cursor.execute("SELECT `recruiter_id`,rank_recruiter.*, COUNT(*) AS recruiter FROM rank_poke LEFT JOIN rank_recruiter ON rank_recruiter.id=rank_poke.recruiter_id GROUP BY `recruiter_id` ORDER BY recruiter DESC LIMIT 3")
	stats_top = list(cursor.fetchall())

	# Примеры самых успешных профилей на Джинне
	cursor.execute("SELECT * FROM `rank_recruiter` ORDER BY RAND() LIMIT 0,5")
	stats_popular = list(cursor.fetchall())

	return json.dumps({"stats_popular": stats_popular, "stats_top": stats_top, "stats_candidate_deals": stats_candidate_deals})

if __name__ == '__main__':
	app.debug = True
	app.run()