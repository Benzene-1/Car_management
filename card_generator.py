import random
import string
import datetime

# Generate a unique id
id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

# Generate a dummy card number
card_number = ''.join(random.choices(string.digits, k=16))

# Generate a dummy card holder name
card_holder = 'John Doe'

# Generate a dummy expiry date
expiry_date = (datetime.date.today() + datetime.timedelta(days=random.randint(365, (365*random.randint(1,10))))).strftime('%m/%y')

# Generate a dummy CVV
cvv = ''.join(random.choices(string.digits, k=3))

# Generate a unique user id
user_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

print(f"id: {id}")
print(f"card_number: {card_number}")
print(f"card_holder: {card_holder}")
print(f"expiry_date: {expiry_date}")
print(f"cvv: {cvv}")
print(f"user_id: {user_id}")