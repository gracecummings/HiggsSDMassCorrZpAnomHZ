import uproot
import pandas
import numpy
import argparse
import glob
import scipy.optimize
import matplotlib.pyplot as plt
#import geco_base
#from datetime import date

def puppiCorrGEN2017(pt):
    corrfac = 1+0.0090283*(pt**(-2*(0.0099852)))-7.30123*(pt**(-1))
    return corrfac

def puppiCorrRECO2017_0eta1v3(pt):
    corrfac = (1.04323417805)+(8.20581677106e-05)*pt+(-2.23790959145e-08)*(pt**2)+(-5.56816212196e-12)*(pt**3)+(-2.42702058503e-17)*(pt**4)+(5.23731618031e-19)*(pt**5)
    return corrfac

def puppiCorrRECO2017_1v3eta2v5(pt):
    corrfac = (1.11549406241)+(-2.01425972518e-05)*pt+(8.36181961894e-09)*(pt**2)+(4.39451437171e-11)*(pt**3)+(1.04302756829e-14)*(pt**4)+(-2.10404344784e-17)*(pt**5)
    return corrfac

def makeJetDF(t,branch):
    fatdf = t.pandas.df([branch,branch+'_softDropMass'])#,branch+'_deepDoubleBDiscriminatorH'])
    fatdf['pt'] = (fatdf[branch+'.fX']**2+fatdf[branch+'.fY']**2)**(1/2)
    fatdf['p3'] = (fatdf[branch+'.fX']**2+fatdf[branch+'.fY']**2+fatdf[branch+'.fZ']**2)**(1/2)
    fatdf['eta'] = numpy.log((fatdf['p3']+fatdf[branch+'.fZ'])/(fatdf['p3']-fatdf[branch+'.fZ']))/2
    return fatdf

def gaussian(x,a,x0,sigma):
    return a*numpy.exp(-(x-x0)**2/(2*sigma**2))

def hist2dAndSdProjections(ptbins,sdbins,ptdf,sddf):
    sdbinwidth        = (sdbins[1]-sdbins[0])
    tobincen          = sdbinwidth/2
    bincens           = list(map(lambda x: x+tobincen,sdbins))
    h, xedges, yedges = numpy.histogram2d(ptdf,sddf,(ptbins,sdbins))
    nentsptbins       = numpy.sum(h,axis=1)#number of eventa in each pT bin
    weightedbins      = numpy.apply_along_axis(lambda sdproj : sdproj*bincens[:-1],1,h)#for each pt bin, mulity sd bin entries by sd bin center
    weightedsums      = numpy.sum(weightedbins,axis=1)
    avsds             = numpy.divide(weightedsums,nentsptbins)#average mass each bin
    maxsdbins_idx     = numpy.argmax(h,axis=1)
    maxsdbins_bincen  = list(map(lambda x: yedges[x]+tobincen,maxsdbins_idx))#bin center for max SD mass per pT bin
    return h,xedges,yedges,maxsdbins_bincen,avsds

def plot2dAndProj(hist,hxedg,hyedg,ptcenters,cenetaproj,foretaproj,histlabel,trendlabel):
    fig,(histsub,maxsub) = plt.subplots(2,1,gridspec_kw={'height_ratios':[3,1]})
    hist = hist.T
    xaxis,yaxis = numpy.meshgrid(hxedg,hyedg)
    histsub.pcolormesh(xaxis,yaxis,hist)
    histsub.set_ylabel(histlabel)
    cendiff = list(map(lambda m : (m - 125)/125,cenetaproj))
    fordiff = list(map(lambda m : (m - 125)/125,foretaproj))
    maxsub.plot(ptcenters[:-1],cendiff,'bo',label = '0 < eta < 1.3')
    maxsub.plot(ptcenters[:-1],fordiff,'go',label = '1.3 <= eta < 2.5')
    maxsub.set_ylabel(trendlabel)
    maxsub.set_xlabel("AK8PUPPI Jet pT")
    maxsub.set_ylim(-.4,0.1)
    maxsub.set_xlim(300,1200)
    #maxsub.legend()
    #plt.show()


parser = argparse.ArgumentParser()

