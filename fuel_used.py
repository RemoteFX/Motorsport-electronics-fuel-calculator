import csv
import tkinter as tk
from tkinter import filedialog

def calculate_total_fuel_cost(csv_file, price_per_liter):
    total_fuel = 0

    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)

        # Check if the expected columns are present
        if 'Time' not in reader.fieldnames or ' Fuelfow Est.' not in reader.fieldnames:
            raise ValueError("Columns 'Time' and 'Fuelflow Est.' are required in the CSV file.")

        previous_time = 0
        previous_fuel_flow = 0

        for row in reader:
            time = float(row['Time'])
            fuel_flow = float(row[' Fuelfow Est.'])

            # Calculate the time difference and fuel consumption for this time increment
            time_difference = time - previous_time
            fuel_consumed = (fuel_flow / 3600) * time_difference  # Convert fuel flow from L/hr to L/s

            # Add the fuel consumed to the total
            total_fuel += fuel_consumed

            # Update the previous time and fuel flow for the next iteration
            previous_time = time
            previous_fuel_flow = fuel_flow

    # Calculate the fuel cost based on the total fuel used and price per liter
    fuel_cost = total_fuel * price_per_liter
    return fuel_cost

def browse_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if file_path:
        try:
            price_per_liter = float(price_entry.get())
            total_fuel_cost = calculate_total_fuel_cost(file_path, price_per_liter)
            result_label.config(text=f'Total Fuel Cost: £{total_fuel_cost:.2f}')
        except ValueError:
            result_label.config(text="Invalid price per liter. Please enter a valid number.")
        except Exception as e:
            result_label.config(text=f"An error occurred: {str(e)}")
    else:
        result_label.config(text="No file selected")

# Create the main window
root = tk.Tk()
root.title("Fuel Consumption Calculator")

# Create and configure the GUI components
browse_button = tk.Button(root, text="Browse", command=browse_file)
price_label = tk.Label(root, text="Enter price per liter (£):")
price_entry = tk.Entry(root)
result_label = tk.Label(root, text="Select a CSV file and enter the price per liter to calculate total fuel cost.")

# Place the components in the window
browse_button.pack(pady=10)
price_label.pack(pady=5)
price_entry.pack(pady=5)
result_label.pack(pady=10)

# Start the GUI event loop
root.mainloop()
