import requests
import pandas as pd
import os
from datetime import datetime, timezone

def fetch_meme_coins_data():
    url = "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        'vs_currency': 'usd',
        'category': 'meme-token',
        'order': 'market_cap_desc',
        'per_page': 100,
        'page': 1,
        'sparkline': 'false',
        'price_change_percentage': '24h'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        df = pd.DataFrame(data)
        df = df[['symbol', 'name', 'current_price', 'market_cap', 
                'total_volume', 'price_change_percentage_24h', 
                'last_updated']]
        
        df['data_collection_time'] = datetime.now(timezone.utc).isoformat()
        return df
        
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()

def save_data(df):
    os.makedirs('data', exist_ok=True)
    filename = f"data/meme_coins_{datetime.now(timezone.utc).strftime('%Y%m%d_%H%M')}.csv"
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
    return filename

if __name__ == "__main__":
    print("Starting data collection...")
    data = fetch_meme_coins_data()
    if not data.empty:
        save_data(data)
        print("Data collection completed successfully!")
    else:
        print("Failed to fetch data.")