import tkinter as tk
import json

def load_users():
    # Load users from the file
    try:
        with open('users.json', 'r') as file:
            data = json.load(file)
            return data.get('users', [])
    except FileNotFoundError:
        return []

def save_users(users):
    # Save users to the file
    with open('users.json', 'w') as file:
        json.dump({"users": users}, file)

def add_user():
    # Get data from input fields and save the new user
    name = name_entry.get()
    email = email_entry.get()
    halls = halls_entry.get().split(', ')  # Assuming comma-separated input
    meals = meals_entry.get().split(', ')  # Assuming comma-separated input
    users.append({'name': name, 'email': email, 'halls': halls, 'meals': meals})
    save_users(users)
    update_dropdown()

def remove_user():
    # Remove the selected user
    selected_name = selected_user_var.get()
    global users
    users = [user for user in users if user['name'] != selected_name]
    save_users(users)
    update_dropdown()

def update_dropdown():
    # Update the dropdown menu with users
    dropdown['menu'].delete(0, 'end')
    for user in users:
        dropdown['menu'].add_command(label=user['name'], command=lambda value=user['name']: selected_user_var.set(value))
    selected_user_var.set('')

# Create the main window
root = tk.Tk()
root.title("User Management")

# Load existing users
users = load_users()

# User input fields
name_entry = tk.Entry(root)
name_entry.pack()
email_entry = tk.Entry(root)
email_entry.pack()
halls_entry = tk.Entry(root)
halls_entry.pack()
meals_entry = tk.Entry(root)
meals_entry.pack()

# Submit button for adding new users
submit_button = tk.Button(root, text="Add User", command=add_user)
submit_button.pack()

# Dropdown for selecting existing users
selected_user_var = tk.StringVar(root)
dropdown = tk.OptionMenu(root, selected_user_var, *[user['name'] for user in users])
dropdown.pack()

# Buttons for user-specific actions
remove_button = tk.Button(root, text="Remove Selected User", command=remove_user)
remove_button.pack()
# ... add more buttons for updating dining halls and meals ...

# Start the Tkinter event loop
root.mainloop()
