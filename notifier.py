import sys
try:
    import winsound
except ImportError:
    winsound = None

def play_notification():
    try:
        if sys.platform == 'win32' and winsound:
            winsound.MessageBeep(winsound.MB_ICONASTERISK)
    except Exception:
        pass
