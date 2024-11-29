import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# Function to calculate results
def calculate():
    global contributions_list, interests_list

    # Reset the lists for each calculation
    contributions_list = []
    interests_list = []

    try:
        principal = float(principal_entry.get())
        monthly_contribution = float(contribution_entry.get())
        current_age = int(current_age_entry.get())
        retirement_age = int(retirement_age_entry.get())
        withdrawal_years = int(withdrawal_years_entry.get())  # Added withdrawal years input
    except ValueError:
        for text_widget in result_text_widgets:
            text_widget.delete(1.0, tk.END)
            text_widget.insert(tk.END, "Please enter valid numbers for all fields.\n")
        return

    years_until_retirement = retirement_age - current_age
    withdrawal_rates = [3, 4]  # Withdrawal rates in percentages
    average_annual_returns = [6, 8, 10]  # Annual returns in percentages

    # Clear previous results in all tabs
    for text_widget in result_text_widgets:
        text_widget.delete(1.0, tk.END)

    for i, rate in enumerate(average_annual_returns):
        annual_rate = rate / 100
        total_balance = principal
        contributions = principal
        annual_contributions = monthly_contribution * 12

        total_principal = principal  # Start with the initial principal
        total_interest = 0  # Initialize total interest earned

        contributions_progress = []
        interests_progress = []

        for year in range(years_until_retirement):
            total_balance += annual_contributions
            total_principal += annual_contributions  # Adding yearly contributions to total principal
            total_balance *= (1 + annual_rate)

            # Track contributions and interests for graphing purposes
            contributions_progress.append(total_principal)
            interests_progress.append(total_balance - total_principal)

        # Append the progress data to the global lists
        contributions_list.append(contributions_progress)
        interests_list.append(interests_progress)

        total_interest = total_balance - total_principal  # Calculate total interest earned at retirement

        # Display Results for Retirement
        result_text_widgets[i].delete(1.0, tk.END)
        result_text_widgets[i].insert(
            tk.END,
            f"--- Results for {rate}% Average Annual Return ---\n"
            f"Total amount at retirement: ${total_balance:,.2f}\n"
            f"Total Invested (Principal + Contributions): ${total_principal:,.2f}\n"
            f"Total Interest Earned: ${total_interest:,.2f}\n"
        )

        for withdraw_rate in withdrawal_rates:
            withdraw_rate_decimal = withdraw_rate / 100
            annual_withdrawal = total_balance * withdraw_rate_decimal
            monthly_withdrawal = annual_withdrawal / 12

            # Calculate balance after withdrawals
            balance_after_withdrawals = total_balance
            for _ in range(withdrawal_years):
                balance_after_withdrawals -= annual_withdrawal
                balance_after_withdrawals *= (1 + annual_rate)

            result_text_widgets[i].insert(
                tk.END,
                f"Withdrawal Rate: {withdraw_rate}%\n"
                f"  Annual withdrawal: ${annual_withdrawal:,.2f}\n"
                f"  Monthly withdrawal: ${monthly_withdrawal:,.2f}\n"
                f"  Balance after {withdrawal_years} years of withdrawals: ${balance_after_withdrawals:,.2f}\n\n"
            )

# Function to plot the graph for a selected rate
def plot_graph(rate_index):
    if not contributions_list or not interests_list:
        return

    years = list(range(1, len(contributions_list[rate_index]) + 1))
    contributions = contributions_list[rate_index]
    interest = interests_list[rate_index]

    # Create a Matplotlib figure
    fig, ax = plt.subplots(figsize=(5, 4))
    ax.fill_between(years, contributions, label="Contributions", color="skyblue", alpha=0.6)
    ax.fill_between(years, [c + i for c, i in zip(contributions, interest)],
                    contributions, label="Interest Earned", color="orange", alpha=0.6)
    ax.set_title(f"Growth Breakdown for {average_annual_returns[rate_index]}% Return")
    ax.set_xlabel("Years")
    ax.set_ylabel("Balance ($)")
    ax.legend()

    # Embed the plot in the GUI
    for widget in graph_frame.winfo_children():
        widget.destroy()
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)
    canvas.draw()

# Set up the main window
root = tk.Tk()
root.title("Compound Interest Calculator with Graphs")

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Get the window's width and height
window_width = 1200  # You can adjust the window size as per your preference
window_height = 600  # You can adjust the window size as per your preference

# Calculate the position to center the window
position_top = int(screen_height / 2 - window_height / 2)
position_left = int(screen_width / 2 - window_width / 2)

# Set the window size and position
root.geometry(f'{window_width}x{window_height}+{position_left}+{position_top}')

# Left frame for inputs and tabs
left_frame = ttk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Input fields
input_frame = ttk.Frame(left_frame)
input_frame.pack(padx=10, pady=10, fill=tk.X)

ttk.Label(input_frame, text="Initial Investment Amount ($):").grid(row=0, column=0, sticky=tk.W)
principal_entry = ttk.Entry(input_frame)
principal_entry.grid(row=0, column=1)

ttk.Label(input_frame, text="Monthly Contribution ($):").grid(row=1, column=0, sticky=tk.W)
contribution_entry = ttk.Entry(input_frame)
contribution_entry.grid(row=1, column=1)

ttk.Label(input_frame, text="Current Age:").grid(row=2, column=0, sticky=tk.W)
current_age_entry = ttk.Entry(input_frame)
current_age_entry.grid(row=2, column=1)

ttk.Label(input_frame, text="Retirement Age:").grid(row=3, column=0, sticky=tk.W)
retirement_age_entry = ttk.Entry(input_frame)
retirement_age_entry.grid(row=3, column=1)

ttk.Label(input_frame, text="Withdrawal Duration (Years):").grid(row=4, column=0, sticky=tk.W)  # Added Withdrawal Duration
withdrawal_years_entry = ttk.Entry(input_frame)
withdrawal_years_entry.grid(row=4, column=1)

# Calculate button
calculate_button = ttk.Button(input_frame, text="Calculate", command=calculate)
calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

# Tabs for results
notebook = ttk.Notebook(left_frame)
notebook.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

average_annual_returns = [6, 8, 10]
result_text_widgets = []
tabs = []

for i, rate in enumerate(average_annual_returns):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=f"{rate}% Return")
    tabs.append(tab)

    # Add title for each return rate tab
    ttk.Label(tab, text=f"Results for {rate}% Average Annual Return", font=("Helvetica", 12, "bold")).pack(padx=10, pady=5)

    # Add result text widget for each tab
    text_widget = tk.Text(tab, wrap=tk.WORD, width=60, height=20)
    text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
    result_text_widgets.append(text_widget)

# Right frame for the graph
right_frame = ttk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10, pady=10, fill=tk.BOTH, expand=True)

graph_buttons_frame = ttk.Frame(right_frame)
graph_buttons_frame.pack(fill=tk.X, padx=10, pady=5)

for i, rate in enumerate(average_annual_returns):
    ttk.Button(graph_buttons_frame, text=f"Show Graph for {rate}%",
               command=lambda i=i: plot_graph(i)).pack(side=tk.TOP, padx=5, pady=5)

graph_frame = ttk.Frame(right_frame)
graph_frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

# Initialize global variables
balances = []
contributions_list = []
interests_list = []

# Run the main loop
root.mainloop()
