from playwright.sync_api import sync_playwright, Playwright
import json
import os
import re
from pathlib import Path

# url query of results from copart
url = "lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22PRID%22:%5B%22damage_type_code:DAMAGECODE_NW%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2014%20TO%202017%5D%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23MakeCode:HOND%20OR%20%23MakeDesc:Honda%22,%22%23LotModel:%5C%22ACCORD%5C%22%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D%20&displayStr=AUTOMOBILE,NORMAL%20WEAR,%5B0%20TO%209999999%5D,%5B2014%20TO%202017%5D,Honda,Accord&from=%2FvehicleFinder&fromSource=widget&qId=b121218d-a368-4941-a95c-ab37b276580e-1758645680911"
base_url = "https://www.copart.com/"


def run(pw: Playwright):
    chromium = pw.chromium
    launch_chromium = chromium.launch(
        headless=False,
        slow_mo=2000
    )
    page = launch_chromium.new_page(
        accept_downloads=True,
        base_url=base_url,
        bypass_csp=True,
    )

    # go to url
    page.goto(url=url, timeout=0)

    span_element = page.locator(
        ".search_result_title_block span[roundoffcounts].blue-heading"
    )
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
                clean_href = href.lstrip("/")
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
            with open(db_file, "r") as f:
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

    # Process each URL in the new_urls list
    for url_index, current_url in enumerate(urls):
        print(f"\nProcessing URL {url_index + 1}/{len(urls)}: {current_url}")

        # Extract lot number from URL
        lot_match = re.search(r"/lot/(\d+)/", current_url)
        if not lot_match:
            print(f"Error: Could not extract lot number from URL: {current_url}")
            continue

        lot_number = lot_match.group(1)
        print(f"Lot number: {lot_number}")

        # Create download directory
        download_path = Path.home() / "scraped-data" / "honda" / "accord" / f"{lot_number}"
        download_path.mkdir(parents=True, exist_ok=True)
        print(f"Download directory: {download_path.absolute()}")

        # Navigate to the URL
        try:
            page.goto(current_url, timeout=30000)
            page.wait_for_load_state("networkidle")
        except Exception as e:
            print(f"Error navigating to URL: {e}")
            continue

        # Try to find and click the download button
        download_success = False
        max_attempts = 5

        for attempt in range(max_attempts):
            print(
                f"Attempt {attempt + 1}/{max_attempts}: Looking for download button..."
            )

            # Check if download button is visible
            download_button = page.locator(
                ".lot-details-header-sprite.download-image-sprite-icon"
            )
            # download_button = page.locator('a.lot-image-floating-CTA.p-cursor-pointer.p-d-flex')

            if download_button.is_visible():
                print("Download button found! Clicking to download...")
                try:
                    download_button.click()
                    page.wait_for_timeout(1000)

                    second_download_button = page.locator(
                        # ".btn-reset.p-pb-5.text-dark-gray-3.p-decor-none" #differs on viewport
                        ".p-pb-5.text-dark-gray-3.p-decor-none"
                    )

                    if second_download_button.is_visible():
                        print("Second download button found! Starting download...")
                        # Set download path for this page
                        with page.expect_download() as download_info:
                            second_download_button.click()

                        download = download_info.value
                        # Save the downloaded file
                        downloaded_file = download_path / f"{lot_number}_images.zip"
                        download.save_as(downloaded_file)
                        print(f"Download successful! Saved to: {downloaded_file.absolute()}")
                        print(f"File exists: {downloaded_file.exists()}")
                        print(f"File size: {downloaded_file.stat().st_size if downloaded_file.exists() else 'N/A'} bytes")
                        download_success = True
                        break
                    else:
                        print(
                            "Second download button not found after clicking first button"
                        )
                        continue

                except Exception as e:
                    print(f"Error during download: {e}")
                    continue

            # If download button not found, try clicking next button
            if attempt < max_attempts - 1:  # Don't click next on the last attempt
                print("Download button not found. Clicking next button...")
                try:
                    next_button = page.locator(
                        "span.p-galleria-item-next-icon.pi.pi-chevron-right"
                    )
                    if next_button.is_visible():
                        next_button.click()
                        page.wait_for_timeout(2000)  # Wait for carousel to load
                    else:
                        print("Next button not found or not visible")
                        break
                except Exception as e:
                    print(f"Error clicking next button: {e}")
                    break

        if not download_success:
            print(
                f"Error: Could not find download button after {max_attempts} attempts for URL: {current_url}"
            )
            continue

        print(f"Successfully processed lot {lot_number}")

    print(f"\nCompleted processing {len(urls)} URLs")
    
    # Show summary of downloaded files
    download_base_path = Path.home() / "scraped-data" / "honda" / "accord"
    if download_base_path.exists():
        print(f"\nDownload Summary:")
        print(f"Download directory: {download_base_path.absolute()}")
        downloaded_files = list(download_base_path.glob("*.zip"))
        if downloaded_files:
            print(f"Downloaded {len(downloaded_files)} files:")
            for file in downloaded_files:
                file_size = file.stat().st_size
                print(f"  - {file.name} ({file_size:,} bytes)")
        else:
            print("No downloaded files found in the directory")

    input("Press Enter to close browser...")


# download all images into respective folders outside the project
# make additional txt file for each folder, including url, title and etc.
# push parsed link into db

playwright = sync_playwright().start()
run(playwright)
