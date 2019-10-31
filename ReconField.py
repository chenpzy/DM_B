# Rescale a field according to amplitude and phase

import numpy as np
import fftanalysis as fa
import sys
import time
import modify as mf
datadir="/lustre/home/acct-phyzpj/phyzpj-cz/Data/Fields/"
grid=256
zs=99
#zs=np.int(sys.argv[1])
boxlen=75
debug=0
method=2


def ReconField(mapk, amp=False, theta=False, kamp=False,kthe=False):
	print("==================================")
	# find k, r>0.9
	'''
	for kno in range(len(kthe)):
		if theta[kno]>0.75:break
	print("k cut-off:",kthe[kno])
	'''
	print("Reconstruct a field")
	kmod=fa.karrayfor(grid)
	if type(amp)==bool:
		print("Amplitude is False")
	else:
		print("Amplitude is True")
		fa.ChangeAmp(mapk,kmod,amp,kamp, 2*np.pi/boxlen)
	if type(theta)==bool:
		print("Theta is False")
	else:
		print("Theta is True")
		fa.ChangeTheta(mapk, kmod, theta, kthe, 2*np.pi/boxlen)
	return mapk		


if __name__=='__main__':
	print("Rescale the velosity and density field according to amplitude and phase")

	#read map data
	#NAME:	mapAAABBB,	
	#AAA:	dm,ele,rec
	#BBB:	den,mom,vel

	t0=time.time()
	mapdmdata=np.load(datadir+"TNG100-1-Dark/denmomdm"+str(grid)+'_'+str(zs)+'.npz')
	mapeledata=np.load(datadir+"TNG100-1/denmomele"+str(grid)+'_'+str(zs)+'.npz')
	print("Finish Reading the map data \t costs", np.round(time.time()-t0,3))
	
	t0=time.time()
	mapdmden=mapdmdata["denmap"].reshape(grid,grid,grid)
	mapdmmom=mapdmdata["mommap"].reshape(grid,grid,grid,3)
	mapeleden=mapeledata["denmap"].reshape(grid,grid,grid)
	mapelemom=mapeledata["mommap"].reshape(grid,grid,grid,3)
	del mapdmdata, mapeledata
	print("Pre-process data\t costs", np.round(time.time()-t0,3))

	#amplitude and theta
	#NAME:	AAABBBCCC
	#AAA:	ps
	#BBB:	dm,ele,vel
	#CCC:	den,vel,vx,vy,vz
	#	ampden, ampdenk,	ampvel,	ampvelk
	#	theden,	thedenk,	thevel,	thevelk
	'''
	# 1. read from a file
	#den
	psdendata=np.load("comparedmdeneleden.npz")
	psdenamp=(psdendata["ps2"]/psdendata["ps1"])[2:]
	psdenthe2=psdendata["theta2"][2:]
	psdenk=2*np.pi/boxlen*10**((np.arange(2,len(psdenamp)+2)+0.5)*0.1)
	thedenk=psdenk
	print("Den Amplitude:", psdenamp)
	print("Den Theta^2:", psdenthe2)
	del	psdendata
	#vel
	psvxdata=np.load("comparedmvxelevx.npz")
	psvydata=np.load("comparedmvyelevy.npz")
	psvzdata=np.load("comparedmvzelevz.npz")
	psvelamp=(psvxdata["ps2"]/psvxdata["ps1"]+psvydata["ps2"]/psvydata["ps1"]+psvzdata["ps2"]/psvzdata["ps1"])[2:]/3
	psvelthe2=(psvxdata["theta2"]+psvydata["theta2"]+psvzdata["theta2"])[2:]/3
	psvelk=2*np.pi/boxlen*10**((np.arange(2,len(psvelamp)+2)+0.5)*0.1)
	thevelk=psvelk
	print("Vel Amplitude:",psvelamp)
	'''
	# 2. Calculate
	#amplitude
	psdmden,ampdenk=fa.CalPS(mapdmden,grid)
	pseleden,ampdenk=fa.CalPS(mapeleden,grid)
	ampdenk*=2*np.pi/boxlen
	amp2den=pseleden/psdmden

	if method==1:
		#get vel
		mapdmvel=fa.denmom2vel(mapdmden,mapdmmom,grid)
		mapelevel=fa.denmom2vel(mapeleden,mapelemom,grid)
		psdmvx,ampvelk=fa.CalPS(mapdmvel[:,:,:,0],grid)
		psdmvy,ampvelk=fa.CalPS(mapdmvel[:,:,:,1],grid)
		psdmvz,ampvelk=fa.CalPS(mapdmvel[:,:,:,2],grid)
		pselevx,ampvelk=fa.CalPS(mapelevel[:,:,:,0],grid)
		pselevy,ampvelk=fa.CalPS(mapelevel[:,:,:,1],grid)
		pselevz,ampvelk=fa.CalPS(mapelevel[:,:,:,2],grid)
		ampvelk*=2*np.pi/boxlen
		amp2vel=(pselevx/psdmvx+pselevy/psdmvy+pselevz/psdmvz)/3.0

	psdmpx,ampmomk=fa.CalPS(mapdmmom[:,:,:,0],grid)
	psdmpy,ampmomk=fa.CalPS(mapdmmom[:,:,:,1],grid)
	psdmpz,ampmomk=fa.CalPS(mapdmmom[:,:,:,2],grid)
	pselepx,ampmomk=fa.CalPS(mapelemom[:,:,:,0],grid)
	pselepy,ampmomk=fa.CalPS(mapelemom[:,:,:,1],grid)
	pselepz,ampmomk=fa.CalPS(mapelemom[:,:,:,2],grid)
	ampmomk*=2*np.pi/boxlen
	amp2mom=(pselepx/psdmpx+pselepy/psdmpy+pselepz/psdmpz)/3.0

	#theta
	rden,thedenk=fa.CalR(mapdmden,mapeleden,grid)
	thedenk*=2*np.pi/boxlen
	the2den=-np.log(rden)*2

	if method==1:
		rvelx,thevelk=fa.CalR(mapdmvel[:,:,:,0],mapelevel[:,:,:,0],grid)
		rvely,thevelk=fa.CalR(mapdmvel[:,:,:,1],mapelevel[:,:,:,1],grid)
		rvelz,thevelk=fa.CalR(mapdmvel[:,:,:,2],mapelevel[:,:,:,2],grid)
		thevelk*=2*np.pi/boxlen
		rvel=(rvelx+rvely+rvelz)/3
		the2vel=-np.log(rvel)*2

	if method==2:
		rmomx,themomk=fa.CalR(mapdmmom[:,:,:,0],mapelemom[:,:,:,0],grid)
		rmomy,themomk=fa.CalR(mapdmmom[:,:,:,1],mapelemom[:,:,:,1],grid)
		rmomz,themomk=fa.CalR(mapdmmom[:,:,:,2],mapelemom[:,:,:,2],grid)
		themomk*=2*np.pi/boxlen
		rmom=(rmomx+rmomy+rmomz)/3
		the2mom=-np.log(rmom)*2
	print("Finish cal")

	if debug:
		print("DEN amp",amp2den)
		print("k",ampdenk)
		print("VEL amp",amp2vel)
		print("k",ampvelk)
		print("DEN theta^2",the2den)
		print("k",thedenk)
		print("VEL theta^2",the2vel)
		print("k",thevelk)
		np.savez("reconstpara/rp"+str(zs),k=ampdenk,ampden=np.sqrt(amp2den),ampvel=np.sqrt(amp2vel),ampmom=np.sqrt(amp2mom),theden=np.sqrt(the2den),thevel=np.sqrt(the2vel),themom=np.sqrt(the2mom))
		exit()

	if method==1:
		t0=time.time()
		#den
		mapdmdenk=np.fft.rfftn(mapdmden)
		mapnewden=np.fft.irfftn(ReconField(mapdmdenk,amp=np.sqrt(amp2den),theta=np.sqrt(the2den),kamp=ampdenk,kthe=thedenk))
		if debug:
			print("psden re/ele",fa.CalPS(mapnewden,grid)[0]/fa.CalPS(mapeleden,grid)[0])
			print("Rden_dm_rec/R_dm_ele",fa.CalR(mapdmden,mapnewden,grid)[0]/fa.CalR(mapdmden,mapeleden,grid)[0])
		#vel
		mapnewvel=np.zeros(mapdmvel.shape)
		mapdmvelxk=np.fft.rfftn(mapdmvel[:,:,:,0])
		mapdmvelyk=np.fft.rfftn(mapdmvel[:,:,:,1])
		mapdmvelzk=np.fft.rfftn(mapdmvel[:,:,:,2])
		mapnewvel[:,:,:,0]=np.fft.irfftn(ReconField(mapdmvelxk,amp=np.sqrt(amp2vel),theta=np.sqrt(the2vel),kamp=ampvelk,kthe=thevelk))
		mapnewvel[:,:,:,1]=np.fft.irfftn(ReconField(mapdmvelyk,amp=np.sqrt(amp2vel),theta=np.sqrt(the2vel),kamp=ampvelk,kthe=thevelk))
		mapnewvel[:,:,:,2]=np.fft.irfftn(ReconField(mapdmvelzk,amp=np.sqrt(amp2vel),theta=np.sqrt(the2vel),kamp=ampvelk,kthe=thevelk))
		if debug:
			print("psvx re/ele",fa.CalPS(mapnewvel[:,:,:,0],grid)[0]/fa.CalPS(mapelevel[:,:,:,0],grid)[0])
			print("Rvx_dm_rec/R_dm_ele",fa.CalR(mapdmvel[:,:,:,0],mapnewvel[:,:,:,0],grid)[0]/fa.CalR(mapdmvel[:,:,:,0],mapelevel[:,:,:,0],grid)[0])


		#mom
		mapnewmom=((mapnewden.reshape(-1,1)).repeat(3,axis=1)*mapnewvel.reshape(-1,3)).reshape(grid,grid,grid,3)

		psnewpx,ampmomk=fa.CalPS(mapnewmom[:,:,:,0],grid)
		psnewpy,ampmomk=fa.CalPS(mapnewmom[:,:,:,1],grid)
		psnewpz,ampmomk=fa.CalPS(mapnewmom[:,:,:,2],grid)
		ampmomk*=2*np.pi/boxlen
		amp2mom=(pselepx/psnewpx+pselepy/psnewpy+pselepz/psnewpz)/3.0
		mapnewmomxk=np.fft.rfftn(mapnewmom[:,:,:,0])
		mapnewmomyk=np.fft.rfftn(mapnewmom[:,:,:,1])
		mapnewmomzk=np.fft.rfftn(mapnewmom[:,:,:,2])
		mapnewmom[:,:,:,0]=np.fft.irfftn(ReconField(mapnewmomxk,amp=np.sqrt(amp2mom),kamp=ampmomk))
		mapnewmom[:,:,:,1]=np.fft.irfftn(ReconField(mapnewmomyk,amp=np.sqrt(amp2mom),kamp=ampmomk))
		mapnewmom[:,:,:,2]=np.fft.irfftn(ReconField(mapnewmomzk,amp=np.sqrt(amp2mom),kamp=ampmomk))

		#np.savez("reconpara1",k=ampdenk,amp2den=amp2den,amp2vel=amp2vel,the2den=the2den,the2vel=the2vel,amp2mom=amp2mom)
		print "Grid=",grid, "Method1 cost time", time.time()-t0

	if method==2:
		t0=time.time()
		np.savez("reconpara2",k=ampdenk,amp2den=amp2den,amp2mom=amp2mom,the2den=the2den,the2mom=the2mom)

		

		#den
		mapdmdenk=np.fft.rfftn(mapdmden)
		mapnewden=np.fft.irfftn(ReconField(mapdmdenk,amp=np.sqrt(amp2den),theta=np.sqrt(the2den),kamp=ampdenk,kthe=thedenk))
	
		#mom
		mapnewmom=np.zeros(mapdmmom.shape)
		mapdmmomxk=np.fft.rfftn(mapdmmom[:,:,:,0])
		mapdmmomyk=np.fft.rfftn(mapdmmom[:,:,:,1])
		mapdmmomzk=np.fft.rfftn(mapdmmom[:,:,:,2])
		mapnewmom[:,:,:,0]=np.fft.irfftn(ReconField(mapdmmomxk,amp=np.sqrt(amp2mom),theta=np.sqrt(the2mom),kamp=ampmomk,kthe=themomk))
		mapnewmom[:,:,:,1]=np.fft.irfftn(ReconField(mapdmmomyk,amp=np.sqrt(amp2mom),theta=np.sqrt(the2mom),kamp=ampmomk,kthe=themomk))
		mapnewmom[:,:,:,2]=np.fft.irfftn(ReconField(mapdmmomzk,amp=np.sqrt(amp2mom),theta=np.sqrt(the2mom),kamp=ampmomk,kthe=themomk))


	
		print "Grid=",grid, "Method2 cost time", time.time()-t0

		'''
		#test if the vel is correct
		mapnewvel=fa.denmom2vel(mapnewden,mapnewmom,grid)
		print "The elevel PS:", fa.CalPSvector(mapelevel,grid,mapscale=(boxlen*1.0/grid**2)**3)[0],mapelevel[23,23,:]
		print "The newvel PS:", fa.CalPSvector(mapnewvel,grid,mapscale=(boxlen*1.0/grid**2)**3)[0],mapnewvel[23,23,:]
		exit()
		'''

	name=datadir+"Recon/elemom"+str(grid)+'_'+str(zs)+'_'+str(method)
	np.savez(name,denmap=mapnewden,mommap=mapnewmom)
	print("save data to" +name)
	