if __name__=='__main__':
    parser.add_argument("-f","--sample",help= "sample file")
    args = parser.parse_args()

    samp = args.sample
    recomass = 20.0
    genmass  = 110.0
    ptcut    = 300.0
    ptmax    = 1200
    ptbinwidth = 20

    path = '../RestFrames/sigSamplesCommitf27c357/'
    files = glob.glob(path+'ZpAnomalonHZ_UFO-Zp*')

    #Make tree arrays
    #for one file
    #f = uproot.open('../RestFrames/sigSamplesCommitf27c357/'+samp)
    #t = f['TreeMaker2']['PreSelection']
    #for multiple
    uproots = list(map(lambda x : uproot.open(x),files))
    trees   = list(map(lambda x : x['TreeMaker2']['PreSelection'],uproots))
    recodfs = list(map(lambda x : makeJetDF(x,'JetsAK8Clean'),trees))
    gendfs  = list(map(lambda x : makeJetDF(x,'GenJetsAK8'),trees))

    #Make the general dataframes
    #for single file
    #recodf = makeJetDF(trees[0],'JetsAK8Clean')
    #gendf  = makeJetDF(trees[0],'GenJetsAK8')
    recodf = pandas.concat(recodfs)
    gendf  = pandas.concat(gendfs)
    
    #Make selections`
    selrecofat    = recodf[(recodf['JetsAK8Clean_softDropMass'] > recomass) & (recodf['pt'] > ptcut) & (numpy.abs(recodf['eta']) < 2.5)]
    selgenfat     = gendf[(gendf['GenJetsAK8_softDropMass'] > genmass) & (gendf['pt'] > ptcut) & (gendf['eta'] < 2.5)]
    recoeta1v3    = selrecofat[numpy.abs(selrecofat['eta']) < 1.3].copy()#makes a new dataframe
    reco1v3eta2v5 = selrecofat[(numpy.abs(selrecofat['eta']) >= 1.3)].copy()
    #geneta1v3     = selgenfat[numpy.abs(selgenfat['eta']) < 1.3].copy()
    #gen1v3eta2v5  = selgenfat[(numpy.abs(selgenfat['eta']) >= 1.3) & (numpy.abs(selgenfat['eta']) < 2.5)].copy()

    #Apply Correcions
    recoeta1v3["corr_softDropMass"] = puppiCorrGEN2017(recoeta1v3["pt"])*puppiCorrRECO2017_0eta1v3(recoeta1v3["pt"])*recoeta1v3['JetsAK8Clean_softDropMass']
    reco1v3eta2v5["corr_softDropMass"] = puppiCorrGEN2017(reco1v3eta2v5["pt"])*puppiCorrRECO2017_1v3eta2v5(reco1v3eta2v5["pt"])*reco1v3eta2v5['JetsAK8Clean_softDropMass']
    recocorr = recoeta1v3.append(reco1v3eta2v5)

    #Binning
    ptbins = list(range(int(ptcut),ptmax,ptbinwidth))
    ptcenters = list(map(lambda x : x+ptbinwidth/2,ptbins))
    sdbins = list(range(20,150,5))
    showh, xedges, yedges  = numpy.histogram2d(selrecofat["pt"],selrecofat["JetsAK8Clean_softDropMass"],(ptbins,sdbins))
    cenh, cxs, cys, csds, cavsds   = hist2dAndSdProjections(ptbins,sdbins,recoeta1v3["pt"],recoeta1v3["JetsAK8Clean_softDropMass"])
    forh, fxs, fys, fsds, favsds   = hist2dAndSdProjections(ptbins,sdbins,reco1v3eta2v5["pt"],reco1v3eta2v5["JetsAK8Clean_softDropMass"])

    showcorrh, xedgescorr, yedgescorr  = numpy.histogram2d(recocorr["pt"],recocorr["corr_softDropMass"],(ptbins,sdbins))
    cencorrh, cxscorr, cyscorr, csdscorr, ccorravs   = hist2dAndSdProjections(ptbins,sdbins,recoeta1v3["pt"],recoeta1v3["corr_softDropMass"])
    forcorrh, fxscorr, fyscorr, fsdscorr, fcorravs   = hist2dAndSdProjections(ptbins,sdbins,reco1v3eta2v5["pt"],reco1v3eta2v5["corr_softDropMass"])

    #Plotting
    #fig = plt.figure()
    #histcanv = fig.add_subplot(111,title='title placeholder',aspect='equal')#This actually finally made the subplot the whole fig

    #plot2dAndProj(showh,xedges,yedges,ptcenters,cavsds,favsds,"soft drop mass","average sd mass")
    plot2dAndProj(showh,xedges,yedges,ptcenters,csds,fsds,"soft drop mass","peak sd mass")
    #plot2dAndProj(showcorrh,xedgescorr,yedgescorr,ptcenters,csdscorr,fsdscorr,"corr sd mass","peak corrsd mass")
    
    #fig,(histsub,maxsub) = plt.subplots(2,1,gridspec_kw={'height_ratios':[3,1]})
    #showh = showh.T
    #xaxis,yaxis = numpy.meshgrid(xedges,yedges)
    #histsub.pcolormesh(xaxis,yaxis,showh)
    #histsub.set_ylabel("soft drop mass")
    #maxsub.plot(ptcenters[:-1],csds,'b',label = '0 < eta < 1.3')
    #maxsub.plot(ptcenters[:-1],fsds,'g',label = '1.3 <= eta < 2.5')
    #maxsub.set_ylabel("peak soft drop mass")
    #maxsub.set_xlabel("AK8PUPPI Jet pT")
    #maxsub.set_ylim(70,130)
    #maxsub.set_xlim(300,1200)
    #maxsub.legend()
    plt.show()
    
    #print(cenh)
    #print(numpy.argmax(cenh,axis=0))#index of max of each column (y bin for max of x bin)
    #print(sdbins)
    #print(cyedges)
    #print(cen_maxbins_val)
    #print(fxedges)
    
    #Playing around with binning the pandas df
    #reco1v3eta2v5["ptbin"] = pandas.cut(reco1v3eta2v5["pt"],ptbins)
    #sd = reco1v3eta2v5["JetsAK8Clean_softDropMass"].groupby(pandas.cut(reco1v3eta2v5["pt"],ptbins))
    #sd = reco1v3eta2v5.groupby(pandas.cut(reco1v3eta2v5["pt"],ptbins))
    
    
    


    


    
    
