#!/usr/bin/env python3
"""
Test script to validate your folder structure and create labels
"""

import os
import sys
from pathlib import Path

def validate_folder_structure(data_folder):
    """Validate that the folder structure is correct"""
    data_path = Path(data_folder)
    smell_folder = data_path / "smell"
    non_smell_folder = data_path / "non-smell"
    
    print(f"Checking folder structure in: {data_path}")
    
    # Check main folder
    if not data_path.exists():
        print(f"❌ Error: Data folder {data_path} does not exist!")
        return False
    
    # Check smell folder
    if not smell_folder.exists():
        print(f"❌ Error: 'smell' subfolder not found in {data_path}")
        print("Expected structure:")
        print("  your_data/")
        print("  ├── smell/")
        print("  └── non-smell/")
        return False
    
    # Check non-smell folder
    if not non_smell_folder.exists():
        print(f"❌ Error: 'non-smell' subfolder not found in {data_path}")
        print("Expected structure:")
        print("  your_data/")
        print("  ├── smell/")
        print("  └── non-smell/")
        return False
    
    print("✅ Folder structure is correct!")
    
    # Count Java files
    smell_files = list(smell_folder.rglob("*.java"))
    non_smell_files = list(non_smell_folder.rglob("*.java"))
    
    print(f"📊 Found {len(smell_files)} Java files with code smells")
    print(f"📊 Found {len(non_smell_files)} Java files without code smells")
    
    if len(smell_files) == 0:
        print("⚠️  Warning: No Java files found in smell/ folder")
    
    if len(non_smell_files) == 0:
        print("⚠️  Warning: No Java files found in non-smell/ folder")
    
    total_files = len(smell_files) + len(non_smell_files)
    if total_files > 0:
        smell_ratio = len(smell_files) / total_files
        print(f"📈 Dataset balance: {smell_ratio:.1%} smell, {(1-smell_ratio):.1%} non-smell")
        
        if smell_ratio < 0.2 or smell_ratio > 0.8:
            print("⚠️  Warning: Dataset is quite imbalanced")
        else:
            print("✅ Dataset balance looks reasonable")
    
    return total_files > 0

def main():
    print("Code Smell Data Validation Tool")
    print("=" * 40)
    
    if len(sys.argv) != 2:
        print("Usage: python validate_data.py <path_to_data_folder>")
        print("\nExample:")
        print("  python validate_data.py C:\\data\\my_code_smell_dataset")
        print("\nExpected folder structure:")
        print("  your_data/")
        print("  ├── smell/       # Java files with code smells")
        print("  └── non-smell/   # Java files without code smells")
        sys.exit(1)
    
    data_folder = sys.argv[1]
    
    if validate_folder_structure(data_folder):
        print("\n🎉 Your data is ready!")
        print(f"\nNext steps:")
        print(f"1. cd cpgnn")
        print(f"2. python prepare_code_smell_data.py --input_folder \"{data_folder}\" --output_csv \"code_smell_labels.csv\"")
        print(f"3. python main_code_smell.py --dataset code_smell_encoding --smell_test_supervised")
    else:
        print("\n❌ Please fix the folder structure and try again")
        sys.exit(1)

if __name__ == "__main__":
    main()
