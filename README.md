# Fecom Inc. Berlin E‑commerce Sales Analysis

**Tools:** Python (Pandas, Matplotlib)  
**Data source:** Real order data from a Berlin‑based e‑commerce company (99,441 orders, 112,650 order items)

## What I did
- Loaded and cleaned 8 tables (orders, order items, payments, customers, products, etc.)
- Merged orders with order items to calculate the true total amount per order (Price + Freight)
- **Detected and fixed a major data error**: previously computed order totals were incorrectly scaled by 1/100
- Conducted sales analysis including:
  - monthly revenue trends
  - top 10 highest‑value orders
  - revenue breakdown by order status
- Visualised monthly sales with line charts

## Key findings
- **Total delivered revenue:** €15.42 million
- **Highest sales month:** November 2023 (€1.18 million)
- **Highest single order:** €13,664.08 (delivered)
- **Canceled orders revenue:** €105,885.72 (only 0.7% of total revenue)
- **Shipped orders revenue:** €177,129.34 (awaiting delivery)
- **Top 10 best‑selling products** are mainly from **Health & Beauty** and **Computers Accessories**.  
  The highest‑selling single product generated €67,606, and the Top 10 together contributed ~€0.5M.

## Code
The full analysis code is available in this repository as `analysis.py`.  
**Run the analysis directly in Google Colab – no setup required.**

## Author
Yu Rongrong – [GitHub](https://github.com/Yu-rongrong)
