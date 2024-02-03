---

# Table Data Harvester

This Python script automates the process of harvesting data from 'dynamic' tables found on websites. This script is designed to streamline the workflow of blockchain analysts by automating the tedious task of data extraction from tables.

## Installation Instructions

### Prerequisites

- Python 3.x
- PyQt5
- pyautogui
- pygetwindow
- pyperclip

### Setup

1. **Install Python 3.x**: Ensure Python 3.x is installed on your system. You can download it from [the official Python website](https://www.python.org/downloads/).

2. **Install Required Libraries**: Open your terminal or command prompt and run the following command:

    ```bash
    pip install PyQt5 pyautogui pygetwindow pyperclip
    ```

3. **Download the Script**: Download the script directly.

4. **Install Notepad++**: Download from https://notepad-plus-plus.org/downloads/

## Usage

Before running the script, ensure Notepad++ is open with a blank document focused.

1. **Start the Script**: Run the script by executing the following command in the terminal:

    ```bash
    python TRM_TABLE_DATA.py
    ```

2. **Set Row and Copy Command Positions of the 'Related IP' Data**: 
   - For the 'Row Position', aim to select the middle '.' of the 'IP Address' in the first row.
   - Right click on the middle '.'.
   - For the 'Copy Command', target the middle of the letter 'Y' in 'Copy Row'.
   
3. **Specify Expected Row Count**: Due to scrolling inaccuracies beyond 30 rows, it's recommended to set a maximum of 30 rows at a time. You can reposition the table and append more rows in batches of 30.

4. **Column Headers**: 
   - Select 'Yes' to include column headers in the first execution.
   - Choose 'No' for appending data to ensure headers are not duplicated.

5. **Start Data Harvesting**: Click the 'Start' button to commence data harvesting. Make sure the Notepad++ window is in focus.

## Features

- **Automated Data Copying**: Streamlines the extraction of 'Related IP' data.
- **Customizable Coordinates**: Users can specify exact coordinates for row selection and the copy command, enhancing accuracy.
- **Header Inclusion**: Option to include a predefined header before appending data, suitable for initial data setup.
- **Batch Processing**: Supports processing up to 30 rows at a time, optimizing for scrolling accuracy.
- **Notepad++ Integration**: Directly pastes data into Notepad++, ready for analysis.

## Notes

- Ensure a blank document is open in Notepad++ and in focus before starting the script.