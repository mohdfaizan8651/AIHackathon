# CREATE TABLE customers (
#     customer_id TEXT PRIMARY KEY,
#     fname TEXT,
#     lname TEXT,
#     email TEXT,
#     password TEXT,
#     segment TEXT,
#     city TEXT,
#     state TEXT,
#     country TEXT,
#     street TEXT,
#     zipcode TEXT
# );

# CREATE TABLE departments (
#     department_id INTEGER PRIMARY KEY,
#     department_name TEXT
# );

# CREATE TABLE categories (
#     category_id INTEGER PRIMARY KEY,
#     category_name TEXT
# );

# CREATE TABLE products (
#     product_card_id TEXT PRIMARY KEY,
#     product_category_id TEXT,
#     category_id INTEGER REFERENCES categories(category_id),
#     description TEXT,
#     image TEXT,
#     product_name TEXT,
#     product_price FLOAT,
#     product_status TEXT
# );

# CREATE TABLE orders (
#     order_id TEXT PRIMARY KEY,
#     customer_id TEXT REFERENCES customers(customer_id),
#     order_date DATE,
#     shipping_date DATE,
#     shipping_mode TEXT,
#     status TEXT,
#     city TEXT,
#     state TEXT,
#     country TEXT,
#     zipcode TEXT,
#     region TEXT,
#     market TEXT,
#     latitude FLOAT,
#     longitude FLOAT,
#     Type TEXT
# );

# CREATE TABLE order_items (
#     order_item_id TEXT PRIMARY KEY,
#     order_id TEXT REFERENCES orders(order_id),
#     product_id TEXT REFERENCES products(product_card_id),
#     cardprod_id TEXT,
#     quantity INTEGER,
#     discount FLOAT,
#     discount_rate FLOAT,
#     product_price FLOAT,
#     total FLOAT,
#     profit_ratio FLOAT,
#     profit_per_order FLOAT,
#     benefit_per_order FLOAT,
#     sales_per_customer FLOAT
# );


# CREATE TABLE shipping (
#     order_id TEXT PRIMARY KEY REFERENCES orders(order_id),
#     days_for_shipping_real FLOAT,
#     days_for_shipment_scheduled FLOAT,
#     delivery_status TEXT,
#     late_delivery_risk INTEGER
# );


# import pandas as pd

# df = pd.read_csv("DataCoSupplyChainDataset.csv (1).csv")
# # df.head()


# import psycopg2

# conn = psycopg2.connect(
#     host="localhost",
#     database="DataCoSupplyChainDataset",
#     user="postgres",
#     password="umra"
# )
# cursor = conn.cursor()

# Connect to PostgreSQL
# conn = psycopg2.connect(
#     dbname="DataCoSupplyChainDataset",
#     user="postgres",
#     password="umra",
#     host="localhost",
#     port="5432"  # default PostgreSQL port
# )
# cursor = conn.cursor()
# print(cursor,'------------')
# departments = df[['Department Id', 'Department Name']].drop_duplicates()

# for _, row in departments.iterrows():
#     cursor.execute("""
#         INSERT INTO departments (department_id, department_name)
#         VALUES (%s, %s)
#         ON CONFLICT (department_id) DO NOTHING
#     """, (row['Department Id'], row['Department Name']))

# categories = df[['Category Id', 'Category Name']].drop_duplicates()

# for _, row in categories.iterrows():
#     cursor.execute("""
#         INSERT INTO categories (category_id, category_name)
#         VALUES (%s, %s)
#         ON CONFLICT (category_id) DO NOTHING
#     """, (row['Category Id'], row['Category Name']))


# customers = df[[
#     'Customer Id', 'Customer Fname', 'Customer Lname', 'Customer Email',
#     'Customer Password', 'Customer Segment', 'Customer City', 'Customer State',
#     'Customer Country', 'Customer Street', 'Customer Zipcode'
# ]].drop_duplicates()

# for _, row in customers.iterrows():
#     cursor.execute("""
#         INSERT INTO customers (
#             customer_id, fname, lname, email, password, segment,
#             city, state, country, street, zipcode
#         )
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         ON CONFLICT (customer_id) DO NOTHING
#     """, tuple(row))

# products = df[[
#     'Product Card Id', 'Product Category Id', 'Category Id',
#     'Product Description', 'Product Image', 'Product Name',
#     'Product Price', 'Product Status'
# ]].drop_duplicates()

# for _, row in products.iterrows():
#     cursor.execute("""
#         INSERT INTO products (
#             product_card_id, product_category_id, category_id,
#             description, image, product_name, product_price, product_status
#         )
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#         ON CONFLICT (product_card_id) DO NOTHING
#     """, tuple(row))
# orders = df[[
#     'Order Id', 'Customer Id', 'order_date (DateOrders)',
#     'shipping_date (DateOrders)', 'Shipping Mode', 'Order Status',
#     'Order City', 'Order State', 'Order Country', 'Order Zipcode',
#     'Order Region', 'Market', 'Latitude', 'Longitude', 'Type'
# ]].drop_duplicates()


# for _, row in orders.iterrows():
#     cursor.execute("""
#         INSERT INTO orders (
#             order_id, customer_id, order_date, shipping_date,
#             shipping_mode, status, city, state, country, zipcode, region, market, latitude, longitude, Type
#         )
#         VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         ON CONFLICT (order_id) DO NOTHING
#     """, tuple(row))

# shipping = df[[
#     'Order Id', 'Days for shipping (real)', 'Days for shipment (scheduled)',
#     'Delivery Status', 'Late_delivery_risk'
# ]].drop_duplicates()

# for _, row in shipping.iterrows():
#     cursor.execute("""
#         INSERT INTO shipping (
#             order_id, days_for_shipping_real, days_for_shipment_scheduled,
#             delivery_status, late_delivery_risk
#         )
#         VALUES (%s, %s, %s, %s, %s)
#         ON CONFLICT (order_id) DO NOTHING
#     """, tuple(row))




# for index, row in df.iterrows():
#     try:
#         cursor.execute("""
#             INSERT INTO order_items (
#                 order_item_id,
#                 order_id,
#                 product_id,
#                 cardprod_id,
#                 quantity,
#                 discount,
#                 discount_rate,
#                 product_price,
#                 total,
#                 profit_ratio,
#                 profit_per_order,
#                 benefit_per_order,
#                 sales_per_customer
#             ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """, (
#             str(row['Order Item Id']),
#             str(row['Order Id']),
#             str(row['Product Card Id']),
#             str(row['Order Item Cardprod Id']),
#             int(row['Order Item Quantity']),
#             float(row['Order Item Discount']),
#             float(row['Order Item Discount Rate']),
#             float(row['Order Item Product Price']),
#             float(row['Order Item Total']),
#             float(row['Order Item Profit Ratio']),
#             float(row['Order Profit Per Order']),
#             float(row['Benefit per order']),
#             float(row['Sales per customer'])
#         ))
#     except Exception as e:
#         print(f"❌ Error inserting row {index}: {e}")
#         conn.rollback()
#         continue
# conn.commit()
# cursor.close()
# conn.close()
# print("✅ All data inserted into order_items.")



