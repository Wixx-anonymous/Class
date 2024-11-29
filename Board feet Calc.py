def calculate_board_feet(length, width, thickness, quantity):
    # Convert dimensions to inches
    length_inch = length
    width_inch = width
    thickness_inch = thickness

    # Calculate board feet for one piece
    board_feet_per_piece = (length_inch * width_inch * thickness_inch) / 144

    # Calculate total board feet for all pieces
    total_board_feet = board_feet_per_piece * quantity

    return total_board_feet

# Get user input
length = float(input("Enter the length of the wood piece in inches: "))
width = float(input("Enter the width of the wood piece in inches: "))
thickness = float(input("Enter the thickness of the wood piece in inches: "))
cost_per_board_foot = float(input("Enter the cost per board foot of lumber: "))
quantity = int(input("Enter the number of pieces for the project: "))
waste_factor = 1.25  # 25% waste

# Calculate total board feet
total_board_feet = calculate_board_feet(length, width, thickness, quantity)

# Include 25% waste
total_board_feet_with_waste = total_board_feet * waste_factor

# Calculate total cost
total_cost = total_board_feet_with_waste * cost_per_board_foot

# Display the result
print(f"The project uses {total_board_feet_with_waste:.2f} board feet of wood including 25% waste for {quantity} pieces.")
print(f"The total cost of the lumber is ${total_cost:.2f}.")