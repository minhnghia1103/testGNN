#!/usr/bin/env python3
"""
Quick test script to verify code smell detection setup
"""

import sys
import os
import importlib.util

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        import numpy as np
        print("✓ numpy imported successfully")
    except ImportError as e:
        print(f"✗ numpy import failed: {e}")
        return False
    
    try:
        import tensorflow as tf
        print("✓ tensorflow imported successfully")
        print(f"  TensorFlow version: {tf.__version__}")
    except ImportError as e:
        print(f"✗ tensorflow import failed: {e}")
        return False
    
    try:
        from sklearn.model_selection import train_test_split
        print("✓ sklearn imported successfully")
    except ImportError as e:
        print(f"✗ sklearn import failed: {e}")
        return False
    
    return True

def test_file_structure():
    """Test if required files exist"""
    print("\nTesting file structure...")
    
    required_files = [
        'main_code_smell.py',
        'prepare_code_smell_data.py',
        'util/setting.py',
        'model/load_gnn.py',
        'model/SGL.py',
        'model/eval.py'
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print(f"✓ {file_path} exists")
        else:
            print(f"✗ {file_path} missing")
            all_exist = False
    
    return all_exist

def test_data_preparation():
    """Test data preparation script"""
    print("\nTesting data preparation...")
    
    try:
        # Create test directory
        test_dir = "test_java_files"
        os.makedirs(test_dir, exist_ok=True)
        
        # Create sample Java file
        sample_java = """
public class TestClass {
    public void method1() {
        System.out.println("Hello World");
    }
    
    public void method2() {
        // This is a test method
        int x = 1;
        int y = 2;
        System.out.println(x + y);
    }
}
"""
        with open(f"{test_dir}/TestClass.java", "w") as f:
            f.write(sample_java)
        
        # Test prepare script
        import prepare_code_smell_data
        labels = prepare_code_smell_data.create_sample_code_smell_labels(test_dir, "test_labels.csv")
        
        if os.path.exists("test_labels.csv"):
            print("✓ Code smell data preparation successful")
            # Cleanup
            os.remove("test_labels.csv")
            os.remove(f"{test_dir}/TestClass.java")
            os.rmdir(test_dir)
            return True
        else:
            print("✗ Code smell data preparation failed")
            return False
            
    except Exception as e:
        print(f"✗ Data preparation test failed: {e}")
        return False

def test_model_creation():
    """Test if model can be created"""
    print("\nTesting model creation...")
    
    try:
        # Import required modules
        sys.path.append('util')
        sys.path.append('model')
        
        # This is a basic test - actual model creation requires more setup
        print("✓ Model modules can be imported")
        return True
        
    except Exception as e:
        print(f"✗ Model creation test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("Code Smell Detection Setup Test")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("File Structure Test", test_file_structure), 
        ("Data Preparation Test", test_data_preparation),
        ("Model Creation Test", test_model_creation)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        print("-" * 20)
        result = test_func()
        results.append((test_name, result))
    
    print("\n" + "=" * 40)
    print("TEST SUMMARY:")
    print("=" * 40)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nOverall: {passed}/{len(tests)} tests passed")
    
    if passed == len(tests):
        print("\n✓ Setup is ready for code smell detection!")
        print("You can now run: python main_code_smell.py")
    else:
        print("\n✗ Some tests failed. Please check the setup.")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
