import webview
from admin_web import app

if __name__ == '__main__':
    window = webview.create_window(
        'PUP Shop - Admin Panel',
        app,
        width=1024,
        height=768
    )
    webview.start(debug=True)