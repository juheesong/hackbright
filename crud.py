"""CRUD operations."""

from model import db, User, Creator, UserCreator, Metric, connect_to_db


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)
    return user


def get_user_by_email(email):
    """Return a user by email."""

    return User.query.filter(User.email == email).first()


def create_creator(username):
    """Create and return a new creator."""

    creator = Creator(username=username)
    return creator


def get_creators_for_user(email):
    """Return all creators followed by specific user."""

    user = User.query.filter_by(email=email).first() 

    return user.creators 


def create_association(user_id, creator_id): 
    userCreator = UserCreator(user_id=user_id,
        creator_id=creator_id
    )
    return userCreator 


def follow_creator(email, username): 
    """User follows a new creator"""

    # use email to get the user_ID 
    userinfo = User.query.filter_by(email=email).first() 

    # search for creator 
    creator = Creator.query.filter_by(username=username).first() 

    # if creator exists, append creator to user profile 
    if creator is not None: 
        creator.users.append(userinfo) 
    # else, create creator and THEN append creator to user profile 
    else:
        creator = Creator(username=username)
        creator.users.append(userinfo)  

    return creator 

def unfollow_creator(email, username): 
    """User unfollows creator"""

    # use email to get the user_ID 
    userinfo = User.query.filter_by(email=email).first() 

    # search for creator 
    creator = Creator.query.filter_by(username=username).first() 

    # search for user_creator connection 
    link_id = UserCreator.query.filter_by(user_id=userinfo.user_id, creator_id=creator.creator_id).first() 

    # creator.users.pop(userinfo)  

    return link_id  




def get_creator_by_username(username):
    """Return a creator_id by username."""

    creator = Creator.query.filter_by(username=username).first() 

    return creator

 
def create_metrics(creator_id, dl_date, followers, following, videos, likes):
    """Return a metrics table by username and date."""

    metric = Metric(
            creator_id=creator_id, 
            dl_date=dl_date, 
            followers=followers, 
            following=following, 
            videos=videos, 
            likes=likes
    )
    return metric 

## if creator is in database already: get current metrics and create new entry 
## otherwise, add the creator and then the metrics 

def update_metrics(username, dl_date, followers, following, videos, likes): 
    """Add another row to existing metrics table given creator username"""

    creator = Creator.query.filter_by(username=username).first()
    
    if creator is not None:
        # creator_id = db.session.query(creator.creator_id)
        metrics = Metric(
            creator_id=creator.creator_id, 
            dl_date=dl_date, 
            followers=followers, 
            following=following, 
            videos=videos, 
            likes=likes
        )
        creator.metrics.append(metrics) 
    else:
        new_creator = Creator(username=username)
        # creator_id = db.session.query(new_creator.creator_id)
        metrics = Metric(creator.creator_id, dl_date, followers, following, videos, likes)
        creator.metrics.append(metrics)  

    return metrics

# def monthly_average(username): 
#     """Returns monthly average followers and videos for creator."""

#     creator = Creator.query.filter_by(username=username).first() 

#     for creator.metrics.followers in creator:

def chart_metrics(username):
    """Return averages to display in chart for each creator."""

    creator = Creator.query.filter_by(username=username).first()
    metrics = creator.metrics 

    return metrics 




if __name__ == "__main__":
    from server import app

    connect_to_db(app)
