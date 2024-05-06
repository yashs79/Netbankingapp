-- Create the users table
CREATE TABLE users (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  username VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  role VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create the accounts table with the user_id foreign key
CREATE TABLE accounts (
  account_number INTEGER PRIMARY KEY AUTO_INCREMENT,
  holder_name VARCHAR(255) NOT NULL,
  balance REAL NOT NULL,
  user_id INTEGER,
  CONSTRAINT fk_user_id FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the transactions table with the user_id foreign key
CREATE TABLE transactions (
  id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  transaction_type VARCHAR(255),
  amount REAL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the loans table with the user_id foreign key
CREATE TABLE loans (
  loan_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  amount REAL NOT NULL,
  interest_rate REAL NOT NULL,
  term_months INTEGER NOT NULL,
  start_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the withdrawals table with the user_id foreign key
CREATE TABLE withdrawals (
  withdrawal_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  amount REAL NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the deposits table with the user_id foreign key
CREATE TABLE deposits (
  deposit_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  amount REAL NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the online_transfers table with the sender_user_id and receiver_user_id foreign keys
CREATE TABLE online_transfers (
  transfer_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  sender_user_id INTEGER,
  receiver_user_id INTEGER,
  amount REAL NOT NULL,
  timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (sender_user_id) REFERENCES users(id),
  FOREIGN KEY (receiver_user_id) REFERENCES users(id)
);

-- Create the cards table with the user_id foreign key
CREATE TABLE cards (
  card_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  card_type VARCHAR(255) NOT NULL,
  card_number VARCHAR(255) NOT NULL,
  expiration_date DATE NOT NULL,
  CVV VARCHAR(3) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the beneficiaries table with the user_id foreign key
CREATE TABLE beneficiaries (
  beneficiary_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  beneficiary_name VARCHAR(255) NOT NULL,
  account_number_beneficiary VARCHAR(255) NOT NULL,
  bank_name_beneficiary VARCHAR(255),
  relationship VARCHAR(255),
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the payees table with the user_id foreign key
CREATE TABLE payees (
  payee_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  payee_name VARCHAR(255) NOT NULL,
  payment_details TEXT,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the bill_payment table with the user_id and payee_id foreign keys
CREATE TABLE bill_payment (
  payment_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  payee_id INTEGER,
  amount REAL NOT NULL,
  due_date DATE,
  payment_date DATE,
  payment_status VARCHAR(255) NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users(id),
  FOREIGN KEY (payee_id) REFERENCES payees(payee_id)
);

-- Create the credit_score table with the user_id foreign key
CREATE TABLE credit_score (
  score_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  credit_score INTEGER,
  last_updated DATE,
  FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Create the branch_details table
CREATE TABLE branch_details (
  branch_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  branch_name VARCHAR(255) NOT NULL,
  address TEXT NOT NULL,
  contact_number VARCHAR(255),
  operating_hours TEXT
);

-- Create the customer_support table with the user_id foreign key
CREATE TABLE customer_support (
  ticket_id INTEGER PRIMARY KEY AUTO_INCREMENT,
  user_id INTEGER,
  subject VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  status VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  closed_at TIMESTAMP,
  FOREIGN KEY (user_id) REFERENCES users(id)
);
