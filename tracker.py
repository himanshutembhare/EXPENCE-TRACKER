import sqlite3
import datetime
import csv

# ---------------- DATABASE ----------------
conn = sqlite3.connect("expenses.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS expenses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    category TEXT,
    amount REAL,
    description TEXT
)
""")
conn.commit()

# ---------------- FUNCTIONS ----------------
def add_expense():
    date = input("Enter date (YYYY-MM-DD): ")
    category = input("Enter category (Food, Travel, Rent, etc): ")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    cursor.execute("INSERT INTO expenses (date, category, amount, description) VALUES (?, ?, ?, ?)",
                   (date, category, amount, description))
    conn.commit()
    print("Expense added successfully!")

def view_expenses():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    print("\nID | Date | Category | Amount | Description")
    print("-" * 60)
    for row in rows:
        print(row[0], row[1], row[2], row[3], row[4])

def search_by_category():
    cat = input("Enter category: ")
    cursor.execute("SELECT * FROM expenses WHERE category=?", (cat,))
    rows = cursor.fetchall()

    if rows:
        for row in rows:
            print(row)
    else:
        print("No expenses found for this category.")

def monthly_report():
    month = input("Enter month (YYYY-MM): ")
    cursor.execute("SELECT SUM(amount) FROM expenses WHERE date LIKE ?", (month + "%",))
    total = cursor.fetchone()[0]

    if total:
        print(f"Total expense for {month}: ₹{total}")
    else:
        print("No expenses for this month.")

def delete_expense():
    eid = input("Enter expense ID to delete: ")
    cursor.execute("DELETE FROM expenses WHERE id=?", (eid,))
    conn.commit()
    print("Expense deleted.")

def export_to_csv():
    cursor.execute("SELECT * FROM expenses")
    rows = cursor.fetchall()

    with open("expenses_export.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["ID", "Date", "Category", "Amount", "Description"])
        writer.writerows(rows)

    print("Data exported to expenses_export.csv")

# ---------------- MAIN MENU ----------------
def menu():
    while True:
        print("\n===== PERSONAL EXPENSE TRACKER =====")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search by Category")
        print("4. Monthly Report")
        print("5. Delete Expense")
        print("6. Export to CSV")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_expense()
        elif choice == "2":
            view_expenses()
        elif choice == "3":
            search_by_category()
        elif choice == "4":
            monthly_report()
        elif choice == "5":
            delete_expense()
        elif choice == "6":
            export_to_csv()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid choice!")

menu()
