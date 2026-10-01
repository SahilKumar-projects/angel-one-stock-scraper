import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.common.exceptions import (
    TimeoutException,
    StaleElementReferenceException
)

from config import WAIT_TIMEOUT, MAX_RETRIES

# WAIT FOR TABLE

def wait_for_table(driver):

    try:

        WebDriverWait(driver, WAIT_TIMEOUT).until(
            EC.presence_of_element_located(
                (
                    By.CSS_SELECTOR,
                    "#stocks-sector-listing-ssr table"
                )
            )
        )

        return True

    except TimeoutException:

        return False

# EXTRACT CURRENT PAGE

def extract_current_page(driver):

    for attempt in range(MAX_RETRIES):

        try:

            print(
                f"Extracting page... "
                f"Attempt {attempt + 1}/{MAX_RETRIES}"
            )

            table = driver.find_element(
                By.CSS_SELECTOR,
                "#stocks-sector-listing-ssr table"
            )

            # Get table headers
            header_elements = table.find_elements(
                By.CSS_SELECTOR,
                "thead th"
            )

            headers = []

            for header in header_elements:

                text = header.get_attribute(
                    "textContent"
                ).strip()

                if text:

                    headers.append(text)

            # Required columns
            required_columns = [
                "Company",
                "LTP",
                "Volume",
                "Market Cap",
                "52W High",
                "52W Low",
                "Sector"
            ]

            # Map header names to column indexes
            header_index = {}

            for index, header in enumerate(headers):

                clean_header = header.strip()

                if clean_header in required_columns:

                    header_index[clean_header] = index

            # Check for missing columns
            missing_columns = []

            for column in required_columns:

                if column not in header_index:

                    missing_columns.append(column)

            if missing_columns:

                print(
                    "Missing columns:",
                    missing_columns
                )

                return []

            # Get table rows
            rows = table.find_elements(
                By.CSS_SELECTOR,
                "tbody tr"
            )

            stocks = []

            for row in rows:

                try:

                    cells = row.find_elements(
                        By.CSS_SELECTOR,
                        "td"
                    )

                    if not cells:

                        continue

                    stock = {}

                    for column in required_columns:

                        index = header_index[column]

                        if index < len(cells):

                            value = cells[index].get_attribute(
                                "textContent"
                            ).strip()

                        else:

                            value = ""

                        stock[column] = value

                    if stock["Company"]:

                        stocks.append(stock)

                except StaleElementReferenceException:

                    raise

            print(
                f"Extracted {len(stocks)} stocks."
            )

            return stocks

        except StaleElementReferenceException:

            print(
                "Table changed while extracting."
            )

            print(
                "Retrying extraction..."
            )

            time.sleep(1)

        except Exception as error:

            print(
                "Could not extract page:",
                error
            )

            return []

    print(
        "Extraction failed after all retries."
    )

    return []


# FIND NEXT BUTTON

def get_next_button(driver):

    try:

        return driver.find_element(
            By.CSS_SELECTOR,
            'a[aria-label="Go to next page"]'
        )

    except Exception as e:
        print(f"An error occurred: {e}")
        return None


# CHECK WHETHER NEXT BUTTON IS DISABLED

def is_next_button_disabled(next_button):

    if next_button is None:

        return True

    try:

        disabled = next_button.get_attribute(
            "disabled"
        )

        if disabled is not None:

            return True

        aria_disabled = next_button.get_attribute(
            "aria-disabled"
        )

        if aria_disabled == "true":

            return True

        class_name = next_button.get_attribute(
            "class"
        )

        if class_name and "disabled" in class_name.lower():

            return True

        return False

    except StaleElementReferenceException:

        return True

    except Exception:

        return True


# GET NEXT PAGE URL

def get_next_page_url(driver):

    try:

        next_button = get_next_button(driver)

        if next_button is None:

            return None

        return next_button.get_attribute(
            "href"
        )

    except Exception:

        return None


