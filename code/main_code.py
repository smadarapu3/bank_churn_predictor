
!apt install postgresql
!service postgresql start

!sudo -u postgres psql -c "CREATE USER eva WITH SUPERUSER PASSWORD 'password'"
!sudo -u postgres psql -c "CREATE DATABASE evadb"

# Commented out IPython magic to ensure Python compatibility.
# %pip install --quiet "evadb[document, forecasting, ludwig]"
# %pip install psycopg2

import evadb
cursor = evadb.connect().cursor()

params = {
    "user": "eva",
    "password": "password",
    "host": "localhost",
    "port": "5432",
    "database": "evadb",
}
query = f"CREATE DATABASE postgres_data WITH ENGINE = 'postgres', PARAMETERS = {params};"
cursor.query(query).df()

cursor.query("""
  USE postgres_data {
    CREATE TABLE IF NOT EXISTS bank_predictor (customer_id INT, credit_score INT, country VARCHAR(20),
    gender VARCHAR(10), age INT, tenure INT, balance FLOAT, num_prods INT, credit_card boolean,
    active_mem boolean, est_salary FLOAT, churn boolean)
  }
""").df()

"""
# Train the Model
Make sure to upload the training data before running this section, and make sure the file path in the following code block is correct

"""

cursor.query("""
  USE postgres_data {
    COPY bank_predictor (customer_id, credit_score, country, gender, age, tenure,
    balance, num_prods, credit_card, active_mem, est_salary, churn)
    FROM '/content/training_data.csv'
    DELIMITER ',' CSV HEADER
  }
""").df()

# OPTIONAL: checks to make sure training data was uploaded and copied successfully
# cursor.query("SELECT * FROM postgres_data.bank_predictor LIMIT 3;").df()

# Train the model
cursor.query("""CREATE OR REPLACE FUNCTION BankPredictor FROM
( SELECT * FROM postgres_data.bank_predictor )
TYPE Ludwig
PREDICT 'churn'
TIME_LIMIT 3600;
""").df()

# OPTIONAL: ensures the prediction model works and compares answers to the training data
# cursor.query("""
# SELECT churn, predicted_churn
# FROM postgres_data.bank_predictor
# JOIN LATERAL BankPredictor(*) AS Predicted(predicted_churn)
# LIMIT 3;
# """).df()

"""# Predict Churn"""

cursor.query("""
  USE postgres_data {
    CREATE TABLE IF NOT EXISTS bank_predictor_input (customer_id INT, credit_score INT, country VARCHAR(20),
    gender VARCHAR(10), age INT, tenure INT, balance FLOAT, num_prods INT, credit_card boolean,
    active_mem boolean, est_salary FLOAT, churn boolean)
  }
""").df()

# USER INPUT HERE

credit_score= "608"      # customer credit score: number from 350-850
country = "Spain"       # choose between France, Germany, or Spain
gender = "Female"          # Male or Female
age = "41"               # number between 18-100
tenure = "1"             # how many years have they been at ABC bank: number between 0-10
balance = "83807"       # current account balance: number between 0-250000
num_prods = "1"          # number of products with ABC bank: number between 1-4
credit_card = "False"     # does the customer have a credit card: boolean
active_mem  = "true"    # is the customer an active member: boolean
est_salary = "112542"     # estimated salary of customer

import random
random.seed(25)
customer_id = str(random.randrange(100,600))

# Deletes previous entries from the table
cursor.query("USE postgres_data {DELETE FROM bank_predictor_input};").df()

statement = """USE postgres_data {
    INSERT INTO bank_predictor_input
    VALUES ("""+customer_id+""","""+credit_score+""",'"""+country+"""','"""+gender+"""',"""+age+""",
"""+tenure+""","""+balance+""","""+num_prods+""",
"""+credit_card+""","""+active_mem+""","""+est_salary+""", false)};"""


cursor.query(statement).df()

# Outputs the data that was just entered
cursor.query("SELECT * FROM postgres_data.bank_predictor_input;").df()

# Run training model on the data, and determine if the customer will stay or leave!
get_data = cursor.query("""SELECT BankPredictor(*) FROM postgres_data.bank_predictor_input;""").df()

print("-----PREDICTION-----")
if (get_data["bankpredictor.churn_predictions"][0]):
  print("The customer is likely to stop using the bank :(")
else:
  print("The customer is likely to keep using the bank :)")
