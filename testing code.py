import pandas as pd
from prophet import Prophet

# Load the Excel file
file_path = 'Grainpr.xlsx'
data = pd.read_excel(file_path, sheet_name='WHEAT')

# Extract relevant columns
wheat_prices = data.iloc[7:, [0, 1]]  # Selecting rows from 7 onward and columns 0 (date) and 1 (price)
wheat_prices.columns = ['ds', 'y']  # Rename columns for Prophet

# Convert 'ds' to datetime and 'y' to numeric, dropping rows with NaN values
wheat_prices['ds'] = pd.to_datetime(wheat_prices['ds'], errors='coerce')
wheat_prices['y'] = pd.to_numeric(wheat_prices['y'], errors='coerce')
wheat_prices.dropna(inplace=True)

# Initialize and fit the model
model = Prophet()
model.fit(wheat_prices)

# Create a DataFrame for future dates
future = model.make_future_dataframe(periods=365)  # Predicting 1 year into the future

# Predict future prices
forecast = model.predict(future)

# Display the forecast
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

# Optional: Plot the forecast
import matplotlib.pyplot as plt
model.plot(forecast)
plt.show()
