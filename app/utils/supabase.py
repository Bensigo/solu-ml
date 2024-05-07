import os
from supabase import create_client, Client
from supabase.client import ClientOptions
from decouple import Config, RepositoryEnv

# env=Config(RepositoryEnv('.env'))

# url: str = env.get("SUPABASE_URL")
# key: str = env.get("SUPABASE_KEY")

url: str = os.getenv("SUPABASE_URL")
key: str = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(url, key,
  options=ClientOptions(
    postgrest_client_timeout=10,
    storage_client_timeout=10
))

recipe_table = supabase.table('Recipe')
article_table = supabase.table('Resource')
session_table = supabase.table('Session')




