from flask import Flask, request, render_template_string
import yfinance as yf
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # For headless environments
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

app = Flask(__name__)

TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>Stock Analysis Dashboard</title>
    <style>
        body { font-family: Arial; margin: 20px; }
        input, button { padding: 8px; font-size: 16px; }
        img { margin: 20px 0; max-width: 95%; border: 1px solid #ccc; }
    </style>
</head>
<body>
    <h2>📈 Stock Analysis Dashboard</h2>
    <form method="post">
        <label>Symbol (e.g., ^NSEI, RELIANCE.NS):</label><br>
        <input type="text" name="symbol" required><br><br>

        <label>Start Date:</label><br>
        <input type="date" name="start_date" required><br><br>

        <label>End Date:</label><br>
        <input type="date" name="end_date" required><br><br>

        <button type="submit">Generate Charts</button>
    </form>

    {% if error %}
        <p style="color: red;">{{ error }}</p>
    {% endif %}

    {% if symbol %}
        <h3>Results for {{ symbol }}</h3>
        <img src="/static/trend.png">
        <img src="/static/volatility.png">
        <img src="/static/ma.png">
        <img src="/static/yearly.png">
        <img src="/static/heatmap.png">
        <img src="/static/seasonal.png">
    {% endif %}
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        symbol = request.form['symbol']
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        try:
            data = yf.download(symbol, start=start_date, end=end_date)
            if data.empty:
                return render_template_string(TEMPLATE, error="No data found. Please check symbol/date.", symbol=None)

            # Clear old static images
            for f in ['trend.png', 'volatility.png', 'ma.png', 'yearly.png', 'heatmap.png', 'seasonal.png']:
                try:
                    os.remove(f'static/{f}')
                except:
                    pass

            sns.set(style="whitegrid")
            data['Return'] = data['Close'].pct_change()
            data['Volatility'] = data['Return'].rolling(30).std() * 100
            data['MA50'] = data['Close'].rolling(50).mean()
            data['MA200'] = data['Close'].rolling(200).mean()

            def save_plot(fig_id):
                path = f"static/{fig_id}.png"
                plt.savefig(path, bbox_inches='tight')
                plt.clf()

            # Plot 1: Trend
            data['Close'].plot(title="Close Price Trend", color='black', figsize=(10,4))
            save_plot("trend")

            # Plot 2: Volatility
            data['Volatility'].plot(title="30-Day Rolling Volatility (%)", color='black', figsize=(10,4))
            save_plot("volatility")

            # Plot 3: Moving Averages
            data[['Close', 'MA50', 'MA200']].plot(title="Moving Averages", figsize=(10,4))
            save_plot("ma")

            # Plot 4: Yearly Returns
            yearly = data['Close'].resample('Y').last().pct_change() * 100
            yearly.dropna().plot(kind='bar', title="Yearly Returns (%)", figsize=(8,4), color='black')
            save_plot("yearly")

            # Plot 5: Monthly Return Heatmap
            monthly = data['Close'].resample('M').last().pct_change() * 100
            monthly_df = monthly.to_frame(name="Return")
            monthly_df['Year'] = monthly_df.index.year
            monthly_df['Month'] = monthly_df.index.month_name()
            heatmap_data = monthly_df.pivot(index='Year', columns='Month', values='Return')
            month_order = ['January','February','March','April','May','June',
                           'July','August','September','October','November','December']
            heatmap_data = heatmap_data.reindex(columns=month_order)
            plt.figure(figsize=(12,5))
            sns.heatmap(heatmap_data, annot=True, fmt=".1f", cmap="RdYlGn", center=0)
            plt.title("Monthly Return Heatmap")
            save_plot("heatmap")

            # Plot 6: Seasonal Monthly Avg
            seasonal = monthly_df.groupby('Month')['Return'].mean().reindex(month_order)
            seasonal.plot(kind='bar', color='black', title='Average Monthly Return', figsize=(8,4))
            save_plot("seasonal")

            return render_template_string(TEMPLATE, symbol=symbol.upper())
        except Exception as e:
            return render_template_string(TEMPLATE, error=str(e), symbol=None)

    return render_template_string(TEMPLATE, symbol=None)

if __name__ == '__main__':
    if not os.path.exists('static'):
        os.makedirs('static')
    app.run(debug=True)
