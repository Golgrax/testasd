import webview
import os
from web_app import app
from threading import Thread

# Path to a flag file to check if it's the first run
FLAG_FILE = os.path.join(os.path.dirname(__file__), '..', '.first_run_complete')

def is_first_run():
    """Check if the flag file exists."""
    return not os.path.exists(FLAG_FILE)

def mark_first_run_complete():
    """Create the flag file."""
    with open(FLAG_FILE, 'w') as f:
        f.write('completed')

if __name__ == '__main__':
    # Determine the starting URL
    if is_first_run():
        start_url = '/splash/1'
        # The user will navigate to '/' from the splash screen,
        # at which point we mark the first run as complete.
        # A more robust way is to use pywebview's JS API, but this is simpler.
        mark_first_run_complete() 
    else:
        start_url = '/'

    # pywebview will start the Flask server automatically
    window = webview.create_window(
        'PUP E-Commerce Shop',
        app,
        width=450,
        height=800,
        resizable=True,
        min_size=(400, 700)
    )
    
    # Start the pywebview event loop
    webview.start(debug=True) # Set debug=False for production