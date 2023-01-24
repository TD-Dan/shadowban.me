import time

from colorama import Fore, Back, Style, init, Cursor
init(autoreset=True)


CSI ='\033[' #Control sequence introducer
OSC ='\033]'
BEL = '\007'

def main():
	print("Foobarh!")
	for n in range(30,38): #30-37
		print(CSI+str(n)+'m'+"Foreground color "+str(n))
	print(CSI+'38'+';2;255;127;0m'+"Text with custom rgb") # wants colors in 0 - 255
	print(CSI+'39'+'m'+"Text with default color")
	print(CSI+'1'+'m'+"Text with bold") # works in windows, not working in mintty
	print(CSI+'4'+'m'+"Text with underline")
	print(CSI+'9'+'m'+"Text with crossout") # works in mintty, not working in windows
	for n in range(40,48): # 40-47
		print(CSI+str(n)+'m'+"Background color "+str(n))
	print(CSI+'48'+';2;255;55;255m'+"Background with custom rgb")  # wants colors in 0 - 255
	print(CSI+'49'+'m'+"Background with default color")
	
	for n in range(90,98):
		print(CSI+str(n)+'m'+"Foreground color bright "+str(n))
		
	for n in range(100,108):
		print(CSI+str(n)+'m'+"Background color bright "+str(n))
	
	#print(BEL+"Annoying noise")
	
	# Works only in mintty (and xterm?):
	print(OSC+"10;"+"#FFFF66\007"+"set foreground color")
	print(OSC+"11;"+"#103366\007"+"set background color")
	print(OSC+"12;"+"#00FF66\007"+"Change terminal cursor color")
	
	print(OSC+"13;"+"#6666FF\007"+"Change terminal mouse (no effect on mintty)")
	print(OSC+"708;"+"#FF0066\007"+"Change terminal border background (no effect on mintty)")
	
	for n in range(0,16):
		rgb = str(10+n*5)+"66"+str(99-n*2)
		print(OSC+"4;"+str(n)+";#"+rgb+"\007"+"Change palette color "+str(n)+" to "+rgb) # wants colors in 00 - ff
		time.sleep(0.1)
	
	#print("\033]11;#00ff80\007",end='')
	#print("\033[48;1;2;4;3m",end='')
	#print("\033]4;1;rgb:88/66/33\a")
	
	print(CSI+'32m'+"foobah")
	
	print(CSI+'0m'+"Reset color") #Note: no effect as colorama autoreset=True
	
	print("foobah")
	return
	

if __name__ == "__main__":
    main()