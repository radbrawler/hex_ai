import random

IsOver = True
Size = 11
Fld = [[0 for i in range(Size)] for j in range(Size)]
Start0 = 0
theLevel = 3
MoveCount = 0
MaxMoveCount, IsSwap, ActiveColor = 121, 0, -1
MaxFld = Size*Size

IsPlayer = []
Level = []
Pot = [[[0 for i in range(5)] for j in range(Size)] for k in range(Size)]
Bridge = [[[0 for i in range(5)] for j in range(Size)] for k in range(Size)]
Upd = [[0 for i in range(Size)] for j in range(Size)]
vv = [0 for i in range(6)]
tt = [0 for i in range(6)]

IsStart0 = True
IsPlayer.append(True)
IsPlayer.append(False)
Level.append(2)
Level.append(3)

out = open("output.txt", "wb")


def CanConnectFarBorder(nn, mm, cc):
	if cc > 0:  # blue
		if 2*mm < Size-1:
			for ii in range(Size):
				for jj in range(mm):
					if (jj-ii < mm-nn)and(ii+jj <= nn+mm)and(Fld[ii][jj] != 0):
						return 2
			if Fld[nn-1][mm] == -cc:
				return 0
			if Fld[nn-1][mm-1] == -cc:
				if GetFld(nn+2, mm-1) == -cc:
					return 0
				return -1
			if GetFld(nn+2, mm-1) == -cc:
				return -2

		else:
			for ii in range(Size):
				for jj in range(Size-1, mm, -1):
					if (jj-ii > mm-nn)and(ii+jj >= nn+mm)and(Fld[ii][jj] != 0):
						return 2
			if Fld[nn+1][mm] == -cc:
				return 0
			if Fld[nn+1][mm+1] == -cc:
				if GetFld(nn-2, mm+1) == -cc:
					return 0
				return -1
			if GetFld(nn-2, mm+1) == -cc:
				return -2

	else:
		if 2*nn < Size-1:
			for jj in range(Size):
				for ii in range(nn):
					if (ii-jj < nn-mm)and(ii+jj <= nn+mm)and(Fld[ii][jj] != 0):
						return 2
			if Fld[nn][mm-1] == -cc:
				return 0
			if Fld[nn-1][mm-1] == -cc:
				if GetFld(nn-1, mm+2) == -cc:
					return 0
				return -1
			if GetFld(nn-1, mm+2) == -cc:
				return -2
		else:
			for jj in range(Size):
				for ii in range(Size-1, nn, -1):
					if (ii-jj > nn-mm)and(ii+jj >= nn+mm)and(Fld[ii][jj] != 0):
						return 2
			if Fld[nn][mm+1] == -cc:
				return 0
			if Fld[nn+1][mm+1] == -cc:
				if GetFld(nn+1, mm-2) == -cc:
					return 0
				return -1
			if GetFld(nn+1, mm-2) == -cc:
				return -2
	return 1


def GetFld(ii, jj):
	if ii < 0:
		return -1
	if jj < 0:
		return 1
	if ii >= Size:
		return -1
	if jj >= Size:
		return 1
	return Fld[ii][jj]


def sign(xx):
	if xx > 0:
		return 1
	if xx < 0:
		return -1
	return 0


def PotVal(ii,jj,kk,cc):
	if ii<0: return 30000
	if jj<0: return 30000
	if ii>=Size: return 30000
	if jj>=Size: return 30000
	if Fld[ii][jj]==0: return Pot[ii][jj][kk]
	if Fld[ii][jj]==-cc: return 30000
	return Pot[ii][jj][kk]-30000


