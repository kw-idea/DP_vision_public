import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 읽기
image = cv2.imread('img.png')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# R, G, B 범위 지정 (예시 값, 수동으로 변경할 부분)
lower_r, upper_r = 205, 240
lower_g, upper_g = 165, 190
lower_b, upper_b = 220, 235

# 범위 내에 있는 픽셀을 찾기 위한 마스크 생성
mask_r = (image_rgb[:, :, 0] >= lower_r) & (image_rgb[:, :, 0] <= upper_r)
mask_g = (image_rgb[:, :, 1] >= lower_g) & (image_rgb[:, :, 1] <= upper_g)
mask_b = (image_rgb[:, :, 2] >= lower_b) & (image_rgb[:, :, 2] <= upper_b)

# R, G, B 모든 범위에 걸치는 픽셀의 위치
combined_mask = mask_r & mask_g & mask_b

# 원본 이미지를 복사하여 흰색으로 변환
output_image = image_rgb.copy()
output_image[combined_mask] = [255, 255, 255]  # 흰색으로 설정

# 결과 출력
plt.imshow(output_image)
plt.title('Image with Specified RGB Range Changed to White')
plt.axis('off')
plt.show()


image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)

# 흰색에 대한 범위 정의 (예: RGB에서 (255, 255, 255))
lower_white = np.array([200, 200, 200], dtype=np.uint8)
upper_white = np.array([255, 255, 255], dtype=np.uint8)

# 흰색 영역 마스크 생성
mask = cv2.inRange(image_rgb, lower_white, upper_white)
non_white_mask = cv2.bitwise_not(mask)

# 마스크가 적용된 이미지에 대한 히스토그램 계산
colors = ('r', 'g', 'b')
for i, color in enumerate(colors):
    histogram = cv2.calcHist([image_rgb], [i], non_white_mask, [256], [0, 256])
    plt.plot(histogram, color=color)

plt.title('Color Histogram (Excluding White Areas)')
plt.xlabel('Pixel Intensity')
plt.ylabel('Frequency')
plt.xlim([0, 256])
plt.show()