from flask import Flask, render_template, request, session, redirect, url_for
import pymysql
from datetime import datetime
from flask import jsonify
app = Flask(__name__)
app.secret_key = 'yash'

# Database connection
conn = pymysql.connect(host='localhost',
                       user='root',
                       password='password',
                       database='banking_system',
                       cursorclass=pymysql.cursors.DictCursor)
cursor = conn.cursor()
@app.route("/")
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form['role']

        # Authenticate user
        cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s AND role=%s", (username, password, role))
        user = cursor.fetchone()

        if user:
            session['username'] = user['username']
            session['role'] = user['role']
            if role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('user_dashboard'))
        else:
            return "Invalid username, password, or role. Please try again."

    return render_template('login.html')

# Function to fetch user profile details
def get_user_profile(user_id):
    cursor.execute("""
        SELECT users.id, users.username, accounts.account_number, accounts.holder_name, 
               credit_score.credit_score 
        FROM users 
        LEFT JOIN accounts ON users.id = accounts.user_id 
        LEFT JOIN credit_score ON users.id = credit_score.user_id 
        WHERE users.id = %s
        """, (user_id,))
    user_profile = cursor.fetchone()

    # Fetch beneficiary details
    cursor.execute("SELECT * FROM beneficiaries WHERE user_id = %s", (user_id,))
    beneficiaries = cursor.fetchall()

    return user_profile, beneficiaries
@app.route('/user_profile')
def user_profile():
    if 'username' in session and session['role'] == 'user':
        user_id = get_user_id(session['username'])
        user_profile, beneficiaries = get_user_profile(user_id)
        if user_profile:
            return render_template('user_profile.html', user_profile=user_profile, beneficiaries=beneficiaries)
        else:
            return "User profile not found."
    return redirect(url_for('login'))

'''
# Dashboard route for both user and admin
@app.route('/admin_dashboard')
def dashboard():
    if 'username' in session:
        role = session['role']
        if role == 'admin':
            return redirect(url_for('admin_dashboard'))
       
    return redirect(url_for('login'))
'''

# User dashboard
'''@app.route('/user_dashboard')
def user_dashboard():
    if session.get('role') == 'user':
        if 'user_id' in session:
            cursor.execute("SELECT balance FROM accounts WHERE user_id=%s", (session['user_id'],))
            user_balance = cursor.fetchone()
            if user_balance:
                balance = user_balance['balance']
                print("Balance fetched from database:", balance)  # Debug statement
                return render_template('user_dashboard.html', username=session['username'], balance=balance)
            else:
                return "Error: User balance not found"
    return redirect(url_for('login')) '''

'''@app.route('/user_dashboard')
def user_dashboard():
    if session.get('role') == 'user':
        return render_template('user_dashboard.html', username=session['username'],)
    return redirect(url_for('login'))'''
'''@app.route('/user_dashboard')
def user_dashboard():
    if 'username' in session and session['role'] == 'user':
        # Fetch user ID from session
        cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user_id = cursor.fetchone()['id']
        
        # Fetch user loans
        user_loans = get_user_loans(user_id)
        # Fetch user balance
        cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
        user_balance = cursor.fetchone()['balance']

        return render_template('user_dashboard.html', username=session['username'], user_loans=user_loans)
    return redirect(url_for('login'))'''
# User dashboard
@app.route('/user_dashboard')
def user_dashboard():
    if 'username' in session and session['role'] == 'user':
        # Fetch user ID from session
        cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
        user_id = cursor.fetchone()['id']
        
        # Fetch user loans
        user_loans = get_user_loans(user_id)
        
        # Fetch user balance
        user_balance = get_user_balance(user_id)
        
        # Fetch user transactions
        user_transactions = get_user_transactions(user_id)
        
        # Fetch user cards
        user_cards = get_user_cards(user_id)

        return render_template('user_dashboard.html', 
                               username=session['username'], 
                               user_loans=user_loans, 
                               balance=user_balance,
                               transactions=user_transactions,
                               cards=user_cards)
    return redirect(url_for('login'))
# Function to fetch user ID based on username
def get_user_id(username):
    cursor.execute("SELECT id FROM users WHERE username = %s", (username,))
    user_id = cursor.fetchone()['id']
    return user_id


# Function to fetch cards for the currently logged-in user
def get_user_cards(user_id):
    cursor.execute("SELECT * FROM cards WHERE user_id = %s", (user_id,))
    user_cards = cursor.fetchall()
    return user_cards


