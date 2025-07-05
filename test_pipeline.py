#!/usr/bin/env python3
"""
Simple test script for code smell detection pipeline
"""

import os
import sys
import subprocess

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n{'='*50}")
    print(f"Running: {description}")
    print(f"Command: {command}")
    print(f"{'='*50}")
    
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print("✅ SUCCESS")
        if result.stdout:
            print("Output:", result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print("❌ FAILED")
        print("Error:", e.stderr)
        return False

def main():
    print("Code Smell Detection Pipeline Test")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("cpg") or not os.path.exists("cpgnn"):
        print("❌ Error: Please run this script from the Tailor root directory")
        print("Expected structure:")
        print("  Tailor/")
        print("  ├── cpg/")
        print("  ├── cpgnn/")
        print("  └── test_pipeline.py")
        sys.exit(1)
    
    # Get data folder from user
    data_folder = input("Enter path to your data folder (or press Enter for demo): ").strip()
    
    if not data_folder:
        print("Using demo mode with sample data")
        src_path = os.path.abspath("bigclonebench")
        data_folder = src_path
    else:
        src_path = os.path.abspath(data_folder)
        if not os.path.exists(src_path):
            print(f"❌ Error: Data folder {src_path} does not exist!")
            sys.exit(1)
    
    print(f"Using data from: {src_path}")
    
    # Step 1: Prepare labels
    print("\n📋 Step 1: Preparing code smell labels...")
    os.chdir("cpgnn")
    
    if not data_folder or not os.path.exists(os.path.join(data_folder, "smell")):
        print("No organized data found, creating demo labels...")
        cmd = f'python prepare_code_smell_data.py --input_folder "{src_path}" --output_csv "code_smell_labels.csv"'
    else:
        print("Found organized data structure")
        cmd = f'python prepare_code_smell_data.py --input_folder "{data_folder}" --output_csv "code_smell_labels.csv"'
    
    if not run_command(cmd, "Prepare code smell labels"):
        print("❌ Failed to prepare labels")
        sys.exit(1)
    
    # Step 2: Extract features
    print("\n🔍 Step 2: Extracting CPG features...")
    os.chdir("../cpg")
    
    cmd = f'python driver.py --lang java --task code_smell --src_path "{src_path}" --encoding --encode_path "../datasets/code_smell_encoding" --store_iresult --iresult_path "../datasets/code_smell_inter_results"'
    
    if not run_command(cmd, "Extract CPG features"):
        print("❌ Failed to extract features")
        sys.exit(1)
    
    # Step 3: Train model
    print("\n🏋️ Step 3: Training code smell detection model...")
    os.chdir("../cpgnn")
    
    cmd = 'python main_code_smell.py --dataset code_smell_encoding --smell_test_supervised --epoch 5 --lr 0.01 --batch_size_smell 32 --smell_threshold 0.5'
    
    if not run_command(cmd, "Train code smell model"):
        print("❌ Failed to train model")
        sys.exit(1)
    
    print("\n🎉 Pipeline completed successfully!")
    print("Next steps:")
    print("- Check the training results above")
    print("- Adjust hyperparameters if needed")
    print("- Use the trained model for prediction")

if __name__ == "__main__":
    main()
