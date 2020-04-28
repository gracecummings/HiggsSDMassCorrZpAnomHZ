import ROOT
import argparse
import glob
import geco_base
import os
from datetime import date

parser = argparse.ArgumentParser()

if __name__=='__main__':
    parser.add_argument("-f","--sample",help = "sample file")
    parser.add_argument("-s","--isSig", type=bool,help="is this a signal sample?")
    args = parser.parse_args()

    samp   = args.sample
    is_sig = args.isSig

    #Gather the troops
    ch = ROOT.TChain("TreeMaker2/PreSelection")
    inlist = glob.glob('../RestFrames/sigSamplesCommitf27c357/'+samp+'*.root')
    ch = ROOT.TChain("TreeMaker2/Preselection")
    inlist = glob.glob('sigSamplesCommitf27c357/'+samp+'*.root')
    genzp,gennd,genns = geco_base.massPoints(samp)
    for f in inlist:
        ch.Add(f)
    events = ch.GetEntries()

    #Make OutputFile
    sampname = samp.split(".root")[0]
    outname = sampname+"_hists_"+str(events)+"Events.root"
    if not os.path.exits("analysis_output_ZpAnomalon/"+str(date.today())+"/"):
        os.makedirs("analysis_output_ZpAnomalon/"+str(date.today())+"/")
    outfile = ROOT.TFile("analysis_output_ZpAnomalon/"+str(date.today())+"/"+outname,"RECREATE")

    #Define Histograms
    #softdrop dists for jet closest to higgs mass
    hsfat_reco_uncorr_sd = ROOT.TH1F("hsfat_reco_uncorr_sd","reco uncorr higgs softdrop",28,10,150)
    hsfat_reco_corr_sd   = ROOT.TH1F("hsfat_reco_corr_sd","reco corr higgs softdrop",28,10,150)
    hsfat_gen_uncorr_sd  = ROOT.TH1F("hsfat_gen_uncorr_sd","gen uncorr higgs softdrop",28,10,150)
    hsfat_gen_corr_sd    = ROOT.TH1F("hsfat_gen_corr_sd","gen corr higgs softdrop",28,10,150)

    #softdrop dists for all jets in mass window
    hfat_reco_uncorr_sd = ROOT.TH1F("hfat_reco_uncorr_sd","reco uncorr softdrop",28,10,150)
    hfat_reco_corr_sd   = ROOT.TH1F("hfat_reco_corr_sd","reco corr softdrop",28,10,150)
    hfat_gen_uncorr_sd  = ROOT.TH1F("hfat_gen_uncorr_sd","gen uncorr softdrop",28,10,150)
    hfat_gen_corr_sd    = ROOT.TH1F("hfat_gen_corr_sd","gen corr softdrop",28,10,150)

    #softdrop dists for jet closet to higgs mass and with eta < 1.3
    hsfat_reco_uncorr_sd_0eta1d3 = ROOT.TH1F("hsfat_reco_uncorr_sd_0eta1d3","reco uncorr higgs softdrop eta < 1.3",28,10,150)
    hsfat_reco_corr_sd_0eta1d3   = ROOT.TH1F("hsfat_reco_corr_sd_0eta1d3","reco corr higgs softdrop eta < 1.3",28,10,150)
    hsfat_gen_uncorr_sd_0eta1d3  = ROOT.TH1F("hsfat_gen_uncorr_sd_0eta1d3","gen uncorr higgs softdrop eta < 1.3",28,10,150)
    hsfat_gen_corr_sd_0eta1d3    = ROOT.TH1F("hsfat_gen_corr_sd_0eta1d3","gen corr higgs softdrop eta < 1.3",28,10,150)

    #softdrop dists for all jets in mass window with eta < 1.3
    hfat_reco_uncorr_sd_0eta1d3 = ROOT.TH1F("hfat_reco_uncorr_sd_0eta1d3","reco uncorr softdrop eta < 1.3",28,10,150)
    hfat_reco_corr_sd_0eta1d3   = ROOT.TH1F("hfat_reco_corr_sd_0eta1d3","reco corr softdrop eta < 1.3",28,10,150)
    hfat_gen_uncorr_sd_0eta1d3  = ROOT.TH1F("hfat_gen_uncorr_sd_0eta1d3","gen uncorr softdrop eta < 1.3",28,10,150)
    hfat_gen_corr_sd_0eta1d3    = ROOT.TH1F("hfat_gen_corr_sd_0eta1d3","gen corr softdrop eta < 1.3",28,10,150)

    #soft drop dists for jet closest to higgs mass and with 1.3 <= eta < 2.5
    hsfat_reco_uncorr_sd_1d3eta2d5 = ROOT.TH1F("hsfat_reco_uncorr_sd_1d3eta2d5","reco uncorr h softdrop eta 1.3 - 2.5",28,10,150)
    hsfat_reco_corr_sd_1d3eta2d5   = ROOT.TH1F("hsfat_reco_corr_sd_1d3eta2d5","reco corr higgs softdrop eta 1.3 - 2.5",28,10,150)
    hsfat_gen_uncorr_sd_1d3eta2d5  = ROOT.TH1F("hsfat_gen_uncorr_sd_1d3eta2d5","gen uncorr higgs softdrop eta 1.3 - 2.5",28,10,150)
    hsfat_gen_corr_sd_1d3eta2d5    = ROOT.TH1F("hsfat_gen_corr_sd_1d3eta2d5","gen corr higgs softdrop eta 1.3 - 2.5",28,10,150)

    #soft drop dists for all jets in mass window with 1.3 <= eta < 2.5
    hfat_reco_uncorr_sd_1d3eta2d5 = ROOT.TH1F("hfat_reco_uncorr_sd_1d3eta2d5","reco uncorr softdrop eta 1.3 - 2.5",28,10,150)
    hfat_reco_corr_sd_1d3eta2d5   = ROOT.TH1F("hfat_reco_corr_sd_1d3eta2d5","reco corr softdrop eta 1.3 - 2.5",28,10,150)
    hfat_gen_uncorr_sd_1d3eta2d5  = ROOT.TH1F("hfat_gen_uncorr_sd_1d3eta2d5","gen uncorr softdrop eta 1.3 - 2.5",28,10,150)
    hfat_gen_corr_sd_1d3eta2d5    = ROOT.TH1F("hfat_gen_corr_sd_1d3eta2d5","gen corr softdrop eta 1.3 - 2.5",28,10,150)

    #soft drop mass closest higgs cand vs. pT
    hSDvpT_sfat_reco_uncorr = ROOT.TH2F("hSDvpT_sfat_reco_uncorr","reco uncorr higgs sd vs pt",40,200,1200,28,10,150)
    hSDvpT_sfat_reco_corr = ROOT.TH2F("hSDvpT_sfat_reco_corr","reco corr higgs sd vs pt",40,200,1200,28,10,150)
    hSDvpT_sfat_gen_uncorr = ROOT.TH2F("hSDvpT_sfat_gen_uncorr","gen uncorr higgs sd vs pt",40,200,1200,28,10,150)
    hSDvpT_sfat_gen_corr = ROOT.TH2F("hSDvpT_sfat_gen_corr","gen corr higgs sd vs pt",40,200,1200,28,10,150)

    #soft drop mass all jets in higgs mass window vs. pT
    hSDvpT_fat_reco_uncorr = ROOT.TH2F("hSDvpT_fat_reco_uncorr","reco uncorr sd vs pt",40,200,1200,28,10,150)
    hSDvpT_fat_reco_corr = ROOT.TH2F("hSDvpT_fat_reco_corr","reco corr sd vs pt",40,200,1200,28,10,150)
    hSDvpT_fat_gen_uncorr = ROOT.TH2F("hSDvpT_fat_gen_uncorr","gen uncorr sd vs pt",40,200,1200,28,10,150)
    hSDvpT_fat_gen_corr = ROOT.TH2F("hSDvpT_fat_gen_corr","gen corr sd vs pt",40,200,1200,28,10,150)

    #soft drop mass closest higgs cand vs. pT eta < 1.3
    hSDvpT_sfat_reco_uncorr_0eta1d3 = ROOT.TH2F("hSDvpT_sfat_reco_uncorr_0eta1d3","runcor eta 1.3 h sdvpt",40,200,1200,28,10,150)
    hSDvpT_sfat_reco_corr_0eta1d3 = ROOT.TH2F("hSDvpT_sfat_reco_corr_0eta1d3","reco corr eta 1.3 h sdvpt",40,200,1200,28,10,150)
    hSDvpT_sfat_gen_uncorr_0eta1d3 = ROOT.TH2F("hSDvpT_sfat_gen_uncorr_0eta1d3","gen uncorr eta 1.3 h sdvpt",40,200,1200,28,10,150)
    hSDvpT_sfat_gen_corr_0eta1d3 = ROOT.TH2F("hSDvpT_sfat_gen_corr_0eta1d3","gen corr eta 1.3 h sdvpt",40,200,1200,28,10,150)

    #soft drop mass all jets in higgs mass window vs. pT eta < 1.3
    hSDvpT_fat_reco_uncorr_0eta1d3 = ROOT.TH2F("hSDvpT_fat_reco_uncorr_0eta1d3","reco uncorr eta 1.3 sdvpt",40,200,1200,28,10,150)
    hSDvpT_fat_reco_corr_0eta1d3 = ROOT.TH2F("hSDvpT_fat_reco_corr_0eta1d3","reco corr eta 1.3 sd vs pt",40,200,1200,28,10,150)
    hSDvpT_fat_gen_uncorr_0eta1d3 = ROOT.TH2F("hSDvpT_fat_gen_uncorr_0eta1d3","gen uncorr eta 1.3 sd vs pt",40,200,1200,28,10,150)
    hSDvpT_fat_gen_corr_0eta1d3 = ROOT.TH2F("hSDvpT_fat_gen_corr_0eta1d3","gen corr eta 1.3 sd vs pt",40,200,1200,28,10,150)

        #soft drop mass closest higgs cand vs. pT 1.3 <= eta < 2.5
    hSDvpT_sfat_reco_uncorr_1d3eta2d5 = ROOT.TH2F("hSDvpT_sfat_reco_uncorr_1d3eta2d5","runcor beta h sdvpt",40,200,1200,28,10,150)
    hSDvpT_sfat_reco_corr_1d3eta2d5 = ROOT.TH2F("hSDvpT_sfat_reco_corr_1d3eta2d5","reco corr beta h sdvpt",40,200,1200,28,10,150)
    hSDvpT_sfat_gen_uncorr_1d3eta2d5 = ROOT.TH2F("hSDvpT_sfat_gen_uncorr_1d3eta2d5","guncor 13eta25 h sdvpt",40,200,1200,28,10,150)
    hSDvpT_sfat_gen_corr_1d3eta2d5 = ROOT.TH2F("hSDvpT_sfat_gen_corr_1d3eta2d5","gcorr 13eta25 higgs sdvpt",40,200,1200,28,10,150)

    #soft drop mass all jets in higgs mass window vs. pT 1.3 <= eta < 2.5
    hSDvpT_fat_reco_uncorr_1d3eta2d5 = ROOT.TH2F("hSDvpT_fat_reco_uncorr_1d3eta2d5","runcor 13eta25 sdvpt",40,200,1200,28,10,150)
    hSDvpT_fat_reco_corr_1d3eta2d5 = ROOT.TH2F("hSDvpT_fat_reco_corr_1d3eta2d5","recocorr 1d3eta2d5 sdvpt",40,200,1200,28,10,150)
    hSDvpT_fat_gen_uncorr_1d3eta2d5 = ROOT.TH2F("hSDvpT_fat_gen_uncorr_1d3eta2d5","guncorr 1d3eta2d5 sdvpt",40,200,1200,28,10,150)
    hSDvpT_fat_gen_corr_1d3eta2d5 = ROOT.TH2F("hSDvpT_fat_gen_corr_1d3eta2d5","gcorr 1d3eta2d5 sd vs pt",40,200,1200,28,10,150)


    #Start analysis
    print "beginning event loop"
    for i,event in enumerate(ch):
        if i % 5000 == 0:
            print "analyzing event ",i

        #Gather jets from a desired mass window and eta < 2.5
        #ghcandlist = jetGrabber(ch.GenJetsAK8,ch.GenJetsAK8_softDropMass,20.0,150.0,sd_corrGEN,sd_corrRECO_cen,sd_corrRECO_for)
        #rhcandlist = jetGrabber(ch.JetsAK8Clean,ch.JetsAK8Clean_softDropMass,20.0,150.0,sd_corrGEN,sd_corrRECO_cen,sd_corrRECO_for)

        #Find jet closest to Higgs mass
        if ghcandlist != []:
            sgfat = min(ghcandlist, key = lambda fat: abs(125.0 - fat["sd"]))
            hsfat_gen_uncorr_sd.Fill(sgfat["sd"])
            hSDvpT_sfat_gen_uncorr.Fill(sgfat["v"].Pt(),sgfat["sd"])
            hsfat_gen_corr_sd.Fill(sgfat["sd"]*sgfat["corr"])
            hSDvpT_sfat_gen_corr.Fill(sgfat["v"].Pt(),sgfat["sd"]*sgfat["corr"])
            
            if sgfat["v"].Eta() < 1.3:
                hsfat_gen_uncorr_sd_0eta1d3.Fill(sgfat["sd"])
                hSDvpT_fat_gen_uncorr_0eta1d3.Fill(sgfat["v"].Pt(),sgfat["sd"])
                hsfat_gen_corr_sd_0eta1d3.Fill(sgfat["sd"]*sgfat["corr"])
                hSDvpT_fat_gen_corr_0eta1d3.Fill(sgfat["v"].Pt(),sgfat["sd"]*sgfat["corr"])
            else:
                hsfat_gen_uncorr_sd_1d3eta2d5.Fill(sgfat["sd"])
                hSDvpT_sfat_gen_uncorr_1d3eta2d5.Fill(sgfat["v"].Pt(),sgfat["sd"])
                hsfat_gen_corr_sd_1d3eta2d5.Fill(sgfat["sd"]*sgfat["corr"])
                hSDvpT_sfat_gen_corr_1d3eta2d5.Fill(sgfat["v"].Pt(),sgfat["sd"]*sgfat["corr"])

            for jet in ghcandlist:
                hfat_gen_uncorr_sd.Fill(jet["sd"])
                hfat_gen_corr_sd.Fill(jet["sd"]*jet["corr"])
                hSDvpT_fat_gen_uncorr.Fill(jet["v"].Pt(),jet["sd"])
                hSDvpT_fat_gen_corr.Fill(jet["v"].Pt(),jet["sd"]*jet["corr"])

                if jet["v"].Eta() < 1.3:
                    hfat_gen_uncorr_sd_0eta1d3.Fill(jet["sd"])
                    hfat_gen_corr_sd_0eta1d3.Fill(jet["sd"]*jet["corr"])
                    hSDvpT_fat_gen_uncorr_0eta1d3.Fill(jet["v"].Pt(),jet["sd"])
                    hSDvpT_fat_gen_corr_0eta1d3.Fill(jet["v"].Pt(),jet["sd"]*jet["corr"])
                else:
                    hfat_gen_uncorr_sd_1d3eta2d5.Fill(jet["sd"])
                    hfat_gen_corr_sd_1d3eta2d5.Fill(jet["sd"]*jet["corr"])
                    hSDvpT_fat_gen_uncorr_1d3eta2d5.Fill(jet["v"].Pt(),jet["sd"])
                    hSDvpT_fat_gen_corr_1d3eta2d5.Fill(jet["v"].Pt(),jet["sd"]*jet["corr"])
            
        if rhcandlist != []:
            srfat = min(rhcandlist, key = lambda fat: abs(125.0 - fat["sd"]))
            hsfat_reco_uncorr_sd.Fill(srfat["sd"])
            hSDvpT_sfat_reco_uncorr.Fill(srfat["v"].Pt(),srfat["sd"])
            hsfat_reco_corr_sd.Fill(srfat["sd"]*srfat["corr"])
            hSDvpT_sfat_reco_corr.Fill(srfat["v"].Pt(),srfat["sd"]*srfat["corr"])
            
            if srfat["v"].Eta() < 1.3:
                hsfat_reco_uncorr_sd_0eta1d3.Fill(srfat["sd"])
                hSDvpT_sfat_reco_uncorr_0eta1d3.Fill(srfat["v"].Pt(),srfat["sd"])
                hsfat_reco_corr_sd_0eta1d3.Fill(srfat["sd"]*srfat["corr"])
                hSDvpT_sfat_reco_corr_0eta1d3.Fill(srfat["v"].Pt(),srfat["sd"]*srfat["corr"])
            else:
                hsfat_reco_uncorr_sd_1d3eta2d5.Fill(srfat["sd"])
                hSDvpT_sfat_reco_uncorr_1d3eta2d5.Fill(srfat["v"].Pt(),srfat["sd"])
                hsfat_reco_corr_sd_1d3eta2d5.Fill(srfat["sd"]*srfat["corr"])
                hSDvpT_sfat_reco_corr_1d3eta2d5.Fill(srfat["v"].Pt(),srfat["sd"]*srfat["corr"])

            #Chance of all mass window jets
            for jet in rhcandlist:
                hfat_reco_uncorr_sd.Fill(jet["sd"])
                hfat_reco_corr_sd.Fill(jet["sd"]*jet["corr"])
                hSDvpT_fat_reco_uncorr.Fill(jet["v"].Pt(),jet["sd"])
                hSDvpT_fat_reco_corr.Fill(jet["v"].Pt(),jet["sd"]*jet["corr"])

                if jet["v"].Eta() < 1.3:
                    hfat_reco_uncorr_sd_0eta1d3.Fill(jet["sd"])
                    hfat_reco_corr_sd_0eta1d3.Fill(jet["sd"]*jet["corr"])
                    hSDvpT_fat_reco_uncorr_0eta1d3.Fill(jet["v"].Pt(),jet["sd"])
                    hSDvpT_fat_reco_corr_0eta1d3.Fill(jet["v"].Pt(),jet["sd"]*jet["corr"])
                else:
                    hfat_reco_uncorr_sd_1d3eta2d5.Fill(jet["sd"])
                    hfat_reco_corr_sd_1d3eta2d5.Fill(jet["sd"]*jet["corr"])
                    hSDvpT_fat_reco_uncorr_1d3eta2d5.Fill(jet["v"].Pt(),jet["sd"])
                    hSDvpT_fat_reco_corr_1d3eta2d5.Fill(jet["v"].Pt(),jet["sd"]*jet["corr"])
                 

    outfile.Write()
    outfile.Close()
    sdFile.Close()
                 
