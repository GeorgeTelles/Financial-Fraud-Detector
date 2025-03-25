import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()
np.random.seed(42)

NUM_USERS = 2500
TRANS_PER_USER_MIN = 4
TRANS_PER_USER_MAX = 15
FILENAME = "transactions.xlsx"

users = [{
    "user_id": f"USR{str(i).zfill(5)}",
    "home_country": fake.country_code(),
    "primary_device": fake.user_agent(),
    "average_amount": np.random.lognormal(mean=4.5, sigma=1.2)
} for i in range(NUM_USERS)]

countries = ['US', 'CA', 'GB', 'FR', 'DE', 'BR', 'RU', 'CN', 'JP', 'MX']
categories = ['Electronics', 'Retail', 'Travel', 'Services', 'Groceries']

def generate_user_transactions(user):
    num_trans = np.random.randint(TRANS_PER_USER_MIN, TRANS_PER_USER_MAX)
    transactions = []
    
    for _ in range(num_trans):
        timestamp = fake.date_time_between(start_date="-180d", end_date="now")
        
        transaction = {
            "transaction_id": f"TX{fake.unique.random_number(digits=8)}",
            "timestamp": timestamp,
            "user_id": user['user_id'],
            "amount": round(abs(np.random.normal(user['average_amount'], user['average_amount']/3))), 
            "merchant": fake.company(),
            "category": np.random.choice(categories, p=[0.15, 0.35, 0.1, 0.25, 0.15]),
            "country": user['home_country'] if np.random.rand() > 0.1 else np.random.choice(countries),
            "device": user['primary_device'] if np.random.rand() > 0.05 else fake.user_agent(),
            "ip": fake.ipv4(),
            "is_fraud": 0 
        }
        
        transactions.append(transaction)
    
    return transactions

# Generate all transactions
all_transactions = []
for user in users:
    all_transactions.extend(generate_user_transactions(user))

df = pd.DataFrame(all_transactions)

# Simulate hidden fraud patterns
fraud_mask = (
    (df['amount'] > df.groupby('user_id')['amount'].transform('mean') * 4) |
    (df['country'] != df.groupby('user_id')['country'].transform('first')) |
    (df['device'].str.contains('Unknown|Emulator')) |
    (df['category'].isin(['Travel', 'Electronics']))
) & (np.random.rand(len(df)) < 0.02)  # Random noise

df['is_fraud'] = np.where(fraud_mask, 1, 0)

# Reorder and save
df = df.sort_values(['user_id', 'timestamp']).reset_index(drop=True)
df.to_excel(FILENAME, index=False)

print(f"Dataset generated: {FILENAME}")
print(f"Statistics:\n{df['is_fraud'].value_counts(normalize=True)}")
print(f"User example:\n{df[df['user_id'] == 'USR00042'][['timestamp', 'amount', 'category', 'is_fraud']]}")