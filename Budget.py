import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Initialize main window
root = tk.Tk()
root.title("Monthly Budget Tracker")
root.geometry("800x600")

# Placeholder for combined data
data = pd.DataFrame()


# Function to load multiple CSV or Excel files
def load_files():
    global data
    file_paths = filedialog.askopenfilenames(filetypes=[("CSV files", "*.csv"), ("Excel files", "*.xlsx")])

    if file_paths:
        try:
            # Initialize an empty list to hold dataframes
            dfs = []
            for file_path in file_paths:
                if file_path.endswith(".csv"):
                    dfs.append(pd.read_csv(file_path))
                else:
                    dfs.append(pd.read_excel(file_path))

            # Combine all dataframes into one
            data = pd.concat(dfs, ignore_index=True)

            # Check if 'Booking Date' is in the DataFrame
            if 'Posting Date' in data.columns:
                # Convert 'Booking Date' column to datetime format
                data['Posting Date'] = pd.to_datetime(data['Posting Date'], format='%m/%d/%Y', errors='coerce')
                # Rename 'Booking Date' to 'Date' for consistency
                data.rename(columns={'Posting Date': 'Date'}, inplace=True)

                # Check for any NaT (Not a Time) values in the 'Date' column
                if data['Date'].isna().sum() > 0:
                    messagebox.showwarning("Warning", "Some dates could not be parsed and have been set to NaT.")

                # Remove or comment out this print statement
                # print(data.head())  # Debugging: Show the first few rows of the loaded data

                # Create a custom success message window
                success_window = tk.Toplevel(root)
                success_window.title("File Loaded")

                # Set window size and calculate position to center it
                window_width = 300
                window_height = 100
                screen_width = success_window.winfo_screenwidth()
                screen_height = success_window.winfo_screenheight()
                x = (screen_width // 2) - (window_width // 2)
                y = (screen_height // 2) - (window_height // 2)
                success_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

                success_window_label = tk.Label(success_window, text=f"Success! Loaded {len(file_paths)} files.")
                success_window_label.pack(pady=20)  # Add some padding

                # Automatically close the success window after 1000 milliseconds (1 second)
                success_window.after(1000, success_window.destroy)

                # Populate month and year options
                update_month_year_options()
            else:
                messagebox.showerror("Error", "No 'Posting Date' column found in the files.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while loading the files: {str(e)}")


# Function to categorize expenses
def categorize_expenses(filtered_data):
    # Initialize categories
    def categorize_expenses(filtered_data):
        # Initialize categories
        filtered_data['Category'] = "Other"  # Default category

        # Assign categories based on 'Credit Debit Indicator'
        filtered_data.loc[filtered_data['Credit Debit Indicator'] == 'Credit', 'Category'] = 'Income'
        filtered_data.loc[filtered_data['Credit Debit Indicator'] == 'Debit', 'Category'] = 'Expense'

        return filtered_data


# Function to update month and year dropdowns based on available data
def update_month_year_options():
    months = sorted(data['Date'].dt.month.unique())
    years = sorted(data['Date'].dt.year.unique())
    month_menu['values'] = months
    year_menu['values'] = years


# Function to filter data based on selected month and year
def filter_data():
    global filtered_data
    selected_month = month_var.get()
    selected_year = year_var.get()

    # Check if both month and year are selected
    if selected_month == 0 or selected_year == 0:
        messagebox.showwarning("Warning", "Please select both a month and a year.")
        return  # Exit the function if either is not selected

    # Filter data by selected month and year
    filtered_data = data[(data['Date'].dt.month == selected_month) & (data['Date'].dt.year == selected_year)].copy()

    if not filtered_data.empty:
        categorize_expenses(filtered_data)
        show_summary(filtered_data)  # Now displays the total transactions in the summary
        show_pie_chart(filtered_data)
    else:
        messagebox.showwarning("No Data", "No records found for the selected month and year.")


# Function to show summary in a table
def show_summary(filtered_data):
    if filtered_data.empty:
        return

    # Create a new column 'Adjusted Amount' where 'Credit' is positive and 'Debit' is negative
    filtered_data['Adjusted Amount'] = filtered_data.apply(
        lambda row: row['Amount'] if row['Credit Debit Indicator'] == 'Credit' else -row['Amount'], axis=1
    )

    # Calculate total income and total expenses
    total_income = filtered_data[filtered_data['Credit Debit Indicator'] == 'Credit']['Amount'].sum()
    total_spent = filtered_data[filtered_data['Credit Debit Indicator'] == 'Debit']['Amount'].sum()

    # Update the total income and spent labels
    total_income_label.config(text=f"Total Income for {month_var.get()}/{year_var.get()}: ${total_income:,.2f}")
    total_spent_label.config(text=f"Total Expenses for {month_var.get()}/{year_var.get()}: ${total_spent:,.2f}")

    total_transactions = len(filtered_data)
    total_label.config(text=f"Total Transactions Pulled from CSV File: {total_transactions}")

    # Calculate net income
    net_income = total_income - total_spent
    net_income_label.config(text=f"Net Income: ${net_income:,.2f} ({'Positive' if net_income >= 0 else 'Negative'})")

    # Grouping by category using the 'Adjusted Amount'
    summary = filtered_data.groupby("Category")['Adjusted Amount'].sum().reset_index()

    # Clear the summary tree before inserting new values
    for row in summary_tree.get_children():
        summary_tree.delete(row)

    # Insert new summary data into the tree
    for _, row in summary.iterrows():
        formatted_amount = f"${row['Adjusted Amount']:,.2f}"
        summary_tree.insert("", tk.END, values=(row['Category'], formatted_amount))
# Function to create a pie chart
def show_pie_chart(filtered_data):
    if filtered_data.empty:
        return

    summary = filtered_data.groupby("Category")['Amount'].sum()

    for widget in chart_frame.winfo_children():
        widget.destroy()

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(summary, labels=summary.index, autopct="%1.1f%%", startangle=90)
    ax.set_title(f"Expenses by Category - {month_var.get()}/{year_var.get()}")

    chart_canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    chart_canvas.get_tk_widget().pack()
    chart_canvas.draw()

def on_closing():
    root.quit()  # Close the application when the window is closed

# Calculate the center position for the window
window_width = 800  # Set your desired window width
window_height = 600  # Set your desired window height

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate x and y coordinates for the window
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)

# Set the dimensions of the window and position it in the center of the screen
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Call the on_closing function when the window is closed
root.protocol("WM_DELETE_WINDOW", on_closing)

# GUI Layout
notebook = ttk.Notebook(root)
notebook.pack(fill="both", expand=True)

load_tab = ttk.Frame(notebook)
notebook.add(load_tab, text="Load Files")

# Load bank statement button
load_button = tk.Button(load_tab, text="Load Bank Statements", command=load_files)
load_button.pack(pady=20)

# Month and Year Dropdowns for filtering
month_var = tk.IntVar()
year_var = tk.IntVar()

month_label = tk.Label(load_tab, text="Select Month:")
month_label.pack()
month_menu = ttk.Combobox(load_tab, textvariable=month_var)
month_menu.pack()

year_label = tk.Label(load_tab, text="Select Year:")
year_label.pack()
year_menu = ttk.Combobox(load_tab, textvariable=year_var)
year_menu.pack()

filter_button = tk.Button(load_tab, text="Filter Data", command=filter_data)
filter_button.pack(pady=10)

# Tab for Summary Table
summary_tab = ttk.Frame(notebook)
notebook.add(summary_tab, text="Summary")

# Label for total transactions
total_label = tk.Label(summary_tab, text="Total Transactions Pulled from CSV File: 0")
total_label.pack(pady=10)

# Add labels to display total income and total money spent
total_income_label = tk.Label(summary_tab, text="Total Income for 0/0: $0.00")
total_income_label.pack(pady=5)

total_spent_label = tk.Label(summary_tab, text="Total Money Spent for 0/0: $0.00")
total_spent_label.pack(pady=5)

# Add label for net income
net_income_label = tk.Label(summary_tab, text="Net Income: $0.00 (Neutral)")
net_income_label.pack(pady=5)

# Treeview for summary
summary_tree = ttk.Treeview(summary_tab, columns=("Category", "Amount"), show="headings")
summary_tree.heading("Category", text="Category")
summary_tree.heading("Amount", text="Amount")
summary_tree.pack(fill="both", expand=True)

# Tab for Pie Chart
chart_tab = ttk.Frame(notebook)
notebook.add(chart_tab, text="Pie Chart")

chart_frame = ttk.Frame(chart_tab)
chart_frame.pack(fill="both", expand=True)

root.mainloop()