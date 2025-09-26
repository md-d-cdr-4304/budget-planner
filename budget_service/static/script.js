// Budget Planner JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the dashboard
    if (document.getElementById('monthlyBudgetForm')) {
        initializeDashboard();
    }
    
    // Initialize login page
    if (document.getElementById('loginForm')) {
        initializeLogin();
    }
});

function initializeDashboard() {
    // Monthly Budget Form Handler
    document.getElementById('monthlyBudgetForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addMonthlyBudget();
    });
    
    // Daily Expense Form Handler
    document.getElementById('dailyExpenseForm').addEventListener('submit', function(e) {
        e.preventDefault();
        addDailyExpense();
    });
    
    // Load existing data
    loadMonthlyBudgets();
    loadDailyExpenses();
    updateSummary();
}

function initializeLogin() {
    // Add form validation and UX improvements
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.disabled = true;
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Processing...';
            }
        });
    });
}

async function addMonthlyBudget() {
    const form = document.getElementById('monthlyBudgetForm');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    try {
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Adding...';
        
        const budgetData = {
            category: document.getElementById('budgetCategory').value,
            amount: parseFloat(document.getElementById('budgetAmount').value),
            month: document.getElementById('budgetMonth').value
        };
        
        const response = await fetch('/api/monthly-budgets', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(budgetData)
        });
        
        if (response.ok) {
            const budget = await response.json();
            addBudgetToList(budget);
            allBudgets.push(budget);
            form.reset();
            showAlert('Monthly budget added successfully!', 'success');
            updateSummary();
            updateItemCounters();
        } else {
            const error = await response.json();
            showAlert(error.error || 'Failed to add monthly budget', 'danger');
        }
    } catch (error) {
        console.error('Error adding monthly budget:', error);
        showAlert('Failed to add monthly budget. Please try again.', 'danger');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Add Monthly Budget';
    }
}

async function addDailyExpense() {
    const form = document.getElementById('dailyExpenseForm');
    const submitBtn = form.querySelector('button[type="submit"]');
    
    try {
        // Show loading state
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Adding...';
        
        const expenseData = {
            description: document.getElementById('expenseDescription').value,
            amount: parseFloat(document.getElementById('expenseAmount').value),
            category: document.getElementById('expenseCategory').value,
            date: document.getElementById('expenseDate').value
        };
        
        const response = await fetch('/api/daily-expenses', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(expenseData)
        });
        
        if (response.ok) {
            const expense = await response.json();
            addExpenseToList(expense);
            allExpenses.push(expense);
            form.reset();
            showAlert('Daily expense added successfully!', 'success');
            updateSummary();
            updateExpenseChart();
            updateItemCounters();
        } else {
            const error = await response.json();
            showAlert(error.error || 'Failed to add daily expense', 'danger');
        }
    } catch (error) {
        console.error('Error adding daily expense:', error);
        showAlert('Failed to add daily expense. Please try again.', 'danger');
    } finally {
        // Reset button state
        submitBtn.disabled = false;
        submitBtn.innerHTML = 'Add Daily Expense';
    }
}

async function loadMonthlyBudgets() {
    try {
        const response = await fetch('/api/monthly-budgets');
        if (response.ok) {
            const budgets = await response.json();
            const container = document.getElementById('monthlyBudgetsList');
            container.innerHTML = '';
            budgets.forEach(budget => addBudgetToList(budget));
        }
    } catch (error) {
        console.error('Error loading monthly budgets:', error);
    }
}

async function loadDailyExpenses() {
    try {
        const response = await fetch('/api/daily-expenses');
        if (response.ok) {
            const expenses = await response.json();
            const container = document.getElementById('dailyExpensesList');
            container.innerHTML = '';
            expenses.forEach(expense => addExpenseToList(expense));
        }
    } catch (error) {
        console.error('Error loading daily expenses:', error);
    }
}

