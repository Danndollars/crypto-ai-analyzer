# Crypto AI Market Analyzer

An automated research pipeline that ingests real-time cryptocurrency data, performs deep tokenomics analysis, 
and generates institutional-grade reports using a resilient multi-model LLM system.

---

## 📌 Overview

This project combines live market data with AI-driven analysis to produce structured crypto research reports. 
It is designed for reliability, modularity, and production-level workflows.

---

##  Features

-  **Real-time Data Ingestion**  
  Integrates with CoinMarketCap Professional API for live listings and global metrics.

-  **Quantitative Analysis**  
  Calculates key metrics such as:
  - Fully Diluted Valuation (FDV)
  - Volume-to-Market Cap ratios
  - Supply inflation risk

-  **Market Sentiment Analysis**  
  Incorporates:
  - Fear & Greed Index  
  - BTC Dominance trends  

-  **Resilient AI Pipeline**  
  Uses dynamic fallback across multiple LLMs via OpenRouter:
  - Gemini  
  - Qwen  
  - Mistral  

  - **Production-Ready Setup**  
  - `.env`-based credential management  
  - Environment isolation  

---

##  Tech Stack

- Python 3.12+
- requests
- httpx
- python-dotenv
- openai
- OpenRouter API
- CoinMarketCap API

---

## ⚙️ Installation

### 1. Clone the Repository
~~~
bash
git clone https://github.com/YOUR_USERNAME/crypto-ai-analyzer.git
cd crypto-ai-analyzer
~~~

### 2. Install Dependencies
~~~
pip install -r requirements.txt
~~~
(or manually)
~~~
pip install requests python-dotenv openai httpx
~~~

3. Configure Environment Variables
Create a .env file in the root directory:
~~~
COIN_MARKET_CAP_API_KEY=your_cmc_key_here
OPENROUTER_API_KEY=your_openrouter_key_here
~~~

### Usage
Run the main orchestrator: python main.py

### Output
The script generates: latest_analysis.md (This file contains a structured AI-generated market research report).

### Project Structure
crypto-ai-analyzer/

├── .env                # (ignored) Secure credentials  
├── .gitignore         # Prevents sensitive files from being committed  
├── data_engine.py     # API interaction + quantitative modeling  
├── prompts.py         # Prompt engineering templates  
├── main.py            # AI orchestration + fallback logic
├── requirements.txt   # Dependencies

🔒 Security Notes
-  Never commit your .env file
-  Ensure .gitignore includes:
-  .env
-  virtual environments
-  generated reports


 ### Verification Checklist
Before running in production:
-  ✔ API keys are valid and active
-  ✔ .env is not committed to GitHub
-  ✔ Model list in main.py includes current free-tier options (e.g. google/gemma-4-26b-a4b-it:free)
-  ✔ Market context reflects realistic values:BTC Dominance ≈ 56–60%, Total Market Cap ≈ $2T–$3T

### ⚠️ Disclaimer
-  This project is for educational and research purposes only.
-  It does not constitute financial advice.
-  Always do your own research (DYOR).

### ⭐ Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

### 💡 Future Improvements
-  Dashboard UI (Streamlit / Next.js)
-  Backtesting engine
-  On-chain data integration
-  Alert system (Telegram / Email)
