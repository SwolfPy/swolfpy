# -*- coding: utf-8 -*-
"""
Created on Wed May 22 19:19:12 2019

@author: msmsa
"""
from project_class import *
from building_matrices import *

Treatment_processes = {}
Treatment_processes['AD']={'path':"AD_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['COMP']={'path':"Composting_BW2.csv",'input_type':['MOC','Separated_Organics']}
Treatment_processes['LF']={'path':"trad_landfill _BW2.xlsx",'input_type':['MWC','RWC','Bottom_Ash','Fly_Ash','Other_Residual']}
Treatment_processes['REPROC']={'path':"Material_Reprocessing_BW2.csv",'input_type':['OCC', 'Mixed_Paper', 'ONP', 'OFF', 'Fiber_Other', \
                   'PET', 'HDPE_Unsorted', 'HDPE_P', 'HDPE_T', 'PVC', 'LDPE_Film', 'Polypropylene', 'Polystyrene', 'Plastic_Other', \
                   'Mixed_Plastic', 'Al', 'Fe', 'Cu', 'Brown_glass', 'Clear_glass', 'Green_glass', 'Mixed_Glass']}
Treatment_processes['SSMRF']={'path':"SS_MRF_BW2.csv",'input_type':['SSRC']}
Treatment_processes['WTE']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}
Treatment_processes['WTE1']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}
Treatment_processes['WTE2']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}
Treatment_processes['WTE3']={'path':"WTE_BW2.csv",'input_type':['MWC','RWC','Other_Residual','RDF']}

mojtaba = project("demo_5",Treatment_processes)
mojtaba.init_project('SWOLF_AccountMode_LCI DATA.csv')
mojtaba.write_project()
mojtaba.group_exchanges()

gg=[{'name': 'frac_of_Other_Residual_from_AD_to_LF', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE1', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE2', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_AD_to_WTE3', 'amount': 0.2},
 {'name': 'frac_of_Other_Residual_from_COMP_to_LF', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE1', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE2', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_COMP_to_WTE3', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE1', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE2', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_REPROC_to_WTE3', 'amount': 0},
 {'name': 'frac_of_Bottom_Ash_from_REPROC_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_LF', 'amount': 1},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE1', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE2', 'amount': 0},
 {'name': 'frac_of_Other_Residual_from_SSMRF_to_WTE3', 'amount': 0},
 {'name': 'frac_of_Fe_from_SSMRF_to_REPROC', 'amount': 0},
 {'name': 'frac_of_Al_from_SSMRF_to_REPROC', 'amount': 0},
 {'name': 'frac_of_Bottom_Ash_from_WTE_to_LF', 'amount': 0},
 {'name': 'frac_of_Fly_Ash_from_WTE_to_LF', 'amount': 0},
 {'name': 'frac_of_Al_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE1_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE1_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE1_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE1_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE1_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE2_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE2_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE2_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE2_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE2_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Bottom_Ash_from_WTE3_to_LF', 'amount': 1},
 {'name': 'frac_of_Fly_Ash_from_WTE3_to_LF', 'amount': 1},
 {'name': 'frac_of_Al_from_WTE3_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Fe_from_WTE3_to_REPROC', 'amount': 1},
 {'name': 'frac_of_Cu_from_WTE3_to_REPROC', 'amount': 1}]

mojtaba.update_parameters(gg)
scenario1 = {"WTE":{"Yard_Trimmings_Grass":1,"Paper_Bags":1,"Mixed_Plastic":1},"WTE1":{"Yard_Trimmings_Grass":2,"Paper_Bags":2,"Mixed_Plastic":2},
             "WTE2":{"Yard_Trimmings_Grass":1,"Paper_Bags":0.1,"Mixed_Plastic":1},
             "WTE3":{"Yard_Trimmings_Grass":0.1,"Paper_Bags":1,"Mixed_Plastic":1}}
mojtaba.process_start_scenario(scenario1,'scenario1')
#mojtaba.Do_LCA("scenario1",('IPCC 2007', 'climate change', 'GWP 100a'),1)


mojtaba.unified_params.add_uncertainty('frac_of_Other_Residual_from_AD_to_LF', loc = 0.5, scale = 0.3, uncertainty_type = 3)
mojtaba.unified_params.add_uncertainty('frac_of_Other_Residual_from_AD_to_WTE', loc = 0.5, scale = 0.3, uncertainty_type = 3)
mojtaba.unified_params.add_uncertainty('frac_of_Other_Residual_from_AD_to_WTE1', loc = 0.5, scale = 0.3, uncertainty_type = 3)

project = "demo_5"
projects.set_current(project)
db = Database("waste")
functional_unit = {db.get("scenario1") : 1}
method = ('IPCC 2007', 'climate change', 'GWP 100a')

a = ParallelData(functional_unit, method, project, parameters=mojtaba.unified_params) 
a.run(4,1000)
from matplotlib.pylab import *
hist(a.results, density=True, histtype="step")
xlabel('(IPCC 2007, climate change, GWP 100a)')
ylabel("Probability")
    













     
        
        
    




