import cv2
import numpy as np
import matplotlib.pyplot as plt

# 이미지 읽기
image = cv2.imread('img.png')
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

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
