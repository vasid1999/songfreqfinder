from pylab import *
from scipy.io import wavfile
from sys import argv

rate,data=wavfile.read(argv[1])
print("Duration: %.3f s"%(len(data)/float(rate)))

data_chan=split(data.T,len(data[0]))

data0 = data_chan[0][0]/(2**15)
#data1 = data_chan[1][0]/(2**15)

#t=arange(len(data))/float(rate)
#plot(t,data0)
#savefig("waveform.png")
#clf()

wsec=1
wsize=rate*wsec
w=0
freqw=1000
threshold=0.01

while w<len(data0):
	wnext=min(len(data0),w+wsize)
	Ns_imm=wnext-w
	
	dataimm=data0[w:wnext]
	#plot(arange(w,wnext)/float(rate),dataimm)
	#savefig("secsplit/secsplit%d"%(w/wsize))
	#clf()
	
	fftimm=fft(dataimm)/Ns_imm
	
	#fftimmshift=fftshift(fftimm)
	fftimmshifted=fftshift(concatenate((fftimm[:freqw],fftimm[-freqw:])))
	#omega=linspace(-Ns_imm/2,Ns_imm/2,Ns_imm+1)[:-1]
	omega=linspace(-freqw,freqw,2*freqw+1)[:-1]
	
	plot(omega,abs(fftimmshifted))
	print("%d: "%(w/wsize),end="")
	print(omega[where(fftimmshifted>threshold)])
	savefig("stft/stft%d"%(w/wsize))
	clf()
	
	w=wnext
