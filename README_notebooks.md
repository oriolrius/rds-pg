# SQL Practice Notebooks

Welcome to the SQL Practice environment! This JupyterLab instance is connected to a PostgreSQL database on AWS RDS.

---

## Available Notebooks

### 1. [Getting Started](./getting_started.ipynb)
**Level:** Beginner
**Duration:** 5 minutes

Quick setup to verify your database connection. Run this first to ensure everything is working.

---

### 2. [SQL Practice](./sql_practice.ipynb)
**Level:** Beginner to Intermediate
**Duration:** 30-45 minutes

Learn fundamental SQL concepts:
- Creating tables and inserting data
- SELECT queries with filtering (WHERE)
- Sorting and limiting results
- Aggregate functions (COUNT, SUM, AVG)
- GROUP BY and HAVING clauses

---

### 3. [Advanced SQL Practice](./sql_advanced_practice.ipynb)
**Level:** Intermediate to Advanced
**Duration:** 60-90 minutes

Master advanced SQL techniques with a realistic e-commerce database:
- Complex JOINs (INNER, LEFT, RIGHT, FULL)
- Subqueries and correlated subqueries
- Common Table Expressions (CTEs)
- Window functions (ROW_NUMBER, RANK, LAG, LEAD)
- Triggers and stored procedures
- Database transactions

---

### 4. [Sales Report](./sales_report.ipynb)
**Level:** Advanced
**Duration:** 30 minutes

Business analytics demonstration combining SQL with Python visualization:
- Key Performance Indicators (KPIs)
- Revenue analysis by category and geography
- Customer segmentation
- Trend analysis with charts
- Inventory management alerts

---

## Quick Tips

- **Run cells:** `Shift + Enter`
- **SQL queries:** Use `%%sql` magic command
- **View tables:** Check the SQL Explorer in the left sidebar
- **Need help?** Use `%sql --help` for jupysql documentation

## Database Schema

The advanced notebooks use an e-commerce schema with these tables:
- `customers` - Customer information
- `products` - Product catalog with categories
- `orders` - Order headers
- `order_items` - Order line items
- `inventory_log` - Stock movement tracking (created by triggers)
