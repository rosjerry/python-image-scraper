from playwright.sync_api import sync_playwright, Playwright
import json
import os

# url query of results from copart
url = "lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22PRID%22:%5B%22damage_type_code:DAMAGECODE_NW%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2014%20TO%202017%5D%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23MakeCode:HOND%20OR%20%23MakeDesc:Honda%22,%22%23LotModel:%5C%22ACCORD%5C%22%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D%20&displayStr=AUTOMOBILE,NORMAL%20WEAR,%5B0%20TO%209999999%5D,%5B2014%20TO%202017%5D,Honda,Accord&from=%2FvehicleFinder&fromSource=widget&qId=b121218d-a368-4941-a95c-ab37b276580e-1758645680911"
base_url = "https://www.copart.com/"


def run(pw: Playwright):
    chromium = pw.chromium
    launch_chromium = chromium.launch(headless=False)
    page = launch_chromium.new_page(
        accept_downloads=True, base_url=base_url, bypass_csp=True
    )

    # go to url
    page.goto(url=url, timeout=0)

    span_element = page.locator('.search_result_title_block span[roundoffcounts].blue-heading')
    span_element.wait_for()
    
    quantity_text = span_element.text_content()
    quantity = int(quantity_text) if quantity_text else 0
    
    print(f"Number of search results: {quantity}")

    if quantity <= 20:
        pass
    else:
        paginator_dropdown = page.locator(
            "div.p-paginator-rpp-options.p-dropdown.p-component.p-inputwrapper.p-inputwrapper-filled"
        )
        paginator_dropdown.click()

        for _ in range(4):
            page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")

    
    tr_elements = page.locator("tbody tr")
    
    urls = []
    for i in range(quantity):
        try:
            tr = tr_elements.nth(i)
            second_td = tr.locator("td").nth(1)
            a_element = second_td.locator("a").first
            href = a_element.get_attribute("href")
            if href:
                clean_href = href.lstrip('/')
                urls.append(f"{base_url}{clean_href}")
        except Exception as e:
            print(f"Error extracting href from row {i}: {e}")
            continue

    # scrape all urls
    print(f"Extracted {len(urls)} URLs:")
    for first_list_url in urls:
        print(first_list_url)
    print("urls list ==> ", urls)
    
    # check if this url already exists in db
    db_file = "db.json"
    
    # Load existing parsed URLs from database
    try:
        if os.path.exists(db_file):
            with open(db_file, 'r') as f:
                db_data = json.load(f)
                already_parsed_urls = db_data.get("already_parsed_urls", [])
        else:
            already_parsed_urls = []
            print("Database file not found, starting with empty list")
    except Exception as e:
        print(f"Error loading database: {e}")
        already_parsed_urls = []
    
    print(f"Found {len(already_parsed_urls)} already parsed URLs in database")
    
    new_urls = []
    existing_urls = []
    
    for second_list_url in urls:
        if second_list_url in already_parsed_urls:
            existing_urls.append(second_list_url)
        else:
            new_urls.append(second_list_url)
    
    print(f"\nURL Analysis:")
    print(f"Total URLs found: {len(urls)}")
    print(f"Already parsed: {len(existing_urls)}")
    print(f"New URLs to process: {len(new_urls)}")
    
    if existing_urls:
        print(f"\nAlready parsed URLs (skipping):")
        for third_list_url in existing_urls:
            print(f"  - {third_list_url}")
    
    if new_urls:
        print(f"\nNew URLs to process:")
        for forth_list_url in new_urls:
            print(f"  - {forth_list_url}")
    else:
        print("\nNo new URLs to process - all URLs have already been parsed!")
    
    urls = new_urls
    
    # scrape all gathered urls after one ecahother
    
    input("Press Enter to close browser...")


# download all images into respective folders outside the project
# make additional txt file for each folder, including url, title and etc.
# push parsed link into db

playwright = sync_playwright().start()
run(playwright)
