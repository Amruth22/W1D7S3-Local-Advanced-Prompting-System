#!/usr/bin/env python3
"""
Setup Script for Swagger UI Integration
This script helps integrate Swagger UI into the existing Flask application
"""

import os
import shutil
from pathlib import Path

def backup_original_app():
    """Backup the original app.py file"""
    if os.path.exists('app.py') and not os.path.exists('app_original.py'):
        shutil.copy2('app.py', 'app_original.py')
        print("✅ Original app.py backed up as app_original.py")
    else:
        print("ℹ️  Backup already exists or no original app.py found")

def setup_swagger_app():
    """Replace app.py with Swagger-enabled version"""
    if os.path.exists('app_with_swagger.py'):
        # Backup original
        backup_original_app()
        
        # Replace with Swagger version
        shutil.copy2('app_with_swagger.py', 'app.py')
        print("✅ app.py updated with Swagger UI integration")
        return True
    else:
        print("❌ app_with_swagger.py not found")
        return False

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        'flask-restx',
        'flasgger'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package} is installed")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} is missing")
    
    if missing_packages:
        print(f"\n📦 Install missing packages:")
        print(f"pip install {' '.join(missing_packages)}")
        return False
    
    return True

def create_swagger_endpoints():
    """Display information about Swagger endpoints"""
    print("\n🚀 SWAGGER UI ENDPOINTS:")
    print("=" * 50)
    print("📊 Swagger UI Documentation: http://localhost:5000/api/v1/docs/")
    print("📋 API Info: http://localhost:5000/api/info")
    print("❤️  Health Check: http://localhost:5000/api/health")
    print("🏠 Root: http://localhost:5000/")
    print("=" * 50)

def main():
    """Main setup function"""
    print("🔧 SWAGGER UI SETUP FOR LOCAL ADVANCED PROMPTING SYSTEM")
    print("=" * 60)
    
    # Check dependencies
    print("\n1️⃣ Checking Dependencies...")
    if not check_dependencies():
        print("\n⚠️  Please install missing dependencies first!")
        return False
    
    # Setup Swagger app
    print("\n2️⃣ Setting up Swagger Integration...")
    if not setup_swagger_app():
        print("\n❌ Failed to setup Swagger integration")
        return False
    
    # Show endpoints
    print("\n3️⃣ Swagger UI Ready!")
    create_swagger_endpoints()
    
    print("\n🎉 SETUP COMPLETE!")
    print("\nTo start the server with Swagger UI:")
    print("python app.py")
    print("\nThen visit: http://localhost:5000/api/v1/docs/")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⏹️  Setup interrupted by user")
        exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        exit(1)