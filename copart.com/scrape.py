from playwright.sync_api import sync_playwright, Playwright


# url query of results from copart
url = 'lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22PRID%22:%5B%22damage_type_code:DAMAGECODE_NW%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2014%20TO%202017%5D%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23MakeCode:HOND%20OR%20%23MakeDesc:Honda%22,%22%23LotModel:%5C%22ACCORD%5C%22%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D%20&displayStr=AUTOMOBILE,NORMAL%20WEAR,%5B0%20TO%209999999%5D,%5B2014%20TO%202017%5D,Honda,Accord&from=%2FvehicleFinder&fromSource=widget&qId=b121218d-a368-4941-a95c-ab37b276580e-1758645680911'
base_url = "https://www.copart.com/"


def run(pw: Playwright):
    chromium = pw.chromium
    launch_chromium = chromium.launch(
        headless=False
    )
    page = launch_chromium.new_page(
        accept_downloads=True, base_url=base_url, bypass_csp=True
    )
    
    # go to url
    page.goto(url=url, timeout=0) 
    
    # Find the span with class 'blue-heading' and get its text content
    counted_search_result = page.locator("tbody.p-datatable-tbody")
    tr_elements = counted_search_result.locator("tr")
    quantity = tr_elements.count()
    
    if(quantity <= 20):
        pass
    else:
        paginator_dropdown = page.locator("div.p-paginator-rpp-options.p-dropdown.p-component.p-inputwrapper.p-inputwrapper-filled")
        paginator_dropdown.click()
        
        for _ in range(4):
            page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")
    
    print(f"Number of <tr> elements: {quantity}")
    
    input("Press Enter to close browser...")



# scrape all urls
# check if this url already exists in db
# scrape all gathered urls after one ecahother
# download all images into respective folders outside the project
# make additional txt file for each folder, including url, title and etc.
# push parsed link into db

playwright = sync_playwright().start()
run(playwright)
