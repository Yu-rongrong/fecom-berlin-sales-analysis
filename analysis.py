import pandas as pd
import matplotlib.pyplot as plt

# ------------------------------
# 1. 读取数据
# ------------------------------
orders_df = pd.read_csv('Fecom Inc Orders (1).csv', sep=';')
order_items = pd.read_csv('Fecom Inc Order Items.csv', sep=';')

print("✅ 数据加载完成")
print(f"Orders: {len(orders_df)} 行")
print(f"Order Items: {len(order_items)} 行")

# ------------------------------
# 2. 计算每个订单的正确总金额（Price + Freight_Value）
# ------------------------------
order_total_correct = (
    order_items.groupby('Order_ID')
    .apply(lambda x: (x['Price'] + x['Freight_Value']).sum())
    .reset_index(name='Order_Total_Correct')
)

orders_fixed = orders_df.merge(order_total_correct, on='Order_ID', how='left')

# ------------------------------
# 3. 时间处理 & 月销售额
# ------------------------------
orders_fixed['Order_Purchase_Timestamp'] = pd.to_datetime(orders_fixed['Order_Purchase_Timestamp'])
orders_fixed['Month'] = orders_fixed['Order_Purchase_Timestamp'].dt.to_period('M')

monthly_sales = orders_fixed.groupby('Month')['Order_Total_Correct'].sum()
print("\n=== 月销售额 ===")
print(monthly_sales)

# ------------------------------
# 4. 金额最高的 10 笔订单
# ------------------------------
top10 = orders_fixed.nlargest(10, 'Order_Total_Correct')
print("\n=== 金额最高的 10 笔订单 ===")
print(top10[['Order_ID', 'Order_Total_Correct', 'Order_Status']])

# ------------------------------
# 5. 各订单状态总销售额
# ------------------------------
status_sales = (
    orders_fixed.groupby('Order_Status')['Order_Total_Correct']
    .sum()
    .sort_values(ascending=False)
)
print("\n=== 各订单状态销售额 ===")
print(status_sales)

# ------------------------------
# 6. 销售额趋势图
# ------------------------------
monthly_sales.index = monthly_sales.index.astype(str)

plt.figure(figsize=(12, 6))
plt.plot(monthly_sales.index, monthly_sales.values, marker='o')
plt.title('Monthly Sales Trend (Fecom Inc.)')
plt.xlabel('Month')
plt.ylabel('Total Sales (EUR)')
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.show()
