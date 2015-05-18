import os
import sys

proj = sys.argv[1]
x = 0
lista = []

p = open(proj + ".txt", 'r')
linhas = p.readlines()

for n in linhas:
	l = n.split(',')
	l.pop()
	lista.append(l)
	
profiles = lista[0]
videos = lista[1]
nFs = lista[2]
QPs = lista[3]
sRange = lista[4]
out = "/home/mativi/Results/"
vec = []

f = open (out + "results.csv", 'w')
print >> f, "Video\tQP\tnF\tType\tBitrate\tY-PSNR\tU-PSNR\tV-PSNR\tYUV-PSNR\tTotalTime"
	
def writeOutput(out, name, qp, nf):
	arq = out + name + "_" + qp + "_" + nf + ".txt"
	q = open (arq, 'r')
	text = q.readlines()
	q.close()
	inicioA = [name, qp]
	inicioIPB = [" ", " "]
	flag = 0
	vecA = []
	vecI = []
	vecP = []
	vecB = []
	
	for line in text:
		
		words = line.split()
		
		if (flag == 1 and ' a ' in line):
			flag = 0
			vecA = inicioA + words
		if (flag == 1 and ' i ' in line):
			flag = 0
			vecI = inicioIPB + words
		if (flag == 1 and ' p ' in line):
			flag = 0
			vecP = inicioIPB + words
		if (flag == 1 and ' b ' in line):
			flag = 0
			vecB = inicioIPB + words
		if ('Total Frames' in line):
			flag = 1
		if ('Total Time' in line):
			time = [words[2]]
			vec = vecA + time

	print >> f, "\t".join(vec)
	print >> f, "\t".join(vecI)
	print >> f, "\t".join(vecP)
	print >> f, "\t".join(vecB)
			
def codifica():
	for video in videos:
		for qp in QPs:
			for nf in nFs:
				name = video.split("/")
				name = name[5].split(".")
				name = name[0]
			
				call = "../../HM-16.2/bin/./TAppEncoderStatic -c " + profiles[0] + " -c " + video + " --QP=" + qp + " --SearchRange=" + sRange[0] + " --FramesToBeEncoded=" + nf + " > " + out + name + "_" + qp + "_" + nf + ".txt"
				os.system(call)
				writeOutput(out, name, qp, nf)

codifica()			
f.close()
