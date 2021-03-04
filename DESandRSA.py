from tkinter import Button,StringVar,Label,Entry,Scrollbar,Tk,Frame,Canvas,Text,LabelFrame,Menu,Message,Toplevel,PhotoImage,messagebox
from tkinter.ttk import Treeview
from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import ImageTk,Image
from DES import *
from sympy import symbols
from random import randint	  
from sys import exit

class Frame_Demo:
	def getfroot(self,mode,t_ob=None): #所以，如果要以open模式调用函数，则一定要给t_ob
		if mode == 'open':
			froot = filedialog.askopenfilenames(title='打开文件', filetypes=[('txt','*.txt'),('All Files', '*')])
			self.frame0 = Frame(root,width = 100)
			t_ob.delete('0.0','end')
		elif mode == 'save':froot = filedialog.asksaveasfilename(title=u'保存文件',filetypes=[('txt','*.txt'),('All Files', '*')])
		return froot

	def get_filewords(self,froot):
		if froot:
			f = open(froot)
			try: 
				t = f.read()
			except:
				f = open(froot,encoding = 'utf-8')
				#print('此文件采用utf-8编码')
				t = f.read()
			f.close()
			return t

	def openmfile(self):
		froot = self.getfroot('open',self.text_m)
		if froot:
			t = self.get_filewords(froot[0])
			self.text_m.insert('insert',t)
	
	def opencfile(self):
		froot = self.getfroot('open',self.text_c)
		if froot:
			t = self.get_filewords(froot[0])
			self.text_c.insert('insert',t)

	def save_m(self):
		froot = self.getfroot('save')
		if froot:
			t = self.text_m.get('0.0','end')
			froot_end = froot.split('/')[-1]
			if '.' not in froot_end:
				froot = froot+'.txt'
			f = open(froot,'w')
			f.write(t)
			f.close()

	def save_c(self):
		froot = self.getfroot('save')
		if froot:
			t = self.text_c.get('0.0','end')
			froot_end = froot.split('/')[-1]
			if '.' not in froot_end :
				froot = froot+'.txt'
			f = open(froot,'w')
			f.write(t)
			f.close()

	def getInfo(self,t_ob,Algo = 'DES'):
		'''t_ob将组件名称传入'''
		if Algo == 'DES':
			string_key = self.en_key.get()
		string_mes = t_ob.get('0.0','end')[:-1]
		if Algo == 'RSA':
			return string_mes
		return string_mes,string_key

	def m_change(self,mode,t_ob,need_return = False,algo = None):
		'''在转换前会再一次调用getInfo以获取文本框的内容
		即，如果要调用此函数做预处理，可以不必先调用一次getInfo'''
		if need_return:
			return mode_change(self.getInfo(t_ob,Algo = 'RSA'),mode,algo = self.algo)
		if not need_return :string_mes,string_key = self.getInfo(t_ob)
		t = mode_change(string_mes,mode ,algo=algo)
		try:
			t_ob.insert('insert',t)
			t_ob.delete('0.0','end')
			t_ob.insert('insert',t)
		except Exception as e:
			messagebox.showerror('错误',f'{e}\n但加密已完成，不妨碍其他编码形式密文且仍可解密')

	def MD(self):
		self.text_m.delete('0.0','end')

	def CD(self):
		self.text_c.delete('0.0','end')

	def MB(self):
		self.m_change(2,self.text_m,algo = self.algo)

	def MT(self):
		self.m_change(10,self.text_m,algo = self.algo)

	def MH(self):
		self.m_change(16,self.text_m,algo = self.algo)

	def MU(self):
		self.m_change('unicode',self.text_m,algo = self.algo)

	def CB(self):
		self.m_change(2,self.text_c,algo = self.algo)

	def CT(self):
		self.m_change(10,self.text_c,algo = self.algo)

	def CH(self):
		self.m_change(16,self.text_c,algo = self.algo)
	
	def CU(self):
		self.m_change('unicode',self.text_c,algo = self.algo)

	def MU_RSA(self):
		self.m_change('unicode',self.text_m,algo = 'RSA')

	def CU_RSA(self):
		self.m_change('unicode',self.text_c,algo = 'RSA')

	def MH_RSA(self):
		self.m_change(16,self.text_m,algo = 'RSA')

