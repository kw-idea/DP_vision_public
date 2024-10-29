import os
import cv2
import numpy as np

# 입력 폴더와 출력 폴더 경로 설정
input_base_folder = 'D:/Asan_data_set/resize_50'  # 입력 이미지들이 있는 폴더 경로
output_base_folder = 'image/11'  # 처리된 이미지를 저장할 폴더 경로

# 최소 면적 설정 (필요에 따라 조정)
min_area = 2000  # 객체로 인식할 최소 면적

# 모든 폴더를 순회하면서 이미지 처리
for root, dirs, files in os.walk(input_base_folder):
    for file in files:
        if file.endswith(('.png', '.jpg', '.jpeg')):  # 이미지 파일만 처리
            input_image_path = os.path.join(root, file)
            relative_folder_path = os.path.relpath(root, input_base_folder)
            output_folder_path = os.path.join(output_base_folder, relative_folder_path)

            # 출력 폴더가 없으면 생성
            if not os.path.exists(output_folder_path):
                os.makedirs(output_folder_path)

            output_image_path = os.path.join(output_folder_path, file.split('.')[0] + '.png')

            # 이미지 읽기
            image = cv2.imread(input_image_path)

            # 그레이스케일로 변환
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # 임계 처리로 이진화 (검은 배경을 제외하고 객체만 검출)
            _, thresh = cv2.threshold(gray, 10, 255, cv2.THRESH_BINARY)

            # 컨투어 찾기
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # 알파 채널을 포함한 새로운 4채널 이미지 생성 (투명한 배경으로 시작)
            result = np.zeros((image.shape[0], image.shape[1], 4), dtype=np.uint8)

            # RGB 채널에 원본 이미지 복사
            result[:, :, :3] = image

            # 알파 채널에 마스크 적용 (배경을 투명하게 만들기)
            mask = np.zeros(image.shape[:2], dtype=np.uint8)

            for contour in contours:
                if cv2.contourArea(contour) > min_area:
                    cv2.drawContours(mask, [contour], -1, 255, thickness=cv2.FILLED)

            # 알파 채널에 마스크 적용 (255는 불투명, 0은 투명)
            result[:, :, 3] = mask

            # 결과 이미지 저장 (PNG 형식으로 저장해야 투명 배경을 유지)
            cv2.imwrite(output_image_path, result)

            print(f"Image saved with transparent background at: {output_image_path}")