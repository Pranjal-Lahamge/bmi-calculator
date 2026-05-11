# -------------------------------------------------
# BMI Calculator using Python and Tkinter
# -------------------------------------------------

# Import tkinter library
# Tkinter is used to create GUI applications

import tkinter as tk


# -------------------------------------------------
# Function to calculate BMI
# -------------------------------------------------

def calculate_bmi():

    try:
        # Get weight entered by user
        weight = float(weight_entry.get())

        # Get height entered by user
        height = float(height_entry.get())

        # Convert height from cm to meter
        height_in_meter = height / 100

        # BMI Formula
        bmi = weight / (height_in_meter ** 2)

        # Decide BMI category
        if bmi < 18.5:
            category = "Underweight"

        elif bmi < 25:
            category = "Normal Weight"

        elif bmi < 30:
            category = "Overweight"

        else:
            category = "Obese"

        # Show result on screen
        result_label.config(
            text=f"BMI = {bmi:.2f}\nCategory: {category}"
        )

    except:
        # If user enters wrong input
        result_label.config(
            text="Please enter valid numbers"
        )


# -------------------------------------------------
# Main Window
# -------------------------------------------------

# Create main window
window = tk.Tk()

# Window title
window.title("BMI Calculator")

# Window size
window.geometry("400x350")

# Background color
window.config(bg="#d6f5ff")


# -------------------------------------------------
# Heading
# -------------------------------------------------

heading = tk.Label(
    window,
    text="BMI Calculator",
    font=("Arial", 18, "bold"),
    bg="#d6f5ff"
)

heading.pack(pady=20)


# -------------------------------------------------
# Weight Input
# -------------------------------------------------

weight_label = tk.Label(
    window,
    text="Enter Weight (kg):",
    font=("Arial", 12),
    bg="#d6f5ff"
)

weight_label.pack()

# Weight input box
weight_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=25
)

weight_entry.pack(pady=10)


# -------------------------------------------------
# Height Input
# -------------------------------------------------

height_label = tk.Label(
    window,
    text="Enter Height (cm):",
    font=("Arial", 12),
    bg="#d6f5ff"
)

height_label.pack()

# Height input box
height_entry = tk.Entry(
    window,
    font=("Arial", 12),
    width=25
)

height_entry.pack(pady=10)


# -------------------------------------------------
# Calculate Button
# -------------------------------------------------

calculate_button = tk.Button(
    window,
    text="Calculate BMI",
    font=("Arial", 12),
    command=calculate_bmi
)

calculate_button.pack(pady=20)


# -------------------------------------------------
# Result Label
# -------------------------------------------------

result_label = tk.Label(
    window,
    text="Your BMI will appear here",
    font=("Arial", 13, "bold"),
    bg="#d6f5ff"
)

result_label.pack(pady=20)


# -------------------------------------------------
# Run Window
# -------------------------------------------------

window.mainloop()
