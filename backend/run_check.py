import os
import sys

# Add the backend directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from database.core import check_db_connection

if __name__ == "__main__":
    check_db_connection()
