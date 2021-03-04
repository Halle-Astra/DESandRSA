from tkinter import Button,StringVar,Label,Entry,Scrollbar,Tk,Frame,Canvas,Text,LabelFrame
from tkinter.ttk import Treeview
from tkinter import filedialog
from tkinter.messagebox import showinfo
from PIL import ImageTk,Image
from DES import *

class Demo_Frame():
	def __init__(self):
		pass

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
				print('此文件采用utf-8编码')
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

	def getInfo(self,t_ob):
		'''t_ob将组件名称传入'''
		string_key = self.en_key.get()
		string_mes = t_ob.get('0.0','end')[:-1]
		return string_mes,string_key

	def m_change(self,mode,t_ob):
		string_mes,string_key = self.getInfo(t_ob)
		t_ob.delete('0.0','end')
		t_ob.insert('insert',mode_change(string_mes,mode))

	def MD(self):
		self.text_m.delete('0.0','end')

	def CD(self):
		self.text_c.delete('0.0','end')

	def MB(self):
		self.m_change(2,self.text_m)

	def MH(self):
		self.m_change(16,self.text_m)

	def MU(self):
		self.m_change('unicode',self.text_m)

	def CB(self):
		self.m_change(2,self.text_c)

	def CH(self):
		self.m_change(16,self.text_c)
	
	def CU(self):
		self.m_change('unicode',self.text_c)

