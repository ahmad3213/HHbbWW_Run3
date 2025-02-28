import awkward as ak
from coffea.nanoevents import NanoEventsFactory, NanoAODSchema
import numpy as np
import uproot
from coffea.nanoevents.methods import vector


def update_outfile(EventProcess, outfile):
    isMC = EventProcess.isMC
    doSF = EventProcess.doSF
    debug = EventProcess.debug
    print("Creating save dicts")
    underflow_value = -999999.0
    underflow_value = 0.0

    events = EventProcess.events
    muons = events.Muon
    electrons = events.Electron
    ak4_jets = events.Jet
    ak8_jets = events.FatJet
    ak8_subjets = events.SubJet

    events_double = events[(events.Double_Signal | events.Double_Fake)]
    events_single = events[(events.Single_Signal | events.Single_Fake)]

    muons_double = muons[(events.Double_Signal | events.Double_Fake)]
    muons_single = muons[(events.Single_Signal | events.Single_Fake)]

    electrons_double = electrons[(events.Double_Signal | events.Double_Fake)]
    electrons_single = electrons[(events.Single_Signal | events.Single_Fake)]

    ak4_jets_double = ak4_jets[(events.Double_Signal | events.Double_Fake)]
    ak4_jets_single = ak4_jets[(events.Single_Signal | events.Single_Fake)]

    ak8_jets_double = ak8_jets[(events.Double_Signal | events.Double_Fake)]
    ak8_jets_single = ak8_jets[(events.Single_Signal | events.Single_Fake)]

    ak8_subjets_double = ak8_subjets[(events.Double_Signal | events.Double_Fake)]
    ak8_subjets_single = ak8_subjets[(events.Single_Signal | events.Single_Fake)]


    muons_double["px"] = muons_double.px; muons_double["py"] = muons_double.py; muons_double["pz"] = muons_double.pz; muons_double["energy"] = muons_double.energy
    muons_double_pre = muons_double[(muons_double.preselected)]; muons_double_fake = muons_double[(muons_double.fakeable)]; muons_double_tight = muons_double[(muons_double.tight)]
    muons_single["px"] = muons_single.px; muons_single["py"] = muons_single.py; muons_single["pz"] = muons_single.pz; muons_single["energy"] = muons_single.energy
    muons_single_pre = muons_single[(muons_single.preselected)]; muons_single_fake = muons_single[(muons_single.fakeable)]; muons_single_tight = muons_single[(muons_single.tight)]

    electrons_double["px"] = electrons_double.px; electrons_double["py"] = electrons_double.py; electrons_double["pz"] = electrons_double.pz; electrons_double["energy"] = electrons_double.energy
    electrons_double_pre = electrons_double[(electrons_double.preselected)]; electrons_double_fake = electrons_double[(electrons_double.fakeable)]; electrons_double_tight = electrons_double[(electrons_double.tight)]
    electrons_single["px"] = electrons_single.px; electrons_single["py"] = electrons_single.py; electrons_single["pz"] = electrons_single.pz; electrons_single["energy"] = electrons_single.energy
    electrons_single_pre = electrons_single[(electrons_single.preselected)]; electrons_single_fake = electrons_single[(electrons_single.fakeable)]; electrons_single_tight = electrons_single[(electrons_single.tight)]

    ak4_jets_double["px"] = ak4_jets_double.px; ak4_jets_double["py"] = ak4_jets_double.py; ak4_jets_double["pz"] = ak4_jets_double.pz; ak4_jets_double["energy"] = ak4_jets_double.energy
    ak4_jets_double_cleaned = ak4_jets_double[(ak4_jets_double.cleaned_double)]
    ak4_jets_single["px"] = ak4_jets_single.px; ak4_jets_single["py"] = ak4_jets_single.py; ak4_jets_single["pz"] = ak4_jets_single.pz; ak4_jets_single["energy"] = ak4_jets_single.energy
    ak4_jets_single_cleaned = ak4_jets_single[(ak4_jets_single.cleaned_single)]
    ak4_jets_double_cleaned = ak.pad_none(ak4_jets_double_cleaned, 4)
    ak4_jets_single_cleaned = ak.pad_none(ak4_jets_single_cleaned, 4)

    ak8_jets_double_cleaned = ak8_jets_double[(ak8_jets_double.cleaned_double)]
    ak8_jets_single_cleaned = ak8_jets_single[(ak8_jets_single.cleaned_single)]
    ak8_jets_double_cleaned = ak.pad_none(ak8_jets_double_cleaned, 1)
    ak8_jets_single_cleaned = ak.pad_none(ak8_jets_single_cleaned, 1)

    ak8_jets_double_cleaned_sorted = ak8_jets_double_cleaned[ak.argsort(ak8_jets_double_cleaned.pt, axis=1, ascending=False)]
    ak8_jets_single_cleaned_sorted = ak8_jets_single_cleaned[ak.argsort(ak8_jets_single_cleaned.pt, axis=1, ascending=False)]

    leptons_fakeable_single = ak.concatenate([electrons_single_fake, muons_single_fake], axis=1)
    leptons_fakeable_single = ak.pad_none(leptons_fakeable_single[ak.argsort(leptons_fakeable_single.conept, ascending=False)], 2)
    lep0_single = leptons_fakeable_single[:,0]; lep1_single = leptons_fakeable_single[:,1]

    leptons_fakeable_double = ak.concatenate([electrons_double_fake, muons_double_fake], axis=1)
    leptons_fakeable_double = ak.pad_none(leptons_fakeable_double[ak.argsort(leptons_fakeable_double.conept, ascending=False)], 2)
    lep0_double = leptons_fakeable_double[:,0]; lep1_double = leptons_fakeable_double[:,1]

    #Take first 2 B tagged, then second 2 pT ordered (after removing bTags)
    ak4_jets_bsorted_single = ak4_jets_single_cleaned[ak.argsort(ak4_jets_single_cleaned.btagDeepFlavB, ascending=False)]
    ak4_jet0_single = ak4_jets_bsorted_single[:,0]; ak4_jet1_single = ak4_jets_bsorted_single[:,1]
    ak4_jets_without_bjets_single = ak4_jets_bsorted_single[:,2:]
    ak4_jets_ptsorted_single = ak4_jets_without_bjets_single[ak.argsort(ak4_jets_without_bjets_single.pt, ascending=False)]
    ak4_jet2_single = ak4_jets_ptsorted_single[:,0]; ak4_jet3_single = ak4_jets_ptsorted_single[:,1]

    ak4_jets_bsorted_double = ak4_jets_double_cleaned[ak.argsort(ak4_jets_double_cleaned.btagDeepFlavB, ascending=False)]
    ak4_jet0_double = ak4_jets_bsorted_double[:,0]; ak4_jet1_double = ak4_jets_bsorted_double[:,1]
    ak4_jets_without_bjets_double = ak4_jets_bsorted_double[:,2:]
    ak4_jets_ptsorted_double = ak4_jets_without_bjets_double[ak.argsort(ak4_jets_without_bjets_double.pt, ascending=False)]
    ak4_jet2_double = ak4_jets_ptsorted_double[:,0]; ak4_jet3_double = ak4_jets_ptsorted_double[:,1]

    ak8_jet0_single = ak8_jets_single_cleaned_sorted[:,0]
    ak8_jet0_double = ak8_jets_double_cleaned_sorted[:,0]



    def make_lep_dict(lep, name):
        dict = {
            name+'_pdgId': np.array(ak.fill_none(lep.pdgId, underflow_value), dtype=np.int32),
            name+'_charge': np.array(ak.fill_none(lep.charge, underflow_value), dtype=np.int32),
            name+'_pt': np.array(ak.fill_none(lep.pt, underflow_value), dtype=np.float32),
            name+'_conept': np.array(ak.fill_none(lep.conept, underflow_value), dtype=np.float32),
            name+'_eta': np.array(ak.fill_none(lep.eta, underflow_value), dtype=np.float32),
            name+'_phi': np.array(ak.fill_none(lep.phi, underflow_value), dtype=np.float32),
            name+'_E': np.array(ak.fill_none(lep.energy, underflow_value), dtype=np.float32),
            name+'_px': np.array(ak.fill_none(lep.px, underflow_value), dtype=np.float32),
            name+'_py': np.array(ak.fill_none(lep.py, underflow_value), dtype=np.float32),
            name+'_pz': np.array(ak.fill_none(lep.pz, underflow_value), dtype=np.float32),
        }
        if isMC and doSF:
            MC_dict = {
                name+'_lepton_ID_SF': np.array(ak.fill_none(lep.lepton_ID_SF, underflow_value), dtype=np.float32),
                name+'_lepton_ID_SF_up': np.array(ak.fill_none(lep.lepton_ID_SF_up, underflow_value), dtype=np.float32),
                name+'_lepton_ID_SF_down': np.array(ak.fill_none(lep.lepton_ID_SF_down, underflow_value), dtype=np.float32),
                name+'_lepton_tight_TTH_SF': np.array(ak.fill_none(lep.lepton_tight_TTH_SF, underflow_value), dtype=np.float32),
                name+'_lepton_tight_TTH_SF_up': np.array(ak.fill_none(lep.lepton_tight_TTH_SF_up, underflow_value), dtype=np.float32),
                name+'_lepton_tight_TTH_SF_down': np.array(ak.fill_none(lep.lepton_tight_TTH_SF_down, underflow_value), dtype=np.float32),
                name+'_lepton_relaxed_TTH_SF': np.array(ak.fill_none(lep.lepton_relaxed_TTH_SF, underflow_value), dtype=np.float32),
                name+'_lepton_relaxed_TTH_SF_up': np.array(ak.fill_none(lep.lepton_relaxed_TTH_SF_up, underflow_value), dtype=np.float32),
                name+'_lepton_relaxed_TTH_SF_down': np.array(ak.fill_none(lep.lepton_relaxed_TTH_SF_down, underflow_value), dtype=np.float32),
                #name+'_single_lepton_trigger_SF': np.array(ak.fill_none(lep.single_lepton_trigger_SF, underflow_value), dtype=np.float32),
                #name+'_single_lepton_trigger_SF_up': np.array(ak.fill_none(lep.single_lepton_trigger_SF_up, underflow_value), dtype=np.float32),
                #name+'_single_lepton_trigger_SF_down': np.array(ak.fill_none(lep.single_lepton_trigger_SF_down, underflow_value), dtype=np.float32),

            }
            dict.update(MC_dict)
        return dict

    def make_ak4_jet_dict(jet, name):
        dict = {
            name+'_pt': np.array(ak.fill_none(jet.pt, underflow_value), dtype=np.float32),
            name+'_eta': np.array(ak.fill_none(jet.eta, underflow_value), dtype=np.float32),
            name+'_phi': np.array(ak.fill_none(jet.phi, underflow_value), dtype=np.float32),
            name+'_E': np.array(ak.fill_none(jet.energy, underflow_value), dtype=np.float32),
            name+'_px': np.array(ak.fill_none(jet.px, underflow_value), dtype=np.float32),
            name+'_py': np.array(ak.fill_none(jet.py, underflow_value), dtype=np.float32),
            name+'_pz': np.array(ak.fill_none(jet.pz, underflow_value), dtype=np.float32),
            name+'_btagDeepFlavB': np.array(ak.fill_none(jet.btagDeepFlavB, underflow_value), dtype=np.float32),
        }
        if isMC and doSF:
            MC_dict = {
                name+"_jet_rescale_par": np.array(ak.fill_none(jet.par_jet_rescale, underflow_value), dtype=np.float32),
                name+"_JER_up_par": np.array(ak.fill_none(jet.par_JER_up, underflow_value), dtype=np.float32),
                name+"_JER_down_par": np.array(ak.fill_none(jet.par_JER_down, underflow_value), dtype=np.float32),
                name+"_JES_up_par": np.array(ak.fill_none(jet.par_JES_up, underflow_value), dtype=np.float32),
                name+"_JES_down_par": np.array(ak.fill_none(jet.par_JES_down, underflow_value), dtype=np.float32),
            }
            dict.update(MC_dict)
        return dict

    def make_ak8_jet_dict(jet, name):
        dict = {
            name+'_pt': np.array(ak.fill_none(jet.pt, underflow_value), dtype=np.float32),
            name+'_eta': np.array(ak.fill_none(jet.eta, underflow_value), dtype=np.float32),
            name+'_phi': np.array(ak.fill_none(jet.phi, underflow_value), dtype=np.float32),
            name+'_E': np.array(ak.fill_none(jet.energy, underflow_value), dtype=np.float32),
            name+'_px': np.array(ak.fill_none(jet.px, underflow_value), dtype=np.float32),
            name+'_py': np.array(ak.fill_none(jet.py, underflow_value), dtype=np.float32),
            name+'_pz': np.array(ak.fill_none(jet.pz, underflow_value), dtype=np.float32),
            name+'_tau1': np.array(ak.fill_none(jet.tau1, underflow_value), dtype=np.float32),
            name+'_tau2': np.array(ak.fill_none(jet.tau2, underflow_value), dtype=np.float32),
            name+'_tau3': np.array(ak.fill_none(jet.tau3, underflow_value), dtype=np.float32),
            name+'_tau4': np.array(ak.fill_none(jet.tau4, underflow_value), dtype=np.float32),
            name+'_msoftdrop': np.array(ak.fill_none(jet.msoftdrop, underflow_value), dtype=np.float32),

            name+'_subjet1_E': np.array(ak.fill_none(jet.subjet1.energy, underflow_value), dtype=np.float32),
            name+'_subjet1_px': np.array(ak.fill_none(jet.subjet1.px, underflow_value), dtype=np.float32),
            name+'_subjet1_py': np.array(ak.fill_none(jet.subjet1.py, underflow_value), dtype=np.float32),
            name+'_subjet1_pz': np.array(ak.fill_none(jet.subjet1.pz, underflow_value), dtype=np.float32),
            name+'_subjet1_pt': np.array(ak.fill_none(jet.subjet1.pt, underflow_value), dtype=np.float32),

            name+'_subjet2_E': np.array(ak.fill_none(jet.subjet2.energy, underflow_value), dtype=np.float32),
            name+'_subjet2_px': np.array(ak.fill_none(jet.subjet2.px, underflow_value), dtype=np.float32),
            name+'_subjet2_py': np.array(ak.fill_none(jet.subjet2.py, underflow_value), dtype=np.float32),
            name+'_subjet2_pz': np.array(ak.fill_none(jet.subjet2.pz, underflow_value), dtype=np.float32),
            name+'_subjet2_pt': np.array(ak.fill_none(jet.subjet2.pt, underflow_value), dtype=np.float32),
        }
        if isMC and doSF:
            MC_dict = {
                name+"_jet_rescale_par": np.array(ak.fill_none(jet.par_jet_rescale, underflow_value), dtype=np.float32),
                name+"_JER_up_par": np.array(ak.fill_none(jet.par_JER_up, underflow_value), dtype=np.float32),
                name+"_JER_down_par": np.array(ak.fill_none(jet.par_JER_down, underflow_value), dtype=np.float32),
                name+"_JES_up_par": np.array(ak.fill_none(jet.par_JES_up, underflow_value), dtype=np.float32),
                name+"_JES_down_par": np.array(ak.fill_none(jet.par_JES_down, underflow_value), dtype=np.float32),
            }
            dict.update(MC_dict)
        return dict

    def make_met_dict(met, name):
        dict = {
            name+'_E': np.array(ak.fill_none(met.px*0.0, underflow_value), dtype=np.float32), #Set to 0, but I want to keep the 'none' values
            name+'_px': np.array(ak.fill_none(met.px, underflow_value), dtype=np.float32),
            name+'_py': np.array(ak.fill_none(met.py, underflow_value), dtype=np.float32),
            name+'_pz': np.array(ak.fill_none(met.px*0.0, underflow_value), dtype=np.float32), #Set to 0, but I want to keep the 'none' values
            name+'_unclust_energy_up_x': np.array(ak.fill_none(met.MetUnclustEnUpDeltaX, underflow_value), dtype=np.float32),
            name+'_unclust_energy_up_y': np.array(ak.fill_none(met.MetUnclustEnUpDeltaY, underflow_value), dtype=np.float32),
            name+'_covXX': np.array(ak.fill_none(met.covXX, underflow_value), dtype=np.float32),
            name+'_covXY': np.array(ak.fill_none(met.covXY, underflow_value), dtype=np.float32),
            name+'_covYY': np.array(ak.fill_none(met.covYY, underflow_value), dtype=np.float32),
        }
        if isMC and doSF:
            MC_dict = {
                name+"_jet_rescale_par": np.array(ak.fill_none(met.par_jet_rescale, underflow_value), dtype=np.float32),
                name+"_JER_up_par": np.array(ak.fill_none(met.par_JER_up, underflow_value), dtype=np.float32),
                name+"_JER_down_par": np.array(ak.fill_none(met.par_JER_down, underflow_value), dtype=np.float32),
                name+"_JES_up_par": np.array(ak.fill_none(met.par_JES_up, underflow_value), dtype=np.float32),
                name+"_JES_down_par": np.array(ak.fill_none(met.par_JES_down, underflow_value), dtype=np.float32),
            }
            dict.update(MC_dict)
        return dict

    event_dict_single = {
        #Event level information
        'event': np.array(events_single.event),
        'ls': np.array(events_single.luminosityBlock),
        'run': np.array(events_single.run),
        'n_presel_muons': np.array(ak.sum(muons_single.preselected, axis=1), dtype=np.int32),
        'n_fakeable_muons': np.array(ak.sum(muons_single.fakeable, axis=1), dtype=np.int32),
        'n_tight_muons': np.array(ak.sum(muons_single.tight, axis=1), dtype=np.int32),

        'n_presel_electrons': np.array(ak.sum(electrons_single.preselected, axis=1), dtype=np.int32),
        'n_fakeable_electrons': np.array(ak.sum(electrons_single.fakeable, axis=1), dtype=np.int32),
        'n_tight_electrons': np.array(ak.sum(electrons_single.tight, axis=1), dtype=np.int32),

        'n_presel_ak4_jets': np.array(ak.sum(ak4_jets_single.preselected, axis=1), dtype=np.int32),
        'n_cleaned_ak4_jets': np.array(ak.sum(ak4_jets_single.cleaned_single, axis=1), dtype=np.int32),
        'n_loose_btag_ak4_jets': np.array(ak.sum(ak4_jets_single.loose_btag_single, axis=1), dtype=np.int32),
        'n_medium_btag_ak4_jets': np.array(ak.sum(ak4_jets_single.medium_btag_single, axis=1), dtype=np.int32),

        'n_presel_ak8_jets': np.array(ak.sum(ak8_jets_single.preselected, axis=1), dtype=np.int32),
        'n_cleaned_ak8_jets': np.array(ak.sum(ak8_jets_single.cleaned_single, axis=1), dtype=np.int32),
        'n_btag_ak8_jets': np.array(ak.sum(ak8_jets_single.btag_single, axis=1), dtype=np.int32),

        'Single_HbbFat_WjjRes_AllReco': np.array(events_single.Single_HbbFat_WjjRes_AllReco, dtype=np.int32),
        'Single_HbbFat_WjjRes_MissJet': np.array(events_single.Single_HbbFat_WjjRes_MissJet, dtype=np.int32),
        'Single_Res_allReco_2b': np.array(events_single.Single_Res_allReco_2b, dtype=np.int32),
        'Single_Res_allReco_1b': np.array(events_single.Single_Res_allReco_1b, dtype=np.int32),
        'Single_Res_MissWJet_2b': np.array(events_single.Single_Res_MissWJet_2b, dtype=np.int32),
        'Single_Res_MissWJet_1b': np.array(events_single.Single_Res_MissWJet_1b, dtype=np.int32),
        'Single_Signal': np.array(events_single.Single_Signal, dtype=np.int32),
        'Single_Fake': np.array(events_single.Single_Fake, dtype=np.int32),
        'single_category_cutflow': np.array(events_single.single_cutflow, dtype=np.int32),
        'single_is_e': np.array(ak.fill_none(events_single.is_e, False), dtype=np.int32),
        'single_is_m': np.array(ak.fill_none(events_single.is_m, False), dtype=np.int32),

        'dnn_truth_value': np.array(events_single.dnn_truth_value, dtype=np.int32),
    }

    event_dict_double = {
        #Event level information
        'event': np.array(events_double.event),
        'ls': np.array(events_double.luminosityBlock),
        'run': np.array(events_double.run),
        'n_presel_muons': np.array(ak.sum(muons_double.preselected, axis=1), dtype=np.int32),
        'n_fakeable_muons': np.array(ak.sum(muons_double.fakeable, axis=1), dtype=np.int32),
        'n_tight_muons': np.array(ak.sum(muons_double.tight, axis=1), dtype=np.int32),

        'n_presel_electrons': np.array(ak.sum(electrons_double.preselected, axis=1), dtype=np.int32),
        'n_fakeable_electrons': np.array(ak.sum(electrons_double.fakeable, axis=1), dtype=np.int32),
        'n_tight_electrons': np.array(ak.sum(electrons_double.tight, axis=1), dtype=np.int32),

        'n_presel_ak4_jets': np.array(ak.sum(ak4_jets_double.preselected, axis=1), dtype=np.int32),
        'n_cleaned_ak4_jets': np.array(ak.sum(ak4_jets_double.cleaned_double, axis=1), dtype=np.int32),
        'n_loose_btag_ak4_jets': np.array(ak.sum(ak4_jets_double.loose_btag_double, axis=1), dtype=np.int32),
        'n_medium_btag_ak4_jets': np.array(ak.sum(ak4_jets_double.medium_btag_double, axis=1), dtype=np.int32),

        'n_presel_ak8_jets': np.array(ak.sum(ak8_jets_double.preselected, axis=1), dtype=np.int32),
        'n_cleaned_ak8_jets': np.array(ak.sum(ak8_jets_double.cleaned_double, axis=1), dtype=np.int32),
        'n_btag_ak8_jets': np.array(ak.sum(ak8_jets_double.btag_double, axis=1), dtype=np.int32),

        'Double_HbbFat': np.array(events_double.Double_HbbFat, dtype=np.int32),
        'Double_Res_1b': np.array(events_double.Double_Res_1b, dtype=np.int32),
        'Double_Res_2b': np.array(events_double.Double_Res_2b, dtype=np.int32),
        'Double_Signal': np.array(events_double.Double_Signal, dtype=np.int32),
        'Double_Fake': np.array(events_double.Double_Fake, dtype=np.int32),
        'double_category_cutflow': np.array(events_double.double_cutflow, dtype=np.int32),
        'double_is_ee': np.array(ak.fill_none(events_double.is_ee, False), dtype=np.int32),
        'double_is_mm': np.array(ak.fill_none(events_double.is_mm, False), dtype=np.int32),
        'double_is_em': np.array(ak.fill_none(events_double.is_em, False), dtype=np.int32),

        'dnn_truth_value': np.array(events_double.dnn_truth_value, dtype=np.int32),
    }


    lep_dict_single = make_lep_dict(lep0_single, 'lep0') | make_lep_dict(lep1_single, 'lep1')
    ak4_jet_dict_single = make_ak4_jet_dict(ak4_jet0_single, 'ak4_jet0') | make_ak4_jet_dict(ak4_jet1_single, 'ak4_jet0') | make_ak4_jet_dict(ak4_jet2_single, 'ak4_jet0') | make_ak4_jet_dict(ak4_jet3_single, 'ak4_jet0')
    ak8_jet_dict_single = make_ak8_jet_dict(ak8_jet0_single, 'ak8_jet0')
    met_dict_single = make_met_dict(events_single.MET, 'met')

    lep_dict_double = make_lep_dict(lep0_double, 'lep0') | make_lep_dict(lep1_double, 'lep1')
    ak4_jet_dict_double = make_ak4_jet_dict(ak4_jet0_double, 'ak4_jet0') | make_ak4_jet_dict(ak4_jet1_double, 'ak4_jet0') | make_ak4_jet_dict(ak4_jet2_double, 'ak4_jet0') | make_ak4_jet_dict(ak4_jet3_double, 'ak4_jet0')
    ak8_jet_dict_double = make_ak8_jet_dict(ak8_jet0_double, 'ak8_jet0')
    met_dict_double = make_met_dict(events_double.MET, 'met')


    single_dicts = event_dict_single | lep_dict_single | ak4_jet_dict_single | ak8_jet_dict_single | met_dict_single
    double_dicts = event_dict_double | lep_dict_double | ak4_jet_dict_double | ak8_jet_dict_double | met_dict_double


    if debug: import time
    if debug: print("Save the tree in uproot")
    if debug: startTime = time.time()
    #outfile = uproot.recreate(outname)
    print("Whats in the keys?")
    print(outfile.keys())
    print('\t'.join(outfile.keys()))
    if "Single_Tree" in '\t'.join(outfile.keys()):
        print("Extending!")
        outfile["Single_Tree"].extend(single_dicts)
    else:
        outfile["Single_Tree"] = single_dicts
    if "Double_Tree" in '\t'.join(outfile.keys()):
        print("Extending!")
        outfile["Double_Tree"].extend(double_dicts)
    else:
        outfile["Double_Tree"] = double_dicts
    if debug: print("Took ", time.time() - startTime, " seconds")