function addBudgetToList(budget) {
    const container = document.getElementById('monthlyBudgetsList');
    const budgetElement = document.createElement('div');
    budgetElement.className = 'budget-item mb-2 p-2 border rounded fade-in';
    budgetElement.setAttribute('data-budget-id', budget._id);
    budgetElement.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center">
                <input type="checkbox" class="form-check-input me-2 bulk-select-checkbox" data-id="${budget._id}" style="display: none;">
                <div>
                    <strong>${budget.category}</strong>
                    <small class="text-muted d-block">${budget.month}</small>
                </div>
            </div>
            <div class="d-flex align-items-center gap-2">
                <span class="badge bg-primary">$${budget.amount.toFixed(2)}</span>
                <button class="btn btn-sm btn-outline-primary edit-budget-btn" 
                        data-id="${budget._id}" 
                        data-category="${budget.category}" 
                        data-amount="${budget.amount}" 
                        data-month="${budget.month}">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger delete-budget-btn" data-id="${budget._id}">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(budgetElement);
}

function addExpenseToList(expense) {
    const container = document.getElementById('dailyExpensesList');
    const expenseElement = document.createElement('div');
    expenseElement.className = 'expense-item mb-2 p-2 border rounded fade-in';
    expenseElement.setAttribute('data-expense-id', expense._id);
    expenseElement.innerHTML = `
        <div class="d-flex justify-content-between align-items-center">
            <div class="d-flex align-items-center">
                <input type="checkbox" class="form-check-input me-2 bulk-select-checkbox" data-id="${expense._id}" style="display: none;">
                <div>
                    <strong>${expense.description}</strong>
                    <small class="text-muted d-block">${expense.category} - ${expense.date}</small>
                </div>
            </div>
            <div class="d-flex align-items-center gap-2">
                <span class="badge bg-danger">$${expense.amount.toFixed(2)}</span>
                <button class="btn btn-sm btn-outline-primary edit-expense-btn" 
                        data-id="${expense._id}" 
                        data-description="${expense.description}" 
                        data-amount="${expense.amount}" 
                        data-category="${expense.category}" 
                        data-date="${expense.date}">
                    <i class="fas fa-edit"></i>
                </button>
                <button class="btn btn-sm btn-outline-danger delete-expense-btn" data-id="${expense._id}">
                    <i class="fas fa-trash"></i>
                </button>
            </div>
        </div>
    `;
    container.appendChild(expenseElement);
}

function updateSummary() {
    // Calculate totals
    const budgetItems = document.querySelectorAll('.budget-item .badge');
    const expenseItems = document.querySelectorAll('.expense-item .badge');
    
    let totalBudget = 0;
    let totalExpenses = 0;
    
    budgetItems.forEach(item => {
        const amount = parseFloat(item.textContent.replace('$', ''));
        totalBudget += amount;
    });
    
    expenseItems.forEach(item => {
        const amount = parseFloat(item.textContent.replace('$', ''));
        totalExpenses += amount;
    });
    
    const remaining = totalBudget - totalExpenses;
    
    // Update display
    document.getElementById('totalBudget').textContent = `$${totalBudget.toFixed(2)}`;
    document.getElementById('totalExpenses').textContent = `$${totalExpenses.toFixed(2)}`;
    document.getElementById('remaining').textContent = `$${remaining.toFixed(2)}`;
    
    // Color code remaining amount
    const remainingElement = document.getElementById('remaining');
    if (remaining < 0) {
        remainingElement.className = 'text-danger';
    } else if (remaining > totalBudget * 0.2) {
        remainingElement.className = 'text-success';
    } else {
        remainingElement.className = 'text-warning';
    }
}

function showAlert(message, type) {
    const alertContainer = document.getElementById('alertContainer');
    const alertId = 'alert-' + Date.now();
    
    const alertElement = document.createElement('div');
    alertElement.id = alertId;
    alertElement.className = `alert alert-${type} alert-dismissible fade show`;
    alertElement.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    alertContainer.appendChild(alertElement);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        const alert = document.getElementById(alertId);
        if (alert) {
            alert.remove();
        }
    }, 5000);
}

// Utility function to format currency
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

// Set default date to today
document.addEventListener('DOMContentLoaded', function() {
    const today = new Date().toISOString().split('T')[0];
    const monthInput = document.getElementById('budgetMonth');
    const dateInput = document.getElementById('expenseDate');
    
    if (monthInput) {
        const currentMonth = new Date().toISOString().slice(0, 7);
        monthInput.value = currentMonth;
    }
    
    if (dateInput) {
        dateInput.value = today;
    }
});

