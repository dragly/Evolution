from pylab import *
seed(1)
#from scipy.interpolate import interp1d

x = linspace(-10,10,100)

#def func(x):
#	return exp(x)*exp(2*x)

def func(x):
        z = zeros(len(x))
        for i in range(len(x)):
                if x[i] < 0:
                        z[i] = -1
                else:
                        z[i] = 1
        return z

f = func(x)

y = zeros(len(x))
def fourier(x, coefficients):
	global y
	y *= 0
	flip = True
	#y = coefficients[0]*exp(coefficients[1]*x)*exp(coefficients[2]*x)
	for i in range(len(coefficients)/4):
	#	y = coefficients
		y += coefficients[4*i] * cos (coefficients[4*i+1]*x)
		y += coefficients[4*i + 2] * sin(coefficients[4*i + 3]*x)
	if isnan(y).any():
		y = zeros(len(x))
	return y

nFunc = 64
nCoeff = 32
j = int(random()*nCoeff)
		
scaleLimit = 6
scale = 10**scaleLimit

population1 = 10**(random()*20) * random((nFunc,nCoeff)) - 10**(random()*20) * random((nFunc,nCoeff))
population2 = 10**(random()*20) * random((nFunc,nCoeff)) - 10**(random()*20) * random((nFunc,nCoeff))
bestdifference = zeros(nFunc/2)

def gaussrand(x):
	return random(x)

cyclesWithoutImprovement = 0
cyclesWithImprovement = 0
finalbesti = -1
finalbest = inf
finalbest1 = inf
finalbest2 = inf
finalbestPrev = inf
savedLastTime = False
finalbestY = fourier(x, population1[0])
lastWorkingScale = 0.0
nCycles = 2400
requiredPrecision = 4 # at what digit do we need change not to rescale
## Plotting
figure()
hold('on')
## end plotting
for k in range(nCycles):
        # merge the populations once in a while
        if not k % (nCycles / 4):
                print "Merging!"
                k += 1
                temp = population1.copy()
                population1[0:nCoeff/4] = population2[0:nCoeff/4]
                population2[0:nCoeff/4] = temp[0:nCoeff/4]
                continue
        for l in range(2):
                if l == 0:
                        #print "pop1"
                        population = population1
                        finalbest = finalbest1
                else:
                        #print "pop2"
                        population = population2
                        finalbest = finalbest2
                #print "Iteration " + str(k)
                finalbestPrev = finalbest
                # spawn two completely new functions	
                #population[nFunc - 2] = scale * random(nCoeff) - scale * random(nCoeff)
                population[nFunc - 1] = 10**((random()-0.5)*scaleLimit) * (random(nCoeff) -  random(nCoeff))
                for i in range(nFunc/2):
                        y = fourier(x,population[i]) 
                        difference = sum(abs(y - f)) # let's pretend that the first half are the best
                        bestdifference[i] = difference
                        if difference < finalbest:
                                finalbest = difference
                                finalbesti = i
                                finalbestY = y
                #print "Best index first: " + finalbesti
                for i in range(nFunc/2, nFunc): # calculate and compare the second half
                        y = fourier(x,population[i])
                        difference = sum(abs(y - f))
        #		print difference
                        if difference < bestdifference.max():
                                maxi = bestdifference.argmax()
                                bestdifference[maxi] = difference
                                population[maxi] = population[i].copy()
                                if difference < finalbest:
                                        finalbest = difference
                                        finalbesti = maxi
                                        finalbestY = y
                #print "Best index second: " + finalbesti
                # let's mate the best
                for i in range(nFunc/4):
                        #if random() > 0.5:
                        newi = i + nFunc/2
                        #else:
                        #	newi = i + nFunc*3/4
                        #if random() > 0.5:
                #		oldi = 2*i
                #		oldi2 = 2*i + 1
                #	else:
                        oldi = 2*i + 1
                        oldi2 = 2*i
                        for j in range(nCoeff):
                                if random() > 0.5:
                                        population[newi][j] = population[oldi][j] # the first half from even numbered
                                else:		
        #for j in range(nCoeff/2,nCoeff):
                                        population[newi][j]  = population[oldi2][j] # the other half from odd numbered
	#	population[newi+1] = population[newi].copy()
	# mutation for all that were not best
                for i in range(nFunc/2,nFunc):
                        #population[i] = population[besti]# + (gaussrand(nCoeff) - gaussrand(nCoeff))
                        # random gene to change
                        #for jjj in range(int(random()*nCoeff/2)): # change half or a quarter or just one gene?
                        j = int(random()*nCoeff)
                        population[i][j] = population[i][j] + scale * (gaussrand(1) - gaussrand(1))
                        #population[i] = population[i] + (gaussrand(nCoeff) - gaussrand(nCoeff))
                if finalbestPrev - finalbest < 10**(int(log10(finalbest))-requiredPrecision):
                        cyclesWithoutImprovement += 1
                        cyclesWithImprovement = 0
                        #scale += 2* (random() - 0.5) * scale
                        if cyclesWithoutImprovement > nCoeff/4:
                                if not savedLastTime:
                                        lastWorkingScale = scale
                                        savedLastTime = True
                                
                                if cyclesWithoutImprovement > nCoeff/2:
                                        scale = 10**((random()-0.5)*scaleLimit)
                                else:
                                        scale = scale * 2
                                #if cyclesWithoutImprovement > nCoeff:
                                #	scale = lastWorkingScale
                                #	print "Reverted scale"
                                #	cyclesWithoutImprovement = 0
                                
                        else:
                                savedLastTime = False
                else:
                        cyclesWithoutImprovement = 0
                        cyclesWithImprovement += 1
                        #if cyclesWithImprovement > nCoeff/2:
                        #	scale = 10**(random()*log10(finalbest))
                        #	print "Scaling!"
	        #print besti
                if not k % 50:
                    print "Best difference: " + str(finalbest) + " " + str(cyclesWithoutImprovement) + " " + str(cyclesWithImprovement) + " scale: " + str(scale) + " Best index: " + str(finalbesti)

                    plot(x,fourier(x,population[finalbesti]))
                    plot(x,f)
                    savefig("output/pop{0:01d}-frame{1:03d}".format(l, k) + ".png")
                    clf()
                if l == 0:
                        finalbest1 = finalbest
                else:
                        finalbest2 = finalbest

print "Best guess: " + str(finalbesti)
print population[finalbesti]

y = fourier(x,population[finalbesti])

figure()
plot(x,y)
hold('on')
plot(x,f)
show()
