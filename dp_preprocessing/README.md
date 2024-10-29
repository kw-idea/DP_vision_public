# base 전처리 작업
tiff 가상환경으로 작동 

## Tiff파일을 PNG 파일로 변환
tiff2png.py 
origin이라는 폴더내 55656(번호폴더) 폴더 단위로 적용
RESIZE_SCALE 변수로 해상도 조절



## withoutbackground PNG 파일의 배경 및 파티클 제거
이것도 폴더 안의 폴더들 전부 적용하는 코드
min_area 변수로 contour의 최소면적 조절, 이 변수로 파티클 또는 불필요한 면적 제거