# Function to fetch loans for the currently logged-in user
def get_user_loans(user_id):
    cursor.execute("SELECT * FROM loans WHERE user_id = %s", (user_id,))
    user_loans = cursor.fetchall()
    return user_loans
# Function to fetch transactions for the currently logged-in user
def get_user_transactions(user_id):
    cursor.execute("SELECT * FROM transactions WHERE user_id = %s", (user_id,))
    user_transactions = cursor.fetchall()
    return user_transactions

'''# Admin dashboard
@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') == 'admin':
        return render_template('admin_dashboard.html', username=session['username'])
    return redirect(url_for('login'))'''
@app.route('/admin_dashboard')
def admin_dashboard():
    if session.get('role') == 'admin':
        cursor.execute("SELECT id, username FROM users")
        users = cursor.fetchall()
        return render_template('admin_dashboard.html', users=users)
    return redirect(url_for('login'))

  # Add a route for admin to view and modify user profiles
@app.route('/admin_profile/<int:user_id>', methods=['GET', 'POST'])
def admin_profile(user_id):
    if session.get('role') == 'admin':
        if request.method == 'POST':
            # Handle modifications to user profile
            new_credit_score = request.form['credit_score']
            update_credit_score(user_id, new_credit_score)

        # Fetch user profile and beneficiaries
        user_profile, beneficiaries = get_user_profile(user_id)

        if user_profile:
            return render_template('admin_profile.html', user_profile=user_profile, beneficiaries=beneficiaries)
        else:
            return "User profile not found."
    return redirect(url_for('login'))
def update_credit_score(user_id, new_credit_score):
    cursor.execute("UPDATE credit_score SET credit_score = %s WHERE user_id = %s", (new_credit_score, user_id))
    conn.commit()

@app.route('/logout')
def logout():
    # Clear the session
    session.clear()
    return redirect(url_for('login'))

# Add more routes for other functionalities such as view balance, transfer money, etc.
# Online money transfer
# Transfer money route
@app.route('/transfer_money', methods=['GET', 'POST'])
def transfer_money():
    if 'username' in session:
        if request.method == 'POST':
            recipient = request.form['recipient']
            amount = float(request.form['amount'])

            try:
                # Start a transaction
                conn.begin()

                # Retrieve sender's user ID
                cursor.execute("SELECT id FROM users WHERE username = %s", (session['username'],))
                sender_id = cursor.fetchone()['id']

                # Retrieve sender's account balance with locking
                cursor.execute("SELECT balance FROM accounts WHERE user_id = %s FOR UPDATE", (sender_id,))
                sender_balance = cursor.fetchone()['balance']

                # Check if the sender has sufficient balance
                if amount > sender_balance:
                    return "Insufficient balance. Please enter a valid amount."

                # Retrieve recipient's user ID
                cursor.execute("SELECT id FROM users WHERE username = %s", (recipient,))
                recipient_id = cursor.fetchone()['id']

                # Retrieve recipient's account balance with locking
                cursor.execute("SELECT balance FROM accounts WHERE user_id = %s FOR UPDATE", (recipient_id,))
                recipient_balance = cursor.fetchone()['balance']

                # Update sender's account balance
                sender_new_balance = sender_balance - amount
                cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s", (sender_new_balance, sender_id))

                # Update recipient's account balance
                recipient_new_balance = recipient_balance + amount
                cursor.execute("UPDATE accounts SET balance = %s WHERE user_id = %s", (recipient_new_balance, recipient_id))

                # Add transaction log for sender
                cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, 'withdrawal', %s)", (sender_id, amount))

                # Add transaction log for recipient
                cursor.execute("INSERT INTO transactions (user_id, transaction_type, amount) VALUES (%s, 'deposit', %s)", (recipient_id, amount))

                # Commit changes to the database
                conn.commit()

                # Redirect to the user dashboard after the transfer is completed
                return redirect(url_for('user_dashboard'))

            except Exception as e:
                # Rollback changes if an error occurs
                conn.rollback()
                return f"Error occurred: {str(e)}"

        return render_template('transfer_money.html', username=session['username'])
    return redirect(url_for('login'))

