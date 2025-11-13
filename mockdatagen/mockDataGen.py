import pandas as pd
import numpy as np
from faker import Faker


def generate_retail_data(num_rows=500):
    fake = Faker()
    np.random.seed(42)

    # Generate Customers
    customers = pd.DataFrame({
        'customer_id': [f'CUST{i:04d}' for i in range(num_rows)],
        'first_name': [fake.first_name() for _ in range(num_rows)],
        'last_name': [fake.last_name() for _ in range(num_rows)],
        'email': [fake.email() for _ in range(num_rows)],
        'phone_number': [fake.phone_number() for _ in range(num_rows)],
        'address': [fake.address().replace('\n', ', ') for _ in range(num_rows)],
        'city': [fake.city() for _ in range(num_rows)],
        'state': [fake.state() for _ in range(num_rows)],
        'country': [fake.country() for _ in range(num_rows)],
        'zip_code': [fake.zipcode() for _ in range(num_rows)],
        'gender': np.random.choice(['Male', 'Female', 'Other'], num_rows),
        'birth_date': [fake.date_of_birth(minimum_age=18, maximum_age=70) for _ in range(num_rows)],
        'signup_date': [fake.date_this_decade() for _ in range(num_rows)],
        'customer_segment': np.random.choice(['Silver', 'Gold', 'Platinum'], num_rows),
        'loyalty_points': np.random.randint(100, 10000, num_rows),
        'is_active': np.random.choice([True, False], num_rows, p=[0.8, 0.2]),
        'preferred_channel': np.random.choice(['Email', 'SMS', 'Phone'], num_rows),
        'referral_code': [fake.uuid4()[:8] for _ in range(num_rows)],
        'occupation': [fake.job() for _ in range(num_rows)],
        'marital_status': np.random.choice(['Single', 'Married', 'Divorced'], num_rows)
    })

    # Generate Sales
    sales = pd.DataFrame({
        'sale_id': [f'SALE{i:04d}' for i in range(num_rows)],
        'customer_id': np.random.choice(customers['customer_id'], num_rows),
        'sale_date': [fake.date_this_year() for _ in range(num_rows)],
        'product_id': [fake.ean(length=8) for _ in range(num_rows)],
        'product_name': [fake.word().title() for _ in range(num_rows)],
        'product_category': np.random.choice(['Electronics', 'Clothing', 'Home', 'Books'], num_rows),
        'unit_price': np.round(np.random.uniform(10, 500, num_rows), 2),
        'quantity': np.random.randint(1, 5, num_rows),
        'discount': np.round(np.random.uniform(0.0, 0.3, num_rows), 2),
        'payment_method': np.random.choice(['Credit Card', 'PayPal', 'Cash', 'Bank Transfer'], num_rows),
        'store_location': [fake.city() for _ in range(num_rows)],
        'sales_rep': [fake.name() for _ in range(num_rows)],
        'channel': np.random.choice(['Online', 'In-store'], num_rows),
        'is_returned': np.random.choice([True, False], num_rows, p=[0.05, 0.95]),
        'feedback_score': np.random.randint(1, 6, num_rows),
        'coupon_used': np.random.choice([True, False], num_rows),
        'device_used': np.random.choice(['Mobile', 'Desktop', 'Tablet'], num_rows),
        'promotion_code': [fake.bothify(text='PROMO-###') for _ in range(num_rows)],
        'region': np.random.choice(['North', 'South', 'East', 'West'], num_rows),
        'currency': np.random.choice(['USD', 'SGD', 'INR'], num_rows)
    })

    # Compute derived fields
    sales['total_price'] = sales['unit_price'] * sales['quantity']
    sales['final_price'] = sales['total_price'] * (1 - sales['discount'])

    # Generate Transactions
    transactions = pd.DataFrame({
        'transaction_id': [f'TXN{i:04d}' for i in range(num_rows)],
        'sale_id': np.random.choice(sales['sale_id'], num_rows),
        'txn_date': [fake.date_this_year() for _ in range(num_rows)],
        'txn_amount': np.round(np.random.uniform(10, 1500, num_rows), 2),
        'txn_currency': np.random.choice(['USD', 'SGD', 'INR', 'EUR'], num_rows),
        'txn_type': np.random.choice(['Purchase', 'Refund'], num_rows),
        'card_type': np.random.choice(['Visa', 'MasterCard', 'AMEX', 'UPI'], num_rows),
        'card_last4': np.random.randint(1000, 9999, num_rows),
        'txn_status': np.random.choice(['Success', 'Failed', 'Pending'], num_rows),
        'is_fraud': np.random.choice([False, True], num_rows, p=[0.98, 0.02]),
        'processing_time_sec': np.random.randint(1, 120, num_rows),
        'bank_name': [fake.company() for _ in range(num_rows)],
        'approval_code': [fake.bothify(text='APPROVE###') for _ in range(num_rows)],
        'txn_medium': np.random.choice(['POS', 'Online', 'Mobile App'], num_rows),
        'ip_address': [fake.ipv4() for _ in range(num_rows)],
        'location': [fake.city() for _ in range(num_rows)],
        'device_id': [fake.uuid4()[:12] for _ in range(num_rows)],
        'is_contactless': np.random.choice([True, False], num_rows),
        'reward_applied': np.random.choice([True, False], num_rows),
        'remarks': [fake.sentence(nb_words=6) for _ in range(num_rows)]
    })

    return customers, sales, transactions
