def calculate_square_footage(length, height):
    square_feet = length * height
    return square_feet

def calculate_shiplap_quantity(square_feet, waste_percentage, shiplap_coverage):
    # Calculate the total square footage with waste included
    total_square_feet = square_feet + (square_feet * waste_percentage / 100)
    # Calculate the number of shiplap pieces needed and round to the nearest integer
    shiplap_pieces = round(total_square_feet / shiplap_coverage)
    return shiplap_pieces, total_square_feet

def calculate_total_cost_with_tax(shiplap_pieces, shiplap_price_per_piece, tax_rate):
    # Calculate the total cost of shiplap
    shiplap_cost = shiplap_pieces * shiplap_price_per_piece
    # Calculate the tax amount and add it to the shiplap cost
    tax_amount = shiplap_cost * (tax_rate / 100)
    total_cost_with_tax = shiplap_cost + tax_amount
    return total_cost_with_tax

# Define tax rates for specific counties
tax_rates = {
    "Wake": 7.25,  # Tax rate for Wake County, NC
    "Durham": 7.5,  # Tax rate for Durham County, NC
    "Harnett": 7.0,  # Tax rate for Harnett County, NC
    # You can add more counties and their tax rates here
}

if __name__ == "__main__":
    try:
        length = float(input("Enter the length in feet: "))
        height = float(input("Enter the height in feet: "))
        square_feet = calculate_square_footage(length, height)
        print(f"The square footage of the wall is: {square_feet:,} sq. ft")
        charge_per_sqft = float(input("Enter the charge per square foot for the project: "))
        # Ask the user for the county and validate it
        while True:
            county = input("Enter the county where the house is located (Wake, Durham, Harnett): ")
            county = county.strip().capitalize()  # Normalize input

            if county in tax_rates:
                break
            else:
                print("Invalid county. Please enter one of the specified counties.")

        waste_percentage = 20  # 20% waste

        # New shiplap information
        shiplap_info_12ft = {
            "12ft": {"price": 13.47, "coverage": 5.25},
        }

        shiplap_info_8ft = {
            "8ft": {"price": 9.47, "coverage": 3.5},
        }

        # Look up the sales tax rate based on the entered county
        sales_tax_rate = tax_rates[county]

        shiplap_pieces_12ft, total_square_feet = calculate_shiplap_quantity(square_feet, waste_percentage, shiplap_info_12ft["12ft"]["coverage"])
        total_shiplap_cost_with_tax_12ft = calculate_total_cost_with_tax(shiplap_pieces_12ft, shiplap_info_12ft["12ft"]["price"], sales_tax_rate)
        print(f"You would need {shiplap_pieces_12ft} pieces of 12ft shiplap.")
        print(f"The total cost of 12ft shiplap with sales tax is: ${total_shiplap_cost_with_tax_12ft:,.2f}")

        shiplap_pieces_8ft, total_square_feet_8ft = calculate_shiplap_quantity(square_feet, waste_percentage, shiplap_info_8ft["8ft"]["coverage"])
        total_shiplap_cost_with_tax_8ft = calculate_total_cost_with_tax(shiplap_pieces_8ft, shiplap_info_8ft["8ft"]["price"], sales_tax_rate)
        print(f"You would need {shiplap_pieces_8ft} pieces of 8ft shiplap.")
        print(f"The total cost of 8ft shiplap with sales tax is: ${total_shiplap_cost_with_tax_8ft:,.2f}")

        total_project_cost = total_square_feet * charge_per_sqft * (1 + sales_tax_rate / 100)

        print(f"The total project cost with sales tax for this job is: ${total_project_cost:,.2f}")


    except ValueError:
        print("Please enter valid numeric values for length and height.")
