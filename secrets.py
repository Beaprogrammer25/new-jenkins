import csv
import subprocess
import json

# Replace these values with your own
AWS_REGION = 'us-east-1'

# Read the CSV file and update the secrets
with open('secrets.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        # Adjust the column name to match your CSV file's header exactly
        secret_id = row['secret-name '].strip().replace(' ', '_')  # Replace 'secret-name' with the correct column name
        
        print("Attempting to update secret:", secret_id)

        # Initialize an empty dictionary to store key-value pairs for the secret
        secret_data = {}

        # Iterate through columns and extract 'key-value' pairs
        for key, value in row.items():
            if key.startswith('key') and value:
                idx = key.replace('key', '')
                corresponding_value = row.get('value{}'.format(idx), '').strip()

                # Add the key-value pair to the secret_data dictionary
                if corresponding_value:
                    secret_data[value.strip()] = corresponding_value

        # Update the secret in AWS Secrets Manager using subprocess.call()
        subprocess.call([
            'aws', 'secretsmanager', 'put-secret-value',
            '--region', AWS_REGION,
            '--secret-id', secret_id,
            '--secret-string', json.dumps(secret_data)  # Use formatted key-value pairs for the secret
        ])
