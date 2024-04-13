"""
Expenses table
"""

CREATE TABLE expenses (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    expense VARCHAR(500),
    category VARCHAR(100) NOT NULL,
    amount INTEGER NOT NULL,
    description VARCHAR(500),
    paymentMethod VARCHAR(100) NOT NULL,
    thisMonth INTEGER NOT NULL,
    date DATETIME,
    createdAt DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt DATETIME DEFAULT CURRENT_TIMESTAMP,
    deletedAt DATETIME DEFAULT NULL,
    FOREIGN KEY (userId) REFERENCES users(id)
);
