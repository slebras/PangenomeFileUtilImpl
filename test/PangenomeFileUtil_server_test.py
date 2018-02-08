import unittest
import os
import json
import time
import shutil

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint

from biokbase.workspace.client import Workspace as workspaceService
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
        cls.serviceImpl = PangenomeFileUtil(cls.cfg)
        cls.prepare_data()

    @classmethod
    def prepare_data(cls):
        cls.obj_name = 'pangenome'
        cls.ws_name = "jjeffryes:narrative_1516232220798"
        # with open(os.path.join('data','dummy_pangenome.json')) as data_file:
        #    pgData = json.load(data_file)
        # ws = self.getWsClient();
        # info = ws.save_objects({'workspace':self.getWsName(), 'objects':[
        #            {
        #                'type':'KBaseGenomes.Pangenome',
        #                'data':pgData,
        #                'name':obj_name
        #            }]})
        # print('saved dummy pangenome')
        # pprint(info)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_PangenomeFileUtil_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    def test_to_tsv(self):
        res = self.getImpl().pangenome_to_tsv_file(self.getContext(), {
                'pangenome_name': self.obj_name,
                'workspace_name': self.ws_name,
            })
        pprint(res)
        # test bad input
        with self.assertRaises(ValueError):
            self.getImpl().pangenome_to_tsv_file(self.getContext(), {
                'pangenome_ref': self.ws_name + '/' + self.obj_name
            })

    def test_to_excel(self):
        res = self.getImpl().pangenome_to_excel_file(self.getContext(), {
                'pangenome_name': self.obj_name,
                'workspace_name': self.ws_name,
            })
        pprint(res)
        # test bad input
        with self.assertRaises(ValueError):
            self.getImpl().pangenome_to_excel_file(self.getContext(), {
                'pangenome_ref': self.ws_name + '/' + self.obj_name
            })

    def test_export_tsv(self):
        res = self.getImpl().export_pangenome_as_tsv_file(self.getContext(), {
                'pangenome_ref': self.ws_name + '/' + self.obj_name
            })
        pprint(res)
        # test bad input
        with self.assertRaises(ValueError):
            self.getImpl().export_pangenome_as_tsv_file(self.getContext(), {
                'pangenome_name': self.obj_name,
                'workspace_name': self.ws_name,
            })

    def test_export_excel(self):
        res = self.getImpl().export_pangenome_as_excel_file(self.getContext(),
            {
                'pangenome_ref': self.ws_name + '/' + self.obj_name
            })
        pprint(res)
        # test bad input
        with self.assertRaises(ValueError):
            self.getImpl().export_pangenome_as_excel_file(self.getContext(), {
                'pangenome_name': self.obj_name,
                'workspace_name': self.ws_name,
            })
