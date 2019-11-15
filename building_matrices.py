from brightway2 import *
import numpy as np
from Required_keys import *
import multiprocessing as mp
import sys
from multiprocessing import Queue
from multiprocessing import Pool
from brightway2 import LCA
from bw2data import projects
import os
import pandas as pd
from LF import *
from scipy.optimize import minimize, rosen, rosen_der

    
if sys.version_info < (3, 0):
    # multiprocessing.pool as a context manager not available in Python 2.7
    @contextmanager
    def pool_adapter(pool):
        try:
            yield pool
        finally:
            pool.terminate()
else:
    pool_adapter = lambda x: x



def worker(args):
    project, functional_unit, method, parameters, process_models, process_model_names, common_data, tech_matrix, bio_matrix, seed , n = args
    projects.set_current(project, writable=False)
    if common_data:
        common_data.setup_MC(seed)
    if process_models:
        for x in process_models:
            x.setup_MC(seed)
    if parameters:
        parameters.setup_MC(seed)
    lca = LCA(functional_unit, method[0])
    lca.lci()
    lca.lcia()
    return [parallel_mc (lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models=process_models, process_model_names=process_model_names, parameters=parameters, common_data=common_data) for x in range(n)]


def parallel_mc (lca, project, functional_unit, method, tech_matrix, bio_matrix, process_models = None, process_model_names = None, parameters = None, common_data = None):
    uncertain_inputs = list()
    
    if process_models:
        if common_data:
            uncertain_inputs += common_data.gen_MC()
            for process in process_models:
                process.CommonData = common_data
                uncertain_inputs += process.MC_calc()
        else:    
            for process in process_models:
                uncertain_inputs += process.MC_calc()
        
        i = 0
        for process_name in process_model_names:
            report_dict = process_models[i].report()
    
            for material,value in report_dict["Technosphere"].items():
                for key2, value2 in value.items():
                    if not np.isnan(value2):
                        if tech_matrix[((key2),(process_name, material))] != value2:
                            tech_matrix[((key2),(process_name, material))] = value2 
                            
            for material,value in report_dict["Waste"].items():
                for key2, value2 in value.items():
                    if key2 in ['Bottom_Ash','Fly_Ash','Separated_Organics','Other_Residual','RDF','Al','Fe','Cu']:
                        key2 = (process_name + "_product", material + '_' + key2)
                    else:
                        key2 = (process_name + "_product", key2)
                    if not np.isnan(value2):
                        if tech_matrix[((key2),(process_name, material))] != value2:
                            tech_matrix[((key2),(process_name, material))] = value2
            
            for material,value in report_dict["Biosphere"].items():
                for key2, value2 in value.items():
                    if not np.isnan(value2):
                        if bio_matrix[((key2),(process_name, material))] != value2:
                            bio_matrix[((key2),(process_name, material))] = value2
            i+=1
        
    if parameters:
        matrix,params = parameters.MC_calc()
        uncertain_inputs += params
        for key, value in matrix.items():
            if key in tech_matrix:
                tech_matrix[key] = value    
    
    tech = np.array(list(tech_matrix.values()), dtype=float)
    bio = np.array(list(bio_matrix.values()), dtype=float)
    
    lca.rebuild_technosphere_matrix(tech)
    lca.rebuild_biosphere_matrix(bio)
    lca.lci_calculation()
    if lca.lcia:
        lca.lcia_calculation()

    lca_results = dict()
    lca_results[method[0]]=lca.score

    if len(method)>1:
        for i in range(1,len(method)):
            lca.switch_method(method[i])
            lca.lcia_calculation()
            lca_results[method[i]]=lca.score
        lca.switch_method(method[0])
    
    return(os.getpid(),lca_results,uncertain_inputs,report_dict)
    
  