// Edit and Delete Functions for Budgets
function editBudget(id, category, amount, month) {
    document.getElementById('editBudgetId').value = id;
    document.getElementById('editBudgetCategory').value = category;
    document.getElementById('editBudgetAmount').value = amount;
    document.getElementById('editBudgetMonth').value = month;
    document.getElementById('editBudgetForm').style.display = 'block';
    
    // Scroll to edit form
    document.getElementById('editBudgetForm').scrollIntoView({ behavior: 'smooth' });
}

function cancelEditBudget() {
    document.getElementById('editBudgetForm').style.display = 'none';
    document.getElementById('editBudgetFormElement').reset();
}

async function deleteBudget(id) {
    if (!confirm('Are you sure you want to delete this budget?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/monthly-budgets/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Remove the budget item from the UI
            const budgetItem = document.querySelector(`[data-budget-id="${id}"]`);
            if (budgetItem) {
                budgetItem.remove();
            }
            showAlert('Budget deleted successfully!', 'success');
            updateSummary();
        } else {
            const error = await response.json();
            showAlert(error.error || 'Failed to delete budget', 'danger');
        }
    } catch (error) {
        console.error('Error deleting budget:', error);
        showAlert('Failed to delete budget. Please try again.', 'danger');
    }
}

// Edit and Delete Functions for Expenses
function editExpense(id, description, amount, category, date) {
    document.getElementById('editExpenseId').value = id;
    document.getElementById('editExpenseDescription').value = description;
    document.getElementById('editExpenseAmount').value = amount;
    document.getElementById('editExpenseCategory').value = category;
    document.getElementById('editExpenseDate').value = date;
    document.getElementById('editExpenseForm').style.display = 'block';
    
    // Scroll to edit form
    document.getElementById('editExpenseForm').scrollIntoView({ behavior: 'smooth' });
}

function cancelEditExpense() {
    document.getElementById('editExpenseForm').style.display = 'none';
    document.getElementById('editExpenseFormElement').reset();
}

async function deleteExpense(id) {
    if (!confirm('Are you sure you want to delete this expense?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/daily-expenses/${id}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            // Remove the expense item from the UI
            const expenseItem = document.querySelector(`[data-expense-id="${id}"]`);
            if (expenseItem) {
                expenseItem.remove();
            }
            showAlert('Expense deleted successfully!', 'success');
            updateSummary();
        } else {
            const error = await response.json();
            showAlert(error.error || 'Failed to delete expense', 'danger');
        }
    } catch (error) {
        console.error('Error deleting expense:', error);
        showAlert('Failed to delete expense. Please try again.', 'danger');
    }
}

