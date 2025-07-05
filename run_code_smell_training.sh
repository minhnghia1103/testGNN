#!/bin/bash

# Script to run code smell detection training

echo "Starting Code Smell Detection Training with Tailor"

# Step 1: Extract features using driver.py
echo "Step 1: Extracting features from Java code..."
cd ../cpg
python driver.py \
    --lang java \
    --src_path ../../bigclonebench \
    --encoding \
    --encode_path ../datasets/code_smell_encoding \
    --store_iresult \
    --iresult_path ../datasets/code_smell_inter_results

if [ $? -ne 0 ]; then
    echo "Error: Feature extraction failed!"
    exit 1
fi

echo "Feature extraction completed successfully!"

# Step 2: Prepare code smell labels
echo "Step 2: Preparing code smell labels..."
cd ../cpgnn
python prepare_code_smell_data.py

if [ $? -ne 0 ]; then
    echo "Error: Code smell data preparation failed!"
    exit 1
fi

echo "Code smell data preparation completed!"

# Step 3: Train the model
echo "Step 3: Training code smell detection model..."
python main_code_smell.py \
    --dataset code_smell_encoding \
    --smell_test_supervised \
    --epoch 50 \
    --lr 0.01 \
    --batch_size_smell 64 \
    --smell_threshold 0.5 \
    --save_model

if [ $? -ne 0 ]; then
    echo "Error: Model training failed!"
    exit 1
fi

echo "Code smell detection training completed successfully!"
echo "Model saved for future use."
