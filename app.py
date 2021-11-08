from flask import Flask, request
from flask.templating import render_template
from bs4 import BeautifulSoup
import requests

app = Flask(__name__, template_folder='static')

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/search_results', methods = ['POST', 'GET'])
def result():
    data = request.args['search']
    course = data
    url = f"https://www.study.eu/search?utf8=%E2%9C%93&page=1&sort=recommended&search={course}&degreelevel=bachelor&countries=&tuition_eea_min=0&tuition_eea_max=40000&currency=EUR&tuition_term=annual&tuition_region=eea&duration_months_min=0&duration_months_max=72"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    get = soup.find_all('li')
    z = [y.text.replace('\n', '') for y in get]
    q = []
    extras = ['Study.eu', 'Search', 'Active search filters:']
    for a in extras:
        z.remove(a)
    for n in z:
        q.append(' '.join(n.strip().replace('\xa0', ' ').split()).replace(' Learn more', ''))
    q.remove(q[0])
    q.remove(q[0])
    if q:
        q.pop()
        for x in range(6):
            if q:
                q.pop()
    return render_template('search_results.html', search = data, results = q, url = url)

@app.route('/about', methods = ['POST', 'GET'])
def about():
    return render_template('about.html')

@app.route('/recommendation', methods = ['POST', 'GET'])
def recommendation():
    return render_template('recommendation.html')

@app.route('/recommend_results', methods = ['POST', 'GET'])
def recommend_results():
    sci = math = hist = geo = psy = eco = comp = 0
    count = None
    subs = ['Science', 'Mathematics', 'Psychology', 'History', 'Geography', 'Economics', 'Computer Science']
    score = []

    study = request.form.get('inputStudy')
    prof = request.form.get('inputProf')
    book = request.form.get('inputBook')
    goal = request.form.get('inputGoal')
    country = request.form.get('inputCountry')
    if study == "sci":
        sci+=1
    elif study == "psy":
        psy+=1
    elif study == "math":
        math+=1
    elif study == "comp":
        comp+=1
    elif study == "hist":
        hist+=1
    elif study == "geo":
        geo+=1
    elif study == "eco":
        eco+=1
    
    if prof == "psy":
        psy+=1
    elif prof == "sci":
        sci+=1
    elif prof == "math":
        math+=1
    elif prof == "eco":
        eco+=1
    elif prof == "hist":
        hist+=1
    elif prof == "geo":
        geo+=1
    elif prof == "comp":
        comp+=1
    
    if book == "comp math":
        comp+=1
        math+=1
    elif book == "sci hist geo":
        sci+=1
        hist+=1
        geo+=1
    elif book == "eco":
        eco+=1
    elif book == "psy":
        psy+=1

    if goal == "comp math sci":
        comp+=1
        math+=1
        sci+=1
    elif goal == "hist geo":
        hist+=1
        geo+=1
    elif goal == "eco":
        eco+=1
    elif goal == "psy":
        psy+=1
    
    score.append(sci)
    score.append(math)
    score.append(psy)
    score.append(hist)
    score.append(geo)
    score.append(eco)
    score.append(comp)

    val = max(math, sci, psy, hist, geo, comp, eco)
    for i in list(zip(subs, score)):
        if i[1] == val:
            choice = i[0]

    location = country
    course = choice
    url = f"https://www.study.eu/search?utf8=%E2%9C%93&page=1&sort=recommended&search={course}&degreelevel=bachelor&countries={location}&tuition_eea_min=0&tuition_eea_max=40000&currency=EUR&tuition_term=annual&tuition_region=eea&duration_months_min=0&duration_months_max=72"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, 'html.parser')
    get = soup.find_all('li')
    z = [y.text.replace('\n', '') for y in get]
    q = []
    extras = ['Study.eu', 'Search', 'Active search filters:']
    for a in extras:
        z.remove(a)
    for n in z:
        q.append(' '.join(n.strip().replace('\xa0', ' ').split()).replace(' Learn more', ''))
    q.remove(q[0])
    q.remove(q[0])
    q.remove(q[0])
    if q:
        q.pop()
        for x in range(6):
            if q:
                q.pop()
    c = 0
    for i in score:
        if i!=0:
            c+=1
    if c == 0:
        score = False
    else:
        score = True
    return render_template('recommend_results.html', data = score, search = choice, results = q, url = url, countries = book)

if __name__ == '__main__':
    app.run(debug = True)