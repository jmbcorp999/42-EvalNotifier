# Evaluation Monitor
This Python project helps you monitor your email inbox for specific subjects and provides visual and audio alerts when new emails matching the criteria are detected.
The user interface is built using the Tkinter library, and audio alerts are played using the Pygame library.
Mail are checked every 60 seconds by defaut, and found mail are set as read when corresponding.

## Dependencies
To run this project, you will need Python 3.x and the following libraries:
- Tkinter: for the graphical user interface.
- Pygame: to play audio alerts.
You can install these libraries using pip:

```pip install pygame```

Note: Tkinter comes pre-installed with most Python installations, so there's no need to install it separately.

## How to use
1. Clone this repository or download the source code.
2. Update the EMAIL, PASSWORD, and SERVER variables in the EvalNotifier.py file with your email address, password, and IMAP server information, respectively.
3. Place your audio files (e.g., new.wav and imminent.wav) in the same directory as the EvalNotifier.py script.
4. Run the EvalNotifier.py script:

```python EvalNotifier.py```

The program will monitor your inbox for new emails with the subjects "You have a new booking" and "Evaluation imminent".
When an email with the subject "You have a new booking" is detected, the program will play the new.wav audio file,
and when an email with the subject "Evaluation imminent" is detected, the imminent.wav audio file will be played.
Additionally, the program's window will be brought to the foreground when a new email with the subject "Evaluation imminent" is detected.

## Customization
To customize the program for your specific needs, you can modify the following sections in the EvalNotifier.py script:
1. Update the `if subject == "You have a new booking":` and `elif subject == "Evaluation imminent":` conditions to match the subjects you want to monitor.
2. Replace the audio files new.wav and imminent.wav with your preferred audio alerts.

# Happy monitoring!