class Unit_Frame(Frame_Demo):
	def __init__(self):
		self.frame0 = Frame(self.root)
		self.frame_m = LabelFrame(self.frame0,text = '明文',font = ('宋体')) #密文可以乱码显示，数字化加密不行
		self.canvas = Canvas(self.frame0, width=self.img.size[0],height=self.img.size[1],bd=0, highlightthickness=0)
		self.menu = Menu(self.root)
		self.menu_algo = Menu(self.menu,tearoff = 0)
		self.menu_algo.add_command(label = 'DES',font = (10),command = self.toDES)
		self.menu_algo.add_command(label = 'RSA',font = (10),command = self.toRSA)
		self.menu_algo.add_separator()
		self.menu_algo.add_command(label='Exit',font = (10),command =  self.Exit_All)
		self.menu.add_cascade(label = 'Algorithm',font = (10),menu = self.menu_algo)
		self.menu_illust = Menu(self.menu,tearoff = 0)
		self.menu_illust.add_command(label = 'Tutorial',font = (10),command = self.Tutorial)
		self.menu_illust.add_separator()
		self.menu_illust.add_command(label = 'About',font = (10),command = self.About)
		self.menu.add_cascade(label = 'Tutorial',font = (10),menu = self.menu_illust)
		self.root.config(menu = self.menu)

		self.btn1 = Button(self.frame_m ,text = 'txt导入',font = ('宋体'),command = self.openmfile)
	
		self.btn_m_b = Button(self.frame_m ,text = '二进制明文',font = ('宋体'),command = self.MB)
		self.btn_m_h = Button(self.frame_m ,text = '十六进制明文',font = ('宋体'),command = self.MH)
		self.btn_m_m = Button(self.frame_m ,text = 'Unicode明文',font = ('宋体'),command = self.MU)
		self.btn_m_clear = Button(self.frame_m,text = '清空明文',font = ('宋体'),command = self.MD)
		self.text_m = Text(self.frame_m ,insertbackground='blue', highlightthickness = 2,font = ('楷体',16,'bold'),width = 60,height = 14)
	
		self.frame_c = LabelFrame(self.frame0,text = '密文',font = ('宋体'))
		self.btn2 = Button(self.frame_c,text = '一键加密',font = ('宋体'),command = self.Algo_m2c)
		self.btn_c_b = Button(self.frame_c,text = '二进制密文',font = ('宋体'),command = self.CB)
		self.btn_c_h = Button(self.frame_c,text = '十六进制密文',font = ('宋体'),command = self.CH)
		self.btn_c_m = Button(self.frame_c,text = 'Unicode密文',font = ('宋体'),command = self.CU)
		self.btn_c_clear = Button(self.frame_c,text = '清空密文',font = ('宋体'),command = self.CD)
		self.btn_c_file = Button(self.frame_c,text = 'txt导入',font = ('宋体'),command = self.opencfile)
		self.text_c = Text(self.frame_c,insertbackground='blue', highlightthickness = 2,font = ('楷体',16,'bold'),width = 60,height = 13)
	
		self.frame_mess = Frame(self.frame0)
		self.frame_key = LabelFrame(self.frame_mess,text = '密钥',font = ('宋体'))
		self.frame_de = LabelFrame(self.frame_mess,text = '解密及保存文件',font = ('宋体'))
		self.en_key = Entry(self.frame_key,font = ('楷体',15,'bold'))#手动调宽度
		self.btn_de_b = Button(self.frame_de ,text = '一键解密',font = ('宋体'),command = self.Algo_c2m)
		self.btn_save_m = Button(self.frame_de ,text = '保存明文',font = ('宋体'),command = self.save_m)
		self.btn_save_c = Button(self.frame_de ,text = '保存密文',font = ('宋体'),command = self.save_c)
		self.scr_m = Scrollbar(self.frame_m,orient = 'vertical',command = self.text_m.yview)
		self.scr_c = Scrollbar(self.frame_c,orient = 'vertical',command = self.text_c.yview)
		self.photo = ImageTk.PhotoImage(self.img) 
		self.canvas.create_image( 0,0,image=self.photo,anchor = 'nw')

		self.canvas1 = Canvas(self.frame_mess, width=self.width_img1,height=self.height_img1,bd=0, highlightthickness=0)
		
		self.img1 = self.img1.resize((self.width_img1,self.height_img1))
		self.img1_photo = ImageTk.PhotoImage(self.img1)
		self.canvas1.create_image(0,0,image=self.img1_photo,anchor = 'nw')

	def toDES(self):
		for i in self.frame0.winfo_children():
			i.destroy()
		self.frame0.grid_forget()
		self.frame0.destroy()
		self.root.option_clear()
		DES_Frame(self.root)

	def toRSA(self):
		for i in self.frame0.winfo_children():
			i.destroy()
		self.frame0.grid_forget()
		self.frame0.destroy()
		self.root.option_clear()
		RSA_Frame(self.root)

	def Tutorial(self):
		root_temp = Tk(className = 'Tutorial')
		
		text_about = '''使用教程
本软件包含有DES和RSA加密两种算法。
可以通过左上角菜单中的Algorithm选项选择加密算法。

参数意义请参照《密码学教程》（陈少真 著）
注：尽管两个算法都提供了unicode输出，
但两者在转换成二进制时的补零长度是不同的。
-------------------------------------------------
DES加解密
一键加密与一键解密都是在ECB模式下进行，
密钥默认值已设置为“哈哈哈哈”。
副钥实际上是《密码学教程》中的c0，
ECB与CM模式均不涉及此参数。
在OFB与CFB模式中，均已将s设定为64位。
请正确选择各加密模式与对应的解密模式。
-------------------------------------------------
RSA加解密：
e为加密指数（公钥），d为解密指数（私钥）

!!!解密时请使用正确的e和私钥d，
在仅教学展示时建议点击“固定e”进行示范。

另外，本程序能够测试p，q是否满足条件，
目前测试可用组合为p=3，q=17。'''
		label_tut = Message(root_temp,text = text_about ,font = ('楷体',15))
		btn_tut = Button(root_temp,text = '确定',font = ('楷体',15),command = root_temp.destroy)
		label_tut.grid(row = 0 ,column = 0,sticky = 'NEWS')
		btn_tut.grid(row = 1,column = 0,sticky = 'NEWS')
		root_temp.mainloop()

	def About(self):
		root_about = Tk(className = 'About')
		text_about = '''\t About
Author\t:Halle Astra
Date \t:2019.11.10
Name\t:DES & RSA
Ver\t:2.4
Email\t:halle.wang@qq.com
可愛い女の子が大好きです❀'''
		mes_about = Message(root_about,text = text_about,font = ('楷体',15),width = 260)
		btn_about = Button(root_about,text = '确定',font = ('楷体',15),command = root_about.destroy)
		mes_about.grid(row = 0,column = 0 ,sticky = 'NEWS')
		btn_about.grid(row = 1,column = 0,sticky = 'NEWS')
		root_about.mainloop()

	def Exit_All(self):
		exit(0)

