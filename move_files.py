import os
import shutil

# 현재 디렉토리
base_dir = r"C:\Users\jk972\Desktop\새 폴더"
target_dir = os.path.join(base_dir, "데이터", "지역소멸의 원인 분석")

# 대상 디렉토리 생성
os.makedirs(target_dir, exist_ok=True)

# 이동할 파일 목록
files_to_move = [
    "01_EDA_and_Data_Preprocessing.ipynb",
    "02_Machine_Learning_Modeling.ipynb",
    "03_Data_Visualization_Dashboard.py",
    "04_Instagram_Data_Collection.py",
    "05_Instagram_Data_Analysis.py",
    "data_analysis_pipeline.py"
]

# 파일 이동
for file in files_to_move:
    source = os.path.join(base_dir, file)
    dest = os.path.join(target_dir, file)
    if os.path.exists(source):
        shutil.copy2(source, dest)
        print(f"복사됨: {file} -> {dest}")
    else:
        print(f"파일을 찾을 수 없음: {source}")

print("\n파일 이동 완료!")

