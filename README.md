##Overview

The Activity Monitor program is designed to track user activity on a computer and automatically log out the user after a period of inactivity. It uses several libraries to achieve its functionality:

    pynput: For detecting mouse movements and keyboard actions.

    keyboard: For capturing keyboard events.

    pyautogui: For tracking mouse position and determining inactivity.

    tkinter: For the graphical user interface (GUI).

#Features

    Mouse Activity Monitoring: Monitors mouse movements and interactions.

    Keyboard Activity Monitoring: Captures keyboard actions.

    Automatic Logout: Logs out the user after a predefined period of inactivity.

    Graphical User Interface: Provides a GUI for user interaction and notifications using tkinter.

#Installation

Clone the Repository:
git clone https://github.com/Deepak3168/Activity-Monitor.git
cd Activity-Monitor

Install the Required Libraries:

Ensure you have Python installed. Install the necessary libraries using the requirements.txt file:

    pip install -r requirements.txt

#Configuration

Inactivity Threshold: The default threshold for inactivity is set to 5 minutes (300 seconds). This can be adjusted in the code in needed
    ```bash on action.py  lineno:10

    self.inactivity_threshold = 300 ```

    Back end Configuration: Ensure that the back end endpoints are running before using the Activity Monitor program. Configure the back end endpoints in login.py and logout.py to match your server's URL.

Usage

Run the Program:

Navigate to the directory where monitor.py is located and execute the following command:

    python monitor.py

    Program Operation:

        The GUI window provided by tkinter will launch, allowing you to interact with the program.

        The program will start monitoring user activity.

        If no mouse or keyboard activity is detected for the set threshold period, the program will automatically log out the user.

Repository

    Repository Link: Activity Monitor Program Repository

Example Use Case

    Security: Automatically logs out users after a period of inactivity to enhance security.

    Session Management: Helps manage idle sessions effectively, freeing up system resources.

    User Interaction: Provides a graphical interface for monitoring and notifications.
