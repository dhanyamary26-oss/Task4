import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

# -----------------------------
# STEP 1: Load Dataset
# -----------------------------
file_path = r"C:\Users\user\Downloads\DecodeLabs pgms\Project 4\Dataset for Data Analytics project 4.xlsx"
df = pd.read_excel(file_path)

# -----------------------------
# STEP 2: Create SQL Database
# -----------------------------
conn = sqlite3.connect("project4.db")
df.to_sql("orders", conn, if_exists="replace", index=False)

# -----------------------------
# STEP 3: SQL QUERIES
# -----------------------------

# 1. Total Sales by Product (for Bar Chart)
q1 = "SELECT Product, SUM(TotalPrice) AS Total_Sales FROM orders GROUP BY Product ORDER BY Total_Sales DESC"
product_sales = pd.read_sql(q1, conn)

# 2. Monthly Revenue (for Line Chart)
q2 = "SELECT SUBSTR(Date,1,7) AS Month, SUM(TotalPrice) AS Revenue FROM orders GROUP BY Month ORDER BY Month"
monthly_sales = pd.read_sql(q2, conn)

# 3. Product Sales by Order Status (for Stacked Bar Chart)
q3 = """
SELECT Product, OrderStatus, COUNT(*) AS Count
FROM orders
GROUP BY Product, OrderStatus
"""
status_by_product = pd.read_sql(q3, conn)
stacked_data = status_by_product.pivot(index="Product", columns="OrderStatus", values="Count").fillna(0)

# 4. Quantity vs TotalPrice (for Scatter Plot)
q4 = "SELECT Quantity, TotalPrice FROM orders"
scatter_data = pd.read_sql(q4, conn)

# 5. Payment Method Distribution (for Pie Chart)
q5 = "SELECT PaymentMethod, COUNT(*) AS Count FROM orders GROUP BY PaymentMethod"
payment_data = pd.read_sql(q5, conn)

# 6. Yearly Sales (for Distorted vs Honest Axis demo)
q6 = "SELECT SUBSTR(Date,1,4) AS Year, SUM(TotalPrice) AS Sales FROM orders GROUP BY Year"
yearly_sales = pd.read_sql(q6, conn)

conn.close()

# -----------------------------
# STEP 4: VISUALIZATIONS
# -----------------------------

# 🔹 1. Bar / Column Chart - Total Sales by Product
plt.figure()
plt.bar(product_sales["Product"], product_sales["Total_Sales"], color="#185FA5")
plt.title("Total Sales by Product")
plt.xlabel("Product")
plt.ylabel("Sales ($)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 🔹 2. Line Chart - Monthly Revenue Trend
plt.figure()
plt.plot(monthly_sales["Month"], monthly_sales["Revenue"], color="#185FA5", marker="o")
plt.title("Monthly Revenue Trend")
plt.xlabel("Month")
plt.ylabel("Revenue ($)")
plt.xticks(rotation=90, fontsize=6)
plt.tight_layout()
plt.show()

# 🔹 3. Stacked Bar Chart - Order Status by Product
stacked_data.plot(kind="bar", stacked=True, figsize=(8, 5))
plt.title("Order Status Breakdown by Product")
plt.xlabel("Product")
plt.ylabel("Number of Orders")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# 🔹 4. Scatter Plot - Quantity vs Total Price
plt.figure()
plt.scatter(scatter_data["Quantity"], scatter_data["TotalPrice"], alpha=0.4, color="#185FA5")
plt.title("Quantity vs Total Price")
plt.xlabel("Quantity")
plt.ylabel("Total Price ($)")
plt.tight_layout()
plt.show()

# 🔹 5. Pie Chart - Payment Method Distribution (only top 3 shown, rest grouped)
top3 = payment_data.sort_values("Count", ascending=False).head(3)
others = payment_data["Count"].sum() - top3["Count"].sum()
pie_labels = list(top3["PaymentMethod"]) + ["Others"]
pie_values = list(top3["Count"]) + [others]

plt.figure()
plt.pie(pie_values, labels=pie_labels, autopct="%1.1f%%", colors=["#185FA5", "#73726c", "#1D9E75", "#cccccc"])
plt.title("Payment Method Distribution (Top 3 + Others)")
plt.tight_layout()
plt.show()

# 🔹 6a. Distorted Chart - Truncated Y-Axis (misleading)
plt.figure()
plt.bar(yearly_sales["Year"], yearly_sales["Sales"], color="#E24B4A")
plt.ylim(yearly_sales["Sales"].min() - 5000, yearly_sales["Sales"].max() + 5000)  # truncated axis
plt.title("Distorted Chart - Truncated Y-Axis (Misleading)")
plt.xlabel("Year")
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.show()

# 🔹 6b. Honest Chart - Zero Baseline Axis (correct)
plt.figure()
plt.bar(yearly_sales["Year"], yearly_sales["Sales"], color="#185FA5")
plt.ylim(0, yearly_sales["Sales"].max() + 20000)  # zero baseline
plt.title("Honest Chart - Zero Baseline Axis (Correct)")
plt.xlabel("Year")
plt.ylabel("Sales ($)")
plt.tight_layout()
plt.show()

# -----------------------------
# STEP 5: PRINT INSIGHTS
# -----------------------------
print("\n🔹 INSIGHTS:")

print("\n1. Top Selling Product:")
print(product_sales.head(1))

print("\n2. Best Month for Revenue:")
print(monthly_sales.sort_values(by="Revenue", ascending=False).head(1))

print("\n3. Most Used Payment Method:")
print(payment_data.sort_values(by="Count", ascending=False).head(1))

print("\n4. Yearly Sales Comparison:")
print(yearly_sales)