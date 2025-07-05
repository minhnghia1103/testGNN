# Code Smell Detection với Tailor

## Tổng quan
Đã chuyển đổi project Tailor từ bài toán phát hiện code clone sang bài toán phân loại code smell và không smell.

## Các thay đổi chính

### 1. Files đã thêm/sửa đổi:
- `cpgnn/main_code_smell.py`: File chính để training code smell detection
- `cpgnn/prepare_code_smell_data.py`: Script chuẩn bị dữ liệu labels
- `cpgnn/util/setting.py`: Thêm parameters cho code smell detection
- `cpgnn/model/load_gnn.py`: Thêm methods xử lý dữ liệu code smell
- `cpgnn/model/SGL.py`: Thêm model architecture cho binary classification
- `cpgnn/model/eval.py`: Thêm functions đánh giá code smell detection
- `run_code_smell_training.ps1`: Script PowerShell để chạy toàn bộ pipeline

### 2. Thay đổi architecture:
- Chuyển từ similarity learning (clone detection) sang binary classification
- Model output: 2 classes (smell vs no-smell)
- Loss function: Cross-entropy loss thay vì cosine similarity loss

## Hướng dẫn chạy

### Bước 1: Chuẩn bị môi trường
```powershell
# Cài đặt dependencies (nếu chưa có)
pip install tensorflow==1.14
pip install scikit-learn
pip install numpy
pip install scipy
```

### Bước 2: Validate dữ liệu của bạn (Tùy chọn)
```powershell
cd cpgnn
python validate_data.py "đường_dẫn_đến_thư_mục_data"
```

Ví dụ:
```powershell
python validate_data.py "C:\data\my_code_smell_dataset"
```

### Bước 3: Chạy toàn bộ pipeline

#### Cách 1: Script tự động (Khuyến nghị)
```powershell
# Chạy script PowerShell - sẽ hỏi đường dẫn đến data
.\run_code_smell_training.ps1
```

#### Cách 2: Chạy từng bước thủ công

**Bước 3a: Chuẩn bị labels**
```powershell
cd cpgnn
python prepare_code_smell_data.py --input_folder "C:\path\to\your\data" --output_csv "code_smell_labels.csv"
```

**Bước 3b: Trích xuất features**
```powershell
cd ..\cpg
python driver.py --lang java --src_path "C:\path\to\your\data" --encoding --encode_path "..\datasets\code_smell_encoding" --store_iresult --iresult_path "..\datasets\code_smell_inter_results"
```

**Bước 3c: Training model**
```powershell
cd ..\cpgnn
python main_code_smell.py --dataset code_smell_encoding --smell_test_supervised --epoch 50 --lr 0.01 --batch_size_smell 64 --smell_threshold 0.5 --save_model
```

### Bước 2: Chuẩn bị dữ liệu code smell labels

#### Cách 1: Từ folder structure có sẵn (Khuyến nghị cho bạn)
Nếu bạn đã có dữ liệu được phân loại trong 2 folder `smell` và `non-smell`:

```
your_data/
├── smell/          # Chứa các file Java có code smell
│   ├── file1.java
│   ├── file2.java
│   └── ...
└── non-smell/      # Chứa các file Java không có code smell
    ├── file3.java
    ├── file4.java
    └── ...
```

Chạy script để tạo labels:
```powershell
cd cpgnn
python prepare_code_smell_data.py --input_folder "đường_dẫn_đến_thư_mục_data" --output_csv "code_smell_labels.csv"
```

Ví dụ:
```powershell
python prepare_code_smell_data.py --input_folder "C:\data\my_code_smell_dataset" --output_csv "code_smell_labels.csv"
```

#### Cách 2: Sử dụng tool tự động
Sử dụng các tool phát hiện code smell như:
- **PMD**: https://pmd.github.io/
- **SpotBugs**: https://spotbugs.github.io/
- **SonarQube**: https://www.sonarqube.org/

Ví dụ với PMD:
```powershell
# Download PMD
# Chạy PMD trên code
pmd check -d "bigclonebench" -R rulesets/java/quickstart.xml -f csv -r code_smell_results.csv
```

#### Cách 3: Demo với dữ liệu mẫu
```powershell
cd cpgnn
python prepare_code_smell_data.py --input_folder "../bigclonebench" --output_csv "demo_labels.csv"
```

### Bước 3: Chạy toàn bộ pipeline
```powershell
# Chạy script PowerShell
.\run_code_smell_training.ps1
```

Hoặc chạy từng bước:

#### Bước 3a: Trích xuất features
```powershell
cd cpg
python driver.py --lang java --src_path "..\bigclonebench" --encoding --encode_path "..\datasets\code_smell_encoding" --store_iresult --iresult_path "..\datasets\code_smell_inter_results"
```

#### Bước 3b: Training model
```powershell
cd cpgnn
python main_code_smell.py --dataset code_smell_encoding --smell_test_supervised --epoch 50 --lr 0.01 --batch_size_smell 64 --smell_threshold 0.5 --save_model
```

## Parameters quan trọng

### Training parameters:
- `--epoch`: Số epochs training (default: 50)
- `--lr`: Learning rate (default: 0.01)
- `--batch_size_smell`: Batch size (default: 64)
- `--smell_threshold`: Ngưỡng phân loại (default: 0.5)

### Data parameters:
- `--smell_val_size`: Tỷ lệ validation set (default: 0.1)
- `--smell_test_size`: Tỷ lệ test set (default: 0.1)

## Kết quả đầu ra

Sau khi training xong, bạn sẽ có:
1. **Metrics**: Precision, Recall, F1-score, Accuracy, AUC
2. **Model weights**: Lưu trong `datasets/code_smell_encoding/saved_models/`
3. **Logs**: Chi tiết quá trình training

## Ví dụ output:
```
Code Smell Validation: [tp, fn, tn, fp]==[145, 23, 178, 34] [rec, pre, f1, auc]==[0.863, 0.810, 0.836, 0.891]
Code Smell Test: [tp, fn, tn, fp]==[142, 28, 175, 32] [rec, pre, f1, auc]==[0.835, 0.816, 0.825, 0.878]
```

## Tùy chỉnh cho dữ liệu thực tế

### 1. Cập nhật code smell labels:
Sửa file `cpgnn/model/load_gnn.py`, hàm `_load_code_smell_labels()` để đọc từ file labels thực tế của bạn.

### 2. Thêm loại code smell:
Nếu muốn phân loại nhiều loại code smell, thay đổi:
- `classification_num` từ 2 thành số classes cần thiết
- Cập nhật model architecture trong `_build_smell_model()`

### 3. Feature engineering:
Có thể thêm features đặc trưng cho code smell trong quá trình xử lý CPG.

## Troubleshooting

### Lỗi thường gặp:
1. **Import error**: Cài đặt đúng version dependencies
2. **Memory error**: Giảm batch_size_smell
3. **No labels file**: Chạy prepare_code_smell_data.py trước

### Performance tuning:
- Tăng epoch nếu model chưa converge
- Điều chỉnh learning rate
- Thử different thresholds cho classification

## Kết luận
Project đã được chuyển đổi thành công từ code clone detection sang code smell detection. Architecture sử dụng CPG (Code Property Graph) để học representation, sau đó áp dụng binary classification để phân loại smell/no-smell.
