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




fftanalysis.py 函数索引

  interp0(field,grid0)
    将没有粒子的格子用插值补上（只适用于没有粒子的格点很少的情况）
  denmom2vel(mapden,mapmom,grid)
    在有den和mom的情况下，得到vel

  karray(grid, BE=False)
    （3d，数组）产生一个数组，顺序和np.fft.nfftr结果相同，值是k的模，（x,y,z方向分量）
  karrayfor (grid, BE=False)
    （3d，for numba）产生一个数组，顺序和np.fft.nfftr结果相同，值是k的模，（x,y,z方向分量）
  karrayfor2d (grid, BE=False)
    （2d，for numba）产生一个数组，顺序和np.fft.nfftr结果相同，值是k的模，（x,y,z方向分量）

  CalPS(field,grid,mapscale=1,kscale=1)
    3d标量场场的功率谱
  CalR(field1, field2, grid)
    两个3d标量场的互相关系数
  CalPSvector(field,grid,mapscale=1,kscale=1)
    3d矢量场场的功率谱
  CalRvector(field1, field2, grid)
    两个3d矢量量场的互相关系数
  CalPS2d(field,grid,mapscale=1,kscale=1)
    2d标量场场的功率谱
  CalR2d(field1, field2, grid)
    两个2d标量场的互相关系数

  BEdec(field,grid)
    返回一个3d矢量场的BE模
  BEdecomposition(xk,yk,zk,xk,yk,zk,kmod)
    同上，输入值返回值不同

  Compare2field(map1k,map2k，kmod,mapscale=1,kscale=1,name1="1",name2="2")
    比较两个3d标量场，返回各自功率谱及互相关功率谱
  Compare2vectorfield(map1xk,map1yk,map1zk,map2xk,map2yk,map2zk,kmod,mapscale=1,kscale=1,savename="111")
    比较两个3d矢量场，返回各自功率谱及互相关功率谱
  ThetaPDF(map1k,map2k,kmod,kvalue,kscale=1)
    得到某一个k处the的PDF
  SigmaTheta(map1,map2,grid,kscale)
    得到每一个k处的sigma_the
  ChangeAmp(mapk,kmod,amp,kamp,kscale)
    改变一个3d标量场的Amp
  ChangeTheta(mapk,kmod,theta,kthe,kscale)
    改变一个3d标量场的the

  getampthe(field1, field2, grid,kscale=1)
  getampthevector(field1, field2, grid,kscale=1)

