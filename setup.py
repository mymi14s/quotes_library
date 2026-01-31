import os
import urllib.request
from setuptools import setup, find_packages
from setuptools.command.install import install
from setuptools.command.build_py import build_py

DB_URL = "https://github.com/mymi14s/quotes_library/raw/refs/heads/production/quotes_library/db.sqlite3?download="
DB_PATH = os.path.join("quotes_library", "db.sqlite3")

def download_db():
    """Download the database if it doesn't exist or is too small (LFS pointer)."""
    if os.path.exists(DB_PATH) and os.path.getsize(DB_PATH) >= 100 * 1024 * 1024:
        return

    print(f"Downloading database to {DB_PATH}... (approx 114MB)")
    try:
        urllib.request.urlretrieve(DB_URL, DB_PATH)
        print("Download complete.")
    except Exception as e:
        print(f"Warning: Failed to download database during install: {e}")
        print("The library will attempt to download it again on first use.")

class CustomInstall(install):
    def run(self):
        download_db()
        super().run()

class CustomBuildPy(build_py):
    def run(self):
        download_db()
        super().run()

setup(
    cmdclass={
        'install': CustomInstall,
        'build_py': CustomBuildPy,
    },
    package_data={
        'quotes_library': ['db.sqlite3'],
    },
)
