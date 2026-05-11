from google.colab import files
uploaded = files.upload()

import pandas as pd

# 读取订单表
orders_df = pd.read_csv('Fecom Inc Orders (1).csv', sep=';')

print("✅ Orders 表读取成功")
print(f"总行数：{len(orders_df)}")
print("\n列名：")
print(orders_df.columns.tolist())
print("\n前3行：")
print(orders_df.head(3))

order_items = pd.read_csv('Fecom Inc Order Items.csv', sep=';')
print(f"Order Items 行数：{len(order_items)}")
print("\n列名：")
print(order_items.columns.tolist())
print("\n前3行：")
print(order_items.head(3))

# 按订单 ID 分组，计算每个订单的商品价格总和
order_product_total = order_items.groupby('Order_ID')['Price'].sum()
print(order_product_total.head())

# 按订单 ID 分组，计算每个订单的运费总和
order_freight_total = order_items.groupby('Order_ID')['Freight_Value'].sum()
print(order_freight_total.head())

# 把商品总价和运费合并成一张表
order_amount = pd.DataFrame({
    'Product_Total': order_product_total,
    'Freight_Total': order_freight_total
})
order_amount['Order_Total'] = order_amount['Product_Total'] + order_amount['Freight_Total']
print(order_amount.head())

# 把总金额加到订单表里
orders_with_amount = orders_df.merge(order_amount[['Order_Total']], left_on='Order_ID', right_index=True)
print(f"关联后行数：{len(orders_with_amount)}")
print(orders_with_amount[['Order_ID', 'Order_Total']].head())

avg_order_value = orders_with_amount['Order_Total'].mean()
print(f"平均订单金额：{avg_order_value:.2f}")

# 如果你已经跑过之前的关联代码，这一步是确认
print(f"订单表行数：{len(orders_with_amount)}")
print(f"金额列前5行：")
print(orders_with_amount[['Order_ID', 'Order_Total']].head())

# 把订单购买时间转换成日期格式
orders_with_amount['Order_Purchase_Timestamp'] = pd.to_datetime(orders_with_amount['Order_Purchase_Timestamp'])

# 按月分组求和
orders_with_amount['Month'] = orders_with_amount['Order_Purchase_Timestamp'].dt.to_period('M')
monthly_sales = orders_with_amount.groupby('Month')['Order_Total'].sum()

print("月销售额：")
print(monthly_sales)

top_orders = orders_with_amount.nlargest(10, 'Order_Total')
print("金额最高的 10 笔订单：")
print(top_orders[['Order_ID', 'Order_Total', 'Order_Status']])

status_sales = orders_with_amount.groupby('Order_Status')['Order_Total'].sum().sort_values(ascending=False)
print("各状态订单总金额：")
print(status_sales)

import matplotlib.pyplot as plt

# 把月份转换成字符串（方便显示）
monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Total Sales (EUR)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()

print(order_items['Price'].describe())

# 选一个订单 ID，看它在 Order Items 里的价格
sample_order = 'e481f51cbdc54678b7cc49136f2d6af7'
sample_items = order_items[order_items['Order_ID'] == sample_order]
print(sample_items[['Order_ID', 'Price', 'Freight_Value']])

sample_order_total = orders_with_amount[orders_with_amount['Order_ID'] == sample_order]
print(sample_order_total[['Order_ID', 'Order_Total']])

import pandas as pd

# 1. 读取订单明细表（Order Items）
order_items = pd.read_csv('Fecom Inc Order Items.csv', sep=';')

# 2. 计算每个订单的总金额（Price + Freight_Value）
order_total_correct = order_items.groupby('Order_ID').apply(
    lambda x: (x['Price'] + x['Freight_Value']).sum()
).reset_index(name='Order_Total_Correct')

# 3. 读取订单主表（Orders）
orders_df = pd.read_csv('Fecom Inc Orders (1).csv', sep=';')

# 4. 把正确的总金额合并到订单表
orders_fixed = orders_df.merge(order_total_correct, left_on='Order_ID', right_on='Order_ID', how='left')

# 5. 验证之前那个订单的金额
sample_id = 'e481f51cbdc54678b7cc49136f2d6af7'
print(orders_fixed[orders_fixed['Order_ID'] == sample_id][['Order_ID', 'Order_Total_Correct']])

# 转换时间列
orders_fixed['Order_Purchase_Timestamp'] = pd.to_datetime(orders_fixed['Order_Purchase_Timestamp'])
orders_fixed['Month'] = orders_fixed['Order_Purchase_Timestamp'].dt.to_period('M')

# 按月分组求和
monthly_sales_fixed = orders_fixed.groupby('Month')['Order_Total_Correct'].sum()

# 显示结果
print("月销售额（修正后）：")
print(monthly_sales_fixed)

# 找出金额最高的月份
top_month = monthly_sales_fixed.sort_values(ascending=False).head(1)
print(top_month)

top_orders = orders_fixed.nlargest(10, 'Order_Total_Correct')
print(top_orders[['Order_ID', 'Order_Total_Correct', 'Order_Status']])

status_sales = orders_fixed.groupby('Order_Status')['Order_Total_Correct'].sum().sort_values(ascending=False)
print(status_sales)

import matplotlib.pyplot as plt

# 把月份转换成字符串（用于显示）
monthly_sales_fixed.index = monthly_sales_fixed.index.astype(str)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales_fixed.index, monthly_sales_fixed.values, marker='o')
plt.title('Monthly Sales Trend (Fixed)')
plt.xlabel('Month')
plt.ylabel('Total Sales (EUR)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
