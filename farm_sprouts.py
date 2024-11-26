# farm_sprouts.py

pip install streamlit

# Import necessary libraries
import pandas as pd
import sqlite3
import streamlit as st
import matplotlib.pyplot as plt
from datetime import datetime

# Step 1: Environment Setup
conn = sqlite3.connect('farm_erp.db')
cursor = conn.cursor()

# Step 2: Database Initialization
# Create tables if they don't exist
def initialize_db():
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

# Step 3: CRUD Operations
# Add crop
def add_crop(name, season, acreage):
    cursor.execute("INSERT INTO Crops (Name, Season, Acreage) VALUES (?, ?, ?)", (name, season, acreage))
    conn.commit()

# View crops
def view_crops():
    return pd.read_sql_query("SELECT * FROM Crops", conn)

# Record production
def record_production(crop_id, date, quantity, grade):
    cursor.execute("INSERT INTO Production (CropID, Date, Quantity, Grade) VALUES (?, ?, ?, ?)",
                   (crop_id, date, quantity, grade))
    conn.commit()

# Record sale
def record_sale(crop_id, quantity, price, buyer):
    cursor.execute("INSERT INTO Sales (CropID, Quantity, Price, Buyer) VALUES (?, ?, ?, ?)",
                   (crop_id, quantity, price, buyer))
    conn.commit()

# Step 4: Reporting
# Yield report
def yield_report():
    return pd.read_sql_query("""
    SELECT Crops.Name, SUM(Production.Quantity) AS TotalYield, Production.Grade
    FROM Production
    JOIN Crops ON Production.CropID = Crops.CropID
    GROUP BY Crops.Name, Production.Grade
    """, conn)

# Profitability report
def profitability_report():
    return pd.read_sql_query("""
    SELECT Crops.Name, SUM(Sales.Price * Sales.Quantity) AS Revenue,
           (SELECT SUM(Amount) FROM Expenses WHERE Category = 'Crop') AS Expenses
    FROM Sales
    JOIN Crops ON Sales.CropID = Crops.CropID
    GROUP BY Crops.Name
    """, conn)

# Step 5: Streamlit Interface
def main():
    # Initialize the database
    initialize_db()

    # Title
    st.title("Farm ERP System")

    # Sidebar for navigation
    menu = ["Home", "Add Crop", "Add Production", "Add Sale", "View Reports"]
    choice = st.sidebar.selectbox("Select an Option", menu)

    # Home page
    if choice == "Home":
        st.subheader("Welcome to the Farm ERP System")
        st.write("You can add crops, production data, sales data, and view reports.")

    # Add Crop page
    elif choice == "Add Crop":
        st.subheader("Add New Crop")
        name = st.text_input("Crop Name")
        season = st.selectbox("Season", ["Winter", "Spring", "Summer", "Fall"])
        acreage = st.number_input("Acreage", min_value=0.0)
        if st.button("Add Crop"):
            add_crop(name, season, acreage)
            st.success(f"Crop '{name}' added successfully!")

    # Add Production page
    elif choice == "Add Production":
        st.subheader("Record Production")
        crop_id = st.number_input("Crop ID", min_value=1)
        date = st.date_input("Date", value=datetime.today())
        quantity = st.number_input("Quantity", min_value=0)
        grade = st.selectbox("Grade", ["A", "B", "C"])
        if st.button("Record Production"):
            record_production(crop_id, str(date), quantity, grade)
            st.success(f"Production for Crop ID {crop_id} recorded.")

    # Add Sale page
    elif choice == "Add Sale":
        st.subheader("Record Sale")
        crop_id = st.number_input("Crop ID", min_value=1)
        quantity = st.number_input("Quantity", min_value=0)
        price = st.number_input("Price per Unit", min_value=0.0)
        buyer = st.text_input("Buyer")
        if st.button("Record Sale"):
            record_sale(crop_id, quantity, price, buyer)
            st.success(f"Sale for Crop ID {crop_id} recorded.")

    # View Reports page
    elif choice == "View Reports":
        st.subheader("View Reports")
        report_choice = st.selectbox("Select Report", ["Yield Report", "Profitability Report"])

        if report_choice == "Yield Report":
            yield_df = yield_report()
            st.dataframe(yield_df)

            # Plot yield report
            st.subheader("Yield per Crop")
            yield_df.plot(kind='bar', x='Name', y='TotalYield', title="Yield per Crop")
            plt.xticks(rotation=45)
            st.pyplot()

        elif report_choice == "Profitability Report":
            profit_df = profitability_report()
            st.dataframe(profit_df)

            # Plot profitability report
            st.subheader("Revenue vs Expenses")
            profit_df.plot(kind='bar', x='Name', y='Revenue', title="Revenue per Crop")
            plt.xticks(rotation=45)
            st.pyplot()

if __name__ == "__main__":
    main()