def get_best_move(theCol):
	condition = True
	outputCount = 0
	while(condition):
		ii_q, jj_q, ii_b, jj_b, ff = 0, 0, 0, 0, 0
		vv = [False for i in range(121)]
		mm = 20000
		if MoveCount > 0:
			ff = 190/(MoveCount*MoveCount)
		# out.write(str(MoveCount))
		for ii in range(Size):
			for jj in range(Size):
				if Fld[ii][jj] != 0:
					ii_q += 2*ii+1-Size
					jj_q += 2*jj+1-Size
		ii_q = sign(ii_q)
		jj_q = sign(jj_q)
		# out.write(str(ii_q) + str(jj_q))
		for ii in range(Size):
			for jj in range(Size):
				if Fld[ii][jj] == 0:
					mmp = random.random()*(49-theLevel*16)
					mmp += (abs(ii-5)+abs(jj-5))*ff
					mmp += 8*(ii_q*(ii-5)+jj_q*(jj-5))/(MoveCount+1)
					for kk in range(4):
						mmp -= Bridge[ii][jj][kk]
					pp0 = Pot[ii][jj][0]+Pot[ii][jj][1]
					pp1 = Pot[ii][jj][2]+Pot[ii][jj][3]
					mmp += pp0+pp1
					if (pp0 <= 268)or(pp1 <= 268):
						mmp -= 400
					vv[ii*Size+jj] = mmp
					if mmp < mm:
						mm = mmp
						ii_b = ii
						jj_b = jj

		if theLevel > 2:
			mm += 108
			for ii in range(Size):
				for jj in range(Size):
					if vv[ii*Size+jj] < mm:
						if theCol < 0:
							if (ii > 3)and(ii < Size-1)and(jj > 0)and(jj < 3):
								if Fld[ii-1][jj+2] == -theCol:
									cc = CanConnectFarBorder(ii-1, jj+2, -theCol)
									if cc < 2:
										ii_b = ii
										if cc < -1:
											ii_b-=1
											cc+=1
										jj_b = jj-cc
										mm = vv[ii*Size+jj]
							if (ii > 0)and(ii < Size-1)and(jj == 0):
								if (Fld[ii-1][jj+2] == -theCol)and(Fld[ii-1][jj]==0)and(Fld[ii-1][jj+1]==0)and(Fld[ii][jj+1]==0)and(Fld[ii+1][jj]==0):
									ii_b=ii
									jj_b=jj
									mm=vv[ii*Size+jj]
							if (ii>0)and(ii<Size-4)and(jj<Size-1)and(jj>Size-4):
								if Fld[ii+1][jj-2] == -theCol:
									cc = CanConnectFarBorder(ii+1,jj-2,-theCol)
									out.write(str(ii+1)+str(jj-2)+str(-theCol))
									if cc < 2:
										ii_b = ii
										if cc<-1:
											ii_b+=1
											cc+=1
										jj_b = jj+cc
										mm = vv[ii*Size+jj]
							if (ii>0)and(ii<Size-1)and(jj==Size-1):
								if (Fld[ii+1][jj-2]==-theCol)and(Fld[ii+1][jj]==0)and(Fld[ii+1][jj-1]==0)and(Fld[ii][jj-1]==0)and(Fld[ii-1][jj]==0):
									ii_b=ii
									jj_b=jj
									mm=vv[ii*Size+jj]
						else:
							if (jj>3)and(jj<Size-1)and(ii>0)and(ii<3):
								if Fld[ii+2][jj-1]==-theCol:
									cc = CanConnectFarBorder(ii+2,jj-1,-theCol)
									if cc<2:
										jj_b=jj
										if cc<-1:
											jj_b-=1
											cc+=1
										ii_b=ii-cc
										mm=vv[ii*Size+jj]
							if (jj>0)and(jj<Size-1)and(ii==0):
								if (Fld[ii+2][jj-1]==-theCol)and(Fld[ii][jj-1]==0)and(Fld[ii+1][jj-1]==0)and(Fld[ii+1][jj]==0)and(Fld[ii][jj+1]==0):
									ii_b=ii
									jj_b=jj
									mm=vv[ii*Size+jj]
							if (jj>0)and(jj<Size-4)and(ii<Size-1)and(ii>Size-4):
								if Fld[ii-2][jj+1]==-theCol:
									cc = CanConnectFarBorder(ii-2,jj+1,-theCol)
									if cc < 2:
										jj_b = jj
										if cc < -1:
											jj_b+=1
											cc+=1
										ii_b=ii+cc
										mm=vv[ii*Size+jj]
							if (jj>0)and(jj<Size-1)and(ii==Size-1):
								if (Fld[ii-2][jj+1]==-theCol)and(Fld[ii][jj+1]==0)and(Fld[ii-1][jj+1]==0)and(Fld[ii-1][jj]==0)and(Fld[ii][jj-1]==0):
									ii_b=ii
									jj_b=jj
									mm=vv[ii*Size+jj]

		if Fld[ii_b][jj_b] == 0:
			print(''.join([chr(jj_b+65), str(ii_b+1)]))
			return
		else:
			outputCount += 1
			condition = (Fld[ii_b][jj_b]!=0)and(outputCount<100)
	for ii in range(Size):
		for jj in range(Size):
			if Fld[ii][jj] == 0:
				print(''.join([chr(jj+65), str(ii+1)]))
				return



