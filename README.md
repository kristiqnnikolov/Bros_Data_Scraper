# Bros Data Scraper

This project is a web scraper designed to extract all air conditioner products from https://brosbg.com/klimatici-ci145
and provide the data through an API.

The extracted data includes product details such as URL, SKU, name, category, brand, price, images, and timestamp.

### 1. Clone the Repository
```bash
    git clone https://github.com/kristiqnnikolov/Bros_Data_Scraper.git
    cd bros_scraper
```
### 2. Set Up Virtual Environment
```bash
    python3 -m venv venv      # Create virtual environment
```
```bash
    venv\Scripts\activate     # Activate the virtual environment on Windows
```
```bash
    source venv/bin/activate  # Activate the virtual environment on Linux/Mac
```
### 3. Install Requirements
```bash
    pip install -r requirements.txt
    pip install flask
```
### 4. Run the Scraper and start the API
```bash
    scrapy crawl bros_bg -O bros.json
```
```bash
    python flask_api.py
```
### 5. Access the API
   Go to http://127.0.0.1:5000/air_conditioners
   Find specific product by ID : http://127.0.0.1:5000/air_conditioners/<product_id>

