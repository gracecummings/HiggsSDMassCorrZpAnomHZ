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
    h = tfiles[0].Get('hSDvpT_sfat_gen_corr')
    h1d3 = tfiles[0].Get('hSDvpT_sfat_gen_corr_0eta1d3')
    h2d5 = tfiles[0].Get('hSDvpT_sfat_gen_corr_1d3eta2d5')
    for i,tf in enumerate(tfiles):
        if i == 0:
            h = tf.Get('hSDvpT_sfat_gen_corr')
            h1d3 = tf.Get('hSDvpT_sfat_gen_corr_0eta1d3')
            h2d5 = tf.Get('hSDvpT_sfat_gen_corr_1d3eta2d5')
        else:
            h.Add(tf.Get('hSDvpT_sfat_gen_corr'))
            h1d3.Add(tf.Get('hSDvpT_sfat_gen_corr_0eta1d3'))
            h2d5.Add(tf.Get('hSDvpT_sfat_gen_corr_1d3eta2d5'))
    ptbins = h.GetNbinsX()
    sdbins = h.GetNbinsY()
    ptlist = np.zeros(ptbins)
    avsdlist1d3 = np.zeros(ptbins)
    avsdlist2d5 = np.zeros(ptbins)

    #Draw 2D plot
    p1.Draw()
    p1.cd()
    h.Draw("COLZ")
    h.GetXaxis().SetTitle("pT of AK8 jet closest to higgs mass")
    h.GetYaxis().SetTitle("corr gen soft srop mass")
    h.SetStats(0)
    tc.Modified()

    for i in range(ptbins):
        ptcen = h.GetXaxis().GetBinCenter(i+1)
        events1d3 = 0
        mass1d3   = 0
        massav1d3 = 0

        events2d5 = 0
        mass2d5   = 0
        massav2d5 = 0
        
        for j in range(sdbins):
            sdval   = h.GetYaxis().GetBinCenter(j+1)

            sdevnts1d3 = h1d3.GetBinContent(i+1,j+1)
            sdcont1d3  = sdval*sdevnts1d3
            mass1d3 += sdcont1d3
            events1d3 += sdevnts1d3

            sdevnts2d5 = h2d5.GetBinContent(i+1,j+1)
            sdcont2d5  = sdval*sdevnts2d5
            mass2d5 += sdcont2d5
            events2d5 += sdevnts2d5

        if events1d3 == 0:
            massav1d3 = 0
        else:
            massav1d3 = mass1d3/events1d3

        if events2d5 == 0:
            massav2d5 = 0
        else:
            massav2d5 = mass2d5/events2d5
            
        ptlist[i] = ptcen
        avsdlist1d3[i] = massav1d3
        avsdlist2d5[i] = massav2d5

    mg = ROOT.TMultiGraph()
    tg1d3 = ROOT.TGraph(ptbins,ptlist,avsdlist1d3)
    tg1d3.SetTitle("")
    tg1d3.SetLineColor(ROOT.kBlue)
    tg2d5 = ROOT.TGraph(ptbins,ptlist,avsdlist2d5)
    tg2d5.SetTitle("")
    tg2d5.SetLineColor(ROOT.kRed)
    mg.Add(tg1d3)
    mg.Add(tg2d5)
    tc.cd()
    p2.Draw()
    p2.cd()
    mg.Draw("AL")
    mg.SetTitle("")
    mg.GetXaxis().SetTitle("pT of AK8 jet closest to Higgs mass")
    mg.GetYaxis().SetTitle("average SD mass")
    mg.GetXaxis().SetLimits(ptlist[0],ptlist[-1]+h.GetXaxis().GetBinWidth(1)/2)
    mg.SetMaximum(140)
    mg.SetMinimum(50)
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
    pngname = "mass_plots/"+savdir+"/hSDvpt_sfat_gen_corr.png"
    tc.SaveAs(pngname)  
