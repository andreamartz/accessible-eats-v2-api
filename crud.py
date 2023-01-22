"""CRUD operations."""

from model import db, User, Business, Feedback, connect_to_db

# **************************
# CREATE FUNCTIONS
# **************************

def create_user(first_name, last_name, username, password):
    """Create and return a new user."""

    user = User(first_name=first_name,
                last_name=last_name,
                username=username,
                password=password)

    return user


def create_business(yelp_id, 
                    business_name,
                    address1,
                    city,
                    state,
                    zip_code,
                    display_phone,
                    photo):
    """Create and return a new business."""

    business = Business(yelp_id=yelp_id,
                        business_name=business_name,
                        address1=address1,
                        city=city,
                        state=state,
                        zip_code=zip_code,
                        display_phone=display_phone,
                        photo=photo)

    return business


def create_feedback(user_id, business_id, chair_parking, ramp, auto_door, comment):
    """Create and return a new business."""

    feedback = Feedback(user_id=user_id,
                        business_id=business_id,
                        chair_parking=chair_parking,
                        ramp=ramp,
                        auto_door=auto_door,
                        comment=comment)

    return feedback



if __name__ == "__main__":
    from server import app

    connect_to_db(app)