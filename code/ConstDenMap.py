import numpy as np
import sys
import psutil
sys.path.append('/lustre/home/acct-phyzpj/phyzpj-cz/Data/IllustrisTNG/')
import illustris_python as il
grid=np.int(sys.argv[1])
fieldtype=np.int(sys.argv[2])
zs=np.int(sys.argv[3])


if fieldtype==1:
	basepath='/lustre/home/acct-phyzpj/phyzpj-cz/Data/IllustrisTNG/TNG100-1-Dark/output'
	savename="/lustre/home/acct-phyzpj/phyzpj-cz/Data/Fields/TNG100-1-Dark/dendm"
if fieldtype==2:
	basepath='/lustre/home/acct-phyzpj/phyzpj-cz/Data/IllustrisTNG/TNG100-1/output'
	savename="/lustre/home/acct-phyzpj/phyzpj-cz/Data/Fields/TNG100-1/denele"
if fieldtype=3:
	basepath='/lustre/home/acct-phyzpj/phyzpj-cz/Data/IllustrisTNG/TNG100-1-Dark/output'
	savename="/lustre/home/acct-phyzpj/phyzpj-cz/DM_BaryonRelation/data/1fields/TNG100-1/dm"
	#savename="/lustre/home/acct-phyzpj/phyzpj-cz/Data/Fields/TNG100-1-Dark/denmomdm"
if fieldtype==4:
	basepath='/lustre/home/acct-phyzpj/phyzpj-cz/Data/IllustrisTNG/TNG100-1/output'
	savename="/lustre/home/acct-phyzpj/phyzpj-cz/DM_BaryonRelation/data/1fields/TNG100-1/ele"
	#savename="/lustre/home/acct-phyzpj/phyzpj-cz/Data/Fields/TNG100-1/denmomele"
if fieldtype==6:
	basepath='/lustre/home/acct-phyzpj/phyzpj-cz/Data/IllustrisTNG/TNG100-1/output'
	savename="/lustre/home/acct-phyzpj/phyzpj-cz/Data/Fields/TNG100-1/denvelstarunscale"

if fieldtype=7:
	basepath='/lustre/home/acct-phyzpj/phyzpj-cz/Data/IllustrisTNG/TNG300-1-Dark/output'
	savename="/lustre/home/acct-phyzpj/phyzpj-cz/DM_BaryonRelation/data/1fields/TNG300-1/dm"

if fieldtype=8:
	basepath='/lustre/home/acct-phyzpj/phyzpj-cz/Data/IllustrisTNG/TNG300-1/output'
	savename="/lustre/home/acct-phyzpj/phyzpj-cz/DM_BaryonRelation/data/1fields/TNG300-1/ele"

if __name__=='__main__':
#	for zs in [25]:	#zs: z_step
	print "zstep=",zs
	if fieldtype==1 or fieldtype==2:
		denmap=il.snapshot.DenMap(basepath,zs,grid,fieldtype=fieldtype)
		np.save(savename+str(grid)+'_'+str(zs),denmap);
	if fieldtype==3 or fieldtype==4 or fieldtype==7 or fieldtype==8:
		denmap,mommap=il.snapshot.DenMap(basepath,zs,grid,fieldtype=fieldtype)
		np.savez(savename+str(grid)+'_'+str(zs),denmap=denmap,mommap=mommap)
