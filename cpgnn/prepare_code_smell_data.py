"""
Script to prepare code smell labels from folder structure:
- smell/ folder contains files with code smells
- non-smell/ folder contains files without code smells
"""

import os
import csv
import argparse
from pathlib import Path

def get_java_files(folder_path):
    """Get all Java files from a folder recursively"""
    java_files = []
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.java'):
                full_path = os.path.join(root, file)
                java_files.append(full_path)
    return java_files

def create_code_smell_labels_from_folders(input_folder, output_csv="code_smell_labels.csv"):
    """
    Create code smell labels from folder structure
    
    Args:
        input_folder: Path to folder containing 'smell' and 'non-smell' subfolders
        output_csv: Output CSV file path
    """
    input_path = Path(input_folder)
    smell_folder = input_path / "smell"
    non_smell_folder = input_path / "non-smell"
    
    # Check if folders exist
    if not smell_folder.exists():
        print(f"Error: {smell_folder} folder not found!")
        return False
        
    if not non_smell_folder.exists():
        print(f"Error: {non_smell_folder} folder not found!")
        return False
    
    print(f"Processing smell folder: {smell_folder}")
    print(f"Processing non-smell folder: {non_smell_folder}")
    
    # Get all Java files
    smell_files = get_java_files(smell_folder)
    non_smell_files = get_java_files(non_smell_folder)
    
    print(f"Found {len(smell_files)} files with code smells")
    print(f"Found {len(non_smell_files)} files without code smells")
    
    # Create labels CSV
    with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['file_path', 'file_name', 'has_smell', 'function_id']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        function_id = 0
        
        # Process smell files (label = 1)
        for file_path in smell_files:
            file_name = os.path.basename(file_path)
            relative_path = os.path.relpath(file_path, input_folder)
            
            writer.writerow({
                'file_path': relative_path,
                'file_name': file_name,
                'has_smell': 1,
                'function_id': function_id
            })
            function_id += 1
        
        # Process non-smell files (label = 0)
        for file_path in non_smell_files:
            file_name = os.path.basename(file_path)
            relative_path = os.path.relpath(file_path, input_folder)
            
            writer.writerow({
                'file_path': relative_path,
                'file_name': file_name,
                'has_smell': 0,
                'function_id': function_id
            })
            function_id += 1
    
    print(f"\nCreated labels file: {output_csv}")
    print(f"Total files processed: {len(smell_files) + len(non_smell_files)}")
    print(f"Smell files: {len(smell_files)} (label=1)")
    print(f"Non-smell files: {len(non_smell_files)} (label=0)")
    
    # Show balance
    total_files = len(smell_files) + len(non_smell_files)
    if total_files > 0:
        smell_ratio = len(smell_files) / total_files
        print(f"Dataset balance: {smell_ratio:.2%} smell, {1-smell_ratio:.2%} non-smell")
        
        if smell_ratio < 0.3 or smell_ratio > 0.7:
            print("⚠️  Warning: Dataset is imbalanced. Consider data augmentation or class weighting.")
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Prepare code smell labels from folder structure')
    parser.add_argument('--input_folder', type=str, required=True,
                      help='Path to folder containing smell/ and non-smell/ subfolders')
    parser.add_argument('--output_csv', type=str, default='code_smell_labels.csv',
                      help='Output CSV file for labels')
    
    args = parser.parse_args()
    
    print("Code Smell Data Preparation")
    print("=" * 40)
    
    # Create labels from folder structure
    success = create_code_smell_labels_from_folders(args.input_folder, args.output_csv)
    
    if success:
        print("\n✓ Data preparation completed!")
        print(f"Next step: Run the training pipeline with your prepared data.")
    else:
        print("\n✗ Data preparation failed!")

if __name__ == "__main__":
    main()
