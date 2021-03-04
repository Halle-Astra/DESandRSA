from numpy import roll

S1 = '''14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7
0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8
4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0
15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13'''

S2 = '''15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10
3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5
0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15
13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9'''

S3 = '''10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8
13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1
13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7
1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12'''

S4 = '''7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15
13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9
10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4
3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14'''

S5 = '''2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9
14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6
4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14
11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3'''

S6 = '''12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11
10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8
9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6
4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13'''

S7 = '''4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1
13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6
1,4,11,13,12,3,7,14,10,15,6,2,0,5,9,2
6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12'''

S8 = '''13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7
1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2
7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8
2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11'''

roll_table = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

S = [S1,S2,S3,S4,S5,S6,S7,S8]
del S1,S2,S3,S4,S5,S6,S7,S8#节省空间
S = [ii.split('\n') for ii in S]
for i in range(len(S)):
	S_i = S[i]
	S_i = [ii.split(',') for ii in S_i]
	for j in range(len(S_i)):
		S_i[j] = ['0'*(4-len(bin(eval(iii))[2:]))+bin(eval(iii))[2:] for iii in S_i[j]]
	S[i] = S_i	 #S盒制作完成，先用序号 确定是第几个盒子，然后再用行号列号确定，总计三个指标

def IP(m):
	'''IP置换'''
	L = [58,50,42,34,26,18,10,2,60,52,44,36,28,20,12,4,62,54,46,38,30,22,14,6,64,56,48,40,32,24,16,8]#置换时要注意配合python做-1操作
	R = [57,49,41,33,25,17,9,1,59,51,43,35,27,19,11,3,61,53,45,37,29,21,13,5,63,55,47,39,31,23,15,7]
	L_0 = [m[L[i]-1] for i in range(len(L))]
	R_0 = [m[R[i]-1] for i in range(len(R))]
	return ''.join(L_0),''.join(R_0)

def IP_inverse(R,L):
	'''IP逆置换'''
	m = R+L
	site = [40,8,48,16,56,24,64,32,39,7,47,15,55,23,63,31,38,6,46,14,54,22,62,30,37,5,45,13,53,21,61,29,36,4,44,12,52,20,60,28,35,3,43,11,51,19,59,27,34,2,42,10,50,18,58,26,33,1,41,9,49,17,57,25]
	return ''.join([m[site[i]-1] for i in range(len(site))])

def SeletiveExpand(r):
	'''选择扩张函数E'''
	#r = r[::-1]#做一个反转 !最后发现本书的都不用翻转
	place_t = [[32],list(range(1,6)),list(range(4,10)),list(range(8,14)),list(range(12,18)),list(range(16,22)),list(range(20,26)),list(range(24,30)),list(range(28,33)),[1]]
	place = []
	for i in place_t:
		place = place+i
	newr = r
	newr = [r[place[i]-1] for i in range(len(place))]
	return newr

def Get0bforString(i,base = None):
	'''起初思路针对单字符，成品适用于单、多字符均可'''
	i = str(i)#防止传入数字
	if base:
		return ''.join(['0'*(4-len(bin(int(ii,base))[2:]))+bin(int(ii,base))[2:] for ii in i])
	unicode_i = [ord(ii) for ii in i]
	unicode_i = ['0'*(16-len(bin(ii)[2:]))+bin(ii)[2:] for ii in unicode_i]
	return  ''.join(unicode_i)#完成字符串的二进制转换，且适用于多个字符组成的字符串

def Xor(m,k):
	'''传入类型为字符串既可'''
	return ''.join([str(int(m[i]==k[i])) for i in range(len(m))])

def S_box(m):
	'''S盒算法'''
	m = [m[i*6:(i+1)*6] for i in range(8)]
	for i in range(len(m)):
		row = int(m[i][0]+m[i][-1],2)
		col = int(m[i][1:-1],2)
		m[i] = S[i][row][col]
	return ''.join(m)
	
def P_Exchange(y):
	'''P置换算法'''
	site = [16,7,20,21,29,12,28,17,1,15,23,26,5,18,31,10,2,8,24,14,32,27,3,9,19,13,30,6,22,11,4,25]
	return ''.join([y[site[i]-1] for i in range(len(site))])#[::-1]

def PC_1(m):
	'''PC_1置换,输入需要为未经删去校验码的但经过翻转的母钥'''
	site_C0 = [57,49,41,33,25,17,9,1,58,50,42,34,26,18,10,2,59,51,43,35,27,19,11,3,60,52,44,36]
	site_D0 = [63,55,47,39,31,23,15,7,62,54,46,38,30,22,14,6,61,53,45,37,29,21,13,5,28,20,12,4]
	C0 = [m[site_C0[i]-1] for i in range(len(site_C0))]
	D0 = [m[site_D0[i]-1] for i in range(len(site_D0))]#经过与课本的例子的对比，此处无需翻转
	return C0,D0

