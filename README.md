# 顔LandMarkデータのBlenderへの出力


顔動画および顔写真を読み込んでその特徴点(LandMark)をBlenderにてオブジェクトとして表示させます.

スカルプト作成のときに目安として利用したりするとよいかも.


## 実行方法

video2blenderフォルダの下位にvideoというフォルダを作ってそこに任意のvideo.mp4を入れる.

1. video2img.pyを実行
1. images2npy.pyを実行
1. BlenderのPythonスクリプト実行画面を開いてnpy2blender.pyをコピペ
1. filepathを自分の環境で2番を実行したときにファイルが保存されたpathに変える
1. 3番を実行(end)

画像の場合はfacetotxt.pyのコード内のコメントアウト支持に従って実行したのちtxttoblender.pyを3,4番の流れで実行する.

https://user-images.githubusercontent.com/86472676/221435603-519b8dd9-3db5-49cb-a197-147686001a25.mp4
