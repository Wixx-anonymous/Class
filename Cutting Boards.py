def calculate_wood_costs():
    # Dictionary to store wood types and their costs
    wood_types = {}

    # Input loop for wood types, prices, and quantities
    while True:
        wood_type = input("Enter the type of wood (or type 'done' to finish): ").strip().lower()
        if wood_type == 'done':
            break
        price_per_board_foot = float(input(f"Enter the price per board foot for {wood_type}: "))

        pieces = int(input(f"Enter the number of pieces for {wood_type}: "))
        thickness = float(input(f"Enter the thickness (in inches) of {wood_type}: "))
        width = float(input(f"Enter the width (in inches) of {wood_type}: "))
        length = float(input(f"Enter the length (in inches) of {wood_type}: "))

        # Calculate board feet for each piece and total board feet
        board_feet_per_piece = (thickness * width * length) / 144
        total_board_feet = board_feet_per_piece * pieces

        # Store the values in the dictionary
        wood_types[wood_type] = {
            "price_per_board_foot": price_per_board_foot,
            "total_board_feet": total_board_feet
        }

    # Calculate total cost for each wood type and overall cost
    total_cost = 0
    for wood, values in wood_types.items():
        wood_cost = values["price_per_board_foot"] * values["total_board_feet"]
        total_cost += wood_cost
        print(f"Total cost for {wood}: ${wood_cost:.2f}")

    # Output the total cost
    print(f"Overall total cost: ${total_cost:.2f}")


# Run the function
calculate_wood_costs()