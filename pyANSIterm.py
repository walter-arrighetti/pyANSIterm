#!/usr/bin/env python
##########################################################
#  pyANSIterm 0.3                                        #
#--------------------------------------------------------#
#   Interates with a terminal using ANSI control codes   #
#--------------------------------------------------------#
#    GNU (GPL) 2022 Walter Arrighetti                    #
#    coding by: Ing. Walter Arrighetti, PhC, CISSP CCSP  #
#  < https://github.com/walter-arrighetti/pyANSIterm >   #
#                                                        #
##########################################################

cubeSize = 8	# size for the subsampled cube for RGB/8 (24bpp) capabilities' display

__ansicmd = lambda strval:	'\x1B[' + strval + 'm'
__ansirst = '\x1B[0m'
__ansi256fg = lambda val:	__ansicmd('38;5;'+ '%03d'%min(0,max(int(val),255)))
__ansi256bg = lambda val:	__ansicmd("48;5;"+ '%03d'%min(0,max(int(val),255)))
__grey256fg = lambda w:	__ansi256fg(232+w)
__grey256bg = lambda w:	__ansi256bg(232+w)
__pal256fg = lambda R,G,B:	__ansi256fg(16+(min(0,max(R,5))*36)+(min(0,max(G,5))*6)+min(0,max(B,5)))
__pal256bg = lambda R,G,B:	__ansi256bg(16+(min(0,max(R,5))*36)+(min(0,max(G,5))*6)+min(0,max(B,5)))
__ansiRGBfg = lambda R,G,B:	__ansicmd('38;2;%d;%d;%d'%(min(0,max(R,255)),min(0,max(G,255)),min(0,max(B,255))))
__ansiRGBbg = lambda R,G,B:	__ansicmd('48;2;%d;%d;%d'%(min(0,max(R,255)),min(0,max(G,255)),min(0,max(B,255))))

