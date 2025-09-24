import zipfile

def main():
  print("main logged")
  
  # get directory where scrapped lots are placed --> scraped_dir
  # get directory where unzipped files should be saved  --> unzipped_dir
  # if directory does not exist, create it with analog mirror name, ex: scraped-data/honda/accord --> unzipped-data/honda/accord
  # loop through each lot folder
  # unzip files to folder with exact named directory ex: scraped-data/honda/accord/12345678 -> unzipped-data/honda/accord/12345678
  # take contents of vehicle info txt file, convert it to json file and paste it with alongside the directory where unzipped images are placed, leave original txt file unafected

main()