def PC_2(m):
	site_a1 = [14,17,11,24,1,5,3,28,15,6,21,10,23,19,12,4,26,8,16,7,27,20,13,2]
	site_a2 = [41,52,31,37,47,55,30,40,51,45,33,48,44,49,39,56,34,53,46,42,50,36,29,32]
	return ''.join([m[site_a1[i]-1] for i in range(len(site_a1))]+[m[site_a2[i]-1] for i in range(len(site_a2))])

def Key_Expand(key_mom):
	'''子密钥生成器'''
	key_mom_info = ''.join([key_mom[i*8:(i+1)*8-1] for i in range(len(key_mom)//8)])#因为待会还要循环移位
	keys = []
	C_i,D_i = PC_1(key_mom)
	for i in range(16):
		C_i = roll(C_i,-1*roll_table[i]).tolist()
		D_i	= roll(D_i,-1*roll_table[i]).tolist()
		keys.append(PC_2(C_i+D_i))
	return keys

def F_func(m,k):
	'''k为当前的子密钥'''
	m = SeletiveExpand(m)
	m = Xor(m,k)
	m = S_box(m)
	m = P_Exchange(m)
	return m

def DES_unit(m,key):
	'''DES加密算法单元程序，仅适用于64bit串输入，而key是子密钥组'''
	L,R = IP(m)
	for i in range(16): 
		T = Xor(L,F_func(R,key[i]))
		L = R
		R = T
	c = IP_inverse(R,L)
	return c

def keymom20b(key_mom):
	key_mom = Get0bforString(key_mom)
	if len(key_mom)>=64:
		key_mom = key_mom[:64]
	else :
		key_mom = key_mom*2
		key_mom = key_mom[:64]
	return key_mom

def DES_entire(m,key_mom,mode = 'm2c',mode_work = 'ECB',c_0 = None):
	'''mode为加密或解密,mode_work为加解密的工作模式,c_0为CBC等模式需要的初值'''
	mode_m = whatmode(m)
	if mode_m == 'unicode':	m = Get0bforString(m)
	elif mode_m == 16:m = Get0bforString(m,16)
	if type(key_mom)==str:
		key_mom = keymom20b(key_mom)
	elif type(key_mom)==list:
		key_mom = [keymom20b(i) for i in key_mom]#主要是CM模式的存在性
	m_ls = [m[i*64:(i+1)*64] for i in range(len(m)//64)]#如果不足64的话，整除为0，这个就会为空
	#if len(m)>=64:
	if len(m)%64:#否则为0时会重复一遍，下面的-1*len(m)%64会为0，即从头开始
		m_res = m[-1*(len(m)%64):]
		m_res = m_res+'0'*(64-(len(m)%64))
		m_ls.append(m_res)
	m_ls = [i for i in m_ls if i]
	if type(key_mom) == str:
		keys = Key_Expand(key_mom)
	elif type(key_mom)==list:
		keys = [Key_Expand(i) for i in key_mom]

	#若有c_0，则先处理c_0
	if c_0:
		c_0 = Get0bforString(c_0)
		if len(c_0)>=64:
			c_0 = c_0[:64]
		else :
			c_0 = c_0*2
			c_0 = c_0[:64]#已完全得到所需要的c_0

	if mode == 'c2m':	
		keys = keys[::-1]
		if type(key_mom)==list:
			keys = [i[::-1] for i in keys]
	if mode_work=='ECB':		
		return ''.join([DES_unit(m_ls[i],keys) for i in range(len(m_ls))])
	elif mode_work == 'CBC':
		c_i = c_0
		c = []
		if mode == 'm2c':
			for i in range(len(m_ls)):
				m_i = m_ls[i]
				#print(len(c_i),len(m_i))
				#m_i_add_c = ''.join([str((int(m_i[j])+int(c_i[j]))%2) for j in range(len(c_i))])	#逐比特模2相加 其实就是异或Xor
				m_i_add_c = Xor(m_i,c_i)
				c_i = DES_unit(m_i_add_c,keys)
				c.append(c_i)
			return ''.join(c)
		elif mode == 'c2m':
			for i in range(len(m_ls)):
				if i!=0:
					c_i = m_ls[i-1]
				elif i==0:
					c_i = c_0
				c_i = Xor(DES_unit(m_ls[i],keys),c_i)#这里做的是解密，所以c实际上是解密后的明文集
				c.append(c_i)
			return ''.join(c)
	elif mode_work == 'CFB':
		'''尽管这里采用CFB模式，但这里的s取64'''
		c_i = c_0
		c = []
		if mode == 'm2c':
			for i in range(len(m_ls)):
				m_i = m_ls[i]
				c_i = DES_unit(c_i,keys)
				#c_i = ''.join([str((int(m_i[j])+int(c_i[j]))%2) for j in range(len(c_i))])	#逐比特模2相加 其实就是异或Xor
				c_i = Xor(m_i,c_i)
				c.append(c_i)
			return ''.join(c)
		elif mode == 'c2m':
			keys = keys[::-1]#此时变回了和加密时一样的密钥组，因为后面要对c_i-1做加密 后异或
			for i in range(len(m_ls)):
				if i!=0:
					c_i = m_ls[i-1]
				elif i==0:
					c_i = c_0
				c_de = Xor(DES_unit(c_i,keys),m_ls[i])#这里做的是解密，所以c实际上是解密后的明文集
				c.append(c_de)
			return ''.join(c)
	elif mode_work == 'OFB':
		if mode == 'm2c':
			c_i = c_0
			c = []
			for i in range(len(m_ls)):
				c_i = DES_unit(c_i,keys)
				c_add = Xor(c_i,m_ls[i])
				c.append(c_add)
			return ''.join(c)
		elif mode == 'c2m':
			keys = keys[::-1] #同上
			c_i = c_0
			c = []
			for i in range(len(m_ls)):
				c_i = DES_unit(c_i,keys)
				c_add = Xor(m_ls[i],c_i)
				c.append(c_add)
			return ''.join(c)
	elif mode_work == 'CM':
		c = m_ls
		#print('CM is beginning' )
		for i in range(len(keys)):
			c = [DES_unit(c[j],keys[i]) for j in range(len(c))]	 #这里的一个问题是，原本是[DES_unit(c[i],keys[i])for i in ...]，这样的i与想要的不一致。
		return ''.join(c)#所有工作模式的算法编写完成，待整合GUI

def whatmode(m):
	hstring = ''.join([str(i) for i in range(10)])+'abcdef'#十六进制集
	intstring = ''.join([str(i)for i in range(10)])
	bstring = '01'
	mode = 2
	if len(m)>100:
		m = m[:100]
	for i in m:
		if i not in bstring:
			if mode<10:mode = 10
			if i not in intstring:
				if mode<16:mode = 16
				if i not in hstring:
					mode = 'unicode'
					break
	return mode 

def mode_change(m,mode_n,algo = None):
	mode_o = whatmode(m)
	if mode_o == mode_n:
		return m		  
	if mode_o == 'unicode':#现在mode_n在这个条件判断通过时，mode_n必定不是unicode
		if algo == 'DES':
			m = Get0bforString(m)
			mode_o = 2	
		if algo == 'RSA':
			m = ''.join(['0'*(5-len(str(ord(ii))))+str(ord(ii)) for ii in m])
			mode_o = 10
	#不转10进制了，16进制与10进制共存也太难了
	if mode_o == 10:#不玩了，10进制与16进制之间太难转换了。	 #不能用4，有时会出现5位数二进制长度为17,4又未必能整除
		m = [bin(int(i))[2:] for i in m]
		#print(m)
		long_diff = [4-len(i) for i in m]
		#print(long_diff)
		m = ['0'*long_diff[i]+m[i] for i in range(len(m))]
		#print(len(m))
		m = ''.join(m)
		mode_o = 2
	
	#! 5位数转二进制会翻车
	elif mode_o == 16:
		m = Get0bforString(m,16)
		mode_o = 2
	if mode_n == 2:
		return m
	if mode_n == 10:
		m = [m[i*4:(i+1)*4] for i in range(len(m)//4)]
		#print(len(m),len(m)//4,len(m)%4)
		m = [str(int(i,mode_o)) for i in m]
		m = ''.join(m )
		return m
	if mode_n == 16:
		m = [m[i*4:(i+1)*4] for i in range(len(m)//4)]
		return ''.join([hex(int(i,mode_o))[2:] for i in m])
	if mode_n == 'unicode':
		if algo == 'RSA':
			m = [m[i*4:(i+1)*4] for i in range(len(m)//4)]
			m = ''.join([str(int(i,mode_o)) for i in m])
			m = [m[i*5:(i+1)*5]	for i in range(len(m)//5)]
			m = [int(i) for i in m]
			return ''.join([chr(i) for i in m])
		m = [m[i*16:(i+1)*16] for i in range(len(m)//16)]
		return ''.join([chr(int(ii,2)) for ii in m])

if __name__=='__main__': 
	k = ''.join([str(i) for i in range(10)])+'abcdef'
	#print(k)
	a = Get0bforString(k,16)
	#print(len(a))
	##print(a)
	C0,D0=PC_1(a)
	#c = [c[i*4:(i+1)*4] for i in range(7)]
	#c = [hex(int(c[i],2)) for i in range(7)]
	##print(c)
	c1 = roll(C0,-1*roll_table[0]).tolist()
	d1 = roll(D0,-1*roll_table[0]).tolist()
	k = PC_2(c1+d1)
	k = [k[i*4:(i+1)*4] for i in range(len(k)//4)]
	k = ''.join([hex(int(k[i],2))[2:] for i in range(len(k))]).upper()
	#print(k)	  