"""Portable local launcher. Start with START_WINDOWS.bat or start_mac_linux.sh."""
import argparse
import os
from pathlib import Path
import threading
import time
import urllib.request
import webbrowser

ROOT = Path(__file__).resolve().parent


def load_config():
    source = ROOT / 'config.env'
    if source.exists():
        for raw in source.read_text(encoding='utf-8-sig').splitlines():
            line = raw.strip()
            if not line or line.startswith('#'):
                continue
            key, sep, value = line.partition('=')
            key = key.strip()
            if not sep or not key.startswith('TRACEPILOT_'):
                raise ValueError('config.env only accepts TRACEPILOT_ key=value settings.')
            os.environ.setdefault(key, value.strip().strip('"').strip("'"))


def main():
    parser = argparse.ArgumentParser(description='TracePilot local REST API testing dashboard')
    parser.add_argument('--port', type=int, default=8000)
    parser.add_argument('--no-browser', action='store_true')
    args = parser.parse_args()
    if not 1024 <= args.port <= 65535:
        parser.error('Choose a port between 1024 and 65535.')
    load_config()
    os.chdir(ROOT)
    url = f'http://127.0.0.1:{args.port}'
    print(f'\nTracePilot 1.0.0 | seed 42\nDashboard: {url}\nREST API docs: {url}/docs\nPress Ctrl+C to stop.\n', flush=True)
    if not args.no_browser:
        def open_when_ready():
            for _ in range(60):
                try:
                    with urllib.request.urlopen(url + '/api/health', timeout=1) as response:
                        if response.status == 200:
                            webbrowser.open(url)
                            return
                except OSError:
                    time.sleep(.5)
        threading.Thread(target=open_when_ready, daemon=True).start()
    import uvicorn
    uvicorn.run('app.main:app', host='127.0.0.1', port=args.port, workers=1, log_level='info')


if __name__ == '__main__':
    main()
