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
    _first = request.form.get('inputIE')
    _second = request.form.get('inputNS')
    _third = request.form.get('inputTF')
    _fourth = request.form.get('inputJP')
    type = _first+_second+_third+_fourth
    url = f'https://www.mbtitest.com/{type}/career-match-jobs'
    page = requests.get(url).content
    soup = BeautifulSoup(page, 'html.parser')
    data = soup.find_all('strong')
    data2 = [str(x) for x in list(data)]
    recommended = []
    for item in data2:
        if len(item.split()) < 4:
            recommended.append(item[11:-9])
    type = type.upper()
    if type == 'INTJ':
        data = 'great!'
    return render_template('recommend_results.html', type = type, data=recommended)

if __name__ == '__main__':
    app.run(debug = True)
