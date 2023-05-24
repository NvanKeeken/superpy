import csv
import pandas as pd
from sell import add_sold_product
from advance import get_date_file , get_date_Format
from convert import make_table_from_csv
import datetime
from rich.console import Console

console= Console()
# This file contains all the functions related to the report inventory CLI argument
def reset_inventory():
    with open("Invent.csv", "w") as file:
        writer = csv.writer(file)
        writer.writerow(["Product Name", "Count", "Buy Price", "Expiration Date"])

def add_to_csv(path, item):
       with open(path, "a", newline="") as file:
           writer = csv.writer(file)
           writer.writerow(item)

def show_Inventory():
     make_table_from_csv()
        # df = pd.read_csv("Invent.csv")
        # print(df)

         
def is_inStock(product_name,price, amount, expiration_date):
    with open("Invent.csv", "r") as file:
        reader = csv.DictReader(file)
        from expired import expiration_check
        is_in_stock = False
        for row in reader:
            if row["Product Name"] == product_name and row["Expiration Date"] == expiration_date:
                if int(row["Count"]) == int(amount):
                    is_in_stock = True
                    delete_product(row)
                    print("delete")
                if int(row["Count"]) > 0 and int(row["Count"]) >= int(amount):
                    is_in_stock = True
                    update_count_inventory(product_name,"sold",expiration_date, amount)
                    is_in_stock = True
                if expiration_check(row):
                    console.print("Product(s) are expired", style="bold magenta") 
                    is_in_stock=False
        if is_in_stock:
            add_sold_product(product_name, price, amount, expiration_date)  
        else:
            console.print("Error: product is out of stock", style="red bold")
            

def delete_product(product_row): 
    newLines = []
    with open("Invent.csv", "r+") as inv:
        lines = csv.DictReader(inv)
        for line in lines:
            if line != product_row:
                newLines.append(line)
        reset_inventory()
        for line in newLines:
             product = [line["Product Name"], line["Count"], line["Buy Price"], line["Expiration Date"]]
             add_to_csv("Invent.csv", product)
            #  with open("Invent.csv", "a", newline="") as file:
            #      writer = csv.writer(file)
            #      writer.writerow([line["Product Name"], line["Count"], line["Buy Price"], line["Expiration Date"]])
     
def update_count_inventory(product_name,status,expiration_date, amount = 1): 
    newLines = []
    with open("Invent.csv", "r+") as inv:
        lines = csv.DictReader(inv)
        for line in lines:
            count = int(line["Count"]) - int(amount) if status == "sold" else int(line["Count"]) + int(amount)
            print(expiration_date)
            print("Date",line["Expiration Date"], expiration_date)
            if line["Product Name"] == product_name and line["Expiration Date"]==expiration_date:
                newLines.append(
                    {
                        "Product Name": line["Product Name"],
                        "Count": count,
                        "Buy Price": line["Buy Price"],
                        "Expiration Date": line["Expiration Date"]
                    }
                )
            else:
                newLines.append(line)
        reset_inventory()
        for line in newLines:
             product = [line["Product Name"], line["Count"], line["Buy Price"], line["Expiration Date"]]
             add_to_csv("Invent.csv",product)

# Dit werkt het filterd de producten voor een bepaalde datum
def get_products_before(date, csv_path, product_date ):
     products = []
     format = get_date_Format(date)
     with open(csv_path, "r") as file:
       reader = csv.DictReader(file)
       for row in reader:
         inventorydate = datetime.datetime.strptime(date, format)
         formatted_row_date = datetime.datetime.strptime(row[product_date], "%Y-%m-%d").strftime(format)
         row_date = datetime.datetime.strptime(formatted_row_date, format)
         if row_date <= inventorydate:
            products.append(row)
       return products
# get_date_Format("2023-05-1")
""" calculates al products bought before or on a certain date, and does the same for sold products
if a bought product in that list is also in the sold products list, calculate amount of bought products minus sold products 
if that difference is not zero append it to the new inventory, if bought product is not part of sold product list append it 
as well to the new inventory """
def make_inventory(date):
    sold_products = get_products_before(date, "sold.csv", "sell_date")
    bought_products = get_products_before(date, "bought.csv", "buy_date")
    new_inventory =[]
    for bought_product in bought_products:
            #  sold_id = find_sold_product(bought_product["id"],sold_products, "bought_id")
            #  sold_amount = find_sold_product(bought_product["id"],sold_products, "amount")
             sold_products= find_sold_product(bought_product["id"],date)
             sold_amount = 0
             for product in sold_products:
                # if  bought_product["id"] == product["bought_id"]:
                    sold_amount += int(product["amount"])
                #    amount_difference = int(bought_product["amount"]) - int(sold_amount)
                #    print(amount_difference)
             amount_difference = int(bought_product["amount"]) - sold_amount
             if amount_difference != 0:
                    new_inventory.append(
                    {
                        "Product Name": bought_product["product_name"],
                        "Count": amount_difference,
                        "Buy Price": bought_product["buy_price"],
                        "Expiration Date": bought_product["expiration_date"]
                    })      
             else:
                      new_inventory.append({
                        "Product Name": bought_product["product_name"],
                        "Count": bought_product["amount"],
                        "Buy Price": bought_product["buy_price"],
                        "Expiration Date": bought_product["expiration_date"]
                    }) 
    reset_inventory()
    for line in new_inventory:
        product = [
                line["Product Name"],
                line["Count"],
                line["Buy Price"],
                line["Expiration Date"] ]  
        add_to_csv("Invent.csv",product)

def find_bought_product(id,path,characteristic):
    with open(path, "r") as boughtproduct:
        reader= csv.DictReader(boughtproduct)
        for row in reader:
            if id == row["bought_id"]:
                   return row[characteristic]
            
def find_sold_product(id, date):
        sold_products_before = get_products_before(date, "sold.csv", "sell_date")
        sold_products =[]
        print("hdbhjebjeh",sold_products_before)
        for product in sold_products_before:
            if id == product["bought_id"]:
                print("yes", product, id)
                sold_products.append(product) 
        return sold_products        

def add_to_inventory(product_name, buy_price, expiration_date, status, amount):
       with open("Invent.csv", "r") as file:
           csvreader = csv.DictReader(file)
           is_inStock = False
           for row in csvreader:
               if row["Product Name"] == product_name and row["Expiration Date"] == expiration_date:
                   is_inStock = True
           if is_inStock:
             update_count_inventory(product_name, status,expiration_date,amount)
             
           else:
                
                product =[product_name,amount, buy_price, expiration_date]
                add_to_csv("Invent.csv", product)

def validation_check_date(expected_date_format, date):
    date_format = get_date_Format(date)
    is_date_valid = False
    print(date_format)
    if date_format == expected_date_format:
           print("hello")
           is_date_valid += True
    else:
        is_date_valid += False
        raise ValueError(f"Date needs to be formatted as {expected_date_format}")
    return is_date_valid
    

           