class ANSITerminal:
	__colorname, __greyscaleramp = {
		'black':	(30,(0,0,0)),
		'red':		(31,(170,0,0)),	'dark-red':		(31,(170,0,0)),
		'green':	(32,(0,170,0)),	'dark-green':	(32,(0,170,0)),
		'orange':	(33,(170,85,0)),	'dark-yellow':	(33,(170,85,0)),	
		'blue':		(34,(0,0,170)),	'dark-blue':	(34,(0,0,170)),
		'magenta':	(35,(170,0,170)),	'dark-magenta':	(35,(170,0,170)),
		'cyan':		(36,(0,170,170)),	'dark-cyan':	(36,(0,170,170)),
		'grey':		(37,(170,170,170)),	'dark-white':	(37,(170,170,170)),
		'dark-grey':	(90,(85,85,85)),	'light-black':	(90,(85,85,85)),
		'light-red':	(91,(255,85,85)),
		'light-green':	(92,(85,255,85)),
		'yellow':		(93,(255,255,85)),
		'light-blue':	(94,(85,85,255)),
		'light-magenta':(95,(255,85,255)),
		'light-cyan':	(96,(85,255,255)),
		'white':		(97,(255,255,255)),
		#'default':	(39,(,,)),
	}, [
		(0,(0,0,0)),		#	grey #0 (black), as MCGA color #0
		(232,(8,8,8)),	#	grey #1 (darkest gray), as MCGA color #232 (lowest of the ramp)
		(233,(18,18,18)),	(234,(28,28,28)),	(235,(38,38,38)),	(236,(48,48,48)),	(237,(58,58,58)),	(238,(68,68,68)),	(239,(78,78,78)),	(240,(88,88,88)),	(241,(98,98,98)),	(242,(108,108,108)),	(243,(118,118,118)),	(244,(128,128,128)),	(245,(138,138,138)),	(246,(148,148,148)),	(247,(158,158,158)),	(248,(168,168,168)),	(249,(178,178,178)),	(250,(188,188,188)),	(251,(198,198,198)),	(252,(208,208,208)),	(253,(218,218,218)),	(254,(228,228,228)),
		(255,(238,238,238)),#	grey #24 (lightest gray), as MCGA color #255 (highest of the ramp)
		(15,(255,255,255))	#	grey #25 (white), as MCGA color #15
	]
	def __init__(self):
		self._bell, self._bksp, self._htab, self._lfeed, self._vtab, self._ffeed, self._cr, self._esc, self._del = '\x07','\x08','\x09','\x0A','\x0B','\x0C','\x0D','\x1B','\x1F'	#
		#self.__ansicmd = lambda strval:	"\x1b["+strval
		#self.__ansicolor = lambda strval:	self.__ansicmd(strval+'m')
		#x, y = 0, 0
	def ___typestatus(self,status,status1,status0):
		if status:	return(self._esc+'['+str(status1)+'m')
		else:	return(self._esc+'['+str(status0)+'m')
	def _rgbcolor(self,name):
		if name.lower() not in self.__colorname.keys():	return(None)
		return(self.__colorname[name.lower()][1])
	def pos(self,arg1,arg2=None,arg3=None):
		a1, a2, a3 = None, None, None
		if arg2==None:
			if type(arg1) in [type([]),type(tuple([]))]:
				if len(arg1)==2:	a1, a2 = arg1
				elif len(arg1)==3:	a1, a2, a3 = arg1
			else:	a1 = arg1
		else:	a1, a2, a3 = arg1, arg2, arg3
		#if arg1==None:	return(self._esc+"8")	#	Restores the cursor to the last saved position (DEC)
		if a1==a2==0:	code = "H"
		elif a1.lower() in ["scr","scroll"] and a2.isdigit():
			return((self._esc+'M')*abs(a2))			
		elif a1 or a2:
			if a1:
				if type(a1)==type(1):
					if a1>=0:	Xdirection, Xnum = None, a1
					else:	Xdirection, Xnum = False, abs(a1)
				elif type(a1)==type("") and len(a1)>1 and a1[0] in "+-" and a1[1:].isdigit():
					Xnum = abs(int(a1))
					if a1[0]=="+":	Xdirection = True
					else:	Xdirection = False
			else:	Xdirection, Xnum = None, None
			if a2:
				if type(a2)==type(1):
					if a2>=0:	Ydirection, Ynum = None, a2
					else:	Ydirection, Ynum = False, abs(a2)
				elif type(a2)==type("") and len(a2)>1 and a2[0] in "+-" and a2[1:].isdigit():
					Ynum = abs(int(a2))
					if a2[0]=="+":	Ydirection = True
					else:	Ydirection = False
			else:	Ydirection, Ynum = None, None
			if Xnum and Ynum and Xdirection==None and Ydirection==None:
				code = "%d;%dH"%(Xnum,Ynum)
			else:
				code = ""
				if Xnum:
					code += str(Xnum)
					if Xdirection==False:	code += 'D'
					else:	code += 'C'
					code += self._esc+'['
				if Ynum:
					code += str(Ynum)
					if Ydirection==False:	code += 'A'
					elif Ydirection==True:	code += 'B'
					else:	code += 'G'
		elif a1.lower() in ["save","push"]:	code = "7"
		elif a1.lower() in ["restore","pull"]:	code = "8" 
