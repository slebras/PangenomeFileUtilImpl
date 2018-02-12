import unittest
import os
import json
import time
import pandas as pd
import filecmp

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
from GenomeAnnotationAPI.GenomeAnnotationAPIClient import GenomeAnnotationAPI
from PangenomeFileUtil.PangenomeFileUtilImpl import PangenomeFileUtil
from PangenomeFileUtil.PangenomeFileUtilServer import MethodContext


class PangenomeFileUtilTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'provenance': [
                            {'service': 'PangenomeFileUtil',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('PangenomeFileUtil'):
            cls.cfg[nameval[0]] = nameval[1]
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL, token=token)
        suffix = int(time.time() * 1000)
        cls.wsName = "test_PangenomeFileUtil_" + str(suffix)
        cls.wsClient.create_workspace({'workspace': cls.wsName})
        cls.serviceImpl = PangenomeFileUtil(cls.cfg)
        cls.gaa = GenomeAnnotationAPI(os.environ['SDK_CALLBACK_URL'])
        cls.prepare_data()

    @classmethod
    def prepare_data(cls):
        cls.obj_name = 'pangen3'
        g_1_data = json.load(open("data/Rhodobacter_CACIA_14H1.json"))
        info = cls.gaa.save_one_genome_v1({"data": g_1_data,
                                           "workspace": cls.wsName,
                                           "name": "Acoerulea.JGI1.1"
                                           })['info']
        g_1_ref = "{}/{}/{}".format(info[6], info[0], info[4])

        g_2_data = json.load(open("data/Rhodobacter_sphaeroides_2.4.1.json"))
        info = cls.gaa.save_one_genome_v1({"data": g_2_data,
                                           "workspace": cls.wsName,
                                           "name": "Rhodobacter_sphaeroides_2.4.1"
                                           })['info']
        g_2_ref = "{}/{}/{}".format(info[6], info[0], info[4])

        pangen_text = open("data/pangen3.json").read()
        pangen_data = json.loads(pangen_text.replace(
            "<genome_1>", g_1_ref).replace("<genome_2>", g_2_ref))

        info = cls.wsClient.save_objects({'workspace': cls.wsName, 'objects': [
                   {
                        'type': 'KBaseGenomes.Pangenome',
                        'data': pangen_data,
                        'name': cls.obj_name
                    }]})
        print('saved dummy pangenome')
        pprint(info)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_to_tsv(self):
        res = self.getImpl().pangenome_to_tsv_file(self.getContext(), {
                'pangenome_name': self.obj_name,
                'workspace_name': self.wsName,
            })[0]
        assert filecmp.cmp(res['genomes_path'], 'data/pangen3_Genomes.tsv')
        assert filecmp.cmp(res['orthologs_path'], 'data/pangen3_Orthologs.tsv')
        pprint(res)
        # test bad input
        with self.assertRaises(ValueError):
            self.getImpl().pangenome_to_tsv_file(self.getContext(), {
                'input_ref': self.wsName + '/' + self.obj_name
            })

    def test_to_excel(self):
        res = self.getImpl().pangenome_to_excel_file(self.getContext(), {
                'pangenome_name': self.obj_name,
                'workspace_name': self.wsName,
            })[0]
        pprint(res)
        df1 = pd.read_excel(res['path'])
        df2 = pd.read_excel('data/pangen3.xlsx')
        assert all(df1 == df2)

        # test bad input
        with self.assertRaises(ValueError):
            self.getImpl().pangenome_to_excel_file(self.getContext(), {
                'input_ref': self.wsName + '/' + self.obj_name
            })

    def test_export_tsv(self):
        res = self.getImpl().export_pangenome_as_tsv_file(self.getContext(), {
                'input_ref': self.wsName + '/' + self.obj_name
            })
        pprint(res)
        # test bad input
        with self.assertRaises(ValueError):
            self.getImpl().export_pangenome_as_tsv_file(self.getContext(), {
                'pangenome_name': self.obj_name,
                'workspace_name': self.wsName,
            })

    def test_export_excel(self):
        res = self.getImpl().export_pangenome_as_excel_file(self.getContext(),
            {
                'input_ref': self.wsName + '/' + self.obj_name
            })
        pprint(res)
        # test bad input
        with self.assertRaises(ValueError):
            self.getImpl().export_pangenome_as_excel_file(self.getContext(), {
                'pangenome_name': self.obj_name,
                'workspace_name': self.wsName,
            })
