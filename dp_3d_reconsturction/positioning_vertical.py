import pandas as pd

def normalize_contours_with_z(csv_input, csv_output, z_interval):
    df = pd.read_csv(csv_input)

    normalized_data = []
    current_z = 500  # z 축 시작 값

    for index, row in df.iterrows():
        filename = row['Filename']
        contours = eval(row['Contours'])
        avg_centroid = eval(row['Average_Centroid'])

        # 중심을 (0,0)으로 정규화하고 z 값을 추가
        normalized_contours = [[x - avg_centroid[0], y - avg_centroid[1], current_z] for x, y in contours]

        #결과 리스트에 추가
        normalized_data.append([filename, normalized_contours, [0, 0, current_z]])

        # z 값 생성
        current_z -= z_interval

    normalized_df = pd.DataFrame(normalized_data, columns=['Filename', 'Contours', 'Average_Centroid'])

    normalized_df.to_csv(csv_output, index=False)

csv_input_path = 'csv/contours_centroids.csv'  # 기존 CSV 파일
csv_output_path = 'normalized_contours_centroids_with_z.csv'  # 결과를 저장할 CSV 파일 경로
z_interval = 100  # 각 이미지마다 z 값의 간격을 설정

normalize_contours_with_z(csv_input_path, csv_output_path, z_interval)
