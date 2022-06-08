"""Server for TikTokTracker app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify 
from model import User, connect_to_db, db
from pprint import pformat 
from jinja2 import StrictUndefined
import crud, os, requests
from datetime import date, datetime 


app = Flask(__name__)
app.secret_key = "tikkytokky"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['X_API_KEY']

@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/registration")
def registration_page():
    """Open registration page."""

    return render_template("registration.html")

@app.route("/register", methods=["POST"])
def register_user():
    """Register a new user."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)
    if user:
        flash("Account with that email already exists. Log in or use a different email.")
    else:
        user = crud.create_user(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect('/')


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""
    
    email = request.form.get("email")
    password = request.form.get("password")

    user = crud.get_user_by_email(email)

    if not user or (user.password != password):
        flash(f"Email and password combo incorrect. Register or try again.") 
        return redirect ("/") 
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        # flash(f"Welcome back, {user.email}!")
        return redirect('/users_index')

@app.route('/logout')
def logout():
    session.clear()
    return redirect ('/')

@app.route('/search')
def show_search_form(): 
    """Show the search form after logging in."""

    if "user_email" in session: 
        email = session["user_email"] 
        # flash("Account is logged in.")
    else: 
        flash("Please log in.")
        return redirect ("/") 

    user = crud.get_user_by_email(email)

    return render_template('search_form.html', user=user)

@app.route('/creators/search')
def find_creators():
    """Search for creators on TikTok"""

    username = request.args.get('username', '')
    email = session["user_email"]

    url = 'https://api.tikapi.io/public/check'
    payload = {'username': username}

    headers = {'X-API-KEY': API_KEY}
    # https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers

    response = requests.get(url, params=payload, headers=headers)
    data = response.json()

    dl_date= datetime.now() 

    creators = crud.get_creators_for_user(email)
    user = crud.get_user_by_email(email)

    return render_template('search_results.html',
                           data=data, dl_date=dl_date, creators=creators, user=user)


@app.route('/creators/add') 
def follow_creator(): 
    """User adds creator --> users_creators link."""
    """Logic checks: 1/ if creator already exists, just add users_creators row."""
    """2/ if creator does not exist, create Creator, Metric, and users_creators."""

    username = request.args.get('username', '')
    email = session["user_email"]

    follow = crud.follow_creator(email, username)
    db.session.add(follow)
    db.session.commit()

    url = 'https://api.tikapi.io/public/check'
    payload = {'username': username}

    headers = {'X-API-KEY': API_KEY}
    # https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers

    response = requests.get(url, params=payload, headers=headers)
    data = response.json()

    dl_date= datetime.now() 
    username = data['userInfo']['user']['uniqueId']
    followers = data['userInfo']['stats']['followerCount'] 
    following = data['userInfo']['stats']['followingCount']
    videos = data['userInfo']['stats']['videoCount'] 
    likes = data['userInfo']['stats']['heartCount']

    metric = crud.update_metrics(username, dl_date, followers, following, videos, likes)
    db.session.add(metric)
    db.session.commit() 

    creator = crud.get_creator_by_username(username)

    return redirect('/users_index')

@app.route('/creators/remove') 
def unfollow_creator(): 

    username = request.args.get('username', '')
    email = session["user_email"]

    creators = crud.get_creators_for_user(email) 

    unfollow = crud.unfollow_creator(email, username)
    db.session.delete(unfollow)
    db.session.commit()

    creators = crud.get_creators_for_user(email) 

    return redirect('/users_index')

@app.route('/users_index')
def user_details():
    """View details for a user (creator list)."""

    email = session["user_email"]
    creators = crud.get_creators_for_user(email) 

    return render_template('all_creators_index.html', creators=creators)


@app.route('/creators/<username>')
def creator_details(username): 
    """Display details for creator."""

    creator = crud.get_creator_by_username(username)

    if creator is None:
        return redirect ('/update')
    else:
        return render_template('creator_details.html', creator=creator)

@app.route('/update')
def update_one_creator():
    """"Update and display metrics for one creator."""

    username = request.args.get('username', '')
    # username = 'creator3'
    email = session["user_email"]
    # creators = crud.get_creators_for_user(email)

    print(username, "\n\n\n\n\njlkdlksjdflkjssldkjflksjdflskdjflskdfjlskdfjlskdfjslkdfj********************")


    url = 'https://api.tikapi.io/public/check'
    payload = {'username': username}

    headers = {'X-API-KEY': API_KEY}
    # https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers

    response = requests.get(url, params=payload, headers=headers)
    data = response.json()
    dl_date= datetime.now() 
    # username = data['userInfo']['user']['uniqueId']
    followers = data['userInfo']['stats']['followerCount'] 
    following = data['userInfo']['stats']['followingCount']
    videos = data['userInfo']['stats']['videoCount'] 
    likes = data['userInfo']['stats']['heartCount']

    metric = crud.update_metrics(username, dl_date, followers, following, videos, likes)
    db.session.add(metric)
    db.session.commit() 

    return {'username' : username, 'followers' : followers, 'following': following, 'videos' : videos, 'likes': likes }


@app.route('/update_all')
def update_all_creators():
    """"Update and display metrics for all creators followed by user."""

    # get all the creators for the user and loop it 

    # username = request.args.get('username', '')
    email = session["user_email"]
    creators = crud.get_creators_for_user(email)
    print(creators, "*******************")
    
    for creator in creators: 

        username = creator.username 
        url = 'https://api.tikapi.io/public/check'
        payload = {'username': username}

        headers = {'X-API-KEY': API_KEY}
        # https://docs.python-requests.org/en/latest/user/quickstart/#custom-headers

        response = requests.get(url, params=payload, headers=headers)
        data = response.json()

        dl_date= datetime.now() 
        # username = data['userInfo']['user']['uniqueId']
        followers = data['userInfo']['stats']['followerCount'] 
        following = data['userInfo']['stats']['followingCount']
        videos = data['userInfo']['stats']['videoCount'] 
        likes = data['userInfo']['stats']['heartCount']

        metric = crud.update_metrics(username, dl_date, followers, following, videos, likes)
        db.session.add(metric)
        db.session.commit() 

    return {'username' : username, 'followers' : followers, 'following': following, 'videos' : videos, 'likes': likes }

@app.route("/metrics.json/<username>")
def get_metrics(username): 
    """Get all metrics for one creator this year"""

    creator = crud.get_creator_by_username(username)
    metrics = crud.chart_metrics(username)  

    
    metrics_cy = []
    for metric in metrics: 
        ## do any mathy here OR in the crud make GROUPBYs 

        # [{% for videos in data.data %} 
        #       {{videos}},
        #     {% endfor %} ],


        metrics_cy.append({'followers': metric.followers,
                                'videos': metric.videos, 
                                'date': metric.dl_date})

    return jsonify({'data': metrics_cy})




@app.route("/about")
def about():
	"""Show author info."""

	return render_template("main.html")

if __name__ == '__main__':
    app.debug = True
    connect_to_db(app)
    app.run(host='0.0.0.0')