class TLforKeys(Toplevel):
	def __init__(self):
		super().__init__()
		self.geometry('+220+220')
		self.keys_bywin = []
				
		#self.frame_win = Frame(self.win)
		self.info_win_layers = Label(self,text = 'CM层数',font = ('楷体',15))
		self.en_win_layers = Entry(self,font = ('楷体',15))
		self.btn_win_layers = Button(self,text = '确定',font = ('楷体',15),command = self.get_keys_bywin)	 

		#self.frame_win.grid()
		self.info_win_layers.grid(row = 0,column = 0,sticky = 'NEWS')
		self.en_win_layers.grid(row = 0,column = 1,sticky = 'NEWS')
		self.btn_win_layers.grid(row = 1,column = 0,sticky = 'NEWS',columnspan = 2 )

		#self.mainloop()
		#print('win_main_loop is canceled')											  
		
	def get_keys_bywin(self):
		self.cmlayers = self.en_win_layers.get().strip()
		try:
			self.cmlayers = int(self.cmlayers)
			self.labels_win = [Label(self,text = f'密钥{i+1}',font = ('',15)) for i in range(self.cmlayers)]
			self.en_keys_win = [Entry(self,font = ('楷体',15)) for i in range(self.cmlayers)]
			self.btn_win_keys = Button(self,text = '确定并加密',font = ('楷体',15),command = self.eval_keys)
			#self.frame_win.grid_forget()
			for i in range(len(self.labels_win)):
				self.labels_win[i].grid(row = i,column = 0,sticky = 'NEWS')
				self.en_keys_win[i].grid(row = i,column = 1,sticky = 'NEWS')
			self.btn_win_keys.grid(row = self.cmlayers,column = 0,sticky = 'NEWS',columnspan = 2)
		except:
			messagebox.showwarning('警告','您的输入有误，请输入整数')

	def eval_keys(self):
		self.keys_bywin = []
		for i in self.en_keys_win:
			self.keys_bywin.append(i.get().strip())
		self.destroy()


