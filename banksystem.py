import mysql.connector
import hashlib

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="Damilare_db",  
        password="Damilare12", 
        database="mydatabase12"
    )

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_account():
    conn = get_db_connection()
    cursor = conn.cursor()

    username = input("Enter a username: ")
    password = input("Enter a password: ")
    account_number = input("Enter an account number: ")
    initial_balance = float(input("Enter an initial deposit: "))
    hashed_password = hash_password(password)

    try:
        cursor.execute("INSERT INTO users (username, password, account_number, balance) VALUES (%s, %s, %s, %s)",
                       (username, hashed_password, account_number, initial_balance))
        conn.commit()
        print("Account created successfully!")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()

def login():
    conn = get_db_connection()
    cursor = conn.cursor()

    username = input("Enter your username: ")
    password = input("Enter your password: ")
    hashed_password = hash_password(password)

    cursor.execute("SELECT id, username, balance FROM users WHERE username = %s AND password = %s",
                   (username, hashed_password))
    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user:
        print(f"Welcome back, {user[1]}!")
        return user  # Return user details
    else:
        print("Invalid username or password. Please try again.")
        return None

def deposit(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    amount = float(input("Enter amount to deposit: "))
    if amount > 0:
        cursor.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, user_id))
        conn.commit()
        print(f"#{amount:.2f} deposited successfully!")
    else:
        print("Deposit amount must be positive.")

    cursor.close()
    conn.close()

def withdraw(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    amount = float(input("Enter amount to withdraw: "))
    cursor.execute("SELECT balance FROM users WHERE id = %s", (user_id,))
    balance = cursor.fetchone()[0]

    if amount > 0 and amount <= balance:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, user_id))
        conn.commit()
        print(f"#{amount:.2f} withdrawn successfully!")
    elif amount > balance:
        print("Insufficient funds.")
    else:
        print("Withdrawal amount must be positive.")

    cursor.close()
    conn.close()


def view_account_details(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT username, account_number, balance FROM users WHERE id = %s", (user_id,))
    account = cursor.fetchone()

    print("\n--- Account Details ---")
    print(f"Username: {account[0]}")
    print(f"Account Number: {account[1]}")
    print(f"Balance: #{account[2]:.2f}")

    cursor.close()
    conn.close()

def main():
    while True:
        print("\nWelcome to Sulaeman Bank Plc\n1. Create Account")
        print("2. Login")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            user = login()
            if user:
                user_id = user[0]
                while True:
                    print("\n1. Deposit Money")
                    print("2. Withdraw Money")
                    print("3. View Account Details")
                    print("4. Logout")
                    sub_choice = input("Enter your choice: ")

                    if sub_choice == "1":
                        deposit(user_id)
                    elif sub_choice == "2":
                        withdraw(user_id)
                    elif sub_choice == "3":
                        view_account_details(user_id)
                    elif sub_choice == "4":
                        print("Logged out successfully.")
                        break
                    else:
                        print("Invalid choice. Please try again.")
        elif choice == "3":
            print("Thank you for using Sulaeman bank Plc!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
