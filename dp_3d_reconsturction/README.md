# 3D 랜더링을 위한 폴더
rend 가상환경 사용

### prostate 구조
base : horizon    
body : vertical    
Apex : horizon

## contour 파일
구조에 맞는 파일
폴더 위치 확인
min_area 변수로 최소면적 설정
Region 칼럼으로 조직 구분(이미지에서 중심점의 x 좌표기준으로 정렬)
폴더 내 여러 horizon이미지를 한번에 csv와 각 이미지 내 조직의 중심점과 외곽선이 찍힌 이미지 저장

## positioning
3차원 공간에 위치를 잡는 코드

### vertical
vertical 경우 중심을 0,0 설정
z축 시작값과 간격은 변수를 통해 설정 가능(base와 Apex를 잘 구분, 실제로 base가 위 Apex가 아래)

### horizon
horizon 경우 실제로 세워져 있던 것을 눕힌 케이스
때문에 축 변환을 해줘야함 (코드 오류 이슈)
z축 경우 vertical에서 설정했던 값을 가져왔음


## rendering
3덩어리를 만들기 위해 horizon data에서 apex와 base를 나눔
파일 위치만 맞춰주면 작동