import os

import pandas as pd
from faker import Faker
import json

fake = Faker('en_US')


def generate_user_profile():
    """Generate a realistic user profile for a web store"""
    profile = {
        "name": fake.name(),
        "email": fake.email(),
        "phone": fake.phone_number(),
        "address": fake.address(),
        "payment_method": fake.credit_card_provider(),
        "order_history": [
            {"order_id": fake.uuid4(), "date": fake.date_between(start_date='-1y').strftime('%Y-%m-%d'), "total": fake.random_int(min=1000, max=10000)}
            for _ in range(fake.random_int(min=0, max=10))]  # Order history
    }
    return profile


# Generate 100 user profiles
user_profiles = [generate_user_profile() for _ in range(100)]


# Convert the data to the dataframe
df = pd.json_normalize(user_profiles, sep='_')

# Save as JSON

cwd = os.getcwd()

file_name = f"{cwd}/user_profiles.json"

with open(file_name, 'w', encoding='utf-8') as f:
    json.dump(user_profiles, f, indent=4, ensure_ascii=False)
