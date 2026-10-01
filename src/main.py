from browser import create_driver
from config import LARGE_CAP_URL
from scraper import scrape_large_cap_stocks
from csv_writer import create_Excel_file


def main():
    
    driver = create_driver()
    
    try:
        driver.get(LARGE_CAP_URL)
        data = scrape_large_cap_stocks(driver)

        print("Data:", data)
        
        output_path = create_Excel_file(data)

        print("Excel file:",output_path)

    finally:
        
        driver.quit()
        return


if __name__ == "__main__":
    main()