class DES_Frame(Unit_Frame):
	def __init__(self,root):
		self.algo = 'DES'
		self.root = root
		#self.root.geometry('1152x725')
		#self.root.geometry('1160x780')
		self.root.geometry('1160x725')
		self.mode_new = StringVar()
		self.img = Image.open('background.png')	
		self.img1 = Image.open('img1.jpg')
		self.width_img1 = 118	
		self.height_img1 = 106
		#self.height_img1 = 146
		Unit_Frame.__init__(self)
		self.label_img = PhotoImage(file = 'label_background.png')
		self.label = Label(self.frame0  ,text = 'DES加解密程序',highlightthickness =2,font = ('楷体',15,'bold'),image = self.label_img,compound = 'center')
		self.info_key = Label(self.frame_key,text = '密钥',font = ('宋体'))
		self.info_c0 = Label(self.frame_key , text = '副钥',font = ('宋体'))
		self.en_c0 = Entry(self.frame_key,font = ('楷体'))
		self.btn_CBC_m = Button(self.frame_m,text = 'CBC加密',font = ('宋体'),command = self.DES_CBC_m2c)
		self.btn_CFB_m = Button(self.frame_m,text = 'CFB加密',font = ('宋体'),command = self.DES_CFB_m2c)
		self.btn_OFB_m = Button(self.frame_m,text = 'OFB加密',font = ('宋体'),command = self.DES_OFB_m2c)
		self.btn_CM_m = Button(self.frame_m,text = 'CM加密',font = ('宋体'),command = self.DES_CM_m2c)
		self.btn_CBC_c = Button(self.frame_c,text = 'CBC解密',font = ('宋体'),command = self.DES_CBC_c2m)
		self.btn_CFB_c = Button(self.frame_c,text = 'CFB解密',font = ('宋体'),command = self.DES_CFB_c2m)
		self.btn_OFB_c = Button(self.frame_c,text = 'OFB解密',font = ('宋体'),command = self.DES_OFB_c2m)
		self.btn_CM_c = Button(self.frame_c,text = 'CM解密',font = ('宋体'),command = self.DES_CM_c2m)
		self.btn2 = Button(self.frame_m,text = '一键加密',font = ('宋体'),command = self.Algo_m2c)
		self.btn_de_b = Button(self.frame_c ,text = '一键解密',font = ('宋体'),command = self.Algo_c2m)
		self.text_m.config(height = 12)
		self.text_c.config(height = 13)
		self.frame0.grid(row = 0 ,column = 0,sticky = 'NEWS')
		self.frame0.columnconfigure(0,weight = 1)
		self.frame0.columnconfigure(1,weight = 1)
		self.frame0.columnconfigure(2,weight = 1)
		self.frame_m.columnconfigure(0,weight = 1)
		self.frame_m.columnconfigure(1,weight = 1)
		self.frame_m.columnconfigure(2,weight = 1)
		self.frame_m.columnconfigure(3,weight = 1)
		self.frame_m.grid(row = 1,column = 0,sticky = 'NSEW',rowspan = 2)
		self.canvas.grid(row = 2,column = 1,sticky = 'NW',rowspan = 4,columnspan = 2)
		self.text_m.grid(row = 2,column = 0,sticky = 'NESW',columnspan = 5)
		
		self.btn1.grid(row = 0,column = 4,sticky = 'NEW')
		self.btn_m_b.grid(row = 0,column = 0,sticky = 'NWE')
		self.btn_m_h.grid(row = 0,column = 1,sticky = 'NWE')
		self.btn_m_m.grid(row = 0,column = 2,sticky = 'NWE')
		self.btn_m_clear.grid(row = 0,column = 3,sticky = 'NEW')
		self.label.grid(row=0,column = 0,sticky = 'NSEW',columnspan = 3)
		self.scr_m.grid(row = 2,column = 4,sticky = 'NSE')
				 
		self.btn_CBC_m.grid(row = 1,column = 1,sticky = 'NEWS')
		self.btn_CFB_m.grid(row = 1,column = 2,sticky = 'NEWS')
		self.btn_OFB_m.grid(row = 1,column = 3,sticky = 'NEWS')
		self.btn_CM_m.grid(row = 1,column = 4,sticky = 'NEWS')

		self.frame_c.columnconfigure(0,weight = 1)
		self.frame_c.columnconfigure(1,weight = 1)
		self.frame_c.columnconfigure(2,weight = 1)
		self.frame_c.columnconfigure(3,weight = 1)
		self.frame_c.columnconfigure(4,weight = 1)
		self.frame_c.grid(row = 3,column = 0,sticky = 'NSEW',rowspan = 2)
		self.text_c.grid(row = 2,column = 0,sticky = 'NSEW',columnspan = 5)
		self.btn2.grid(row = 1,column = 0,sticky = 'NEW')
		self.btn_c_b.grid(row = 0,column = 0,sticky = 'NWE')
		self.btn_c_h.grid(row = 0,column = 1,sticky = 'NWE')
		self.btn_c_m.grid(row = 0,column = 2,sticky = 'NWE')
		self.btn_c_clear.grid(row = 0,column = 3,sticky = 'NWE')
		self.btn_c_file.grid(row = 0,column = 4,sticky = 'NEW')
		self.scr_c.grid(row = 2,column = 4,sticky = 'NSE')

		self.btn_CBC_c.grid(row = 1,column = 1,sticky = 'NEWS')
		self.btn_CFB_c.grid(row = 1,column = 2,sticky = 'NEWS')
		self.btn_OFB_c.grid(row = 1,column = 3,sticky = 'NEWS')
		self.btn_CM_c.grid(row = 1,column = 4,sticky = 'NEWS')

		self.frame_mess.grid(row = 1,column = 1,sticky = 'NEW',columnspan = 2)
		self.canvas1.grid(row = 0,column = 1,sticky = 'WS',rowspan = 2)
		self.frame_key.grid(row = 0,column = 0,sticky = 'NESW')
		self.frame_de.grid(row = 1,column = 0,sticky = 'NEWS')
		self.info_key.grid(row = 0 ,column = 0 ,sticky = 'NEWS')
		self.en_key.grid(row = 0,column = 1,sticky = 'NEW')#,ipadx = 30)
		self.info_c0.grid(row = 1 ,column = 0 ,sticky = 'NEWS')
		self.en_c0.grid(row = 1,column = 1 ,sticky = 'NEWS')
		self.btn_de_b.grid(row = 1,column = 0,sticky = 'NEWS')
		self.btn_save_m.grid(row = 0,column = 1,sticky = 'NEWS')
		self.btn_save_c.grid(row = 0,column = 2,sticky = 'NEWS')
		self.root.resizable(False,False)															  
		#self.root.resizable(True,True)

	def DES_run(self,mode_run,mode_work = 'ECB'):
		if mode_run == 'm2c':
			t_ob_get = self.text_m 
			t_ob = self.text_c 
		elif mode_run == 'c2m':
			t_ob_get = self.text_c
			t_ob = self.text_m 
		if mode_work!='ECB':
			c0_string = self.en_c0.get().strip()
			if not c0_string :
				if mode_work!='CM':		 #CM模式加密不涉及c_0
					messagebox.showwarning('警告','请输入副钥c0')
		string_mes,string_key = self.getInfo(t_ob_get)
		if mode_work=='CM':
			tlkeys = TLforKeys()
			self.root.wait_window(tlkeys)
			string_key = tlkeys.keys_bywin 
			del tlkeys
		if not string_key:
			string_key = '哈哈哈哈'
		if mode_work == 'ECB':
			c = DES_entire(string_mes,string_key,mode = mode_run)
		elif mode_work != 'ECB':
			c = DES_entire(string_mes,string_key ,mode = mode_run,mode_work = mode_work,c_0 = c0_string)
		t_ob.delete('0.0','end')
		t_ob.insert('insert',c)

	def Algo_m2c(self):
		'''这个本该命名为DES_ECB_m2c的，这是默认的加密方式'''
		self.DES_run('m2c')

	def Algo_c2m(self):
		'''这个本该命名为DES_ECB_c2m的，这是默认的解密方式'''
		self.DES_run('c2m')

	def DES_CBC_m2c(self):
		self.DES_run('m2c','CBC')

	def DES_CFB_m2c(self):
		self.DES_run('m2c','CFB')

	def DES_OFB_m2c(self):
		self.DES_run('m2c','OFB')

	def DES_CM_m2c(self):
		self.DES_run('m2c','CM')

	def DES_CBC_c2m(self):
		self.DES_run('c2m','CBC')

	def DES_CFB_c2m(self):
		self.DES_run('c2m','CFB')

	def DES_OFB_c2m(self):
		self.DES_run('c2m','OFB')

	def DES_CM_c2m(self):
		self.DES_run('c2m','CM')

