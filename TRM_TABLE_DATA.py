import sys
import threading
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QComboBox, QShortcut, QMessageBox
from PyQt5.QtGui import QKeySequence
import pyautogui
import pygetwindow as gw
import time
import subprocess
import pyperclip

# Global flag to control the loop execution
running = False

# Global variable to keep track of which button was last pressed
last_pressed_button = None

# Function to activate window by title
def activate_window_by_title(title):
    windows = gw.getWindowsWithTitle(title)
    for window in windows:
        if title in window.title:
            window.activate()
            return True
    return False

def main_loop(xOffset, yOffset, x2Offset, y2Offset, expectedRowCount, includeHeaders):
    global running
    running = True
    rowCount = 0  # Initialize row count
    
    if includeHeaders:
        header = '"IP Address","Observation Types","First Observation (UTC)","Last Observation (UTC)","Total Observations","Country","ISP","Related Addresses","Region","City","Latitude","Longitude"\n'
        # Copy header to clipboard
        pyperclip.copy(header)
        sleep_with_check(1)
        # Ensure Notepad or your text editor is focused before pasting
        if activate_window_by_title("Notepad"):
            sleep_with_check(1)  # Optional: Wait a bit to ensure the window is focused
            # Paste from clipboard
            pyautogui.hotkey('ctrl', 'v')
            sleep_with_check(1)  # Wait after pasting to ensure the operation completes

    # Capture the first nine rows without scrolling
    for _ in range(9):
        if not running or rowCount >= expectedRowCount:
            return  # Exit if stopped or expected row count is reached
        
        # Simulate actions to capture a row
        capture_row(xOffset, yOffset, x2Offset, y2Offset)
        rowCount += 1  # Increment the row count after each capture
        
        # Adjust offsets for the next capture
        yOffset += 84
        y2Offset += 84

    # After capturing the first nine rows without scrolling
    while running and rowCount < expectedRowCount:
        # Scroll to reveal new rows and update yOffset and y2Offset accordingly
        yOffset, y2Offset = scroll_to_reveal_new_rows(xOffset, yOffset, y2Offset)

        # Capture up to three new rows revealed by the scroll
        for _ in range(3):
            if not running or rowCount >= expectedRowCount:
                return  # Exit if stopped or expected row count is reached

            # Simulate actions to capture a row
            capture_row(xOffset, yOffset, x2Offset, y2Offset)
            rowCount += 1  # Increment the row count after each capture
            
            # Adjust offsets for the next capture
            yOffset += 84
            y2Offset += 84

def capture_row(xOffset, yOffset, x2Offset, y2Offset):
    if activate_window_by_title("Chrome"):
        pyautogui.click(xOffset, yOffset, button='right')
        sleep_with_check(0.5)
        pyautogui.click(x2Offset, y2Offset)
        if activate_window_by_title("Notepad"):
            sleep_with_check(0.5)
            pyautogui.hotkey('ctrl', 'v')
            pyautogui.press('enter')
            sleep_with_check(0.5)  # Wait after pasting
            activate_window_by_title("Chrome")
            sleep_with_check(1)  # Wait before the next capture cycle

# Function to scroll and reveal new rows
def scroll_to_reveal_new_rows(xOffset, yOffset, y2Offset):
    mouseX, mouseY = pyautogui.position()
    pyautogui.moveTo(xOffset, mouseY - 300)  # Move to the xOffset and an adjusted Y position
    pyautogui.scroll(-115)
    sleep_with_check(1)
    # Adjust for scrolling and return the updated values
    return yOffset - 240, y2Offset - 240

def sleep_with_check(duration):
    for _ in range(int(duration * 10)):  # Convert duration to tenths of a second
        if not running:
            break
        time.sleep(0.1)

