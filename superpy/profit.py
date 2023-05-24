import csv
from revenue import get_total_revenue, get_sold_products_per_date

# this file contains all the functions related to the report profit argument 
def calculate_cost_per_product(row):
 costs_per_product = float(row["buy_price"]) * int(row["amount"])
 return costs_per_product

def get_bought_products_by_date(date):
 with open("bought.csv", "r") as soldfile:
        reader = csv.DictReader(soldfile)
        bought_products_by_date = []
        for row in reader:
            print(row["buy_date"])
            if row["buy_date"] == date:
                bought_products_by_date.append(row)
        return bought_products_by_date
 
def find_sold_products(date):
    with open ("bought.csv", "r") as boughtfile:
        reader = csv.DictReader(boughtfile)
        bought_products =[]
        sold_products_by_date = get_sold_products_per_date(date)
        for row in reader:
            for product in sold_products_by_date:
                if product["bought_id"] == row["id"]:
                    bought_products.append(row)
        return bought_products

 
def get_total_costs(date):
        total_costs = 0
        bought_products = find_sold_products(date)
        for row in bought_products:
             total_costs += calculate_cost_per_product(row)
        return total_costs

def calculate_total_profit(date):
    total_revenue = get_total_revenue(date)
    total_costs = get_total_costs(date)
    total_profit = total_revenue - total_costs
    return total_profit
   