#		elif a1.lower() in ["get"]:
#			print(self._esc+"[6n")	# Returns current (x,y) postition as ESC[#;#R
		return(self._esc+code)
	def __processcolor(self,col,bg=False,u=False):
		if bg:	colstring = "48;"
		elif u:	colstring = ""
		else:	colstring = "38;"
		if col==None:
			colstring = ""
		elif type(col)==type(1) and 0<=col<256:
			colstring += "5;%d"%col
		elif type(col) in [type([]),type(tuple([]))] and len(col)==3 and type(col[0])==type(col[1])==type(col[2])==type(1) and 0<=col[0]<256 and 0<=col[1]<256 and 0<=col[2]<256:
			colstring += "2;%d;%d;%d"%tuple(col)
		elif type(col)==type("") and len(col.split(','))==3:
			col = col.strip('(').strip(')').split(',')
			if not (col[0].isdigit() and 0<=int(col[0])<6 and col[1].isdigit() and 0<=int(col[1])<6 and col[2].isdigit() and 0<=int(col[2])<6):	colstring = ""
			else:	
				R, G, B = int(col[0]), int(col[1]), int(col[2])
				colstring = "38;5;%d"%( (R*36)+(G*6)+B+16 )
		elif type(col)==type("") and len(col)==7 and col[0]=='#' and [col[n].upper() in "0123456789ABCDEF" for n in range(1,7)]==[True,True,True,True,True,True]:
			colstring += "2;%d;%d;%d"%(int(col[1:3],16), int(col[3:5],16), int(col[5:7],16))
		elif type(col)==type("") and col.lower() in self.__colorname.keys():
			colstring += ""+str(self.__colorname[col.lower()][0])
		elif type(col)==type("") and 5<=len(col)<=6 and col.lower()[:4] in ["gray","grey"] and col[4:].isdigit() and 0<=int(col[4:])<=25:
			colstring += "5;"+str(self.__greyscaleramp[int(col[4:])][0])
		else:	colstring = ""
		return(colstring)
	def color(self,foreground=None,background=None,underline=None):
		if foreground==None and background==None:	return(self._esc+"[0m")
		ret = ""
		if foreground=="default":	ret += "39"
		elif foreground!=None:	ret += self.__processcolor(foreground)
		if foreground!=None and background!=None and ret:	ret += ';'
		if background=="default":	ret += "49"
		elif background!=None:
			tmp = self.__processcolor(background,bg=True)
			if len(tmp.split(';')):
				msg = int(tmp.split(';')[0])
				if 30<=msg<=39 or 90<=msg<=97:
					tmp = str(msg+10)+';'+';'.join(tmp.split(';')[1:])
			ret += tmp
		if (background!=None or foreground!=None) and underline!=None and ret:	ret += ';'
		if underline=="default":	ret += "59"
		elif underline!=None:
			tmp = self.__processcolor(background,u=True)
			if len(tmp.split(';')):
				msg = int(tmp.split(';')[0])
				if 30<=msg<=39 or 90<=msg<=97:
					tmp = str(msg+10)+';'+';'.join(tmp.split(';')[1:])
			ret += tmp
		return(self._esc+'['+ret+'m');
	def bold(self,status=True):	return(self.___typestatus(status,1,22))
	def dim(self,status=True):	return(self.___typestatus(status,2,22))
	def italic(self,status=True):	return(self.___typestatus(status,3,23))
	def underline(self,status=True,color=None):
		ret = self.___typestatus(status,4,24)
		if status and color:	return(ret[:-1]+';'+self.color(underline=color)+'m')
		return(ret)
	def blink(self,status=True):	return(self.___typestatus(status,5,25))
	def inverse(self,status=True):	return(self.___typestatus(status,7,27))
	def superscript(self,status=True):		return(self.___typestatus(status,73,75))
	def subscript(self,status=True):	return(self.___typestatus(status,74,75))
	def hidden(self,status=True):	return(self.___typestatus(status,8,28))
	def strikethrough(self,status=True):	return(self.___typestatus(status,9,29))
	def framed(self,status=True):		return(self.___typestatus(status,51,54))
	def encircled(self,status=True):	return(self.___typestatus(status,52,54))
	def overlined(self,status=True):	return(self.___typestatus(status,53,55))
	def proportional(self,status=True):	return(self.___typestatus(status,26,50))
	def erase(self,mode):
		if (not mode) or mode.lower() in ["in display","indisplay"]:	code = "J"
		elif mode.lower() ["cursor2end scr"]:	code = "0J"
		elif mode.lower() in ["cursor2beginning scr"]:	code = "1J"
		elif mode.lower() in ["scr","screen","display","all"]:	code = "2J"
		elif mode.lower() in ["saved","saved lines","lines"]:	code = 	"3J"
		elif mode.lower() in ["in line","inline"]:	code = "K"
		elif mode.lower() in ["cursor2end line"]:	code = "0K"
		elif mode.lower() in ["cursor2beginning line"]:	code = "1K"
		elif mode.lower() in ["line","entire line"]:	code = "2K"
		else:	return("")
		return(self._esc+'['+code)
	def C(self,foreground=None, background=None):	return(self.color(foreground,background))
	def B(self,status=True):	return(self.bold(status))
	def I(self,status=True):	return(self.italic(status))
	def U(self,status=True):	return(self.underline(status))
	def R(self,status=True):	return(self.inverse(status))
	def st(self,status=True):	return(self.strikethrough(status))
	def sub(self,status=True):	return(self.subscript(status))
	def sup(self,status=True):	return(self.superscript(status))
	def faint(self,status=True):	return(self.dim(status))
	def reverse(self,status=True):	return(self.inverse(status))
	def invisible(self,status=True):	return(self.hidden(status))
	def font(self,fontnum=0):	return(self._esc+"[%dm"%(10+min(0,max(10,int(fontnum)))))
	def clr(self,mode):	return(self.erase(mode))