class ParallelData(LCA):
    def __init__(self, functional_unit, method, project, process_models = None, process_model_names = None, common_data = None, parameters = None,seed = None):
        super(ParallelData, self).__init__(functional_unit, method[0])
        self.lci()
        self.lcia()
        self.functional_unit = functional_unit
        self.method = method
        self.project = project
        self.process_models = process_models
        self.process_model_names = process_model_names
        self.parameters = parameters
        self.common_data = common_data
        self.seed = seed
        
        
        activities_dict = dict(zip(self.activity_dict.values(),self.activity_dict.keys()))
        self.tech_matrix = dict()
        for i in self.tech_params:
            self.tech_matrix[(activities_dict[i[2]], activities_dict[i[3]])] = i[6]
        
        
        biosphere_dict = dict(zip(self.biosphere_dict.values(),self.biosphere_dict.keys()))
        self.bio_matrix = dict()
        biosphere_dict_names = dict()
        
        for i in self.bio_params:
            if (biosphere_dict[i[2]], activities_dict[i[3]]) not in self.bio_matrix.keys():
                self.bio_matrix[(biosphere_dict[i[2]], activities_dict[i[3]])] = i[6]
            else:
                self.bio_matrix[(str(biosphere_dict[i[2]]) + " - 1", activities_dict[i[3]])] = i[6]
                print((str(biosphere_dict[i[2]]) + " - 1", activities_dict[i[3]]))                
        
    def run(self, nproc, n):       
        with pool_adapter(mp.Pool(processes=nproc)) as pool:
            res = pool.map(
                worker,
                [
                    (self.project, self.functional_unit, self.method, self.parameters, self.process_models, self.process_model_names, self.common_data, self.tech_matrix, self.bio_matrix, self.seed  + i, n//nproc)
                    for i in range(nproc)
                ]
            )
        self.results = [x for lst in res for x in lst]
    
    
    def objective_function(self, x):
        matrix=self.project.unified_params.get_matrix(x)
        for key, value in matrix.items():
            if key in self.tech_matrix:
                self.tech_matrix[key] = value    
    
        tech = np.array(list(self.tech_matrix.values()), dtype=float)
        bio = np.array(list(self.bio_matrix.values()), dtype=float)
        
        self.rebuild_technosphere_matrix(tech)
        self.rebuild_biosphere_matrix(bio)
        self.lci_calculation()
        if self.lcia:
            self.lcia_calculation()

        return self.score
    
    
    def create_funtion(self, count):
        local_count = self.running_count
        l = lambda x: sum([x[i] for i in range(local_count,local_count+count)]) -1 
        self.running_count+=count
        return l

    
    def create_constraints(self):
        cons = list()
        group = dict()
        self.running_count=0
        
        for key in self.project.unified_params.param_uncertainty_dict.keys():
            group[key] = len(self.project.unified_params.param_uncertainty_dict[key])

        for vals in group.values():
            cons.append({'type':'eq', 'fun':self.create_funtion(vals)})
                
        return cons
        
    def optimize_parameters(self, project):
        self.project = project
        x0 = [i['amount'] for i in self.project.parameters_list]
        bnds = tuple([(0,1) for _ in self.project.parameters_list])
        cons = self.create_constraints()
        
        fun = lambda x: (x[0] - 1)**2 + (x[1] - 2.5)**2 - x[2] + x[3] - 2*x[4]*x[5] + 2*x[5] - x[6]
        
        res = minimize(self.objective_function,x0,method='SLSQP', bounds=bnds, constraints=cons)
        return res.x
		
    
    
    def result_to_DF(self):
        output=pd.DataFrame()
### Reporting the LCIA results; Create a column for each method
        for j in self.results[0][1].keys():
            output[j] = [self.results[i][1][j] for i in range(len(self.results))]
### Reporting the input data    
        for j in range(len(self.results[0][2])):
                output[self.results[0][2][j][0]] = [self.results[i][2][j][1] for i in range(len(self.results))]
        return(output)

    def save_results(self,name):
        self.result_to_DF().to_pickle(name)
    
        #worker((self.project, self.functional_unit, self.method, self.parameters, self.process_models, self.process_model_names, self.common_data, self.tech_matrix, self.bio_matrix, self.seed, n//nproc))
if __name__=='__main__':
    project = "Demo_LF"
    projects.set_current(project)
    db = Database("waste")
    functional_unit = {db.get("scenario1") : 1}
    method = [('SWOLF_IPCC','SWOLF')]
    a = ParallelData(functional_unit, method, project, [LF()], ['LF'],seed = 1)
    a.run(4,12)
    print(a.result_to_DF())
    
     
  

