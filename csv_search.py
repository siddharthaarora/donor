import os
import csv
import argparse
from typing import List, Tuple

def search_csv_files(directory: str, search_words: List[str], case_sensitive: bool = False) -> List[Tuple[str, int, str]]:
    """
    Search for words in all CSV files within the specified directory.
    
    Args:
        directory: Path to the directory containing CSV files
        search_words: List of words to search for
        case_sensitive: Whether the search should be case sensitive
    
    Returns:
        List of tuples containing (filename, line_number, matching_line)
    """
    results = []
    
    # Convert search words to lowercase if case insensitive
    if not case_sensitive:
        search_words = [word.lower() for word in search_words]
    
    # Walk through the directory
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as csvfile:
                        reader = csv.reader(csvfile)
                        for line_num, row in enumerate(reader, 1):
                            # Join all cells in the row for searching
                            line_text = ' '.join(str(cell) for cell in row)
                            if not case_sensitive:
                                line_text = line_text.lower()
                            
                            # Check if any search word is in the line
                            for word in search_words:
                                if word in line_text:
                                    results.append((file_path, line_num, ' '.join(row)))
                                    break  # Stop checking other words once a match is found
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
        for file_path, line_num, line_text in results:
            print(f"\nFile: {file_path}")
            print(f"Line {line_num}: {line_text}")

if __name__ == '__main__':
    main() 