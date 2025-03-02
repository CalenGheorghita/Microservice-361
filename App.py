from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)

# Connect to PostgreSQL database
def connect_db():
    return psycopg2.connect(
        dbname="",
        user="",
        password="",
        host="",
        port=""
    )

# Get expenses by year and month
@app.route('/api/expenses/trend')
def get_expense_trend():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Need user_id"}), 400

    conn = connect_db()
    cur = conn.cursor()

    # Get sum of expenses grouped by year & month, including missing months as 0
    cur.execute("""
        SELECT months.y AS year, months.m AS month, COALESCE(SUM(exp.amount), 0) AS total_expense
        FROM 
            (SELECT y, m FROM generate_series(2023, 2025) AS y 
            CROSS JOIN generate_series(1, 12) AS m) AS months
        LEFT JOIN 
            (SELECT EXTRACT(YEAR FROM date) AS y, EXTRACT(MONTH FROM date) AS m, amount
            FROM budget_win_schema.expense WHERE user_id = %s) AS exp
        ON months.y = exp.y AND months.m = exp.m
        GROUP BY months.y, months.m 
        ORDER BY months.y, months.m;
    """, (user_id,))

    data = cur.fetchall()
    conn.close()

    return jsonify([{"year": row[0], "month": row[1], "total_expense": row[2]} for row in data])

# Get income by year and month
@app.route('/api/income/trend')
def get_income_trend():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Need user_id"}), 400

    conn = connect_db()
    cur = conn.cursor()

    # Get sum of income grouped by year & month
    cur.execute("""
        SELECT EXTRACT(YEAR FROM date) AS year, EXTRACT(MONTH FROM date) AS month, 
               COALESCE(SUM(amount), 0) AS total_income
        FROM budget_win_schema.income
        WHERE user_id = %s
        GROUP BY year, month ORDER BY year, month;
    """, (user_id,))

    data = cur.fetchall()
    conn.close()

    return jsonify([{"year": row[0], "month": row[1], "total_income": row[2]} for row in data])

# Get expenses by year and category
@app.route('/api/expenses/categories')
def get_expense_categories():
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({"error": "Need user_id"}), 400

    conn = connect_db()
    cur = conn.cursor()

    # Get sum of expenses by year & category
    cur.execute("""
        SELECT EXTRACT(YEAR FROM date) AS year, category, 
               COALESCE(SUM(amount), 0) AS total_expense
        FROM budget_win_schema.expense
        WHERE user_id = %s
        GROUP BY year, category ORDER BY year, category;
    """, (user_id,))

    data = cur.fetchall()
    conn.close()

    return jsonify([{"year": row[0], "category": row[1], "total_expense": row[2]} for row in data])

if __name__ == '__main__':
    app.run(debug=True)
    