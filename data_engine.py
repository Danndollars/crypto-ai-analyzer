import os
from shlex import quote
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from dotenv import load_dotenv
import json

load_dotenv()

BASE_URL = "https://pro-api.coinmarketcap.com"
API_KEY = os.getenv("COIN_MARKET_CAP_API_KEY")


cmc_session = Session()
cmc_session.headers.update({
    "Accepts": "application/json",
    "X-CMC_PRO_API_KEY": API_KEY 
    })

def get_coin_listings():
    #This returns the latest projects added to CoinMarketCap.
    listing_url = f"{BASE_URL}/v1/cryptocurrency/listings/latest"

    listing_parameters = {
    "start": "1","limit": "50",
    "convert": "USD","sort": "date_added",
    "sort_dir": "desc","cryptocurrency_type": "all",
    "volume_24h_min": "50000","market_cap_min": "100000",
    "aux": "num_market_pairs,cmc_rank,date_added,max_supply,circulating_supply,total_supply"
    }

    try:
        listing_response = cmc_session.get(listing_url, params=listing_parameters)
        return json.loads(listing_response.text)
    
    except Exception as e:
        print(f" Error: {e}")
        print("There was an error getting the new Cryptocurrency listings")
        return {}

def get_crypto_metadata(id_dict):
    # The "Backstory." This provides the logo, description, website, and social links. 
    # AI needs this text to understand what the coin actually does
    metadata_url = f"{BASE_URL}/v2/cryptocurrency/info"

    # Convert all IDs in your dict to one long string: "1,2,3"
    id_string = ",".join(id_dict.values())
     
    metadata_parameters = {
        "id": id_string,
        "aux": "urls,logo,description,tags"
    }
    try:
        response = cmc_session.get(metadata_url, params=metadata_parameters)
        return json.loads(response.text)
        
    except Exception as e:
         print("There was an error obtaining the metadata for the cryptocurrency listing")
         print(f"Metadata Error: {e}")
         return {}
        
def get_market_sentiment():
    #Fetches current and recent market sentiments(Fear & Greed).
    sentiment_url = f"{BASE_URL}/v3/fear-and-greed/historical"
    sentiment_params = {"limit": "7"} #Get the last 7 days of sentiment

    try:
        sentiment = cmc_session.get(sentiment_url, params=sentiment_params)
        return json.loads(sentiment.text).get("data", [])
    except Exception as e:
        print(f"Sentiment Error!! :{e}")
        return []
    
def get_global_metrics():
    # Provides the 'Market Climate' (Dominance, Total Cap).
    global_metrics_url = f"{BASE_URL}/v1/global-metrics/quotes/latest"

    try:
        response = cmc_session.get(global_metrics_url)
        return json.loads(response.text).get("data", {})
    except Exception as e:
        print(f"Global Metric error!! : {e}")
        return {}
    
def generate_ai_report():
    listing_data = get_coin_listings().get("data", [])

    id_map = {coin["symbol"]: str(coin["id"]) for coin in listing_data}
    metadata = get_crypto_metadata(id_map).get("data", {})

    global_metrics = get_global_metrics()
    sentiment_history = get_market_sentiment()

    report = {
        "market_environment": {
            "overall_stats": {
                "btc_dominance": global_metrics.get("btc_dominance"),
                "total_market_cap": global_metrics.get("quote", {}).get("USD", {}).get("total_market_cap"),
                "daily_volume": global_metrics.get("quote", {}).get("USD", {}).get("total_volume_24h")
            },
            "sentiment_trend": [
                {"date": s["timestamp"], "value": s["value"], "status": s["value_classification"]}
                for s in sentiment_history
            ]
        },
        "new_listing_analysis": []
    }
    for coin in listing_data:
        c_id = str(coin["id"])
        info = metadata.get(c_id, {})
        quote = coin.get('quote', {}).get('USD', {})
        circulating = coin.get('circulating_supply', 0)
        total_supply = coin.get('total_supply', 0)
        max_supply = coin.get('max_supply', 0) or total_supply # Fallback if max isn't set

        # CALCULATIONS
        # 1. FDV: What the market cap would be if all coins were out. 
        # If FDV is 10x higher than Market Cap, it's a warning (future dumping).
        fdv = max_supply * quote.get('price', 0)

        # 2. Vol/Cap Ratio: High ratio (>0.5) = high hype/speculation. 
        # Low ratio (<0.1) = "Ghost town" coin.
        vol_cap_ratio = quote.get('volume_24h', 0) / quote.get('market_cap', 1) # Prevent div by 0

        # 3. Issuance %: How much of the supply is currently "on the street"
        supply_issued_pct = (circulating / max_supply) * 100 if max_supply > 0 else 100

        

        report["new_listing_analysis"].append({
            "name": coin["name"],
            "symbol": coin["symbol"],
            "description": info.get("description", "N/A"),
            "tags": info.get("tags", []),
            "tokenomics": {
                "market_cap": quote.get('market_cap'),
                "fdv": fdv,
                "mcap_fdv_ratio": round(quote.get('market_cap', 0) / fdv, 2) if fdv > 0 else 1,
                "volume_to_mcap": round(vol_cap_ratio, 3),
                "circulating_supply_pct": f"{round(supply_issued_pct, 2)}%",
                "is_deflationary": max_supply > 0 and total_supply >= max_supply
            },
            "links": info.get("urls", {}).get("website", [])
        })
    print("done with report generation")
    return report

if __name__ == "__main__":
    print("Starting the Data Engine...")
    final_report = generate_ai_report()
    
    # This prints the result so you can actually see it in the terminal
    print(json.dumps(final_report, indent=4))
    









  