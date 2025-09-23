from playwright.sync_api import Page, expect

# url query of results from copart
url = 'https://www.copart.com/lotSearchResults?free=false&searchCriteria=%7B%22query%22:%5B%22*%22%5D,%22filter%22:%7B%22PRID%22:%5B%22damage_type_code:DAMAGECODE_NW%22%5D,%22ODM%22:%5B%22odometer_reading_received:%5B0%20TO%209999999%5D%22%5D,%22YEAR%22:%5B%22lot_year:%5B2014%20TO%202017%5D%22%5D,%22MISC%22:%5B%22%23VehicleTypeCode:VEHTYPE_V%22,%22%23MakeCode:HOND%20OR%20%23MakeDesc:Honda%22,%22%23LotModel:%5C%22ACCORD%5C%22%22%5D%7D,%22searchName%22:%22%22,%22watchListOnly%22:false,%22freeFormSearch%22:false%7D%20&displayStr=AUTOMOBILE,NORMAL%20WEAR,%5B0%20TO%209999999%5D,%5B2014%20TO%202017%5D,Honda,Accord&from=%2FvehicleFinder&fromSource=widget&qId=b121218d-a368-4941-a95c-ab37b276580e-1758645680911'

def test_main ():
  print("copart")
  

# go to copart vehicle finder url
def test_visit_website(page: Page):
  page.goto(url)
  security_check_locator = page.locator("p:has-text('Additional security check is required')")
  visible = security_check_locator.is_visible()

  if visible:
    print("continue is unavailable at this moment, try again later")
  else:
    pass

# change pagination to maximum
# scrape all urls
# check if this url already exists in db
# scrape all gathered urls after one ecahother
# download all images into respective folders outside the project
# make additional txt file for each folder, including url, title and etc.
# push parsed link into db
  
if __name__ == "__main__":
  test_main()