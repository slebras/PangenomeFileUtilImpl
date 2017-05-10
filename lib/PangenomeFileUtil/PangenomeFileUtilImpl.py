# -*- coding: utf-8 -*-
#BEGIN_HEADER

import os
import sys
import shutil
import traceback
import uuid
import subprocess
from pprint import pprint, pformat

from biokbase.workspace.client import Workspace

from DataFileUtil.DataFileUtilClient import DataFileUtil

#END_HEADER


class PangenomeFileUtil:
    '''
    Module Name:
    PangenomeFileUtil

    Module Description:
    
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.2"
    GIT_URL = "https://github.com/rsutormin/PangenomeFileUtilImpl"
    GIT_COMMIT_HASH = "7480370491807308fec0f65fce42ca6abd28ece4"

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.shockURL = config['shock-url']
        self.handleURL = config['handle-service-url']
        self.scratch = config['scratch']
        self.transform_plugin_path = config['transform-plugin-path']
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        #END_CONSTRUCTOR
        pass


    def pangenome_to_tsv_file(self, ctx, params):
        """
        :param params: instance of type "PangenomeToFileParams" -> structure:
           parameter "pangenome_name" of String, parameter "workspace_name"
           of String
        :returns: instance of type "PangenomeTsvFiles" -> structure:
           parameter "genomes_path" of String, parameter "orthologs_path" of
           String, parameter "shock_id" of String
        """
        # ctx is the context object
        # return variables are: files
        #BEGIN pangenome_to_tsv_file
        print('pangenome_to_tsv_file -- paramaters = ')
        pprint(params)

        # validate input and set defaults.
        if 'workspace_name' not in params:
            raise ValueError('workspace_name field was not defined')
        workspace_name = params['workspace_name']

        if 'pangenome_name' not in params:
            raise ValueError('pangenome_name field was not defined')
        pangenome_name = params['pangenome_name']

        # construct the working directory where we stage files and output
        working_dir =  os.path.join(self.scratch, 'pangenome-download-'+str(uuid.uuid4()))
        os.makedirs(working_dir)


        # setup and run the command
        trnsScript = os.path.join(self.transform_plugin_path, 'scripts', 'download',
                                    'trns_transform_KBaseGenomes_Pangenome_to_TSV_Pangenome.pl')
        cmd = ['perl', trnsScript, 
                    '--object_name', pangenome_name, 
                    '--workspace_name', workspace_name,
                    '--workspace_service_url', self.workspaceURL,
                     ]
        print('Running Transform command line:')
        pprint(cmd)
        p = subprocess.Popen(cmd,cwd=working_dir,shell=False)
        retcode = p.wait()

        # handle the result and figure out the output file
        print('Return code: ' + str(retcode))
        if p.returncode != 0:
            raise ValueError('Error running Transform script, return code: ' + str(retcode) + '\n')


        files = {}
        # identify the files created
        dir_contents = os.listdir(working_dir)
        print('created file listing:')
        pprint(dir_contents)
        dir_files = []
        for f in dir_contents:
            if os.path.isfile(os.path.join(working_dir, f)):
                if f.endswith('_Genomes.tsv'):
                    files['genomes_path'] = os.path.join(working_dir,f)
                if f.endswith('_Orthologs.tsv'):
                    files['orthologs_path'] = os.path.join(working_dir,f)
        if 'genomes_path' not in files:
            raise ValueError('Something went wrong- no genome TSV file created')
        if 'orthologs_path' not in files:
            raise ValueError('Something went wrong- no orthologs TSV file created')

        #END pangenome_to_tsv_file

        # At some point might do deeper type checking...
        if not isinstance(files, dict):
            raise ValueError('Method pangenome_to_tsv_file return value ' +
                             'files is not type dict as required.')
        # return the results
        return [files]

    def pangenome_to_excel_file(self, ctx, params):
        """
        :param params: instance of type "PangenomeToFileParams" -> structure:
           parameter "pangenome_name" of String, parameter "workspace_name"
           of String
        :returns: instance of type "PangenomeExcelFile" -> structure:
           parameter "path" of String, parameter "shock_id" of String
        """
        # ctx is the context object
        # return variables are: file
        #BEGIN pangenome_to_excel_file
        print('pangenome_to_excel_file -- paramaters = ')
        pprint(params)

        # validate input and set defaults.
        if 'workspace_name' not in params:
            raise ValueError('workspace_name field was not defined')
        workspace_name = params['workspace_name']

        if 'pangenome_name' not in params:
            raise ValueError('pangenome_name field was not defined')
        pangenome_name = params['pangenome_name']

        # construct the working directory where we stage files and output
        working_dir =  os.path.join(self.scratch, 'pangenome-download-'+str(uuid.uuid4()))
        os.makedirs(working_dir)


        # setup and run the command
        trnsScript = os.path.join(self.transform_plugin_path, 'scripts', 'download',
                                    'trns_transform_KBaseGenomes_Pangenome_to_Excel_Pangenome.pl')
        cmd = ['perl', trnsScript, 
                    '--object_name', pangenome_name, 
                    '--workspace_name', workspace_name,
                    '--workspace_service_url', self.workspaceURL,
                     ]
        print('Running Transform command line:')
        pprint(cmd)
        p = subprocess.Popen(cmd,cwd=working_dir,shell=False)
        retcode = p.wait()

        # handle the result and figure out the output file
        print('Return code: ' + str(retcode))
        if p.returncode != 0:
            raise ValueError('Error running Transform script, return code: ' + str(retcode) + '\n')

        # identify the files created
        file = {}
        dir_contents = os.listdir(working_dir)
        print('created file listing:')
        pprint(dir_contents)
        dir_files = []
        for f in dir_contents:
            if os.path.isfile(os.path.join(working_dir, f)):
                if f.endswith('.xls'):
                    file['path'] = os.path.join(working_dir,f)
        if 'path' not in file:
            raise ValueError('Something went wrong- no Excel file created')

        #END pangenome_to_excel_file

        # At some point might do deeper type checking...
        if not isinstance(file, dict):
            raise ValueError('Method pangenome_to_excel_file return value ' +
                             'file is not type dict as required.')
        # return the results
        return [file]

    def export_pangenome_as_tsv_file(self, ctx, params):
        """
        :param params: instance of type "ExportParams" -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_pangenome_as_tsv_file

        print('export_pangenome_as_tsv_file -- paramaters = ')
        pprint(params)

        # validate parameters
        if 'input_ref' not in params:
            raise ValueError('Cannot export Pangenome- not input_ref field defined.')

        # get WS metadata to get ws_name and obj_name
        ws = Workspace(url=self.workspaceURL)
        info = ws.get_object_info_new({'objects':[{'ref': params['input_ref'] }],'includeMetadata':0, 'ignoreErrors':0})[0]

        # export to a file
        file = self.pangenome_to_tsv_file(ctx, { 
                                'pangenome_name': info[1],
                                'workspace_name': info[7]
                            })[0]

        # create the output directory and move the files there
        export_package_dir = os.path.join(self.scratch, info[1])
        os.makedirs(export_package_dir)
        shutil.move(file['genomes_path'], os.path.join(export_package_dir, os.path.basename(file['genomes_path'])))
        shutil.move(file['orthologs_path'], os.path.join(export_package_dir, os.path.basename(file['orthologs_path'])))

        # package it up and be done
        dfUtil = DataFileUtil(self.callback_url)
        package_details = dfUtil.package_for_download({
                                    'file_path': export_package_dir,
                                    'ws_refs': [ params['input_ref'] ]
                                })

        output = { 'shock_id': package_details['shock_id'] }

        #END export_pangenome_as_tsv_file

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_pangenome_as_tsv_file return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]

    def export_pangenome_as_excel_file(self, ctx, params):
        """
        :param params: instance of type "ExportParams" -> structure:
           parameter "input_ref" of String
        :returns: instance of type "ExportOutput" -> structure: parameter
           "shock_id" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN export_pangenome_as_excel_file

        print('export_pangenome_as_excel_file -- paramaters = ')
        pprint(params)

        # validate parameters
        if 'input_ref' not in params:
            raise ValueError('Cannot export Pangenome- not input_ref field defined.')

        # get WS metadata to get ws_name and obj_name
        ws = Workspace(url=self.workspaceURL)
        info = ws.get_object_info_new({'objects':[{'ref': params['input_ref'] }],'includeMetadata':0, 'ignoreErrors':0})[0]

        # export to a file
        file = self.pangenome_to_excel_file(ctx, { 
                                'pangenome_name': info[1],
                                'workspace_name': info[7]
                            })[0]

        # create the output directory and move the files there
        export_package_dir = os.path.join(self.scratch, info[1])
        os.makedirs(export_package_dir)
        shutil.move(file['path'], os.path.join(export_package_dir, os.path.basename(file['path'])))
        
        # package it up and be done
        dfUtil = DataFileUtil(self.callback_url)
        package_details = dfUtil.package_for_download({
                                    'file_path': export_package_dir,
                                    'ws_refs': [ params['input_ref'] ]
                                })

        output = { 'shock_id': package_details['shock_id'] }

        #END export_pangenome_as_excel_file

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method export_pangenome_as_excel_file return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION, 
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
