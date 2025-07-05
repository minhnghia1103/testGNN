# PowerShell script to run code smell detection training

Write-Host "Starting Code Smell Detection Training with Tailor" -ForegroundColor Green

# Get data folder path from user
$dataFolder = Read-Host "Enter path to your data folder (containing smell/ and non-smell/ subfolders), or press Enter to use demo data"

# Step 1: Extract features using driver.py
Write-Host "Step 1: Extracting features from Java code..." -ForegroundColor Yellow
Set-Location "..\cpg"

if ([string]::IsNullOrWhiteSpace($dataFolder)) {
    Write-Host "Using demo data from bigclonebench..." -ForegroundColor Yellow
    python driver.py `
        --lang java `
        --task code_smell `
        --src_path "..\..\bigclonebench" `
        --encoding `
        --encode_path "..\datasets\code_smell_encoding" `
        --store_iresult `
        --iresult_path "..\datasets\code_smell_inter_results"
} else {
    Write-Host "Using your data from: $dataFolder" -ForegroundColor Yellow
    python driver.py `
        --lang java `
        --task code_smell `
        --src_path "$dataFolder" `
        --encoding `
        --encode_path "..\datasets\code_smell_encoding" `
        --store_iresult `
        --iresult_path "..\datasets\code_smell_inter_results"
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Feature extraction failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Feature extraction completed successfully!" -ForegroundColor Green

# Step 2: Prepare code smell labels
Write-Host "Step 2: Preparing code smell labels..." -ForegroundColor Yellow
Set-Location "..\cpgnn"

if ([string]::IsNullOrWhiteSpace($dataFolder)) {
    Write-Host "Using demo data generation..." -ForegroundColor Yellow
    python prepare_code_smell_data.py --input_folder "..\..\bigclonebench" --output_csv "code_smell_labels.csv"
} else {
    Write-Host "Using your organized data from: $dataFolder" -ForegroundColor Yellow
    python prepare_code_smell_data.py --input_folder "$dataFolder" --output_csv "code_smell_labels.csv"
}

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Code smell data preparation failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Code smell data preparation completed!" -ForegroundColor Green

# Step 3: Train the model
Write-Host "Step 3: Training code smell detection model..." -ForegroundColor Yellow

python main_code_smell.py `
    --dataset code_smell_encoding `
    --smell_test_supervised `
    --epoch 50 `
    --lr 0.01 `
    --batch_size_smell 64 `
    --smell_threshold 0.5 `
    --save_model

if ($LASTEXITCODE -ne 0) {
    Write-Host "Error: Model training failed!" -ForegroundColor Red
    exit 1
}

Write-Host "Code smell detection training completed successfully!" -ForegroundColor Green
Write-Host "Model saved for future use." -ForegroundColor Green