'''@app.route('/transfer_money', methods=['GET', 'POST'])
def transfer_money():
    if 'username' in session:
        if request.method == 'POST':
            recipient = request.form['recipient']
            amount = float(request.form['amount'])

            try:
                # Start a transaction
                conn.begin()

                # Retrieve sender's account balance with locking
                cursor.execute("SELECT balance FROM accounts WHERE holder_name=%s FOR UPDATE", (session['username'],))
                sender_balance = cursor.fetchone()['balance']

                # Check if the sender has sufficient balance
                if amount > sender_balance:
                    return "Insufficient balance. Please enter a valid amount."

                # Retrieve recipient's account balance with locking
                cursor.execute("SELECT balance FROM accounts WHERE holder_name=%s FOR UPDATE", (recipient,))
                recipient_balance = cursor.fetchone()['balance']

                # Update sender's account balance
                sender_new_balance = sender_balance - amount
                cursor.execute("UPDATE accounts SET balance=%s WHERE holder_name=%s", (sender_new_balance, session['username']))

                # Update recipient's account balance
                recipient_new_balance = recipient_balance + amount
                cursor.execute("UPDATE accounts SET balance=%s WHERE holder_name=%s", (recipient_new_balance, recipient))

                # Add transaction log for sender
                cursor.execute("INSERT INTO transactions (username, transaction_type, amount) VALUES (%s, 'withdrawal', %s)", (session['username'], amount))

                # Add transaction log for recipient
                cursor.execute("INSERT INTO transactions (username, transaction_type, amount) VALUES (%s, 'deposit', %s)", (recipient, amount))

                # Commit changes to the database
                conn.commit()

                # Redirect to the user dashboard after the transfer is completed
                return redirect(url_for('user_dashboard'))

            except Exception as e:
                # Rollback changes if an error occurs
                conn.rollback()
                return f"Error occurred: {str(e)}"

        return render_template('transfer_money.html', username=session['username'])
    return redirect(url_for('login'))'''

# Add route and function to check account balance
'''@app.route('/check_balance')
def check_balance():
    if 'username' in session:
        # Retrieve user's account balance
        cursor.execute("SELECT balance FROM accounts WHERE username=%s", (session['username'],))
        user_balance = cursor.fetchone()['balance']
        return render_template('check_balance.html', username=session['username'], balance=user_balance)
    return redirect(url_for('login'))'''
'''@app.route('/check_balance')
def check_balance():
    if 'user_id' in session:
        # Retrieve user's account balance using user_id
        cursor.execute("SELECT balance FROM accounts WHERE user_id=%s", (session['user_id'],))
        user_balance = cursor.fetchone()
        if user_balance:
            balance = user_balance['balance']
            print("Balance fetched from database:", balance)  # Debug statement
            return render_template('user_dashboard.html', username=session['username'], balance=balance)
        else:
            return "Error: User balance not found"
    return redirect(url_for('login'))'''
'''@app.route('/check_balance')
def check_balance():
    if 'username' in session:
        holder_name = session['username']
        # Retrieve user's account balance
        cursor.execute("SELECT balance FROM accounts WHERE holder_name = %s", (holder_name,))
        user_balance = cursor.fetchone()
        if user_balance:
            balance = user_balance['balance']
            print("Balance fetched from database:", balance)  # Debug statement
            return render_template('user_dashboard.html', username=session['username'], balance=balance)
        else:
            return "Error: User balance not found"
    return redirect(url_for('login'))'''
@app.route('/check_balance')
def check_balance():
    if 'username' in session:
        holder_name = session['username']
        # Retrieve user's account balance
        cursor.execute("SELECT balance FROM accounts WHERE holder_name = %s", (holder_name,))
        user_balance = cursor.fetchone()
        if user_balance:
            balance = user_balance['balance']
            print("Balance fetched from database:", balance)  # Debug statement
            return render_template('user_dashboard.html', username=session['username'], balance=balance)
        else:
            return "Error: User balance not found"
    return redirect(url_for('login'))
    # Function to fetch account balance for the currently logged-in user
def get_user_balance(user_id):
    cursor.execute("SELECT balance FROM accounts WHERE user_id = %s", (user_id,))
    user_balance = cursor.fetchone()
    if user_balance:
        return user_balance['balance']
    else:
        return None



