# ImageProcessing3

名刺をスキャンし、テキストファイルに出力するコードを以下に示す。

```
import cv2
import numpy as np

#conding: utf-8

from IPython.display import display, Image


capture=cv2.VideoCapture(1) #VideoCaptureオブジェクトを取得
capture.set(3,1280)
capture.set(4,960)
capture.set(5,15)　#取得した画像を表示するフレームの大きさを設定

while(True):
	ret, img = capture.read()　#カメラから1コマのデータを取得

	cv2.imshow("frame", img)　#OSのフレーム（ウィンド）に画像を表示
	k=cv2.waitKey(1)	
	if k==27:　#Escキーをタイプするとループを抜ける
		cv2.imwrite('image.jpg',img)　#指定した画像(img)を名前を付けて保存
		break

capture.release()　#キャプチャをリリース
cv2.destroyAllWindows()　#ウィンドウをすべて閉じる

cv2.imshow("image1",img)　#キャプチャした画像を表示
cv2.waitKey(0)　#キーを押したら終了
cv2.destroyAllWindows()

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)　#画像をグレースケールに変換

ret,th1 = cv2.threshold(gray,200,255,cv2.THRESH_BINARY)　#グレースケール画像を大津の手法を使って２値化

image, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)　#輪郭抽出を行う,
（返り値contoursは輪郭の本数）

areas = []
for cnt in contours:　#輪郭の数だけ実行
    area = cv2.contourArea(cnt)　#輪郭が囲む領域の面積を求める
    if area > 10000:　#領域の面積が10000以上だと、
        epsilon = 0.1*cv2.arcLength(cnt,True)　#輪郭線の周囲長
        approx = cv2.approxPolyDP(cnt,epsilon,True)　#折れ線カーブを指定された精度(epsilon)で近似
        areas.append(approx)　#オブジェクトをリストareaの最後に追加



cv2.drawContours(img,areas,-1,(0,255,0),3)　#検出した輪郭を描画

cv2.imshow("image2",img)　#輪郭を描画した画像を表示
cv2.waitKey(0)
cv2.destroyAllWindows()

img = cv2.imread('image.jpg')　#最初の取得した画像を読みだす

dst = []

pts1 = np.float32(areas[0])
pts2 = np.float32([[600,300],[600,0],[0,0],[0,300]])

M = cv2.getPerspectiveTransform(pts1,pts2)　#４点の対応点から投資返還を求める
dst = cv2.warpPerspective(img,M,(600,300))　#画像の透視変換を行う

cv2.imshow("image3",dst)　#透視変換を行った画像を表示
cv2.waitKey(0)
cv2.destroyAllWindows()

cv2.imshow("dst",dst) #正しい向きに直した画像を表示
cv2.waitKey(0)
cv2.destroyAllWindows()


import pyocr
from PIL import Image
tools = pyocr.get_available_tools() 

if len(tools) == 0: #もし文字が抽出できなければエラーを表示しexitする
      print("No OCR tool found")
      sys.exit(1)
tool = tools[0]　#

txt = tool.image_to_string(Image.fromarray(dst), lang="eng")　#入力画像から文字データを抽出して英語として判別する

print(txt)
file = open('test.txt', 'w') #テキストファイルを書き込み権限でひらく
file.write(txt)	#抽出した文字をテキストファイルに書き込む
file.close() 

```


cv2.findContours:引数は入力画像、抽出モード、近似手法<br>
cv2.contourArea:引数は画像のある部分の領域<br>
cv2.drawContours:引数は入力画像、Pythonのlistとして保存されている輪郭、描画したい輪郭のインデックス、輪郭を描画する色や線の太さを指定<br>

実際の様子:https://youtu.be/4yP7nuXnQ38<br>
参考サイト:<br>
http://programming-study.com/technology/python-file/<br>
https://qiita.com/mix_dvd/items/5674f26af467098842f0


