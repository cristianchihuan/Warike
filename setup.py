#!/usr/bin/env python3
"""
Peruvian Warike Restaurant Setup Script
Helps initialize the database and test the application
"""

import requests
import time
import sys
import os

def print_banner():
    """Print the setup banner"""
    print("=" * 60)
    print("🌮  Peruvian Warike Restaurant Setup")
    print("=" * 60)
    print("Setting up your restaurant website...")
    print()

def check_dependencies():
    """Check if required packages are installed"""
    print("📦 Checking dependencies...")
    
    try:
        import flask
        import pymysql
        import werkzeug
        print("✅ All dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def test_database_connection():
    """Test database connection"""
    print("🔌 Testing database connection...")
    
    try:
        import pymysql
        
        # Default configuration
        config = {
            'host': 'localhost',
            'port': 3306,
            'user': 'root',
            'password': '',
            'database': 'peruvian_warike_db',
            'charset': 'utf8mb4',
            'cursorclass': pymysql.cursors.DictCursor
        }
        
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchone()
        cursor.close()
        conn.close()
        
        print("✅ Database connection successful")
        return True
        
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        print("\nPlease ensure:")
        print("1. MySQL server is running")
        print("2. Database 'peruvian_warike_db' exists")
        print("3. User credentials are correct in app.py")
        return False

def initialize_database():
    """Initialize the database tables"""
    print("🗄️  Initializing database...")
    
    try:
        response = requests.post('http://localhost:5000/api/init-db', timeout=10)
        if response.status_code == 200:
            print("✅ Database initialized successfully")
            return True
        else:
            print(f"❌ Database initialization failed: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not connect to Flask app: {e}")
        print("Make sure the Flask app is running on http://localhost:5000")
        return False

def test_website():
    """Test if the website is accessible"""
    print("🌐 Testing website...")
    
    try:
        response = requests.get('http://localhost:5000', timeout=10)
        if response.status_code == 200:
            print("✅ Website is accessible")
            return True
        else:
            print(f"❌ Website returned status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Could not access website: {e}")
        return False

def print_success():
    """Print success message"""
    print()
    print("🎉 Setup completed successfully!")
    print("=" * 60)
    print("Your Peruvian Warike website is ready!")
    print()
    print("🌐 Website: http://localhost:5000")
    print("📱 Mobile-friendly design")
    print("🎨 Light blue theme matching Peruvian Warike branding")
    print("🍽️  Sample menu items loaded")
    print()
    print("Next steps:")
    print("1. Customize menu items in the database")
    print("2. Update restaurant information in app.py")
    print("3. Add your own food images")
    print("4. Deploy to your hosting platform")
    print()
    print("For support, check the README.md file")
    print("=" * 60)

def print_manual_steps():
    """Print manual setup steps"""
    print()
    print("📋 Manual Setup Steps:")
    print("1. Start the Flask app: python app.py")
    print("2. Open browser to: http://localhost:5000/api/init-db")
    print("3. Visit: http://localhost:5000")
    print()

def main():
    """Main setup function"""
    print_banner()
    
    # Check dependencies
    if not check_dependencies():
        print_manual_steps()
        return
    
    # Test database connection
    if not test_database_connection():
        print_manual_steps()
        return
    
    print()
    print("🚀 Starting Flask application...")
    print("Please start the Flask app in another terminal:")
    print("python app.py")
    print()
    
    # Wait for user to start the app
    input("Press Enter after starting the Flask app...")
    
    # Initialize database
    if not initialize_database():
        print_manual_steps()
        return
    
    # Test website
    if not test_website():
        print_manual_steps()
        return
    
    print_success()

if __name__ == "__main__":
    main() 