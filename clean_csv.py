import pandas as pd
import re
import requests

def clean_text(text):
    """
    Remove HTML tags and normalize whitespace in the given text.
    """
    text = re.sub(r'<.*?>', '', text)  # Remove HTML tags
    text = re.sub(r'\s+', ' ', text).strip()  # Normalize whitespace
    return text

def validate_url(url):
    """
    Check if the URL is valid and reachable.
    """
    try:
        response = requests.head(url, timeout=5)
        return response.status_code == 200
    except:
        return False

def clean_csv(input_file, output_file):
    """
    Perform basic cleaning on a CSV file and save the cleaned version.
    """
    # Load the CSV file
    print("Loading CSV...")
    df = pd.read_csv(input_file)

    # Remove duplicate rows based on URL and Content
    print("Removing duplicates...")
    df = df.drop_duplicates(subset=['URL', 'Content'])

    # Drop rows with missing Content or URL
    print("Dropping rows with missing Content or URL...")
    df = df.dropna(subset=['Content', 'URL'])

    # Fill missing Topic or Subtopic with 'Unknown'
    print("Filling missing Topic and Subtopic with 'Unknown'...")
    df['Topic'] = df['Topic'].fillna('Unknown')
    df['Sub Topic'] = df['Sub Topic'].fillna('Unknown')

    # Clean Content by removing HTML tags and normalizing whitespace
    print("Cleaning Content column...")
    df['Content'] = df['Content'].apply(clean_text)

    # Capitalize Topic and Subtopic consistently
    print("Standardizing Topic and Subtopic capitalization...")
    df['Topic'] = df['Topic'].str.title()
    df['Sub Topic'] = df['Sub Topic'].str.title()

    # Normalize Content Type to lowercase
    print("Normalizing Content Type...")
    df['Content Type'] = df['Content Type'].str.lower()

    # Strip whitespace from all text fields
    print("Stripping whitespace from all text fields...")
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

    # Save the cleaned CSV
    print("Saving cleaned CSV...")
    df.to_csv(output_file, index=False)
    print(f"Cleaned CSV saved to {output_file}")

# Set input and output file paths
input_file = 'content_data.csv'  # Replace with your raw CSV file path
output_file = 'cleaned_data.csv'  # Replace with your desired output file path

# Run the cleaning function
clean_csv(input_file, output_file)
