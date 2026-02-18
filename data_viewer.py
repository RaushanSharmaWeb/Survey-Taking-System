import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

print("--- 🚀 Script Start Ho Raha Hai ---")

# 1. Secret Key Check
secret_key = os.environ.get('FIREBASE_URL')

if not secret_key:
    print("❌ ERROR: GitHub Secret 'FIREBASE_URL' nahi mila!")
    print("Check karo ki YAML file mein 'env:' section sahi hai ya nahi.")
    exit(1)
else:
    print("✅ Secret Key mil gayi. Ab JSON check kar raha hoon...")

# 2. JSON Validation
try:
    cred_info = json.loads(secret_key)
    print("✅ JSON Key valid hai!")
except Exception as e:
    print(f"❌ ERROR: Secret Key sahi JSON format mein nahi hai!")
    print(f"Error Details: {e}")
    exit(1)

# 3. Firebase Connection
try:
    cred = credentials.Certificate(cred_info)
    # Check if app is already initialized to avoid overwrite error
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)
    
    db = firestore.client()
    print("✅ Firebase se connect ho gaya!")
except Exception as e:
    print(f"❌ ERROR: Firebase connect nahi ho paya.")
    print(f"Error Details: {e}")
    exit(1)

# 4. Data Fetching
print("\n--- 📊 DATA FETCHING ---")
try:
    # Collection name wahi hona chahiye jo HTML mein hai ('surveys')
    surveys = db.collection('surveys').stream()
    
    count = 0
    for doc in surveys:
        data = doc.to_dict()
        print(f"User: {data.get('name', 'Unknown')} | Lang: {data.get('language', 'N/A')}")
        count += 1
    
    print(f"\nTotal Surveys Found: {count}")

except Exception as e:
    print(f"❌ ERROR: Data padhne mein dikkat aayi.")
    print(f"Error Details: {e}")

print("--- Script Khatam ---")
