from flask import render_template, request, Flask, url_for
import csv
import difflib

app = Flask(__name__, template_folder = 'static')

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('stdin.html')

@app.route('/out', methods = ['POST', 'GET'])
def result():
    out = request.form
    name = request.form.get('username')
    course = request.form.get('course')
    similar = []
    courseList = orgList = []
    with open('static/courses.csv', 'r', encoding = 'utf-8') as file:
        reader = csv.DictReader(file)
        for i in reader:
            courseList.append(i['course_title'])
            orgList.append(i['course_organization'])
    for j in courseList:
        similar.append(difflib.SequenceMatcher(None, course.lower(), j.lower()).ratio())
    courseContent = dict(zip(similar, courseList))
    organisation = dict(zip(courseList, orgList))
    optProg = sorted(courseContent, reverse=True)
    final = []
    for x in optProg:
        final.append(courseContent[x])
    final = final[0:6]
    org = []
    for y in final:
        org.append(organisation[y])
    k = []
    with open('static/courses.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for a in final:
                if row['course_title'] == a:
                    k.append(row['course_organization'])
    main = list(zip(final, k))
    return render_template('stdout.html', name = name, course = course, seq = main)
if __name__ == '__main__':
    app.run(debug = True)
