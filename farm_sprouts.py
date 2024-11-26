import pandas as pd
import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Step 1: Establish a connection to the SQLite database
conn = sqlite3.connect('farm_erp.db')
cursor = conn.cursor()

# Step 2: Create tables if not already created
cursor.execute("""
CREATE TABLE IF NOT EXISTS Crops (
    CropID INTEGER PRIMARY KEY,
    Name TEXT,
    Season TEXT,
    Acreage REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Production (
    EntryID INTEGER PRIMARY KEY,
    CropID INTEGER,
    Date TEXT,
    Quantity REAL,
    Grade TEXT,
    FOREIGN KEY(CropID) REFERENCES Crops(CropID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Sales (
    SaleID INTEGER PRIMARY KEY,
    CropID INTEGER,
    Quantity REAL,
    Price REAL,
    Buyer TEXT,
    FOREIGN KEY(CropID) REFERENCES Crops(CropID)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Resources (
    ResourceID INTEGER PRIMARY KEY,
    Name TEXT,
    Type TEXT,
    Stock REAL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS Expenses (
    ExpenseID INTEGER PRIMARY KEY,
    Date TEXT,
    Category TEXT,
    Description TEXT,
    Amount REAL
)
""")

conn.commit()

# Step 3: Define functions for CRUD operations

def add_crop(name, season, acreage):
    cursor.execute("INSERT INTO Crops (Name, Season, Acreage) VALUES (?, ?, ?)", (name, season, acreage))
    conn.commit()

def view_crops():
    return pd.read_sql_query("SELECT * FROM Crops", conn)

def record_production(crop_id, date, quantity, grade):
    cursor.execute("INSERT INTO Production (CropID, Date, Quantity, Grade) VALUES (?, ?, ?, ?)",
                   (crop_id, date, quantity, grade))
    conn.commit()

def view_production():
    return pd.read_sql_query("SELECT * FROM Production", conn)

def record_sale(crop_id, quantity, price, buyer):
    cursor.execute("INSERT INTO Sales (CropID, Quantity, Price, Buyer) VALUES (?, ?, ?, ?)",
                   (crop_id, quantity, price, buyer))
    conn.commit()

def view_sales():
    return pd.read_sql_query("SELECT * FROM Sales", conn)

# Step 4: Reporting functions

def yield_report():
    return pd.read_sql_query("""
    SELECT Crops.Name, SUM(Production.Quantity) AS TotalYield, Production.Grade
    FROM Production
    JOIN Crops ON Production.CropID = Crops.CropID
    GROUP BY Crops.Name, Production.Grade
    """, conn)

def profitability_report():
    return pd.read_sql_query("""
    SELECT Crops.Name, SUM(Sales.Price * Sales.Quantity) AS Revenue,
           (SELECT SUM(Amount) FROM Expenses WHERE Category = 'Crop') AS Expenses
    FROM Sales
    JOIN Crops ON Sales.CropID = Crops.CropID
    GROUP BY Crops.Name
    """, conn)

# Step 5: Streamlit UI

st.title("Farm ERP System")

# Add new crop
st.header("Add a new crop")
crop_name = st.text_input("Crop Name")
crop_season = st.selectbox("Season", ["Winter", "Spring", "Summer", "Fall"])
crop_acreage = st.number_input("Acreage", min_value=0.0, step=0.1)
if st.button("Add Crop"):
    add_crop(crop_name, crop_season, crop_acreage)
    st.success(f"Crop '{crop_name}' added!")

# View crops
st.header("View Crops")
crops = view_crops()
st.write(crops)

# Record production
st.header("Record Production")
crop_id = st.number_input("Crop ID (from above list)", min_value=1)
production_date = st.date_input("Production Date")
production_quantity = st.number_input("Quantity Produced", min_value=0)
production_grade = st.selectbox("Grade", ["A", "B", "C"])
if st.button("Record Production"):
    record_production(crop_id, production_date.strftime('%Y-%m-%d'), production_quantity, production_grade)
    st.success(f"Production for Crop ID {crop_id} recorded!")

# View production
st.header("View Production")
production = view_production()
st.write(production)

# Record sale
st.header("Record Sale")
sale_crop_id = st.number_input("Crop ID (for sale)", min_value=1)
sale_quantity = st.number_input("Quantity Sold", min_value=0)
sale_price = st.number_input("Price per Unit", min_value=0.0)
sale_buyer = st.text_input("Buyer")
if st.button("Record Sale"):
    record_sale(sale_crop_id, sale_quantity, sale_price, sale_buyer)
    st.success(f"Sale for Crop ID {sale_crop_id} recorded!")

# View sales
st.header("View Sales")
sales = view_sales()
st.write(sales)

# Generate Yield Report
st.header("Yield Report")
yield_df = yield_report()
st.write(yield_df)

# Plot Yield Report
st.subheader("Yield Visualization")
fig, ax = plt.subplots()
yield_df.plot(kind='bar', x='Name', y='TotalYield', ax=ax, title="Total Yield per Crop")
st.pyplot(fig)

# Generate Profitability Report
st.header("Profitability Report")
profit_df = profitability_report()
st.write(profit_df)

# Plot Profitability Report
st.subheader("Profit Visualization")
fig, ax = plt.subplots()
profit_df.plot(kind='bar', x='Name', y='Revenue', ax=ax, title="Revenue per Crop")
st.pyplot(fig)
