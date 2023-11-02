# Bank Churn Predictor 

An app that takes in data about a fictional person from the user and then predicts the likelihood that the person will continue using the services of the fictional ABC bank. This is called churn, and it is a measure of customer loyalty towards a business. Although this app is tailored towards bank churn, this information is valuable to businesses in all sectors as they are all motivated to reduce churn rate and increase customer loyalty. As maintaining existing customers is usually cheaper than attracting new ones, strong customer loyalty is very important to businesses and is a key factor in determining their growth and profitability. By learning what makes customers more likely to stop using their services, a company can make changes to their product to encourage them to stay. 

# Setup And Running 
Ensure all libraries are installed by running `pip install -r requirements.txt` <br> Navigate to `code/main_code.py` and scroll until you see the following code: 
```
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
```
Enter your desired features, and then run `python main_code.py`

