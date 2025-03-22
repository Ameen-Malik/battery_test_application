import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("Environment variables loaded:")
print(f"DATABASE_URL: {os.getenv('DATABASE_URL')}")
print(f"SUPABASE_URL: {os.getenv('SUPABASE_URL')}")
print(f"PROJECT_NAME: {os.getenv('PROJECT_NAME')}") 