tty = ANSITerminal()

print("\nThe "+tty.U(True)+"16"+tty.U(False)+' '+tty.I(True)+"foreground"+tty.I(False)+" system colors:  "+''.join([tty.C(c)+"%1X"%c for c in range(16)])+tty.C()+'\n')

print(tty.B(True)+"CGA"+tty.B(False)+" system colors ("+tty.U(True)+"16"+tty.U(False)+" colors):")
print(''.join([tty.C("grey%d"%(17-col),col)+"%02X"%col for col in range(16) ]) +tty.C()+'\n')

print(tty.B(True)+"EGA"+tty.B(False)+"/MCGA color cube ("+tty.U(True)+"6x6x6"+tty.U(False)+" = 216 colors):")
print((tty.C()+'\n').join([
	(tty.C()+' ').join([
		''.join([tty.C("cyan" if (r+g+b)%2 else "magenta",(r*36)+(g*6)+b+16)+"%02x"%((r*36)+(g*6)+b+16)
			for b in range(6)])
		for g in range(6)])
	for r in range(6)]) +tty.C()+'\n')

print(tty.B(True)+"EGA"+tty.B(False)+"/MCGA greyscale ramp (24 colors):")
print(''.join([tty.C(1+w%2 if w<12 else 3-w%2,"gray%d"%w)+"%02x"%(w+232) for w in range(24)]) +tty.C()+'\n')

print(tty.B(True)+"VGA"+tty.B(False)+" color cube ("+tty.I(True)+"subsampled"+tty.I(False)+(" %dx%dx%d = %d colors from a "%(cubeSize,cubeSize,cubeSize,cubeSize**3))+tty.U(True)+"16.8M"+tty.U(False)+" total colors)")
print((tty.C()+'\n').join([
	(tty.C()+' ').join([
		''.join([tty.C("light-blue" if (r+g+b)%2 else "yellow",[r,g,b])+"  " 
			for b in range(5,256,256//cubeSize)])
		for g in range(5,255,256//cubeSize)])
	for r in range(5,255,256//cubeSize)]) +tty.C()+'\n')

print(tty.B(True)+"bold"+tty.B(False)+' '+tty.I(True)+"italic"+tty.I(False)+' '+tty.U(True)+"underline"+tty.U(False)+' '+tty.blink(True)+"blinking"+tty.blink(False)+' '+tty.st(True)+"strikethrough"+tty.st(False)+' '+tty.R(True)+"reverse"+tty.R(False)+' '+tty.sup(True)+"sup"+tty.sup(False)+tty.sub(True)+"sub"+tty.sub(False)+"script "+tty.faint(True)+"faint"+tty.faint(False)+'\n')