// Add event listeners for edit forms
document.addEventListener('DOMContentLoaded', function() {
    // Add event listeners for edit and delete buttons
    document.addEventListener('click', function(e) {
        if (e.target.closest('.edit-budget-btn')) {
            const btn = e.target.closest('.edit-budget-btn');
            const id = btn.dataset.id;
            const category = btn.dataset.category;
            const amount = btn.dataset.amount;
            const month = btn.dataset.month;
            editBudget(id, category, amount, month);
        }
        
        if (e.target.closest('.delete-budget-btn')) {
            const btn = e.target.closest('.delete-budget-btn');
            const id = btn.dataset.id;
            deleteBudget(id);
        }
        
        if (e.target.closest('.edit-expense-btn')) {
            const btn = e.target.closest('.edit-expense-btn');
            const id = btn.dataset.id;
            const description = btn.dataset.description;
            const amount = btn.dataset.amount;
            const category = btn.dataset.category;
            const date = btn.dataset.date;
            editExpense(id, description, amount, category, date);
        }
        
        if (e.target.closest('.delete-expense-btn')) {
            const btn = e.target.closest('.delete-expense-btn');
            const id = btn.dataset.id;
            deleteExpense(id);
        }
    });
    
    // Edit Budget Form Handler
    const editBudgetForm = document.getElementById('editBudgetFormElement');
    if (editBudgetForm) {
        editBudgetForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const id = document.getElementById('editBudgetId').value;
            const budgetData = {
                category: document.getElementById('editBudgetCategory').value,
                amount: parseFloat(document.getElementById('editBudgetAmount').value),
                month: document.getElementById('editBudgetMonth').value
            };
            
            try {
                const response = await fetch(`/api/monthly-budgets/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(budgetData)
                });
                
                if (response.ok) {
                    const updatedBudget = await response.json();
                    // Update the budget item in the UI
                    const budgetItem = document.querySelector(`[data-budget-id="${id}"]`);
                    if (budgetItem) {
                        budgetItem.querySelector('strong').textContent = updatedBudget.category;
                        budgetItem.querySelector('.text-muted').textContent = updatedBudget.month;
                        budgetItem.querySelector('.badge').textContent = `$${updatedBudget.amount.toFixed(2)}`;
                    }
                    showAlert('Budget updated successfully!', 'success');
                    cancelEditBudget();
                    updateSummary();
                } else {
                    const error = await response.json();
                    showAlert(error.error || 'Failed to update budget', 'danger');
                }
            } catch (error) {
                console.error('Error updating budget:', error);
                showAlert('Failed to update budget. Please try again.', 'danger');
            }
        });
    }
    
    // Edit Expense Form Handler
    const editExpenseForm = document.getElementById('editExpenseFormElement');
    if (editExpenseForm) {
        editExpenseForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const id = document.getElementById('editExpenseId').value;
            const expenseData = {
                description: document.getElementById('editExpenseDescription').value,
                amount: parseFloat(document.getElementById('editExpenseAmount').value),
                category: document.getElementById('editExpenseCategory').value,
                date: document.getElementById('editExpenseDate').value
            };
            
            try {
                const response = await fetch(`/api/daily-expenses/${id}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(expenseData)
                });
                
                if (response.ok) {
                    const updatedExpense = await response.json();
                    // Update the expense item in the UI
                    const expenseItem = document.querySelector(`[data-expense-id="${id}"]`);
                    if (expenseItem) {
                        expenseItem.querySelector('strong').textContent = updatedExpense.description;
                        expenseItem.querySelector('.text-muted').textContent = `${updatedExpense.category} - ${updatedExpense.date}`;
                        expenseItem.querySelector('.badge').textContent = `$${updatedExpense.amount.toFixed(2)}`;
                    }
                    showAlert('Expense updated successfully!', 'success');
                    cancelEditExpense();
                    updateSummary();
                } else {
                    const error = await response.json();
                    showAlert(error.error || 'Failed to update expense', 'danger');
                }
            } catch (error) {
                console.error('Error updating expense:', error);
                showAlert('Failed to update expense. Please try again.', 'danger');
            }
        });
    }
});

// Global variables
let expenseChart = null;
let allBudgets = [];
let allExpenses = [];

// Initialize enhanced dashboard features
document.addEventListener('DOMContentLoaded', function() {
    initializeEnhancedFeatures();
});

function initializeEnhancedFeatures() {
    // Dark mode toggle
    const darkModeToggle = document.getElementById('darkModeToggle');
    const darkModeIcon = document.getElementById('darkModeIcon');
    
    // Check for saved dark mode preference
    const isDarkMode = localStorage.getItem('darkMode') === 'true';
    if (isDarkMode) {
        document.body.classList.add('dark-mode');
        darkModeIcon.className = 'fas fa-sun';
    }
    
    darkModeToggle.addEventListener('click', function() {
        document.body.classList.toggle('dark-mode');
        const isDark = document.body.classList.contains('dark-mode');
        darkModeIcon.className = isDark ? 'fas fa-sun' : 'fas fa-moon';
        localStorage.setItem('darkMode', isDark);
    });
    
    // Search functionality
    const searchInput = document.getElementById('searchInput');
    searchInput.addEventListener('input', function() {
        filterItems();
    });
    
    // Date filters
    const monthFilter = document.getElementById('monthFilter');
    const yearFilter = document.getElementById('yearFilter');
    
    monthFilter.addEventListener('change', filterItems);
    yearFilter.addEventListener('change', filterItems);
    
    // Bulk select mode
    const bulkSelectMode = document.getElementById('bulkSelectMode');
    const bulkDeleteBtn = document.getElementById('bulkDeleteBtn');
    
    bulkSelectMode.addEventListener('change', function() {
        const checkboxes = document.querySelectorAll('.bulk-select-checkbox');
        checkboxes.forEach(checkbox => {
            checkbox.style.display = this.checked ? 'block' : 'none';
        });
        bulkDeleteBtn.style.display = this.checked ? 'block' : 'none';
    });
    
    // Bulk delete functionality
    bulkDeleteBtn.addEventListener('click', function() {
        const selectedCheckboxes = document.querySelectorAll('.bulk-select-checkbox:checked');
        if (selectedCheckboxes.length === 0) {
            showAlert('Please select items to delete', 'warning');
            return;
        }
        
        if (confirm(`Are you sure you want to delete ${selectedCheckboxes.length} selected items?`)) {
            selectedCheckboxes.forEach(checkbox => {
                const item = checkbox.closest('.budget-item, .expense-item');
                if (item.classList.contains('budget-item')) {
                    deleteBudget(checkbox.dataset.id);
                } else {
                    deleteExpense(checkbox.dataset.id);
                }
            });
        }
    });
    
    // Initialize pie chart
    initializeExpenseChart();
    
    // Load initial data
    loadAllData();
}

