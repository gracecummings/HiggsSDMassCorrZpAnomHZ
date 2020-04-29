import ROOT
import glob
import geco_base
import argparse
import os
import numpy as np
from datetime import date

if __name__=="__main__":
    #Set up commandline input
    parser = argparse.ArgumentParser()
    parser.add_argument("-p","--path",type=str,help = "path to files to analyze")
    args = parser.parse_args()

    #gather commandline options
    #path = args.path

    #gather files
    path = 'analysis_output_ZpAnomalon/2020-04-28/'
    files = glob.glob(path+'ZpAnomalonHZ_UFO-Zp*')#3000-ND500-NS1_hists_25000Events.root')

    #Prep for plotting
    cols = geco_base.colsFromPalette(files,ROOT.kBird)
    tfiles = map(lambda f: ROOT.TFile(f),files)
    keys = tfiles[0].GetListOfKeys()
    hnames = map(lambda k : k.GetName(),keys)

    #Prep the pads
    tc = ROOT.TCanvas("tc","canvas",700,900)
    p1 = ROOT.TPad("p1","2d plot",0,0.4,1.0,1.0)
    p1.SetLeftMargin(0.1)
    p1.SetRightMargin(0.1)
    p1.SetBottomMargin(0.1)
    p2 = ROOT.TPad("p2","graph with ave",0,0.0,1.0,0.4)
    p2.SetTopMargin(0.05)
    p2.SetRightMargin(.1)
    p2.SetLeftMargin(0.1)
    p2.SetBottomMargin(0.15)

    
    #for h in hname:
    h = tfiles[0].Get('hSDvpT_sfat_reco_uncorr')
    for i,tf in enumerate(tfiles):
        if i == 0:
            h = tf.Get('hSDvpT_sfat_reco_uncorr')
        else:
            h.Add(tf.Get('hSDvpT_sfat_reco_uncorr'))
        print "Looking at file ",i
        print "Total Events ",h.Integral()
    ptbins = h.GetNbinsX()
    sdbins = h.GetNbinsY()
    ptlist = np.zeros(ptbins)
    avsdlist = np.zeros(ptbins)

    #Draw 2D plot
    p1.Draw()
    p1.cd()
    h.Draw("COLZ")
    h.GetXaxis().SetTitle("pT of AK8 jet closest to higgs mass")
    h.GetYaxis().SetTitle("uncorr reco soft srop mass")
    h.SetStats(0)
    tc.Modified()

    for i in range(ptbins):
        ptcen = h.GetXaxis().GetBinCenter(i+1)
        events = 0
        mass   = 0
        massav = 0
        for j in range(sdbins):
            sdval   = h.GetYaxis().GetBinCenter(j+1)
            sdevnts = h.GetBinContent(i+1,j+1)
            sdcont  = sdval*sdevnts
            mass += sdcont
            events += sdevnts

        if events == 0:
            massav = 0
        else:
            massav = mass/events
            
        ptlist[i] = ptcen
        avsdlist[i] = massav

    tg = ROOT.TGraph(ptbins,ptlist,avsdlist)
    tc.cd()
    p2.Draw()
    p2.cd()
    tg.Draw()
    tg.SetTitle("")
    tg.GetXaxis().SetTitle("pT of AK8 jet closest to Higgs mass")
    tg.GetYaxis().SetTitle("average SD mass")
    tg.GetXaxis().SetLimits(ptlist[0],ptlist[-1]+h.GetXaxis().GetBinWidth(1)/2)
    tc.cd()
    p1.cd()
    
        
    #print type(h)
    #if type(h) is ROOT.TH2F:
    #    print "yes!"

    #Save the Plot
    savdir = str(date.today())
    if not os.path.exists("mass_plots/"+savdir):
        os.makedirs("mass_plots/"+savdir)
    #pngname = "mass_plots/"+savdir+"/"+hname+"_deepdoubleb_optimization.png"
    pngname = "mass_plots/"+savdir+"/hSDvpt_sfat_reco_uncorr.png"
    tc.SaveAs(pngname)  
