import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

# 투명한 PNG 이미지 읽기 (4채널: RGBA)
image = cv2.imread('68201/68201_23.png', cv2.IMREAD_UNCHANGED)


# 알파 채널 분리
if image.shape[2] == 4:
    # 채널 분할
    b_channel, g_channel, r_channel, alpha_channel = cv2.split(image)
    # 알파 채널이 0인 부분을 흰색으로 설정
    white_background = np.ones_like(alpha_channel) * 255
    r_channel = np.where(alpha_channel == 0, white_background, r_channel)
    g_channel = np.where(alpha_channel == 0, white_background, g_channel)
    b_channel = np.where(alpha_channel == 0, white_background, b_channel)
    # RGB 이미지 재구성
    image_rgb = cv2.merge((r_channel, g_channel, b_channel))
else:
    # 이미 RGB 이미지일 경우
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# 원본 이미지의 복사본 생성
output_image = image_rgb.copy()
image_rgb = cv2.cvtColor(output_image, cv2.COLOR_BGR2RGB)

# 이미지 출력 초기 설정
fig, ax = plt.subplots(figsize=(10,8))
plt.subplots_adjust(left=0.1, bottom=0.4)
image_display = plt.imshow(output_image)
plt.axis('off')

# 슬라이더 위치 설정
ax_r_low_1 = plt.axes([0.1, 0.18, 0.65, 0.02], facecolor='lightgray')
ax_r_high_1 = plt.axes([0.1, 0.15, 0.65, 0.02], facecolor='lightgray')
ax_g_low_1 = plt.axes([0.1, 0.12, 0.65, 0.02], facecolor='lightgray')
ax_g_high_1 = plt.axes([0.1, 0.09, 0.65, 0.02], facecolor='lightgray')
ax_b_low_1 = plt.axes([0.1, 0.06, 0.65, 0.02], facecolor='lightgray')
ax_b_high_1 = plt.axes([0.1, 0.03, 0.65, 0.02], facecolor='lightgray')

ax_r_low_2 = plt.axes([0.1, 0.4, 0.65, 0.02], facecolor='lightgray')
ax_r_high_2 = plt.axes([0.1, 0.37, 0.65, 0.02], facecolor='lightgray')
ax_g_low_2 = plt.axes([0.1, 0.34, 0.65, 0.02], facecolor='lightgray')
ax_g_high_2 = plt.axes([0.1, 0.31, 0.65, 0.02], facecolor='lightgray')
ax_b_low_2 = plt.axes([0.1, 0.28, 0.65, 0.02], facecolor='lightgray')
ax_b_high_2 = plt.axes([0.1, 0.25, 0.65, 0.02], facecolor='lightgray')

# 버튼 위치 설정
ax_button = plt.axes([0.8, 0.05, 0.1, 0.075])
button = Button(ax_button, 'Show Histogram')

# 슬라이더 설정 (범위: 0-255)
s_r_low_1 = Slider(ax_r_low_1, '1R Low', 0, 255, valinit=200, valstep=1)
s_r_high_1 = Slider(ax_r_high_1, '1R High', 0, 255, valinit=240, valstep=1)
s_g_low_1 = Slider(ax_g_low_1, '1G Low', 0, 255, valinit=150, valstep=1)
s_g_high_1 = Slider(ax_g_high_1, '1G High', 0, 255, valinit=255, valstep=1)
s_b_low_1 = Slider(ax_b_low_1, '1B Low', 0, 255, valinit=200, valstep=1)
s_b_high_1 = Slider(ax_b_high_1, '1B High', 0, 255, valinit=240, valstep=1)

s_r_low_2 = Slider(ax_r_low_2, '2R Low', 0, 255, valinit=200, valstep=1)
s_r_high_2 = Slider(ax_r_high_2, '2R High', 0, 255, valinit=240, valstep=1)
s_g_low_2 = Slider(ax_g_low_2, '2G Low', 0, 255, valinit=150, valstep=1)
s_g_high_2 = Slider(ax_g_high_2, '2G High', 0, 255, valinit=255, valstep=1)
s_b_low_2 = Slider(ax_b_low_2, '2B Low', 0, 255, valinit=200, valstep=1)
s_b_high_2 = Slider(ax_b_high_2, '2B High', 0, 255, valinit=240, valstep=1)

