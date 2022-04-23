# CTPN_train
  CTPN是在ECCV 2016提出的一种文字检测算法。CTPN结合CNN与LSTM深度网络，能有效的检测出复杂场景的横向分布的文字。
## Reference
1. 源码：https://github.com/eragonruan/text-detection-ctpn
2. csdn: https://blog.csdn.net/sxlsxl119/article/details/102767710
3. 训练集制作: 使用yolo的Imglabel，生成xml档案，再转换成txt。

------ 
## Environment
 	```
    ubuntu18.04+cuda8+tensorflow1.4++vs2015+pycharm+anaconda
	tqdm==4.11.2
	opencv-python==3.4.0.12
	Shapely==1.6.4.post1
	matplotlib==1.5.3
	numpy==1.14.2
	tensorflow-gpu==1.4.0
	Cython==0.24.1
	ipython==5.1.0
 	```
------ 
## Demo
1. 使用Yolo工具LabelImg进行标注。
2. 运行```xml2txt.py```，生成txt文件夹和photo文件夹，里面的档案对应（001.jpg对应001.txt），放到 data/Mydata
3. 下载vgg模型
4./mlt/image和data/dataset/mlt/label 
5. split_label.py，里面更改路径，label会保存到data路径里
6. 训练
------ 
## Debug
1. run utils/bbox/setup.py
	```
	chmod +x make.sh
	./make.sh   
	```
	Error: ./make.sh失败    
	解决：装完vs2015顺利(windows系统中)

2. demo.py： 
	Error: utils报错
	解决：库路径更改from utils.text_connector.detectors import TextDetector
	
3. train.py：  
	Error: the nvidia driver on your system is too old (found version 9000)  
	解决：显卡驱动版本过低，或者cuda,pytorch版本没有对应。  
	1. 安装对应版本。  
	2. 重新安装新版显卡驱动（https://zhuanlan.zhihu.com/p/59618999）  

4. 中文汉字训练：  
	Error: TypeError: function takes exactly 5 arguments (1 given)  
	解决： 无人解答。parser.add_argument('--workers', type=int, help='number of data loading workers',default=0)#线程数导入数据，default为0    
	
	Error: UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd9 in position 0: invalid continuation byte  
	解决： 无人解答，中文字符解码问题（猜测）
        解决：dataset.py-> label = label_byte.decode('gbk')。gb2312简体汉字编码规范，big5繁体汉字编码规范,gbk大字符集，兼容所有亚洲字符。但针对繁体字这边只能用gbk不知道为什么
