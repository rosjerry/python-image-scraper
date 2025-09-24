import zipfile
import json
import os
from pathlib import Path
import shutil

def main():
    print("Starting unzip process...")
    
    scraped_dir = Path.home() / "scraped-data"
    print(f"Scraped directory: {scraped_dir.absolute()}")
    
    unzipped_dir = Path.home() / "unzipped-data"
    print(f"Unzipped directory: {unzipped_dir.absolute()}")
    
    if not scraped_dir.exists():
        print(f"Scraped directory does not exist: {scraped_dir}")
        return
    
    processed_count = 0
    error_count = 0
    
    for brand_path in scraped_dir.iterdir():
        if not brand_path.is_dir():
            continue
            
        brand_name = brand_path.name
        print(f"\nProcessing brand: {brand_name}")
        
        for model_path in brand_path.iterdir():
            if not model_path.is_dir():
                continue
                
            model_name = model_path.name
            print(f"  Processing model: {model_name}")
            
            unzipped_brand_model = unzipped_dir / brand_name / model_name
            unzipped_brand_model.mkdir(parents=True, exist_ok=True)
            
            for lot_path in model_path.iterdir():
                if not lot_path.is_dir():
                    continue
                    
                lot_number = lot_path.name
                print(f"    Processing lot: {lot_number}")
                
                try:
                    unzipped_lot_path = unzipped_brand_model / lot_number
                    unzipped_lot_path.mkdir(parents=True, exist_ok=True)
                    
                    zip_files = list(lot_path.glob("*.zip"))
                    if not zip_files:
                        print(f"      No zip file found in {lot_path}")
                        continue
                    
                    zip_file = zip_files[0]  # Take the first zip file found
                    print(f"      Unzipping: {zip_file.name}")
                    
                    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                        zip_ref.extractall(unzipped_lot_path)
                    
                    print(f"      Extracted to: {unzipped_lot_path.absolute()}")
                    
                    txt_files = list(lot_path.glob("*_vehicle_info.txt"))
                    if txt_files:
                        txt_file = txt_files[0]
                        print(f"      Processing vehicle info: {txt_file.name}")
                        
                        with open(txt_file, 'r', encoding='utf-8') as f:
                            txt_content = f.read()
                        
                        vehicle_data = parse_vehicle_info_text(txt_content)
                        
                        json_file = unzipped_lot_path / f"{lot_number}_vehicle_info.json"
                        with open(json_file, 'w', encoding='utf-8') as f:
                            json.dump(vehicle_data, f, indent=2, ensure_ascii=False)
                        
                        print(f"      JSON saved to: {json_file.absolute()}")
                    else:
                        print(f"      No vehicle info file found for lot {lot_number}")
                    
                    processed_count += 1
                    
                except Exception as e:
                    print(f"      Error processing lot {lot_number}: {e}")
                    error_count += 1
                    continue
    
    print(f"\nUnzip process completed!")
    print(f"Processed: {processed_count} lots")
    print(f"Errors: {error_count} lots")

def parse_vehicle_info_text(txt_content):
    """Parse vehicle information text file and convert to structured JSON"""
    lines = txt_content.strip().split('\n')
    
    vehicle_data = {
        "url": "",
        "vehicle_info": {},
        "scraped_on": ""
    }
    
    if lines and lines[0].startswith("URL:"):
        vehicle_data["url"] = lines[0].replace("URL:", "").strip()
    
    for line in lines:
        if ":" in line and not line.startswith("URL:") and not line.startswith("=") and not line.startswith("Scraped on:"):
            parts = line.split(":", 1)
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                vehicle_data["vehicle_info"][key] = value
    
    for line in lines:
        if line.startswith("Scraped on:"):
            vehicle_data["scraped_on"] = line.replace("Scraped on:", "").strip()
            break
    
    return vehicle_data

if __name__ == "__main__":
    main()