from flask import Flask, render_template, request, redirect, send_file
from parcer import get_jobs
from exporter import save_t0_csv

app = Flask('JobsParces')

db = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/report')
def report():
    keyword = request.args.get('keyword')
    if keyword is not None:
        keyword = keyword.lower()
        getDb = db.get(keyword)
        if getDb:
            jobs = getDb
        if not getDb:
            jobs = get_jobs(keyword)
            db[keyword] = jobs
    if keyword is None:
        return redirect('/')   
    
    return render_template('report.html', searchBy = keyword, resultNumber = len(jobs), jobs=jobs)

@app.route('/export')
def export():
    try:
        keyword =  request.args.get('keyword')
        keyword = keyword.lower()
        jobs = db.get(keyword)
        if not keyword:
            raise Exception()
        save_t0_csv(jobs)
        return send_file('jobs.csv')
    except:
        return redirect('/')
app.run()