def GetPot(llevel):
	dd = 128
	ActiveColor=((MoveCount+1+Start0)%2)*2-1
	for ii in range(Size):
		for jj in range(Size):
			for kk in range(4):
				Pot[ii][jj][kk]=20000
				Bridge[ii][jj][kk]=0

	for ii in range(Size):
		if (Fld[ii][0]==0):
			Pot[ii][0][0]=dd  # blue border
		else:
			if (Fld[ii][0]>0):
				Pot[ii][0][0]=0
		if (Fld[ii][Size-1]==0):
			Pot[ii][Size-1][1]=dd  # blue border
		else:
			if (Fld[ii][Size-1]>0):
				Pot[ii][Size-1][1]=0

	for jj in range(Size):
		if (Fld[0][jj]==0):
			Pot[0][jj][2]=dd  # red border
		else:
			if (Fld[0][jj]<0):
				Pot[0][jj][2]=0

		if (Fld[Size-1][jj]==0):
			Pot[Size-1][jj][3]=dd  # red border
		else:
			if (Fld[Size-1][jj]<0):
				Pot[Size-1][jj][3]=0

	for kk in range(2):  # blue potential
		for ii in range(Size):
			for jj in range(Size):
				Upd[ii][jj]=True

		nn=0
		condition = True
		while condition:
			nn+=1
			bb=0
			for ii in range(Size):
				for jj in range(Size):
					if (Upd[ii][jj]):
						bb+=SetPot(ii, jj, kk, 1, llevel)

			for ii in range(Size-1,-1,-1):
				for jj in range(Size-1,-1,-1):
					if (Upd[ii][jj]):
						bb+=SetPot(ii, jj, kk, 1, llevel)
			condition = (bb>0)and(nn<12)

	for kk in range(2,4):  # red potential
		for ii in range(Size):
			for jj in range(Size):
				Upd[ii][jj]=True
		nn=0
		condition = True
		while condition:
			nn+=1
			bb=0
			for ii in range(Size):
				for jj in range(Size):
					if (Upd[ii][jj]):
						bb+=SetPot(ii, jj, kk, -1, llevel)

			for ii in range(Size-1,-1,-1):
				for jj in range(Size-1,-1,-1):
					if (Upd[ii][jj]):
						bb+=SetPot(ii, jj, kk, -1, llevel)
			condition = ((bb>0)and(nn<12))


