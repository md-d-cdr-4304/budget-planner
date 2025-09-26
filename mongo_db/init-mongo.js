// MongoDB initialization script
// This script runs when the MongoDB container starts for the first time

// Switch to the budget_planner database
db = db.getSiblingDB('budget_planner');

// Create collections
db.createCollection('users');
db.createCollection('monthly_budgets');
db.createCollection('daily_expenses');

// Create indexes for better performance
db.users.createIndex({ "username": 1 }, { unique: true });
db.monthly_budgets.createIndex({ "user_id": 1, "month": 1 });
db.daily_expenses.createIndex({ "user_id": 1, "date": 1 });

// Insert sample data (optional)
db.users.insertOne({
    username: "demo",
    password: "5e884898da28047151d0e56f8dc6292773603d0d6aabbdd62a11ef721d1542d8", // "password" hashed
    created_at: new Date()
});

print("MongoDB initialization completed successfully!");