# 슬라이더 값 변경 시 호출되는 함수 정의
def update(val):
    # 슬라이더에서 범위 값 읽기
    lower_r_1, upper_r_1 = s_r_low_1.val, s_r_high_1.val
    lower_g_1, upper_g_1 = s_g_low_1.val, s_g_high_1.val
    lower_b_1, upper_b_1 = s_b_low_1.val, s_b_high_1.val

    lower_r_2, upper_r_2 = s_r_low_2.val, s_r_high_2.val
    lower_g_2, upper_g_2 = s_g_low_2.val, s_g_high_2.val
    lower_b_2, upper_b_2 = s_b_low_2.val, s_b_high_2.val
    

    # 범위에 해당하는 마스크 생성
    mask_r_1 = (image_rgb[:, :, 0] >= lower_r_1) & (image_rgb[:, :, 0] <= upper_r_1)
    mask_g_1 = (image_rgb[:, :, 1] >= lower_g_1) & (image_rgb[:, :, 1] <= upper_g_1)
    mask_b_1 = (image_rgb[:, :, 2] >= lower_b_1) & (image_rgb[:, :, 2] <= upper_b_1)

    mask_r_2 = (image_rgb[:, :, 0] >= lower_r_2) & (image_rgb[:, :, 0] <= upper_r_2)
    mask_g_2 = (image_rgb[:, :, 1] >= lower_g_2) & (image_rgb[:, :, 1] <= upper_g_2)
    mask_b_2 = (image_rgb[:, :, 2] >= lower_b_2) & (image_rgb[:, :, 2] <= upper_b_2)

    combined_mask = (mask_r_1 & mask_g_1 & mask_b_1) | (mask_r_2 & mask_g_2 & mask_b_2)


    # 원본 이미지의 복사본에 흰색으로 변경
    modified_image = image_rgb.copy()
    modified_image[combined_mask] = [255, 255, 255]


    # 이미지 업데이트
    image_display.set_data(modified_image)
    fig.canvas.draw_idle()


# 버튼 클릭 시 마스킹된 이미지 히스토그램을 표시하는 함수 정의
def show_masked_histogram(event):

    # 슬라이더에서 범위 값 읽기
    lower_r_1, upper_r_1 = s_r_low_1.val, s_r_high_1.val
    lower_g_1, upper_g_1 = s_g_low_1.val, s_g_high_1.val
    lower_b_1, upper_b_1 = s_b_low_1.val, s_b_high_1.val

    lower_r_2, upper_r_2 = s_r_low_2.val, s_r_high_2.val
    lower_g_2, upper_g_2 = s_g_low_2.val, s_g_high_2.val
    lower_b_2, upper_b_2 = s_b_low_2.val, s_b_high_2.val
    
    # 범위에 해당하는 마스크 생성
    mask_r_1 = (image_rgb[:, :, 0] >= lower_r_1) & (image_rgb[:, :, 0] <= upper_r_1)
    mask_g_1 = (image_rgb[:, :, 1] >= lower_g_1) & (image_rgb[:, :, 1] <= upper_g_1)
    mask_b_1 = (image_rgb[:, :, 2] >= lower_b_1) & (image_rgb[:, :, 2] <= upper_b_1)

    mask_r_2 = (image_rgb[:, :, 0] >= lower_r_2) & (image_rgb[:, :, 0] <= upper_r_2)
    mask_g_2 = (image_rgb[:, :, 1] >= lower_g_2) & (image_rgb[:, :, 1] <= upper_g_2)
    mask_b_2 = (image_rgb[:, :, 2] >= lower_b_2) & (image_rgb[:, :, 2] <= upper_b_2)

    combined_mask = (mask_r_1 & mask_g_1 & mask_b_1) | (mask_r_2 & mask_g_2 & mask_b_2)

    output_image[combined_mask] = [255, 255, 255]
    

    # 흰색에 대한 범위 정의 (예: RGB에서 (255, 255, 255))
    lower_white = np.array([200, 200, 200], dtype=np.uint8)
    upper_white = np.array([255, 255, 255], dtype=np.uint8)

    mask = cv2.inRange(image_rgb, lower_white, upper_white)
    non_white_mask = cv2.bitwise_not(mask)

    # 마스킹된 이미지에서 히스토그램 계산
    #masked_image = image_rgb[combined_mask]

    plt.figure("Masked RGB Histogram", figsize=(10,8))
    colors = ('r', 'g', 'b')
    for i, color in enumerate(colors):
        histogram = cv2.calcHist([image_rgb], [i], non_white_mask, [256], [0, 256])
        plt.plot(histogram, color=color)
        
    plt.title('Masked Color Histogram')
    plt.xlabel('Pixel Intensity')
    plt.ylabel('Frequency')
    plt.xlim([0, 256])
    plt.show()

# 슬라이더 이벤트에 업데이트 함수 연결
s_r_low_1.on_changed(update)
s_r_high_1.on_changed(update)
s_g_low_1.on_changed(update)
s_g_high_1.on_changed(update)
s_b_low_1.on_changed(update)
s_b_high_1.on_changed(update)

s_r_low_2.on_changed(update)
s_r_high_2.on_changed(update)
s_g_low_2.on_changed(update)
s_g_high_2.on_changed(update)
s_b_low_2.on_changed(update)
s_b_high_2.on_changed(update)

button.on_clicked(show_masked_histogram)

plt.show() 
