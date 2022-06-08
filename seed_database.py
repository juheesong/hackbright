"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import crud
import model
import server

os.system("dropdb metrics")
os.system("createdb metrics")

model.connect_to_db(server.app)
model.db.create_all()


# Create 5 users
for n in range(1, 6):
    email = f"user{n}@wally.com"  # Voila! A unique email!
    password = "smalls"

    user = crud.create_user(email, password)
    model.db.session.add(user)
    model.db.session.commit()

# Create my account
email = "juheesong@gmail.com"
password = "hackbright" 

user = crud.create_user(email, password)
model.db.session.add(user) 
model.db.session.commit()


# Create 5 creators 
for n in range(1, 6):
    username = f"creator{n}" 

    creator = crud.create_creator(username)
    model.db.session.add(creator)
    model.db.session.commit()

# Create metrics table for each creator (5) 
for num in range(1, 6): 
    
    dl_date = datetime(2022, 5, 1)
    creator_id = num
    followers = randint(1, 100) 
    following = randint(1, 100)  
    videos = randint(1, 100) 
    likes = randint(1, 100)   

    metric = crud.create_metrics(creator_id, dl_date, followers, following, videos, likes)
    model.db.session.add(metric) 
    model.db.session.commit()

# add additional row to metrics table
# for num in range (1,6):

#     dl_date = datetime(2022, 5, 2)



# associate user_id1 with creator1 
for num in range(1, 6): 
    
    userCreator = crud.create_association(num, num) 
    model.db.session.add(userCreator) 
    model.db.session.commit()