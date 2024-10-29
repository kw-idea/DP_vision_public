import cv2
import numpy as np
import pandas as pd
import os
# 폴더 단위로 외곽선 추출 horizon(Apex, base)

min_area  = 3000

def load_image(image_path):
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"이미지 파일을 불러올 수 없습니다: {image_path}")
    return image

def preprocess_image(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    return blurred

def threshold_image(blurred):
    _, binary = cv2.threshold(blurred, 128, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return binary

def find_contours(binary):
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours

def get_contour_centroid(contour):
    M = cv2.moments(contour)
    if M['m00'] != 0:
        cx = int(M['m10'] / M['m00'])
        cy = int(M['m01'] / M['m00'])
    else:
        cx, cy = 0, 0
    return (cx, cy)

def draw_contours_and_centroids(image, contours, centroids):
    for contour, centroid in zip(contours, centroids):
        if cv2.contourArea(contour) > min_area:  # 최소 면적 설정
            # 외곽선
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
            # 중심점
            cv2.circle(image, centroid, 5, (255, 0, 0), -1)
    return image

def process_image(image_path, min_area, debug=False): # 최소 면적 설정
    image = load_image(image_path)
    preprocessed_image = preprocess_image(image)
    binary_image = threshold_image(preprocessed_image)
    contours = find_contours(binary_image)

    # 결과를 저장할 리스트
    data = []
    centroids = []

    # 각 조직에 대한 외곽선과 중심 좌표 계산
    valid_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if debug:
            print(f"Contour area: {area}")
        if area >= min_area:
            centroid = get_contour_centroid(contour)
            valid_contours.append((contour, centroid, area))

    # 중심점의 x 좌표를 기준으로 정렬(왼쪽부터 순서대로 라벨링)
    valid_contours.sort(key=lambda x: x[1][0])

    for i, (contour, centroid, area) in enumerate(valid_contours):
        contour_coordinates = contour[:, 0, :].tolist() 
        data.append([
            f"{os.path.basename(image_path)}_region_{i+1}",
            contour_coordinates,  # 외곽선 좌표
            centroid,  # 중심 좌표
            area  # 조직의 면적
        ])
        centroids.append(centroid)

    result_image = draw_contours_and_centroids(image.copy(), [c[0] for c in valid_contours], centroids)

    return data, result_image


def process_folder(input_folder, output_csv, output_image_folder, min_area, debug=False): # 최소 면적 설정
    all_data = []

    if not os.path.exists(output_image_folder):
        os.makedirs(output_image_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp', '.gif')):
            image_path = os.path.join(input_folder, filename)
            data, result_image = process_image(image_path, min_area, debug)

            output_image_path = os.path.join(output_image_folder, f"{os.path.splitext(filename)[0]}_contours.jpg")
            cv2.imwrite(output_image_path, result_image)

            all_data.extend(data)

    df = pd.DataFrame(all_data, columns=['Region', 'Contours', 'Centroid', 'Area'])
    df.to_csv(output_csv, index=False)


# 입력 폴더 경로 및 출력 파일 경로 지정
input_folder = 'image/67021 horizon' 
output_csv_path = 'image/67021 horizon result/all_contours_and_centroids.csv'
output_folder = 'image/67021 horizon result'  # 외곽선 이미지

# 폴더 단위로 이미지 처리 및 결과 저장
process_folder(input_folder, output_csv_path, output_folder)
