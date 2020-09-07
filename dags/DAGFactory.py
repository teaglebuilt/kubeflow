from importlib import import_module
from airflow import DAG
import traceback
import sys
import os


AIRFLOW_BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(AIRFLOW_BASE)

class DAGFactory(object):

    def __init__(self):
        self.project_base = os.path.join(AIRFLOW_BASE, 'clients')
    
    @property
    def projects(self):
        return list(filter(lambda x: x not in ['__pycache__'],
            [dirs for _, dirs, _ in os.walk(self.project_base)][0]))

    def get_modules_from_clients(self):
        for client in self.projects:
            import pdb;pdb.set_trace()
            try:
                module_name = "clients.{}.DAG".format(client)
                prj_mod = import_module(module_name)
                no_of_project_dags = 1

                for dag in prj_mod.DAGS:
                    var_name = '{}-{}'.format(client, no_of_project_dags)
                    globals()[var_name] = dag

                    no_of_project_dags += 1
            except Exception as e:
                print( traceback.format_exc() )



dags = DAGFactory()
print(dags.projects)

clients = dags.get_modules_from_clients

print(clients)