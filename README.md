# CSV Word Search Tool

A Python utility for searching specific words within CSV files.

## Features

- Search for multiple words across CSV files
- Case-sensitive and case-insensitive search options
- Recursive directory search
- Detailed output showing file names and line numbers
- Error handling for file reading issues

## Usage

```bash
python csv_search.py "path/to/your/csv/files" word1 word2 word3 [--case-sensitive]
```

### Arguments

- `directory`: Path to the directory containing CSV files
- `words`: One or more words to search for
- `--case-sensitive`: Optional flag for case-sensitive search

### Example

```bash
# Search for "apple" and "banana" in the current directory
python csv_search.py . apple banana

# Case-sensitive search for "Apple" in a specific directory
python csv_search.py ./data Apple --case-sensitive
```

## Requirements

- Python 3.6 or higher
- No external dependencies required

## License

MIT License 