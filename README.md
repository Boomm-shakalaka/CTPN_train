# CTPN_train
  CTPN是在ECCV 2016提出的一种文字检测算法。CTPN结合CNN与LSTM深度网络，能有效的检测出复杂场景的横向分布的文字。
## Reference
1. 源码：https://github.com/eragonruan/text-detection-ctpn
2. csdn:https://blog.csdn.net/sxlsxl119/article/details/102767710
3. 训练集制作:使用yolo的Imglabel，生成xml档案，再转换成txt。

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
1. 建立训练集和验证集，例如1.jpg对应1.txt。.txt中是图片中的文本。
2. 运行 lmdb.py，生成LMDB数据。
3. 修改 train.py中的alphabet和参数。运行 train.py，开始训练。    
------ 
## Debug
1. run lmdb.py     
	Error: 'utf-8' codec can't decode byte 0xff in position 0: inva    
	解决：在python2才能运行

2. warp-ctc编译：  
 	```
	git clone https://github.com/SeanNaren/warp-ctc.git
	cd warp-ctc    
	mkdir build     
	cd build    
	cmake ..  
	make
	cd ../pytorch_binding
	python setup.py install
	 ```
  	Error: nvcc fatal : Value 'c++14' is not defined for option 'std      
   	解决： cuda版本兼容问题，安装cuda10,cudnn7,torch1.2,python3.6```conda install pytorch==1.2.0,torchvision==0.4.0 cudatoolkit=10.0 -c pytorch ```  
	
	Error: fatal error: cuda_runtime_api.h: No such file or directory  
	解决：在warp-ctc/pytorch_binding/setup.py 修改  ```extra_compile_args = ['-std=c++14', '-fPIC']为extra_compile_args = ['-std=c++14', '-fPIC','-I/usr/local/cuda/include'] ```  
	
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
