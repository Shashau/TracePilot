"""Create a platform-local venv using the shared lock; never bundle a foreign venv."""
import hashlib
import os
from pathlib import Path
import platform
import subprocess
import sys
import venv

ROOT = Path(__file__).resolve().parent


def main():
    if not (3, 11) <= sys.version_info[:2] <= (3, 13):
        raise SystemExit('Use Python 3.12 (recommended), 3.11, or 3.13. Windows offline bundle requires Python 3.12 x64.')
    os.chdir(ROOT)
    folder = ROOT / '.venv'
    python = folder / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.exists():
        print('Creating your local Python environment...', flush=True)
        venv.EnvBuilder(with_pip=True).create(folder)
    required = ROOT / 'requirements-dev.txt'
    signature = hashlib.sha256((ROOT / 'requirements.txt').read_bytes() + required.read_bytes()).hexdigest()
    marker = folder / '.tracepilot-dependencies'
    if not marker.exists() or marker.read_text().strip() != signature:
        wheels = ROOT / 'vendor' / 'windows-py312'
        offline = os.name == 'nt' and sys.version_info[:2] == (3, 12) and platform.machine().lower() in {'amd64', 'x86_64'} and wheels.exists()
        cmd = [str(python), '-m', 'pip', 'install', '--disable-pip-version-check']
        if offline:
            print('Installing the pinned Windows packages from the ZIP (no internet needed)...', flush=True)
            cmd += ['--no-index', '--find-links', str(wheels)]
        else:
            print('Installing the pinned package versions. Internet is needed on this platform for first setup.', flush=True)
        subprocess.run(cmd + ['-r', str(required)], check=True)
        subprocess.run([str(python), '-m', 'pip', 'check'], check=True)
        marker.write_text(signature, encoding='utf-8')
    args = sys.argv[1:]
    if '--verify' in args:
        return subprocess.call([str(python), '-m', 'scripts.verify_demo'])
    if '--test' in args:
        return subprocess.call([str(python), '-m', 'pytest', '-q'])
    return subprocess.call([str(python), str(ROOT / 'launcher.py'), *args])


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, subprocess.CalledProcessError) as exc:
        print(f'\nSetup could not finish: {exc}\nCheck Python 3.12 x64 and extract the entire ZIP before launching.', file=sys.stderr)
        raise SystemExit(1)
