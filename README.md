# File Filter Utility

File Filter Utility is a simple Python application that allows users to filter files in a directory based on their type (images, videos, zips, or folders), and perform operations such as opening, deleting, and renaming files.

## Features

- Filter files by type (Images, Videos, Zips, or Folders)
- Double-click to open files or folders
- Delete files or folders
- Rename files or folders while preserving their extensions

## Requirements

- Python 3.x
- Tkinter (should be included with Python)
- Tested on Windows, but should work on other platforms with minor adjustments

## Usage

1. Clone or download the repository.
2. Create a Virtual Environment:

    ```bash
    python -m venv .venv
    ```

3. Activate the Virtual Environment:

    ```bash
    .\.venv\Scripts\activate
    ```

4. Install the requirements from the requirements file:

    ```bash
    pip install -r requirements.txt 
    ```

5. Navigate to the project directory in your terminal.
6. Run the following command to launch the application:

    ```bash
    python main.py
    ```

7. Browse for the directory containing the files you want to filter.
8. Use the radio buttons to select the file type.
9. Double-click on a file or folder in the list to open it.
10. Click the "Delete" button to delete the selected file or folder.
11. Click the "Rename" button to rename the selected file or folder.

## Contributing

Contributions are welcome! If you have any ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
