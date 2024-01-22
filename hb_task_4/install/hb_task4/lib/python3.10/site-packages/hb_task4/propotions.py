import math
import pandas as pd

# Given values
ang_vel = 0
x = 10
r = 1.9
dc = 7.0
epsilon = 0.001  # Small value to avoid division by zero
data = []

def inverse_kinematics(xvel, yvel, ang_vel):
    # Your inverse kinematics calculation here...
    wheel_vel_1= (1/r)*(-0.33*xvel)+(0.58*yvel)+(0.04762*ang_vel)
    wheel_vel_2= (1/r)*(-0.33*xvel)+(-0.58*yvel)+(0.04762*ang_vel)
    wheel_vel_3= (1/r)*(0.66666*xvel)+(0.04762*ang_vel)
    return [wheel_vel_1, wheel_vel_2, wheel_vel_3]

# Create an empty DataFrame to store the results
df = pd.DataFrame(columns=['y', 'wheel_1', 'wheel_2', 'wheel_3', 'ratios'])

# Iterate through y values from 0 to 180 degrees
for y in range(361):
    # Calculate wheel velocities using the inverse_kinematics function
    wheel_velocities = inverse_kinematics(x, x * math.tan(math.radians(y)), ang_vel)

    # Find the minimum and second minimum absolute values among wheel velocities
    min_abs_value = min(map(abs, wheel_velocities))
    wheel_velocities_sorted = sorted(wheel_velocities, key=abs)
    second_min_abs_value = abs(wheel_velocities_sorted[1])

    # If the minimum absolute value is close to zero, set it to 0
    if min_abs_value < epsilon:
        min_abs_value = 0

    # Normalize the values, considering epsilon and using the second minimum value as 1
    normalized_wheel_velocities = [
        v / min_abs_value if min_abs_value != 0 else 0 for v in wheel_velocities
    ]

    # Append the results to the DataFrame
    data.append({
        'y': y,
        'wheel_1':  wheel_velocities[0],
        'wheel_2':  wheel_velocities[1],
        'wheel_3':  wheel_velocities[2],
        'ratios': f"{normalized_wheel_velocities[0]:.2f}:{normalized_wheel_velocities[1]:.2f}:{normalized_wheel_velocities[2]:.2f}"
    })

# Create a DataFrame from the list of dictionaries
df = pd.DataFrame(data)

# Export the DataFrame to a CSV file
df.to_csv('wheel_proportions.csv', index=False)

# Display the DataFrame
print(df)
