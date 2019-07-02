import json

# Enter your keys/secrets as strings in the following fields
credentials = {}  
credentials['CONSUMER_KEY'] = 'FpLcOiJ5v0hexZtOdoA9KYzyD'  
credentials['CONSUMER_SECRET'] = 'CCgGKBril0YC6UmT1938SNqkmIdxMYBWQP7u3AjQ36Djkzmn15'  
credentials['ACCESS_TOKEN'] = '28675174-0JSq5vtag4ywtARrVcGnOHjBKlSnrUIReNbBWVNVt'  
credentials['ACCESS_SECRET'] = 's4CJtFPty0pe0rPv2WE5WDXhgkGZ8yhQCXivLMlgdS7O5'

# Save the credentials object to file
with open("credentials.json", "w") as file:  
    json.dump(credentials, file)