def SetPot(ii, jj, kk, cc, llevel):
	ddb, oo, dd, bb = 0, 0, 140, 66
	Upd[ii][jj]=False
	Bridge[ii][jj][kk]=0
	if (Fld[ii][jj] ==- cc):
		return 0
	if (cc!=ActiveColor):
		bb=52
	vv[0]=PotVal(ii+1,jj,kk,cc)
	vv[1]=PotVal(ii,jj+1,kk,cc)
	vv[2]=PotVal(ii-1,jj+1,kk,cc)
	vv[3]=PotVal(ii-1,jj,kk,cc)
	vv[4]=PotVal(ii,jj-1,kk,cc)
	vv[5]=PotVal(ii+1,jj-1,kk,cc)
	for ll in range(6):
		if ((vv[ll]>=30000)and(vv[(ll+2)%6]>=30000)):
			if (vv[(ll+1)%6]<0):
				ddb=+32
			else:
				vv[(ll+1)%6]+=128 //512
	for ll in range(6):
		if ((vv[ll]>=30000)and(vv[(ll+3)%6]>=30000)):
			ddb+=30
	mm=30000
	for ll in range(6):
		if (vv[ll]<0):
			vv[ll]+=30000
			tt[ll]=10
		else:
			tt[ll]=1
		if (mm>vv[ll]):
			mm=vv[ll]
	nn=0
	for ll in range(6):
		if (vv[ll]==mm):
			nn+=tt[ll]
	if (llevel>1):
		Bridge[ii][jj][kk]=nn/5
		if ((nn>=2)and(nn<10)):
			Bridge[ii][jj][kk] = bb+nn-2
			mm-=32
		if (nn<2):
			oo=30000
			for ll in range(6):
				if (vv[ll]>mm)and(oo>vv[ll]):
					oo=vv[ll]
			if (oo<=mm+104):
				Bridge[ii][jj][kk]=bb-(oo-mm)/4
				mm-=64
			mm+=oo
			mm/=2
	if ((ii>0)and(ii<Size-1)and(jj>0)and(jj<Size-1)):
		Bridge[ii][jj][kk]+=ddb
	else:
		Bridge[ii][jj][kk]-=2
	if (((ii==0)or(ii==Size-1))and((jj==0)or(jj==Size-1))):
		Bridge[ii][jj][kk]/=2  # /=4
	if (Bridge[ii][jj][kk]>68):
		Bridge[ii][jj][kk]=68  # 66

	if (Fld[ii][jj]==cc):
		if (mm<Pot[ii][jj][kk]):
			Pot[ii][jj][kk]=mm
			SetUpd(ii+1,jj,cc)
			SetUpd(ii,jj+1,cc)
			SetUpd(ii-1,jj+1,cc)
			SetUpd(ii-1,jj,cc)
			SetUpd(ii,jj-1,cc)
			SetUpd(ii+1,jj-1,cc)
			return 1
		return 0

	if (mm+dd<Pot[ii][jj][kk]):
		Pot[ii][jj][kk]=mm+dd
		SetUpd(ii+1,jj,cc)
		SetUpd(ii,jj+1,cc)
		SetUpd(ii-1,jj+1,cc)
		SetUpd(ii-1,jj,cc)
		SetUpd(ii,jj-1,cc)
		SetUpd(ii+1,jj-1,cc)
		return 1
	return 0


def SetUpd(ii,jj,cc):
	if ii<0: return
	if jj<0: return
	if ii>=Size: return
	if jj>=Size: return
	Upd[ii][jj]=True


def readFile():
	global MoveCount
	fob = open("board_file.txt", 'r')
	list1 = fob.readlines()
	for i in range(Size):
		for j in range(Size):
			words = list1[i*Size+j+1].split()
			if words[1] == 'U':
				# print(words[0])
				Fld[j][i] = 0
			if words[1] == 'R':
				Fld[j][i] = -1
				MoveCount += 1
			if words[1] == 'B':
				Fld[j][i] = 1
				MoveCount += 1

	return list1[0]


if __name__ == '__main__':
	MoveCount = 0
	color = readFile()
	# print(color)
	GetPot(3)
	if color == '0':  # Blue
		get_best_move(1)
	else:  # Red
		get_best_move(-1)