function filterItems() {
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();
    const monthFilter = document.getElementById('monthFilter').value;
    const yearFilter = document.getElementById('yearFilter').value;
    
    const budgetItems = document.querySelectorAll('.budget-item');
    const expenseItems = document.querySelectorAll('.expense-item');
    
    let visibleBudgets = 0;
    let visibleExpenses = 0;
    
    // Filter budgets
    budgetItems.forEach(item => {
        const category = item.querySelector('strong').textContent.toLowerCase();
        const month = item.querySelector('.text-muted').textContent;
        const isVisible = (searchTerm === '' || category.includes(searchTerm)) &&
                         (monthFilter === '' || month.includes(monthFilter)) &&
                         (yearFilter === '' || month.includes(yearFilter));
        
        item.style.display = isVisible ? 'block' : 'none';
        if (isVisible) visibleBudgets++;
    });
    
    // Filter expenses
    expenseItems.forEach(item => {
        const description = item.querySelector('strong').textContent.toLowerCase();
        const category = item.querySelector('.text-muted').textContent.toLowerCase();
        const date = item.querySelector('.text-muted').textContent;
        const isVisible = (searchTerm === '' || description.includes(searchTerm) || category.includes(searchTerm)) &&
                         (monthFilter === '' || date.includes(monthFilter)) &&
                         (yearFilter === '' || date.includes(yearFilter));
        
        item.style.display = isVisible ? 'block' : 'none';
        if (isVisible) visibleExpenses++;
    });
    
    // Update counters
    document.getElementById('budgetCount').textContent = `${visibleBudgets} items`;
    document.getElementById('expenseCount').textContent = `${visibleExpenses} items`;
}

function initializeExpenseChart() {
    const ctx = document.getElementById('expenseChart').getContext('2d');
    expenseChart = new Chart(ctx, {
        type: 'pie',
        data: {
            labels: [],
            datasets: [{
                data: [],
                backgroundColor: [
                    '#FF6384',
                    '#36A2EB',
                    '#FFCE56',
                    '#4BC0C0',
                    '#9966FF',
                    '#FF9F40'
                ]
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

function updateExpenseChart() {
    if (!expenseChart) return;
    
    const categoryTotals = {};
    allExpenses.forEach(expense => {
        const category = expense.category || 'Other';
        categoryTotals[category] = (categoryTotals[category] || 0) + expense.amount;
    });
    
    const labels = Object.keys(categoryTotals);
    const data = Object.values(categoryTotals);
    
    expenseChart.data.labels = labels;
    expenseChart.data.datasets[0].data = data;
    expenseChart.update();
}

async function loadAllData() {
    try {
        // Load budgets
        const budgetResponse = await fetch('/api/monthly-budgets');
        if (budgetResponse.ok) {
            allBudgets = await budgetResponse.json();
        }
        
        // Load expenses
        const expenseResponse = await fetch('/api/daily-expenses');
        if (expenseResponse.ok) {
            allExpenses = await expenseResponse.json();
        }
        
        // Update chart and counters
        updateExpenseChart();
        updateItemCounters();
        
    } catch (error) {
        console.error('Error loading data:', error);
    }
}

function updateItemCounters() {
    const budgetItems = document.querySelectorAll('.budget-item');
    const expenseItems = document.querySelectorAll('.expense-item');
    
    let visibleBudgets = 0;
    let visibleExpenses = 0;
    
    budgetItems.forEach(item => {
        if (item.style.display !== 'none') visibleBudgets++;
    });
    
    expenseItems.forEach(item => {
        if (item.style.display !== 'none') visibleExpenses++;
    });
    
    document.getElementById('budgetCount').textContent = `${visibleBudgets} items`;
    document.getElementById('expenseCount').textContent = `${visibleExpenses} items`;
}


