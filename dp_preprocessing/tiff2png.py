import os
import cv2
import numpy as np
from osgeo import gdal
from tqdm import tqdm
import multiprocessing
import subprocess

#tiff를 png로 변환하는 파일 tiff 가상환경 사용

def get_image_file_list(img_path):
    return [
        node_name
        for node_name in os.listdir(img_path)
        if os.path.isfile(os.path.join(img_path, node_name))
    ]


def remove_background(img_np):
    img_copy = img_np.copy()
    
    # 백그라운드 색상 범위 설정
    lower_bound = np.array([232, 232, 232], dtype=np.uint8)
    upper_bound = np.array([255, 255, 255], dtype=np.uint8)
    
    # 마스크 생성
    mask = cv2.inRange(img_copy, lower_bound, upper_bound)
    
    # 마스크를 사용하여 백그라운드 제거
    img_copy[mask != 0] = [0, 0, 0]
    
    return img_copy


def process_image(config):
    img_full_path = config["img_full_path"]
    resize_scale = config["resize_scale"]

    # resize image
    print(f"[Resizing] {img_full_path}")

    img_resized_full_path = img_full_path.replace("origin", f"temp_{resize_scale}")
    img_resized_full_path = img_resized_full_path.replace(".tiff", ".png")
    

    translate_options = gdal.TranslateOptions(
        format="GTiff",
        widthPct=100 / resize_scale,
        heightPct=100 / resize_scale,
    )
    gdal.Translate(
        destName=img_resized_full_path,
        srcDS=img_full_path,
        options=translate_options,
    )

    # postprocessing
    print(f"[Postprocessing] {img_resized_full_path}")
    
    img_resized = gdal.Open(img_resized_full_path)

    red = img_resized.GetRasterBand(3).ReadAsArray()
    green = img_resized.GetRasterBand(2).ReadAsArray()
    blue = img_resized.GetRasterBand(1).ReadAsArray()

    img_np = np.dstack((red, green, blue))

    img_clean_bg = remove_background(img_np)

    output_full_path = img_full_path.replace("origin", f"resize_{resize_scale}")
    output_full_path = output_full_path.replace(".tiff", ".png")
    cv2.imwrite(output_full_path, img_clean_bg)
    print(f"[remove background] {output_full_path}")


if __name__ == "__main__":
    # IMG_PATH = "data/origin/67021/"
    # IMG_TEMP_PATH = "data/temp_20/67021/"
    # IMG_RESIZE_PATH = "data/resize_20/67021/"
    
    # origin폴더 안에 폴더들 전부 변경
    # temp 배경제거 전, resize 배경제거 
    IMG_DIR = 'D:/Asan_data_set/origin/'
    ALL_IMG_PATH = os.listdir(IMG_DIR)
    print(ALL_IMG_PATH)
    for IMG_PATH in ALL_IMG_PATH:
        IMG_PATH = IMG_DIR + IMG_PATH + '/'
        RESIZE_SCALE = 50
        
        
        os.makedirs(IMG_PATH.replace("origin", f"temp_{RESIZE_SCALE}"), exist_ok=True)
        os.makedirs(IMG_PATH.replace("origin", f"resize_{RESIZE_SCALE}"), exist_ok=True)
        #subprocess.run(f"mkdir -p '{IMG_PATH.replace('origin', f'temp_{RESIZE_SCALE}')}'", shell=True)
        print(f"mkdir -p '{IMG_PATH.replace('origin', f'temp_{RESIZE_SCALE}')}'")
        #subprocess.run(f"mkdir -p '{IMG_PATH.replace('origin', f'resize_{RESIZE_SCALE}')}'", shell=True)
        print(f"mkdir -p '{IMG_PATH.replace('origin', f'resize_{RESIZE_SCALE}')}'")
        img_file_list = get_image_file_list(IMG_PATH)
        # print(img_file_list)

        img_full_path_list = [
            os.path.join(IMG_PATH, img_file) for img_file in img_file_list
        ]
        configure = [
            {"img_full_path": img_full_path, "resize_scale": RESIZE_SCALE}
            for img_full_path in img_full_path_list
        ]
        with multiprocessing.Pool() as pool:
            pool.map(
                process_image,
                configure,
            )

        # for img_file in (pbar := tqdm(img_file_list)):
        #     img_full_path = os.path.join(IMG_PATH, img_file)
        #     process_images(img_full_path)