class DES_Frame(Demo_Frame):
	def __init__(self,root):
		self.root = root
		self.root.resizable(False,False)
		self.mode_new = StringVar()
		self.frame0 = Frame(self.root,width = 100)
		self.frame_m = LabelFrame(self.frame0,text = '明文',font = ('宋体'))
		self.img = Image.open('background.png')			  #密文可以乱码显示，数字化加密不行
		self.canvas = Canvas(self.frame0, width=self.img.size[0],height=self.img.size[1],bd=0, highlightthickness=0)
		self.label = Label(self.frame0  ,text = 'DES加密程序',highlightthickness =2,font = ('楷体',15,'bold'))
		self.btn1 = Button(self.frame_m ,text = 'txt导入',font = ('宋体'),command = self.openmfile)
	
		self.btn_m_b = Button(self.frame_m ,text = '二进制明文',font = ('宋体'),command = self.MB)
		self.btn_m_h = Button(self.frame_m ,text = '十六进制明文',font = ('宋体'),command = self.MH)
		self.btn_m_m = Button(self.frame_m ,text = 'Unicode明文',font = ('宋体'),command = self.MU)
		self.btn_m_clear = Button(self.frame_m,text = '清空明文',font = ('宋体'),command = self.MD)
		self.text_m = Text(self.frame_m ,insertbackground='blue', highlightthickness = 2,font = ('楷体',16,'bold'),width = 60,height = 14)
	
		self.frame_c = LabelFrame(self.frame0,text = '密文',font = ('宋体'))
		self.btn2 = Button(self.frame_c,text = '一键加密',font = ('宋体'),command = self.DES_m2c)
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
		self.btn_de_b = Button(self.frame_de ,text = '一键解密',font = ('宋体'),command = self.DES_c2m)
		self.btn_save_m = Button(self.frame_de ,text = '保存明文',font = ('宋体'),command = self.save_m)
		self.btn_save_c = Button(self.frame_de ,text = '保存密文',font = ('宋体'),command = self.save_c)
		self.scr_m = Scrollbar(self.frame_m,orient = 'vertical',command = self.text_m.yview)
		self.scr_c = Scrollbar(self.frame_c,orient = 'vertical',command = self.text_c.yview)
		self.photo = ImageTk.PhotoImage(self.img) 
		self.canvas.create_image( 0,0,image=self.photo,anchor = 'nw')

		self.width_img1 = 110	
		self.height_img1 = 97
		self.canvas1 = Canvas(self.frame0, width=self.width_img1,height=self.height_img1,bd=0, highlightthickness=0)
		self.img1 = Image.open('img1.jpg')
		self.img1 = self.img1.resize((self.width_img1,self.height_img1))
		self.img1_photo = ImageTk.PhotoImage(self.img1)
		self.canvas1.create_image(0,0,image=self.img1_photo,anchor = 'nw')

		self.frame0.grid()
		self.frame0.columnconfigure(0,weight = 2)
		self.frame0.columnconfigure(1,weight = 1)
		self.frame0.columnconfigure(2,weight = 2)
		self.frame_m.columnconfigure(0,weight = 1)
		self.frame_m.columnconfigure(1,weight = 1)
		self.frame_m.columnconfigure(2,weight = 1)
		self.frame_m.columnconfigure(3,weight = 1)
		self.frame_m.grid(row = 1,column = 0,sticky = 'NSEW',rowspan = 2)
		self.canvas.grid(row = 2,column = 1,sticky = 'NSEW',rowspan = 4,columnspan = 2)
		self.text_m.grid(row = 1,column = 0,sticky = 'N',columnspan = 5)
	
		self.btn1.grid(row = 0,column = 4,sticky = 'NEW')
		self.btn_m_b.grid(row = 0,column = 0,sticky = 'NWE')
		self.btn_m_h.grid(row = 0,column = 1,sticky = 'NWE')
		self.btn_m_m.grid(row = 0,column = 2,sticky = 'NWE')
		self.btn_m_clear.grid(row = 0,column = 3,sticky = 'NEW')
		self.label.grid(row=0,column = 0,sticky = 'NSEW',columnspan = 2)
		self.scr_m.grid(row = 1,column = 4,sticky = 'NSE')

		self.frame_c.columnconfigure(0,weight = 1)
		self.frame_c.columnconfigure(1,weight = 1)
		self.frame_c.columnconfigure(2,weight = 1)
		self.frame_c.columnconfigure(3,weight = 1)
		self.frame_c.columnconfigure(4,weight = 1)
		self.frame_c.columnconfigure(5,weight = 1)
		self.frame_c.grid(row = 3,column = 0,sticky = 'NSEW',rowspan = 2)
		self.text_c.grid(row = 1,column = 0,sticky = 'NSEW',columnspan = 6)
		self.btn2.grid(row = 0,column = 0,sticky = 'NEW')
		self.btn_c_b.grid(row = 0,column = 1,sticky = 'NWE')
		self.btn_c_h.grid(row = 0,column = 2,sticky = 'NWE')
		self.btn_c_m.grid(row = 0,column = 3,sticky = 'NWE')
		self.btn_c_clear.grid(row = 0,column = 4,sticky = 'NWE')
		self.btn_c_file.grid(row = 0,column = 5,sticky = 'NEW')
		self.scr_c.grid(row = 1,column = 5,sticky = 'NSE')

		self.frame_mess.grid(row = 1,column = 1,sticky = 'NEW')
		self.canvas1.grid(row = 1,column = 2,sticky = 'EWS')
		self.frame_key.grid(row = 0,column = 0,sticky = 'NESW')
		self.frame_de.grid(row = 1,column = 0,sticky = 'NEWS')
		self.en_key.grid(row = 0,column = 0,sticky = 'NEW',ipadx = 40)
		self.btn_de_b.grid(row = 0,column = 0,sticky = 'NEWS')
		self.btn_save_m.grid(row = 0,column = 1,sticky = 'NEWS')
		self.btn_save_c.grid(row = 0,column = 2,sticky = 'NEWS')

	def DES_run(self,mode_run):
		if mode_run == 'm2c':
			t_ob_get = self.text_m 
			t_ob = self.text_c 
		elif mode_run == 'c2m':
			t_ob_get = self.text_c
			t_ob = self.text_m 
		string_mes,string_key = self.getInfo(t_ob_get)
		if not string_key:
			string_key = '王精东王'
		c = DES_entire(string_mes,string_key,mode = mode_run)
		t_ob.delete('0.0','end')
		t_ob.insert('insert',c)

	def DES_m2c(self):
		self.DES_run('m2c')

	def DES_c2m(self):
		self.DES_run('c2m')

class RSA_Frame():
	def __init__(self,):
		pass

if __name__=='__main__':
	root = Tk(className = ' DES')
	DES_Frame(root)
	root.mainloop()
