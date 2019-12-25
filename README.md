# DM_B


第一步： ConstDenMap.py
从TNG文件中读出粒子的pos，vel，构造DM，电子的密度，动量场。
  运行时需要输入的参数：
    grid 格点数
    fieldtype 1:DMden 2:eleden 3:
      1.2 保存的格式都是npy; 3,4保存的格式是npz （如果跑过3,4的话，其实1,2是没有用的）；另外还有6是star的den，vel，现在没有用
    zs  红移
    
第二步：ReconField.py 调用文件 modify.py
根据dm ele的den，mom，产生一个修改场rec


