from fractions import Fraction


# Function to format dimensions in whole inches and fractions
def format_whole_and_fractional(value):
    whole_inch = int(value)  # The whole inch part
    fractional_inch = Fraction(value - whole_inch).limit_denominator(16)  # Fractional part limited to 16ths

    if fractional_inch == 0:
        return f"{whole_inch} inches"  # If there's no fractional part, just show whole inches
    else:
        return f"{whole_inch} inches and {fractional_inch}"  # Whole inches and fraction


# Function to convert input of whole inches and fractions into a float
def convert_fractional_input(value):
    if 'and' in value:
        whole_part, fraction_part = value.split('and')
        return int(whole_part.strip()) + float(Fraction(fraction_part.strip()))
    else:
        return float(Fraction(value.strip()))


# Function to calculate the dimensions of the drawer box
def calculate_drawer_box_dimensions(opening_width, opening_height, slide_size_in, thickness):
    # Adjust drawer width (subtract 1/2 inch from the opening size)
    drawer_width = opening_width - 0.5  # Deduct 1/2 inch from the opening size

    # Adjust drawer height by subtracting 1 inch from the opening height
    drawer_height = opening_height - 1  # Deduct 1 inch for drawer height

    # Drawer depth is determined by the slide size in inches
    drawer_depth = slide_size_in

    # Bottom panel will be 3/8 inch smaller on all sides due to rabbet joint
    bottom_panel_width = drawer_width - (2 * 0.375)  # Deduct 3/8 inch on both sides
    bottom_panel_depth = drawer_depth - (2 * 0.375)  # Deduct 3/8 inch on both sides

    # Calculate the width of the front and back by subtracting 1.5 inches (3/4 inch on each side)
    front_back_width = drawer_width - (2 * thickness)

    # Back piece is 1/2 inch shorter than the front piece in height
    back_height = drawer_height - 0.5  # Back piece height is 1/2 inch shorter

    # List of pieces: (length, width, thickness) for each piece
    pieces = {
        "Side 1": (drawer_depth, drawer_height, thickness),  # Side 1
        "Side 2": (drawer_depth, drawer_height, thickness),  # Side 2
        "Front": (front_back_width, drawer_height, thickness),  # Front
        "Back": (front_back_width, back_height, thickness),  # Back (shorter by 1/2 inch)
        "Bottom": (bottom_panel_width, bottom_panel_depth, 0.5)  # Bottom (1/2 inch thick)
    }

    return pieces


# Input values with fractional inches
opening_width = convert_fractional_input(input("Enter the width of the opening (e.g., 21 and 15/16 inches): "))
opening_height = convert_fractional_input(input("Enter the height of the opening (e.g., 12 and 3/4 inches): "))

# Select drawer slide size (can be in whole or fractional inches)
print("Select the drawer slide size (in inches): 12, 15, 18, or 21")
slide_size_in = convert_fractional_input(
    input("Enter the size of the drawer slides (e.g., 18 inches or 18 and 1/2 inches): "))

# Ensure valid slide size
if slide_size_in not in [12, 15, 18, 21]:
    raise ValueError("Invalid slide size. Please select 12, 15, 18, or 21 inches.")

thickness = 0.75  # All side pieces are 3/4 inch thick

# Calculate dimensions
drawer_pieces = calculate_drawer_box_dimensions(opening_width, opening_height, slide_size_in, thickness)

# Output the dimensions of each piece in whole inches and fractional format
for piece, dimensions in drawer_pieces.items():
    formatted_length = format_whole_and_fractional(dimensions[0])
    formatted_width = format_whole_and_fractional(dimensions[1])
    formatted_thickness = format_whole_and_fractional(dimensions[2])
    print(f"{piece}: Length = {formatted_length}, Width = {formatted_width}, Thickness = {formatted_thickness}")
