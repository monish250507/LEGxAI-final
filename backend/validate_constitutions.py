import json
import os

print("🔍 Constitution Files Validation:")

required_files = ['COI.json', 'China_2018.json', 'Japan_1946.json', 'Russia_2014.json']
data_dir = 'data'

for filename in required_files:
    filepath = os.path.join(data_dir, filename)
    exists = os.path.exists(filepath)
    
    if exists:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check structure - multiple formats possible
            if isinstance(data, list) and len(data) > 0 and isinstance(data[0], list):
                article_count = len(data[0])
                print(f"✅ {filename}: {article_count} articles (nested array format)")
            elif 'document' in data and 'section' in data['document']:
                section_count = len(data['document']['section'])
                print(f"✅ {filename}: {section_count} sections (document format)")
            elif 'articles' in data:
                article_count = len(data['articles'])
                print(f"✅ {filename}: {article_count} articles (standard format)")
            else:
                print(f"⚠️  {filename}: Unexpected structure - {type(data).__name__}")
                
        except Exception as e:
            print(f"❌ {filename}: Error loading - {e}")
    else:
        print(f"❌ {filename}: File missing")

print("\n📋 Constitution data validation completed.")