# RECOVER NEXT PAGE


def recover_next_page(driver, next_page_url):

    if not next_page_url:

        print(
            "No recovery URL available."
        )

        return False

    try:

        print(
            "Trying recovery using Next page URL..."
        )

        driver.get(next_page_url)

        if wait_for_table(driver):

            print(
                "Recovery successful."
            )

            return True

        print(
            "Recovery failed: table did not load."
        )

        return False

    except Exception as error:

        print(
            "Recovery failed:",
            error
        )

        return False


# CLICK NEXT PAGE


def click_next_page(driver):

    try:

        next_button = get_next_button(driver)

        if next_button is None:

            print(
                "Next button not found."
            )

            return False

        if is_next_button_disabled(next_button):

            return False

        # Save href before clicking
        next_page_url = get_next_page_url(driver)

        if not next_page_url:

            print(
                "Next page URL not found."
            )

            return False

        current_url = driver.current_url

        try:

            print(
                "Clicking Next..."
            )

            next_button.click()

            WebDriverWait(
                driver,
                WAIT_TIMEOUT
            ).until(
                EC.url_changes(current_url)
            )

            if wait_for_table(driver):

                print(
                    "Next page loaded successfully."
                )

                return True

            print(
                "Next page table did not load."
            )

        except Exception as error:

            print(
                "Next click failed:",
                error
            )

        # Direct URL recovery
        print(
            "Trying direct URL recovery..."
        )

        return recover_next_page(
            driver,
            next_page_url
        )

    except Exception as error:

        print(
            "Could not move to next page:",
            error
        )

        return False



# MAIN SCRAPER


def scrape_large_cap_stocks(driver):

    all_stocks = []

    current_page = 1

    extraction_complete = False

    try:

        while True:

            print()
            print(
                "========== Page "
                f"{current_page} =========="
            )

            # WAIT FOR CURRENT PAGE
        

            if not wait_for_table(driver):

                print(
                    "Table did not load."
                )

                print(
                    f"Scraping stopped at page "
                    f"{current_page}."
                )

                break

            
            # EXTRACT CURRENT PAGE
            

            page_data = extract_current_page(driver)

            if not page_data:

                print(
                    f"Page {current_page} returned no data."
                )

                print(
                    "Scraping stopped."
                )

                break

            # Add current page records
            all_stocks.extend(page_data)

            print(
                f"Total stocks collected so far: "
                f"{len(all_stocks)}"
            )

    
            # FIND NEXT BUTTON


            next_button = get_next_button(driver)

            # LAST PAGE CHECK

            if is_next_button_disabled(next_button):

                
                print(
                    "Next button is disabled."
                )

                print(
                    "Last page reached."
                )

                extraction_complete = True

                break

            
            # MOVE TO NEXT PAGE

            next_page_loaded = click_next_page(driver)

            if next_page_loaded:

                current_page += 1

                continue

            # NEXT PAGE COULD NOT BE LOADED

            print(
                "Could not move to the next page."
            )

            print(
                f"Scraping stopped after page "
                f"{current_page}."
            )

            break

    except KeyboardInterrupt:

        print(
            "Scraping stopped by user."
        )

        print(
            f"Returning {len(all_stocks)} "
            "records collected so far."
        )

        extraction_complete = False

    except Exception as error:

        print()
        print(
            "Unexpected error:",
            error
        )

        print(
            f"Returning {len(all_stocks)} "
            "records collected so far."
        )

        extraction_complete = False

    # ---------------------------------------------------------
    # FINAL RESULT
    # ---------------------------------------------------------

    print(
        "========== SCRAPING COMPLETED =========="
    )

    print(
        f"Total stocks collected: "
        f"{len(all_stocks)}"
    )

    if extraction_complete:

        print(
            "Extraction status: COMPLETE"
        )

    else:

        print(
            "Extraction status: INCOMPLETE"
        )

    return all_stocks