"""Script to seed the database."""

import os
import json
import crud
from random import choice, randint, sample
import model
import server
from fake_data import NUM_USERS

# *******************************
# DROP & CREATE DATABASE
# *******************************

os.system("dropdb accessible-eats-v2")
os.system("createdb accessible-eats-v2")

model.connect_to_db(server.app)
# In newer versions of Flask, must wrap with "with server.app.app_context()"
with server.app.app_context():
    model.db.create_all()

# *******************************
# CREATE USERS
# *******************************

# # Load data from JSON file
with open('data/users.json') as f:
    user_data = json.loads(f.read())

# Create users, store them in list so we can use them
# to create fake feedback later
users_in_db = []
for user in user_data:
    first_name, last_name, username, password = (
        user["first_name"],
        user["last_name"],
        user["username"],
        user["password"]
    )

    # create a user and append it to users_in_db
    db_user = crud.create_user(first_name=first_name,
                               last_name=last_name,
                               username=username,
                               password=password)
    users_in_db.append(db_user)

# see note above about with server.app.app_context()
with server.app.app_context():
    model.db.session.add_all(users_in_db)
    model.db.session.commit()


# *******************************
# CREATE BUSINESSES
# *******************************

# # Load data from JSON file
with open('data/businesses_55438.json') as f:
    business_data = json.loads(f.read())

# Create businesses, store them in list so we can use them
# to create fake feedback later
businesses_in_db = []
for business in business_data:
    business_name, yelp_id, photo, display_phone = (
        business["business_name"],
        business["yelp_id"],
        business["photo"],
        business["display_phone"],
    )
    address1, city, state, zip_code = (
        business["location"]["address1"],
        business["location"]["city"],
        business["location"]["state"],
        business["location"]["zip_code"]
    )

    # create a business and append it to businesses_in_db
    db_business = crud.create_business(yelp_id=yelp_id,
                                       business_name=business_name,
                                       address1=address1,
                                       city=city,
                                       state=state,
                                       zip_code=zip_code,
                                       display_phone=display_phone,
                                       photo=photo)

    businesses_in_db.append(db_business)

with server.app.app_context():
    model.db.session.add_all(businesses_in_db)
    model.db.session.commit()


# *******************************
# CREATE FEEDBACKS
# *******************************
NUM_RATINGS_PER_USER = 10
# Create list of fake feedbacks and add them to the database.
feedbacks_in_db = []
for user_id in range(NUM_USERS):
    user_id += 1
    # Create 10 feedbacks for user with id of user_id
    comments = ["They have handicapped parking spots, but not enough of them.",
                "The men's bathroom did not have large enough stalls to accommodate my chair.",
                "There were no braille signs in or on the building.",
                "I was able to sit at a table, but the waitress scowled about the amount of room my chair occupied.",
                "I have low vision, and the font on the menu was way too small.",
                "There was a ramp to the front door, but it was closed for repair the day I was there.",
                "The front door normally opens automatically, but the automatic feature was broken the day I visited.",]
    
    # choose NUM_RATINGS_PER_USER businesses for this user to rate
    subset_of_business_ids = sample(range(1, 26), NUM_RATINGS_PER_USER)

    for id in subset_of_business_ids:
        business_id = id
        chair_parking = choice([False, False, False, True, True])
        ramp = choice([False, True, True, True])
        auto_door = choice([False, False, True, True, True, True, True])
        comment = choice(comments)

        # create a feedback and append it to feedbacks_in_db
        db_feedback = crud.create_feedback(user_id=user_id,
                                           business_id=business_id,
                                           chair_parking=chair_parking,
                                           ramp=ramp,
                                           auto_door=auto_door,
                                           comment=comment)

        feedbacks_in_db.append(db_feedback)

with server.app.app_context():
    model.db.session.add_all(feedbacks_in_db)
    model.db.session.commit()
