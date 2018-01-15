## HW 1
## SI 364 W18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

## Alex Shell

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"


import requests
import json
import facebook_info
from flask import Flask
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'


@app.route('/class')
def our_class():
    return 'Welcome to SI 364!'




## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

@app.route('/movie/<movietitle>')
def itunes_movie_data(movietitle):
    baseURL = 'https://itunes.apple.com/search'
    params = {'term':str(movietitle), 'entity':'movie'}
    response_obj = requests.get(baseURL, params = params)
    response_dict = json.loads(response_obj.text)
    return str(response_dict)


## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

@app.route('/question')
def get_number():
    number_form = """<!DOCTYPE html>
<html>
<body>
<h1>Please Enter Your Favorite Number In The Box</h1>
<form action = "/answer" method = "POST">
  Favorite Number:<br>
  <input type="number" name="number">
  <br>
  <input type="submit" value="Submit">
</form>
</body>
</html>"""
    return number_form

@app.route('/answer', methods=['POST'])
def double_number():
  if request.method == 'POST':
    number = request.form['number']
    doubled_number = str(int(number) * 2)
    return '<h1>Double Your Favorite Number Is {}</h1>'.format(doubled_number)

## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. (e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.

@app.route('/problem4form', methods=["GET","POST"])
def info_entry():
  info_form = """<!DOCTYPE html>
<html>
<body>
<h1>Get Search For Users On Facebook</h1>
<form action = "/problem4form" method = "POST">
  Input Search Term:<br>
  Search Term: <input type="text" name="search">
  <br>
  Number of Results(select one):<br>
  <input type="checkbox" name="ten" value="10"> 10 Results
  <br>
  <input type="checkbox" name="fifty" value="50"> 50 Results
  <br>
  <input type="checkbox" name="hundred" value="100"> 100 Results
  <br>
  <input type="submit" value="Submit">
</form>
</body>
</html>"""
  if request.method == 'POST':
    if 'ten' in request.form:
      qlimit = request.form['ten']
    if 'fifty' in request.form:
      qlimit = request.form['fifty']
    if 'hundred' in request.form:
      qlimit = request.form['hundred']
    qterm = request.form['search']
    fb_access_token = facebook_info.api_key
    fbURL = 'https://graph.facebook.com/v2.11/search?'
    params = {'q': qterm, 'type':'user', 'limit':qlimit, 'access_token':fb_access_token}
    fb_responseobject = requests.get(fbURL, params=params)
    fb_responsedict = json.loads(fb_responseobject.text)
    name_list = list ()
    for item in fb_responsedict['data']:
      name_list.append(item['name'])

    return info_form + '<p>Names Matching Your Search: {}<p/>'.format(str(name_list))






  return info_form


if __name__ == '__main__':
    app.run(use_reloader=True, debug=True)
