"""Generate fake data."""

import json
from faker import Faker
import werkzeug.security

fake = Faker()
Faker.seed(0)

NUM_USERS = 50
def generateUsers():
    """Generate users for db."""
    # first_names = []
    # last_names = []
    usernames = []
    passwords = []
    users = []
    first_names = [fake.unique.first_name() for i in range(NUM_USERS)]
    last_names = [fake.unique.last_name() for i in range(NUM_USERS)]
    usernames = []

    for i in range(NUM_USERS):
        # first_name = fake.first_name()
        # last_name = fake.last_name()
        hashed_pw = werkzeug.security.generate_password_hash(f'{last_names[i]}1')

        user = {"first_name": first_names[i],
                "last_name": last_names[i],
                "username": f'{first_names[i]}1',
                "password": hashed_pw,
                # "password": f'{last_names[i]}1',
                }
        users.append(user)

    return json.dumps(users)

print(generateUsers())