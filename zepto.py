from faker import Faker
import random
import mysql.connector

fake = Faker()

# -----------------------------
# 1️⃣ CONNECT TO DATABASE
# -----------------------------
db = mysql.connector.connect(
    host="host name",
    user="user name",
    password="your password",   # Replace with your MySQL root password
    database="zepto_dashboard",
    port="Port number"              # Replace with your MySQL port
)
cursor = db.cursor()
print("✅ Connection successful!")

# -----------------------------
# 2️⃣ INSERT DATA INTO OUTLETS
# -----------------------------
outlet_locations = [
    "Mumbai", "Delhi", "Bangalore", "Hyderabad", "Pune",
    "Chennai", "Kolkata", "Ahmedabad", "Jaipur", "Lucknow"
]
outlet_sizes = ["Small", "Medium", "Large"]
outlet_types = ["Dark Store", "Cafe"]

for _ in range(100):
    cursor.execute("""
        INSERT INTO outlets (outlet_location, outlet_size, outlet_type, establishment_year)
        VALUES (%s, %s, %s, %s)
    """, (
        random.choice(outlet_locations),
        random.choice(outlet_sizes),
        random.choice(outlet_types),
        random.randint(2012, 2024)
    ))

db.commit()  # commit outlets first
print("✅ 100 outlets added.")

# -----------------------------
# 3️⃣ INSERT DATA INTO PRODUCTS
# -----------------------------
categories = [
    "Fruits", "Snacks", "Dairy", "Beverages", "Bakery", "Frozen", 
    "Household", "Health", "Vegetables", "Ready to Eat"
]

product_samples = {
    "Fruits": ["Banana", "Apple", "Mango", "Grapes", "Pineapple", "Papaya"],
    "Snacks": ["Potato Chips", "Nachos", "Popcorn", "Protein Bar", "Masala Makhana"],
    "Dairy": ["Milk 1L", "Butter", "Cheese Slice", "Curd", "Paneer 200g", "Yogurt Cup"],
    "Beverages": ["Iced Tea", "Cold Coffee", "Coca-Cola", "Lassi", "Lemon Soda"],
    "Bakery": ["Croissant", "Brown Bread", "Chocolate Muffin", "Garlic Bread", "Donut"],
    "Frozen": ["French Fries", "Frozen Pizza", "Veg Nuggets", "Ice Cream Tub"],
    "Household": ["Tissue Roll", "Dish Soap", "Floor Cleaner", "Garbage Bag"],
    "Health": ["Vitamin C", "Protein Powder", "Energy Drink", "Electrolyte Sachet"],
    "Vegetables": ["Tomato", "Potato", "Onion", "Spinach", "Cucumber"],
    "Ready to Eat": ["Sandwich", "Pasta Bowl", "Biryani Box", "Chicken Roll"]
}

for _ in range(500):
    cat = random.choice(categories)
    name = random.choice(product_samples[cat])
    cursor.execute("""
        INSERT INTO products (product_name, category, fat_content, item_visibility)
        VALUES (%s, %s, %s, %s)
    """, (
        name,
        cat,
        random.choice(["Low Fat", "Regular"]),
        round(random.uniform(0.01, 0.10), 2)
    ))

db.commit()  # commit products first
print("✅ 500 products added.")

# -----------------------------
# 4️⃣ FETCH VALID FOREIGN KEYS
# -----------------------------
cursor.execute("SELECT outlet_id FROM outlets")
outlet_ids = [row[0] for row in cursor.fetchall()]

cursor.execute("SELECT product_id FROM products")
product_ids = [row[0] for row in cursor.fetchall()]

# -----------------------------
# 5️⃣ INSERT DATA INTO SALES
# -----------------------------
batch_size = 1000  # commit in batches for performance
for i in range(8500):
    outlet_id = random.choice(outlet_ids)
    product_id = random.choice(product_ids)
    sale_date = fake.date_between(start_date='-2y', end_date='today')
    total_sales = round(random.uniform(50, 1200), 2)
    num_items = random.randint(1, 15)
    avg_sales = round(total_sales / num_items, 2)
    avg_rating = round(random.uniform(3.0, 5.0), 1)

    cursor.execute("""
        INSERT INTO sales (outlet_id, product_id, sale_date, total_sales, num_items, avg_sales, avg_rating)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, (
        outlet_id,
        product_id,
        sale_date,
        total_sales,
        num_items,
        avg_sales,
        avg_rating
    ))

    # Commit every batch_size inserts
    if (i + 1) % batch_size == 0:
        db.commit()
        print(f"✅ {i + 1} sales records inserted...")

db.commit()  # final commit for remaining rows
print("✅ 8500 sales records added.")

# -----------------------------
# 6️⃣ CLOSE CONNECTION
# -----------------------------
cursor.close()
db.close()
print("\n🎉 Zepto dataset generation completed successfully (8500+ records).")
