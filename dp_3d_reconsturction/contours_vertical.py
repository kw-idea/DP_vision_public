import cv2
import os
import numpy as np
import pandas as pd

# 폴더에서 모든 이미지(body)를 로드
def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img_path = os.path.join(folder, filename)
        img = cv2.imread(img_path)
        if img is not None:
            images.append((filename, img))
    return images

# 이미지를 전처리
def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return blurred

def threshold_image(blurred):
    _, binary = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary

# 외곽선 추출
def find_contours(binary):
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

# 조직의 중심점
def get_contour_centroid(contour):
    M = cv2.moments(contour)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    else:
        cx, cy = 0, 0
    return (cx, cy)

# 이미지에 외곽선과 중심점 표기 및 저장
def draw_and_save_contours(image, contours, centroids, avg_centroid, output_path):

    cv2.drawContours(image, contours, -1, (0, 255, 0), 2)
    for (cx, cy) in centroids:
        cv2.circle(image, (cx, cy), 5, (255, 0, 0), -1)  # 파란 점
    #cv2.circle(image, avg_centroid, 5, (0, 0, 255), -1)  # 빨간 점
    cv2.imwrite(output_path, image)

def process_images_in_folder(folder, output_csv, output_images_folder, min_contour_area=700): # 최소 면적 설정
    data = []
    images = load_images_from_folder(folder)
    
    if not os.path.exists(output_images_folder):
        os.makedirs(output_images_folder)
    
    for filename, image in images:
        preprocessed_image = preprocess_image(image)
        binary_image = threshold_image(preprocessed_image)
        contours = find_contours(binary_image)
        
        all_contours_points = []
        centroids_x = []
        centroids_y = []
        centroids = []
        
        filtered_contours = [contour for contour in contours if cv2.contourArea(contour) >= min_contour_area]
        
        for contour in filtered_contours:
            contour_coordinates = contour[:, 0, :].tolist()  # 외곽선 좌표를 리스트로 변환
            cx, cy = get_contour_centroid(contour)
            
            all_contours_points.extend(contour_coordinates)
            centroids_x.append(cx)
            centroids_y.append(cy)
            centroids.append((cx, cy))
        
        # 외곽선 평균 계산
        if len(centroids_x) > 0 and len(centroids_y) > 0:
            avg_cx = int(sum(centroids_x) / len(centroids_x))
            avg_cy = int(sum(centroids_y) / len(centroids_y))
        else:
            avg_cx, avg_cy = 0, 0
        
        # 이미지 저장
        output_image_path = os.path.join(output_images_folder, f"contours_{filename}")
        draw_and_save_contours(image.copy(), filtered_contours, centroids, (avg_cx, avg_cy), output_image_path)
        
        data.append([filename, all_contours_points, (avg_cx, avg_cy)])
    
    df = pd.DataFrame(data, columns=['Filename', 'Contours', 'Average_Centroid'])
    df.to_csv(output_csv, index=False)

# 폴더 경로 및 출력 파일 경로 지정
folder_path = 'image/67021 slide'
output_csv_path = 'contours_centroids.csv'
output_images_folder = 'contour_images'

# 이미지 처리 및 결과 저장
process_images_in_folder(folder_path, output_csv_path, output_images_folder)