def start_scrape():
    global xOffset, yOffset, x2Offset, y2Offset, expectedRowCount
    try:
        xOffset = int(xOffsetEdit.text())
        yOffset = int(yOffsetEdit.text())
        x2Offset = int(x2OffsetEdit.text())
        y2Offset = int(y2OffsetEdit.text())
    except ValueError:
        QMessageBox.critical(window, "Input Error", "Please enter valid numbers for all X and Y offsets.")
        return  # Stop the function if the inputs are invalid
    
    if not xOffsetEdit.text().strip() or not yOffsetEdit.text().strip() or not x2OffsetEdit.text().strip() or not y2OffsetEdit.text().strip():
        QMessageBox.critical(window, "Input Error", "X and Y offset fields cannot be blank.")
        return  # Stop the function if any field is blank

    expectedRowCount = int(rowCountComboBox.currentText())  # Get the selected row count
    includeHeaders = columnHeadersComboBox.currentText() == "Yes"
    
    threading.Thread(target=main_loop, args=(xOffset, yOffset, x2Offset, y2Offset, expectedRowCount, includeHeaders), daemon=True).start()

def stop_scrape():
    global running
    running = False

def set_mouse_position():
    global last_pressed_button
    mouseX, mouseY = pyautogui.position()  # Get current mouse position
    
    if last_pressed_button == 'row':
        xOffsetEdit.setText(str(mouseX))
        yOffsetEdit.setText(str(mouseY))
        setRowButton.setText('Set Row Position')  # Reset button text
    elif last_pressed_button == 'copy':
        x2OffsetEdit.setText(str(mouseX))
        y2OffsetEdit.setText(str(mouseY))
        setCopyButton.setText('Set Copy Position')  # Reset button text

    last_pressed_button = None  # Reset the last pressed button

def on_set_row_button_pressed():
    global last_pressed_button
    last_pressed_button = 'row'
    setRowButton.setText('Press Spacebar to Confirm')

def on_set_copy_button_pressed():
    global last_pressed_button
    last_pressed_button = 'copy'
    setCopyButton.setText('Press Spacebar to Confirm')

app = QApplication(sys.argv)
window = QWidget()
window.setWindowTitle("Automation Control")
window.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)

# Adjust the size here
window.setFixedSize(450, 1000)

layout = QVBoxLayout()

# Input fields for coordinates and their set buttons
xOffsetEdit = QLineEdit()
yOffsetEdit = QLineEdit()
setRowButton = QPushButton('Set Row Position')
setRowButton.clicked.connect(on_set_row_button_pressed)

x2OffsetEdit = QLineEdit()
y2OffsetEdit = QLineEdit()
setCopyButton = QPushButton('Set Copy Position')
setCopyButton.clicked.connect(on_set_copy_button_pressed)

# Adding widgets to the layout
layout.addWidget(QLabel("Row X Offset:"))
layout.addWidget(xOffsetEdit)
layout.addWidget(QLabel("Row Y Offset:"))
layout.addWidget(yOffsetEdit)
layout.addWidget(setRowButton)

layout.addWidget(QLabel("Copy Command X Offset:"))
layout.addWidget(x2OffsetEdit)
layout.addWidget(QLabel("Copy Command Y Offset:"))
layout.addWidget(y2OffsetEdit)
layout.addWidget(setCopyButton)

# Row count selection
rowCountComboBox = QComboBox()
for i in range(31):  # Fill with numbers from 0 to 200
    rowCountComboBox.addItem(str(i))
layout.addWidget(QLabel("Expected Row Count:"))
layout.addWidget(rowCountComboBox)

# Row Header selection
layout.addWidget(QLabel("'Related IP' Column Headers:"))
columnHeadersComboBox = QComboBox()
columnHeadersComboBox.addItem("Yes")
columnHeadersComboBox.addItem("No")
layout.addWidget(columnHeadersComboBox)

# Start and Stop buttons
startButton = QPushButton('Start')
stopButton = QPushButton('Stop')
startButton.clicked.connect(start_scrape)
stopButton.clicked.connect(stop_scrape)
layout.addWidget(startButton)
layout.addWidget(stopButton)

# Setup a QShortcut for the Spacebar to call set_mouse_position()
spacebar_shortcut = QShortcut(QKeySequence('Space'), window, set_mouse_position)

window.setLayout(layout)

# Position the window at the right middle of the screen
screen_geometry = QApplication.desktop().screenGeometry()
window.move(screen_geometry.right() - window.width(), (screen_geometry.height() - window.height()) // 2)

window.show()

sys.exit(app.exec_())