class RSA:
	def GetIntforString(self,m):
		'''以5位为长度补零'''
		return ''.join(['0'*(5-len(str(ord(ii))))+str(ord(ii)) for ii in m])

	def isprime(self,num):
		flag = 1
		for i in range(2,num):
			if num//i:
				flag = 0
				break
		if flag:return True
		else :return False

	def DevideinGcd(self,a,b):
		m1 = min(a,b)
		m2 = max(a,b)
		a = m2;b = m1
		del m1,m2
		q = [];r = [a,b]
		while r[-1]!=0:
			q.append(r[-2]//r[-1])
			r.append(r[-2]%r[-1])
		return q,r

	def gcd(self,a,b):
		#print(a,b)
		m = min(a,b)
		res = 0
		for i in range(1,m+1):
			if a%i==0 and b%i==0:
				res = i
		return res

	def gcd_by_devide(self,a,b):
		q,r = DevideinGcd(a,b)
		return r[-2]

	def get_d(self,phi,e):
		q,r = self.DevideinGcd(phi,e)
		#print(q,r)
		R = []
		for i in range(len(r)-2):
			R.append(f'r_{-1-i}=r_{-1-2-i}/r_{-1-1-i}*q_{-1-i}')
		if len(r)<=3:
			return e
		R = R[1:]#只变换到r_-2
		for i in range(len(R)-1):
			R[-2-i] = R[-2-i].replace(R[-1-i].split('=')[0],f"({R[-1-i].split('=')[1]})")
			if i != 0:
				R[-2-i] = R[-2-i].replace(R[-i].split('=')[0],f"({R[-i].split('=')[1]})")
		R = R[0].replace('-','').replace('/','-')
		r_keys = [f'r_{i}' for i in range(1,len(r)-2+1)]
		r_values = [r[-1*int(i.split('_')[1])] for i in r_keys]
		for i in range(len(r_keys)):
			R = R.replace(r_keys[i],str(r_values[i]))
		for j in range(1,len(q)+1):
			R = R.replace(f'q_{j}',str(q[-j]))#等待做符号运算
		R = R[2:]
		R = R.replace(f'r_{len(r)-1}','r_small').replace(f'r_{len(r)}','r_large')
		r_small ,r_large = eval(f"symbols('r_small r_large')")
		y = eval(R)#自动按下标排列，可能出现负系数的情况，常数项放最后
		y = str(y)
		split_for_small = '*'+str(r_small)
		split_for_large = '*'+str(r_large)
		if split_for_small not in y:
			split_for_small = 'r_small'
		if split_for_large not in y:
			split_for_large = 'r_large'		  
		#print(y)
		coe_small = y.split(split_for_small)[0].split(split_for_large)[1].strip()	#因为e肯定小，所以这个的系数就是我们要的模逆元 ,这行经常出错啊
		coe_large = y.split(split_for_large)[0].strip()
		if coe_small == '-':
			coe_small = -1
		elif coe_small == '':
			coe_small = 1
		else:coe_small = eval(coe_small)
		if coe_large == '-':
			coe_large = -1
		elif coe_large == '':
			coe_large = 1
		else:coe_large = eval(coe_large)

		if coe_small < 0:
			coe_small = coe_small+phi
		if coe_large < 0:
			coe_large = coe_large+phi
		return coe_small	#得到d

	def get_e(self,phi):
		if self.e_isRandom==True:
			e = randint(2,phi-1)
			count = 0
			while self.gcd(e,phi)!=1 or self.get_d(phi,e)==e:
				count += 1
				if count == 40:#之后做个，如果e等于0，则停止算法，直接return
					messagebox.showwarning('警告','未寻找到合适的加密指数，算法已停止，请尝试更换p，q')
					e = 0
					break
				e = randint(2,phi-1)
			return e
		else:
			e = self.get_entry(self.e_elect)
			if e == '':
				messagebox.showinfo('提示','未设置e，请先使用随机模式')
				return 0
			#if self.gcd(self.e,phi)==1 or self.e*self.e+1 == phi:
			if self.gcd(e ,phi)!=1 or self.get_d(phi,e)==e:
				messagebox.showwarning('警告','e不满足要求，请重新设置')
			return e

	def QuickMode(self,alpha,a):
		'''快速模逆运算，alpha**a'''
		precal = [alpha]
		a = bin(a)[2:]
		a_ls = [(2**i)*int(a[-1-i]) for i in range(len(a))]
		for i in range(len(a)):
			precal.append((precal[i]**2)%self.n)
		res = 1 
		for i in range(len(a)):
			res = (res*(precal[i])**int(a[-1-i]))%self.n
		return 	res

	def show_all_e(self):
		res = []
		for e in range(2,self.phi):
			if self.gcd(e,self.phi)!=1 :
				res.append(str(e))
		'''
		res_t = ' '.join(res[:12])
		if len(res)>12:
			res = res_t+'\n'+' '.join(res[12:])
		else:res = rest_t
		self.e_optional_disp['text'] = res
		if '\n' in res:
			self.text_c.config(height = 18)
		else:
			self.text_c.config(height = 16)
			'''
		res = ' '.join(res)
		if len(res)>12:
			self.e_optional_disp.config(font = ('楷体',10))
		else:
			self.e_optional_disp.config(font = ('楷体'))
		self.e_optional_disp['text']=res
		
class RSA_Frame(Unit_Frame,RSA):
	def __init__(self,root):
		self.algo = 'RSA'
		self.root = root
		#self.root.geometry('1180x838')
		#self.root.geometry('1148x816')
		#self.root.geometry('1200x863')
		self.root.geometry('1176x820')
		self.e_isRandom = True
		self.img = Image.open('RSA_bg.png')	
		self.img1 = Image.open('img1.jpg')
		self.width_img1 = 110	
		self.height_img1 = 97
		Unit_Frame.__init__(self)
		self.label_img = PhotoImage(file = 'label_background_RSA.png')
		self.label = Label(self.frame0  ,text = 'RSA加解密程序',highlightthickness =2,font = ('楷体',15,'bold'),image = self.label_img,compound = 'center')
		self.frame_key['text'] = '公密钥生成参数'
		self.frame_info = LabelFrame(self.frame_mess,text = '公钥与密钥',font=('宋体'))
		self.e_optional = Label(self.frame_info ,text = 'e可选值:',font=('楷体'),width = 8)
		self.e_optional_disp = Label(self.frame_info,font = ('楷体'))
		self.e_elect_info = Label(self.frame_key ,text = 'e的值为',font = ('楷体',15))
		self.e_elect = Entry(self.frame_key,font = ('楷体',15,'bold'),width = 18)#用于选定e
		self.e_elect_btn = Button(self.frame_key,text = '固定e',font = ('宋体'),command = self.e_Elect)
		self.e_random_btn = Button(self.frame_key,text = '随机e',font = ('宋体'),command = self.e_Random) 
		self.d_info = Label(self.frame_info,text = 'd私钥为:',font = ('楷体',15))#展示私钥
		self.d_disp = Entry(self.frame_info,font = ('楷体',15,'bold'),width = 10)
		self.c2m_long_info = Label(self.frame_info,text = '补零阈值:',font = ('楷体',15))
		self.c2m_long_disp = Entry(self.frame_info,font = ('楷体',15,'bold'),width = 10 )
		
		self.en_p1 = Entry(self.frame_key,font = ('楷体',15,'bold'))#输入p
		self.en_p2 = Entry(self.frame_key,font = ('楷体',15,'bold'))#输入q	 ,这两个的大小即使设定了也是由当前frame下的最后一个决定
		self.label_p1 = Label(self.frame_key,text = '请输入p',font = ('楷体',15))
		self.label_p2 = Label(self.frame_key,text = '请输入q',font = ('楷体',15))
		self.btn_m_t = Button(self.frame_m,text = '十进制明文',font = ('宋体'),command = self.MT)
		self.btn_c_t = Button(self.frame_c,text = '十进制密文',font = ('宋体'),command = self.CT)
		self.btn_m_m['command'] = self.MU_RSA
		self.btn_c_m['command'] = self.CU
		self.btn_m_h['command'] = self.MH_RSA
		
		self.text_m.config(height = 16)
		self.text_c.config(height = 16)

		self.p = 0
		self.q = 0
		self.n = 0
		self.phi = 0
		self.e = 0
		self.d = 0

		self.text_m.grid()
		self.text_c.grid()

		self.frame0.grid(row = 0,column = 0 ,sticky = 'NEWS')
		self.frame0.columnconfigure(0,weight = 1)
		self.frame0.columnconfigure(1,weight = 1)
		self.frame0.columnconfigure(2,weight = 1)
		self.frame_m.columnconfigure(0,weight = 1)
		self.frame_m.columnconfigure(1,weight = 1)
		self.frame_m.columnconfigure(2,weight = 1)
		self.frame_m.columnconfigure(3,weight = 1)
		self.frame_m.grid(row = 1,column = 2,sticky = 'NSEW',rowspan = 2)
		self.canvas.grid(row = 2,column = 0,sticky = 'NE',rowspan = 4)
		self.text_m.grid(row = 1,column = 0,sticky = 'NEWS',columnspan = 5)
	
		self.btn1.grid(row = 0,column = 4,sticky = 'NEW')
		self.btn_m_b.grid(row = 0,column = 0,sticky = 'NWE')
		self.btn_m_t.grid(row = 0,column = 1,sticky = 'NWE')
		#self.btn_m_h.grid(row = 0,column = 2,sticky = 'NWE')
		self.btn_m_m.grid(row = 0,column = 2,sticky = 'NWE')
		self.btn_m_clear.grid(row = 0,column = 3,sticky = 'NEW')
		self.label.grid(row=0,column = 0,sticky = 'NSEW',columnspan = 3)
		self.scr_m.grid(row = 1,column = 4,sticky = 'NSE')

		self.frame_c.columnconfigure(0,weight = 1)
		self.frame_c.columnconfigure(1,weight = 1)
		self.frame_c.columnconfigure(2,weight = 1)
		self.frame_c.columnconfigure(3,weight = 1)
		self.frame_c.columnconfigure(4,weight = 1)
		#self.frame_c.columnconfigure(5,weight = 1)
		self.frame_c.grid(row = 3,column = 2,sticky = 'NSEW',rowspan = 3)
		self.text_c.grid(row = 1,column = 0,sticky = 'NSEW',columnspan = 6)
		self.btn2.grid(row = 0,column = 0,sticky = 'NEW')
		self.btn_c_b.grid(row = 0,column = 1,sticky = 'NWE')
		self.btn_c_t.grid(row = 0,column = 2,sticky = 'NWE')
		#self.btn_c_h.grid(row = 0,column = 3,sticky = 'NWE')
		self.btn_c_m.grid(row = 0,column = 3,sticky = 'NWE')
		self.btn_c_clear.grid(row = 0,column = 4,sticky = 'NWE')
		self.btn_c_file.grid(row = 0,column = 5,sticky = 'NEW')
		self.scr_c.grid(row = 1,column = 5,sticky = 'NSE')
		
		self.frame_mess.grid(row = 1,column = 0,sticky = 'NE')
		self.frame_key.grid(row = 0,column = 0,sticky = 'NEW')
		#self.canvas1.grid(row = 1,column = 0,sticky = 'EWS')
		self.label_p1.grid(row = 0,column = 0,sticky = 'NW')
		self.label_p2.grid(row = 1,column = 0,sticky = 'NW')
		self.en_p1.grid(row = 0,column = 1,sticky = 'NEW',columnspan = 3)
		self.en_p2.grid(row = 1,column = 1,sticky = 'NEW',columnspan = 3)
		self.frame_info.grid(row = 1,column = 0,sticky = 'NEWS')
		self.frame_de.grid(row = 2,column = 0,sticky = 'NEWS')
		self.e_elect_info.grid(row = 2,column = 0,sticky = 'NEWS')
		self.e_elect.grid(row = 2,column = 1,sticky = 'NEWS')
		self.e_elect_btn.grid(row = 2,column = 2,sticky = 'NEWS')
		self.e_random_btn.grid(row = 2,column = 3,sticky = 'NEWS')
		self.e_optional.grid(row = 0,column = 0,sticky = 'NWS')
		self.e_optional_disp.grid(row = 0,column = 1,sticky = 'NEWS',columnspan = 3)
		self.d_info.grid(row = 1,column = 0,sticky = 'NEWS')
		self.d_disp.grid(row = 1,column = 1,sticky = 'NWS')
		self.c2m_long_info.grid(row = 1,column = 2,sticky = 'NWS')
		self.c2m_long_disp.grid(row = 1,column = 3,sticky = 'NWS')
		self.btn_de_b.grid(row = 0,column = 0,sticky = 'NEWS')
		self.btn_save_m.grid(row = 0,column = 1,sticky = 'NEWS')
		self.btn_save_c.grid(row = 0,column = 2,sticky = 'NEWS')
		self.root.resizable(False,False)
	
	def get_entry(self,en_ob):
		'''用于得到p,q'''
		p_temp = en_ob.get().strip(' ')
		#print('p_temp为',p_temp)
		if p_temp!='':
			p = eval(p_temp)
			return p
		return p_temp

	def RSA_run(self,mode = 'm2c',long = 1,c2m_long = 1):
		'''long为每次加密的长度,还原时以5个5个为一组还原'''
		self.p = self.get_entry(self.en_p1)
		self.q = self.get_entry(self.en_p2)
		self.n = self.p*self.q
		self.phi = (self.p-1)*(self.q-1)
		self.show_all_e()

		if mode == 'm2c':
			self.e = self.get_e(self.phi)
			##print('e的取值为',self.e)
			self.e_elect.delete(0,'end')
			self.e_elect.insert(0,str(self.e))
			self.d = self.get_d(self.phi,self.e)
			self.d_disp.delete(0,'end')
			self.d_disp.insert(0,str(self.d))
			if self.e==0:
				return -1
			#m = self.getInfo(self.text_m,Algo = 'RSA')	#因为下面调用m_change,这行会被其内部重新实现
			m = self.m_change('unicode',self.text_m,need_return = True)
			if m:
				m = self.GetIntforString(m)
				m_temp = m
				m = [int(m[long*i:long*(i+1)]) for i in range(len(m)//long)]
				#print('检查明文 ',m)
				if len(m_temp)%long:
					m_res = '0'*(long-(len(m_temp)%long))
					m = m_res
				if self.e!=0 and self.n!=0:
					c = [self.QuickMode(ii,self.e) for ii in m]
					#print('检查密文\t',c)
					#print('检查密文长度\t',[len(str(ii)) for ii in c])
					c2m_long = self.get_entry(self.c2m_long_disp)
					if not c2m_long:
						c2m_long = max([len(str(ii)) for ii in c])
					self.c2m_long_disp.delete(0,'end')
					self.c2m_long_disp.insert(0,str(c2m_long))
					c = ['0'*(c2m_long-len(str(ii)))+str(ii) for ii in c]
					c = ''.join(c )
					self.text_c.delete('0.0','end')
					self.text_c.insert('insert',c)
				else:messagebox.showinfo('提示','未正确设置p,q，请先设置相关参数')
		if mode == 'c2m':	  
			self.d = self.get_entry(self.d_disp)
			#c = self.getInfo(self.text_c,Algo = 'RSA')		#理由同加密
			c2m_long = self.get_entry(self.c2m_long_disp)
			if not c2m_long:
				messagebox.showinfo('提示','请设置解密间隔')
			c = self.m_change(10,self.text_c,need_return = True)
			if c:
				self.c2m_long_disp.delete(0,'end')
				self.c2m_long_disp.insert(0,str(c2m_long))
				c = [c[i*c2m_long:(i+1)*c2m_long] for i in range(len(c)//c2m_long)]
				m = [self.QuickMode(int(ii),self.d) for ii in c]
				m = ''.join([str(ii) for ii in m])
				self.text_m.delete('0.0','end')
				self.text_m.insert('insert',m)

	def Algo_m2c(self):
		try:
			self.RSA_run(mode = 'm2c')
		except:
			return -1

	def Algo_c2m(self):
		try:
			self.RSA_run(mode = 'c2m')
		except:
			return -1

	def e_Elect(self):
		self.e_isRandom = False
	
	def e_Random(self):
		self.e_isRandom = True

class Begin_Frame:
	def __init__(self,root):
		self.root = root
		DES_Frame(self.root)

if __name__=='__main__':
	root = Tk(className = ' DES & RSA')
	root.iconbitmap('icon.ico')
	Begin_Frame(root)
	root.mainloop()
