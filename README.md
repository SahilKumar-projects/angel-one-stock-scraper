# Angel One Stock Scraper

An automated stock data extraction and processing system built with Python and Selenium. The project scrapes paginated stock information from Angel One, extracts structured market data, exports it to CSV and Excel, and stores or updates records in MongoDB.

## Features

- Automated stock data scraping using Selenium
- Paginated stock data extraction
- Automatic detection of the last page using the Next-page control
- Robust table extraction
- Retry mechanism for stale element references
- Pagination recovery using the saved Next-page URL
- Error handling for failed page loads and extraction failures
- CSV export
- Excel export using Pandas and OpenPyXL
- Bold Excel headers
- MongoDB integration using PyMongo
- Duplicate handling using MongoDB `update_one()` with `upsert=True`
- Updates existing stock records when the same company is found
- Preserves partially collected data when scraping is interrupted

## Technologies Used

- Python
- Selenium
- Pandas
- OpenPyXL
- PyMongo
- MongoDB
- Google Chrome / ChromeDriver

## Data Extracted

The scraper extracts:

- Company
- LTP
- Volume
- Market Cap
- 52W High
- 52W Low
- Sector

## Project Structure

```text
angel_one_stock_scraper/
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── browser.py
│   ├── scraper.py
│   ├── csv_writer.py
│   └── main.py
│
├── output/
│   └── .gitkeep
│
├── .gitignore
├── README.md
├── requirements.txt
└── LICENSE
```

## How the Project Works

```text
Angel One Stock Listing
        ↓
      Selenium
        ↓
Wait for Stock Table
        ↓
Extract Current Page
        ↓
Check Next Page
        ↓
 ┌───────────────┐
 │ Next Disabled │
 └───────┬───────┘
         ↓
        Stop

If Next is available
         ↓
   Click Next Page
         ↓
 If Click Fails
         ↓
Recover Using Next URL
         ↓
Extract Next Page
         ↓
Repeat
```

After scraping:

```text
Scraped Stock Data
        ↓
   List of Dictionaries
        ↓
   ┌──────┴──────┐
   ↓             ↓
  CSV          Excel
                 ↓
              Pandas
                 ↓
              MongoDB
```

## Pagination and Error Handling

The scraper does not depend on a hard-coded number of pages.

It checks the actual **Next Page** control on the website.

When the Next button is available:

1. The scraper obtains the Next-page URL.
2. It attempts to click the Next button.
3. It waits for the page URL to change.
4. It waits for the stock table to load.
5. If the click fails, the scraper uses the saved Next-page URL as a recovery method.
6. The next page is then extracted.

The scraper also handles `StaleElementReferenceException` by retrying page extraction.

## MongoDB Integration

The scraped Excel data can be converted into dictionaries using Pandas:

```python
data = df.to_dict(orient="records")
```

Each row becomes one dictionary.

Example:

```python
{
    "Company": "Example Company",
    "LTP": "100.00",
    "Volume": "500000",
    "Market Cap": "1000 Cr",
    "52W High": "120.00",
    "52W Low": "80.00",
    "Sector": "Technology"
}
```

The project uses MongoDB upsert logic:

```python
collection.update_one(
    {"Company": stock["Company"]},
    {"$set": stock},
    upsert=True
)
```

This means:

- If the company does not exist, a new document is inserted.
- If the company already exists, its data is updated.
- If the data has not changed, no modification is made.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/angel-one-stock-scraper.git
cd angel-one-stock-scraper
```

### 2. Install dependencies

```bash
py -m pip install -r requirements.txt
```

### 3. Configure the project

Update the required configuration values in:

```text
src/config.py
```

Do not commit passwords, database credentials, API keys, or other secrets to GitHub.

### 4. Run the scraper

From the project root:

```bash
py src/main.py
```

## Output

Generated files are stored in the `output` folder.

Typical outputs include:

```text
output/
├── large_cap_stocks.csv
└── large_cap_stocks.xlsx
```

Generated CSV and Excel files are ignored by Git using `.gitignore`.

## Configuration

The scraper uses configuration values such as:

```python
LARGE_CAP_URL = "https://oga-prod.angelone.in/stocks/large-cap-stocks"

MAX_STOCKS = 10

WAIT_TIMEOUT = 10

MAX_RETRIES = 3
```

### Configuration Parameters

| Parameter | Description |
|---|---|
| `LARGE_CAP_URL` | URL used to start stock scraping |
| `MAX_STOCKS` | Maximum stock value used by the project configuration |
| `WAIT_TIMEOUT` | Maximum Selenium wait time |
| `MAX_RETRIES` | Number of extraction retry attempts |

## Error Handling

The scraper handles situations including:

- Stock table not loading
- Missing required columns
- Empty page data
- Stale Selenium elements
- Failed Next-page clicks
- Missing Next-page URLs
- Unexpected scraping errors
- Manual interruption using `Ctrl + C`

When possible, the scraper returns records collected before the failure.

## Example Console Flow

```text
========== Page 1 ==========

Extracting page... Attempt 1/3
Extracted 10 stocks.
Total stocks collected so far: 10

Clicking Next...
Next page loaded successfully.

========== Page 2 ==========

Extracting page... Attempt 1/3
Extracted 10 stocks.
Total stocks collected so far: 20
```

If a click fails:

```text
Clicking Next...
Next click failed.

Trying direct URL recovery...
Trying recovery using Next page URL...
Recovery successful.
```

## GitHub Safety

The following should not be committed:

- `.env`
- Database passwords
- API keys
- Personal credentials
- Generated CSV files
- Generated Excel files
- Python cache files
- Virtual environments

These are excluded using `.gitignore`.

## Future Improvements

Possible future improvements include:

- Logging with Python's `logging` module
- Environment-variable based configuration
- MongoDB unique indexes
- Automated scheduled scraping
- Additional stock categories
- Data validation
- Historical stock tracking
- Unit and integration tests

## Disclaimer

This project is created for educational and software-development purposes. The scraper should be used responsibly and in accordance with the target website's terms, policies, and applicable laws.
