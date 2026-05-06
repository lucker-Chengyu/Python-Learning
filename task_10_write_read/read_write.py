def add_log(filename, entry):
    with open(filename,"a") as f:
        f.write(entry+"\n")

def filter_errors(source, destination):
    with open(source, "r") as src, open(destination, "w") as dst:
        for line in src:
            if "ERROR" in line:
                dst.write(f"{line.strip()} [FLAGGED]\n")

def add_item(filename, item, quantity):
    with open(filename,"a") as f:
        f.write(f"{item}: {quantity}\n")

def extract_vip(source, destination):
    with open(source, "r") as src, open(destination, "w") as dst:
        for line in src:
            if "VIP" in line:
                dst.write(f"*** {line}")

# import re
# content = re.findall(r"\d{3}", text)
# content = re.findall(r"ID-\d{2,}", text)
# content = re.findall(r"[A-Z]\d{2}", text)
# content = re.findall(r"[A-Z][3]", text)
# content = re.findall(r"Pass-/d{4,}", text)
# content = re.findall(r"[A-Z][2]/d{2}", text)
import re
def extract_usernames(text):
    usernames = re.findall(r"([a-z0-9]+)@", text)
    return usernames

def extract_plates(text):
    return re.findall(r"[A-Z]{2}-\d{4}", text)

def extract_products(text):
    return re.findall(r"PRD-[A-Z]\d{3,}",text)

import pandas as pd
def count_cities(data):
    df = pd.DataFrame(data)
    return df["city"].value_counts()

def get_high_scores(data, threshold):
    df = pd.DataFrame(data)
    return df[df["score"]> threshold]["name"].tolist()

def city_avg_temp(data, city):
    df = pd.DataFrame(data)
    return round(df[df["city"] == city]["temp"].mean(),2)


class Book:
    MAX_PAGES = 1000
    def __init__(self, title, pages):
        self.title = title

        if pages < 1:
            self.pages = 1
        elif pages > Book.MAX_PAGES:
            self.pages = Book.MAX_PAGES
        else:
            self.pages = pages
    def summary(self):
        return f"{self.title} has {self.pages} pages"


class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.balance = balance
        if balance < 0:
            self.balance = 0
    def deposit(self, amount):
        self.balance += amount
        return f"Deposited {amount}. Balance: {self.balance}"
    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            return f"Withdrew {amount}. Balance: {self.balance}"
        else:
            return f"Insufficient funds. Balance: {self.balance}"















