# Route to add a new card
@app.route('/add_card', methods=['POST'])
def add_card():
    if session.get('role') == 'admin':
        # Retrieve card details from the form
        user_id = request.form['user_id']
        card_number = request.form['card_number']
        card_type = request.form['card_type']
        expiry_date = request.form['expiry_date']
        cvv = request.form['cvv']

        try:
            # Convert expiry_date to the correct format (YYYY-MM-DD)
            expiry_date = datetime.strptime(expiry_date, '%m%y').strftime('%Y-%m-%d')

            # Start a transaction
            conn.begin()

            # Insert card details into the database
            cursor.execute("INSERT INTO cards (user_id, card_number, card_type, expiration_date, CVV) VALUES (%s, %s, %s, %s, %s)",
                           (user_id, card_number, card_type, expiry_date, cvv))

            # Commit changes to the database
            conn.commit()

            return redirect(url_for('admin_dashboard'))

        except Exception as e:
            # Rollback changes if an error occurs
            conn.rollback()
            return f"Error occurred: {str(e)}"

    return redirect(url_for('login'))
  # Add New User and Create Account route
@app.route('/add_user', methods=['POST'])
def add_user():
    if 'username' in session:
        if session.get('role') == 'admin':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            holder_name = request.form['holder_name']
            initial_balance = float(request.form['initial_balance'])

            try:
                # Start a transaction
                conn.begin()

                # Insert new user into users table
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))

                # Retrieve the newly created user's ID
                cursor.execute("SELECT LAST_INSERT_ID() AS user_id")
                user_id = cursor.fetchone()['user_id']

                # Insert a corresponding account into accounts table
                cursor.execute("INSERT INTO accounts (user_id, holder_name, balance) VALUES (%s, %s, %s)", (user_id, holder_name, initial_balance))

                # Commit changes to the database
                conn.commit()

                return redirect(url_for('admin_dashboard'))

            except Exception as e:
                # Rollback changes if an error occurs
                conn.rollback()
                return f"Error occurred: {str(e)}"

    return redirect(url_for('login'))

  
'''@app.route('/add_user', methods=['POST'])
def add_user():
    if 'username' in session:
        if session.get('role') == 'admin':
            username = request.form['username']
            password = request.form['password']
            role = request.form['role']
            holder_name = request.form['holder_name']
            initial_balance = float(request.form['initial_balance'])

            try:
                # Start a transaction
                conn.begin()

                # Insert new user into users table
                cursor.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))

                # Retrieve the newly created user's ID
                cursor.execute("SELECT LAST_INSERT_ID() AS user_id")
                user_id = cursor.fetchone()['user_id']

                # Insert a corresponding account into accounts table
                # cursor.execute("INSERT INTO accounts (user_id, holder_name, balance) VALUES (%s, %s, %s)", (user_id, holder_name, initial_balance))                                                   
                cursor.execute("INSERT INTO accounts (user_id, holder_name, balance) VALUES (%s, %s, %s)", (user_id, holder_name, initial_balance)) 
                  
               # Commit changes to the database
                conn.commit()

                return redirect(url_for('admin_dashboard'))

            except Exception as e:
                # Rollback changes if an error occurs
                conn.rollback()
                return f"Error occurred: {str(e)}"

    return redirect(url_for('login'))'''
    

# Create Loan Against User ID route
@app.route('/create_loan', methods=['POST'])
def create_loan():
    if 'username' in session:
        if session.get('role') == 'admin':
            user_id = int(request.form['user_id'])
            amount = float(request.form['amount'])
            interest_rate = float(request.form['interest_rate'])
            term_months = int(request.form['term_months'])

            try:
                # Start a transaction
                conn.begin()

                # Insert loan details into loans table
                cursor.execute("INSERT INTO loans (user_id, amount, interest_rate, term_months) VALUES (%s, %s, %s, %s)", (user_id, amount, interest_rate, term_months))

                # Commit changes to the database
                conn.commit()

                return redirect(url_for('admin_dashboard'))

            except Exception as e:
                # Rollback changes if an error occurs
                conn.rollback()
                return f"Error occurred: {str(e)}"

    return redirect(url_for('login'))

# Add Money to Any Account route
@app.route('/add_money', methods=['POST'])
def add_money():
    if 'username' in session:
        if session.get('role') == 'admin':
            account_number = int(request.form['account_number'])
            amount = float(request.form['amount'])

            try:
                # Start a transaction
                conn.begin()

                # Update balance of the specified account
                cursor.execute("UPDATE accounts SET balance = balance + %s WHERE account_number = %s", (amount, account_number))

                # Commit changes to the database
                conn.commit()

                return redirect(url_for('admin_dashboard'))

            except Exception as e:
                # Rollback changes if an error occurs
                conn.rollback()
                return f"Error occurred: {str(e)}"

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)

