import os
import csv
import argparse
from typing import List, Tuple
from tabulate import tabulate

def search_csv_files(directory: str, search_words: List[str], case_sensitive: bool = False) -> List[Tuple[str, int, List[str], dict]]:
    """
    Search for words in all CSV files within the specified directory.
    Returns a list of (filename, line_number, row, header_map) for each match.
    """
    results = []
    
    # Convert search words to lowercase if case insensitive
    if not case_sensitive:
        search_words = [word.lower() for word in search_words]
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        header = next(reader, None)
                        if header is None:
                            continue
                        header_map = {name.strip(): idx for idx, name in enumerate(header)}
                        for line_num, row in enumerate(reader, 2):  # 2 because header is line 1
                            line_text = ' '.join(str(cell) for cell in row)
                            if not case_sensitive:
                                line_text = line_text.lower()
                            for word in search_words:
                                if word in line_text:
                                    results.append((file_path, line_num, row, header_map, header))
                                    break
                except Exception as e:
                    print(f"Error reading {file_path}: {str(e)}")
    return results

def main():
    parser = argparse.ArgumentParser(description='Search for words in CSV files')
    parser.add_argument('directory', help='Directory containing CSV files')
    parser.add_argument('words', nargs='+', help='Words to search for')
    parser.add_argument('--case-sensitive', action='store_true', help='Perform case-sensitive search')
    args = parser.parse_args()
    if not os.path.isdir(args.directory):
        print(f"Error: {args.directory} is not a valid directory")
        return
    results = search_csv_files(args.directory, args.words, args.case_sensitive)
    if not results:
        print("No matches found.")
    else:
        print(f"\nFound {len(results)} matches:")
        # Prepare table data
        table_data = []
        headers_needed = [
            'Donor First Name',
            'Donor Last Name',
            'Donation Date',
            'Match Amount',
            'Total Donation to be Acknowledged'
        ]
        for _, _, row, header_map, _ in results:
            row_data = []
            for col in headers_needed:
                idx = header_map.get(col, None)
                row_data.append(row[idx] if idx is not None and idx < len(row) else '')
            table_data.append(row_data)
        print("\nDonation Summary:")
        print(tabulate(table_data, headers=headers_needed, tablefmt='grid'))

        # Print all matching rows with all columns
        print("\nFull Matching Rows:")
        for file_path, line_num, row, _, header in results:
            print(f"\nFile: {file_path}, Line: {line_num}")
            print(tabulate([row], headers=header, tablefmt='grid'))

if __name__ == '__main__':
    main() 