import pandas as pd
import ast
import os

# 파일 이름에 따라 z_offset과 x_value를 설정
def get_offsets_based_on_filename(filename):
    if "67021_1_1.png_region_1" in filename:
        z_offset = 500
        x_value = -550
    elif "67021_1_1.png_region_2" in filename:
        z_offset = 500
        x_value = -450
    elif "67021_1_1.png_region_3" in filename:
        z_offset = 500
        x_value = -350
    elif "67021_1_1.png_region_4" in filename:
        z_offset = 500
        x_value = -250
    elif "67021_1_2.png_region_1" in filename:
        z_offset = 500
        x_value = -150
    elif "67021_1_2.png_region_2" in filename:
        z_offset = 500
        x_value = -50
    elif "67021_1_3.png_region_3" in filename:
        z_offset = 500
        x_value = 50
    elif "67021_1_3.png_region_1" in filename:
        z_offset = 500
        x_value = 150
    elif "67021_1_3.png_region_2" in filename:
        z_offset = 500
        x_value = 250
    elif "67021_1_4.png_region_1" in filename:
        z_offset = 500
        x_value = 350
    elif "67021_1_4.png_region_2" in filename:
        z_offset = 500
        x_value = 450
    elif "67021_1_4.png_region_3" in filename:
        z_offset = 0
        x_value = 550
    elif "67021_8_1.png_region_1" in filename:
        z_offset = 0
        x_value = 550
    elif "67021_8_1.png_region_2" in filename:
        z_offset = 500
        x_value = -450
    elif "67021_8_1.png_region_3" in filename:
        z_offset = 500
        x_value = -350
    elif "67021_8_2.png_region_1" in filename:
        z_offset = 500
        x_value = -250
    elif "67021_8_2.png_region_2" in filename:
        z_offset = 500
        x_value = -150
    elif "67021_8_2.png_region_3" in filename:
        z_offset = 500
        x_value = -50
    elif "67021_8_3.png_region_1" in filename:
        z_offset = 500
        x_value = 50
    elif "67021_8_3.png_region_2" in filename:
        z_offset = 500
        x_value = 150
    elif "67021_8_3.png_region_3" in filename:
        z_offset = 500
        x_value = 250
    elif "67021_8_4.png_region_1" in filename:
        z_offset = 500
        x_value = 350
    elif "67021_8_4.png_region_2" in filename:
        z_offset = 500
        x_value = 450
    elif "67021_8_4.png_region_3" in filename:
        z_offset = 500
        x_value = 550
    elif "67021_8_4.png_region_4" in filename:
        z_offset = 500
        x_value = 650
    else:
        z_offset = 0
        x_value = 0
    return z_offset, x_value

def transform_and_correct_contours(input_csv, output_csv):
    df = pd.read_csv(input_csv)

    transformed_data = []

    for index, row in df.iterrows():
        region = row['Region']
        filename = region.split('_region_')[0]
        contours = ast.literal_eval(row['Normalized_Contour'])

        # 파일 이름에 따라 z_offset과 x_value 설정
        z_offset, x_value = get_offsets_based_on_filename(region)

        # 좌표를 변환하고 보정
        transformed_contours = []
        for x, y in contours:
            if "67021_8_" in filename:
                z = (-x) + z_offset  
            else:
                z = x + z_offset  
            transformed_contours.append([x_value, y, z])

      
        transformed_data.append([region, transformed_contours])

    transformed_df = pd.DataFrame(transformed_data, columns=['Region', 'Contours'])

    transformed_df.to_csv(output_csv, index=False)

# 경로 지정
input_csv_path = 'normalized_contours_by_centroid.csv'
output_csv_path = 'transformed_contours.csv'  

transform_and_correct_contours(input_csv_path, output_csv_path)
