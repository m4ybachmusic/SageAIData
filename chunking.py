import pandas as pd
import json

def split_into_chunks(text, chunk_size=200):
    """
    Splits a text string into smaller chunks of approximately `chunk_size` words.
    """
    words = text.split()
    return [' '.join(words[i:i + chunk_size]) for i in range(0, len(words), chunk_size)]

def process_csv(file_path, chunk_size=200, output_file="processed_data.json"):
    """
    Reads a CSV file, splits the content into chunks, and saves the processed data as a JSON file.
    """
    # Load the CSV
    df = pd.read_csv(file_path)

    # Ensure your CSV has the required columns
    required_columns = ["URL", "Content Type", "Topic", "Sub Topic", "Content"]
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"CSV must contain the following columns: {', '.join(required_columns)}")

    # Initialize a list to hold processed data
    processed_data = []

    # Process each row
    for idx, row in df.iterrows():
        # Chunk the content
        chunks = split_into_chunks(row["Content"], chunk_size)

        # Add each chunk with metadata
        for i, chunk in enumerate(chunks):
            processed_data.append({
                "id": f"{idx}_{i}",  # Unique ID based on row index and chunk number
                "url": row["URL"],
                "content_type": row["Content Type"],
                "topic": row["Topic"],
                "sub_topic": row["Sub Topic"],
                "content": chunk
            })

    # Save processed data as a JSON file
    with open(output_file, 'w') as f:
        json.dump(processed_data, f, indent=4)

    print(f"Processed data saved to {output_file}")

# Example Usage
csv_file_path = "cleaned_data.csv"  # Replace with your CSV file path
chunk_size = 200  # Adjust chunk size as needed (words per chunk)
process_csv(csv_file_path, chunk_size)
