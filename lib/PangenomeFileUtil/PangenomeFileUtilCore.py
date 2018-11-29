import pandas
import os
import shutil
import uuid

from DataFileUtil.DataFileUtilClient import DataFileUtil
from PangenomeAPI.PangenomeAPIClient import PanGenomeAPI

from installed_clients.WsLargeDataIOClient import WsLargeDataIO


class PangenomeUploadDownload:
    def __init__(self, config):
        self.cfg = config
        self.scratch = config['scratch']
        self.pga = PanGenomeAPI(os.environ['SDK_CALLBACK_URL'])
        self.dfu = DataFileUtil(os.environ['SDK_CALLBACK_URL'])
        self.ws_large_data = WsLargeDataIO(os.environ['SDK_CALLBACK_URL'])

    @staticmethod
    def validate_params(params, expected={"workspace_name", "pangenome_name"}):
        expected = set(expected)
        pkeys = set(params)
        # this method doesnt check for keys included in 'params' but included
        # in 'expected'
        if expected - pkeys:
            raise ValueError("Required keys {} not in supplied parameters"
                             .format(", ".join(expected - pkeys)))

    def upload_pangenome(self, params):
        '''
        params:
            workspace_name
            pangenome_name: name to give exported pangenome object
            data: main payload, expect this to be in the form of a Pangenome object described in the Kidl spec.
                highest level should be dict.s

        '''
        # validate and get inputs
        workspace_name = params['workspace_name']
        pg_name = params['pangenome_name']

        pangenome = params['json_data_path']

        if 'meta' in params and params['meta']:
            meta = params['meta']
        else:
            meta = {}

        if 'hidden' in params and str(params['hidden']).lower() in (
                'yes', 'true', 't', '1'):
            hidden = 1
        else:
            hidden = 0

        # # dump pangenome to scratch for upload
        # data_path = os.path.join(self.scratch, pg_name + '.json')
        # json.dump(pangenome, open(data_path, 'w'))

        # define parameters to be saved
        if isinstance(workspace_name, int) or workspace.isdigit():
            workspace_id = workspace_name
        else:
            workspace_id = self.dfu.ws_name_to_id(workspace_name)

        save_params = {
            'id': workspace_id,
            'objects': [{
                'type', 'KBaseGenomes.Pangenome',
                'data_json_file': pangenome,
                'name': name,
                'meta': meta,
                'hidden': hidden
            }]
        }

        info = self.ws_large_data.save_objects(save_params)[0]

        ref = "{}/{}/{}".format(info[6], info[0], info[4])
        print("Pangenome saved to {}".format(ref))

        return ref, info

    def to_tsv(self, params):
        files = {}
        working_dir = os.path.join(self.scratch,
                                   'pangenome-download-' + str(uuid.uuid4()))
        os.makedirs(working_dir)

        pg_id, id_name_map, genome_df = self.make_genomes_df(
            params['pangenome_ref'])
        files['genomes_path'] = os.path.join(
            working_dir, pg_id + "_Genomes.tsv")
        genome_df.to_csv(files['genomes_path'], sep="\t")

        ortho_df = self.make_ortholog_df(params['pangenome_ref'], id_name_map)
        files['orthologs_path'] = os.path.join(working_dir,
                                               pg_id + "_Orthologs.tsv")
        ortho_df.to_csv(files['orthologs_path'], sep="\t")

        return pg_id, files

    def to_excel(self, params):
        files = {}
        working_dir = os.path.join(self.scratch,
                                   'pangenome-download-' + str(uuid.uuid4()))
        os.makedirs(working_dir)

        pg_id, id_name_map, genome_df = self.make_genomes_df(
            params['pangenome_ref'])
        files['path'] = os.path.join(working_dir, pg_id + ".xlsx")
        writer = pandas.ExcelWriter(files['path'])
        genome_df.to_excel(writer, "Genomes")

        ortho_df = self.make_ortholog_df(params['pangenome_ref'], id_name_map)
        ortho_df.to_excel(writer, "Orthologs")
        writer.save()

        return pg_id, files

    def make_genomes_df(self, pg_ref):
        summary = self.pga.compute_summary_from_pangenome({
            "pangenome_ref": pg_ref})
        return summary['pangenome_id'], summary['genome_ref_name_map'], \
            pandas.DataFrame(summary['shared_family_map'])

    def make_ortholog_df(self, pg_ref, id_name_map):
        pangen = self.dfu.get_objects({'object_refs': [pg_ref]}
                                      )['data'][0]['data']
        ortho = {}
        for cluster in pangen['orthologs']:
            ortho[cluster['id']] = {
                "representative function": cluster.get('function', ""),
                "type": cluster.get("type", ""),
                "protein sequence": cluster.get("protein_translation", ""),
            }
            for gid, name in id_name_map.items():
                ortho[cluster['id']][name] = ";".join(
                    [x[0] for x in cluster['orthologs'] if x[2] == gid])

        return pandas.DataFrame.from_dict(ortho, 'index')[
            ["representative function", "type", "protein sequence"] +
            sorted([x for x in id_name_map.values()])]

    def export(self, files, name, params):
        export_package_dir = os.path.join(
            self.scratch, name + str(uuid.uuid4()))
        os.makedirs(export_package_dir)
        for file in files:
            shutil.move(file, os.path.join(export_package_dir,
                                           os.path.basename(file)))

        # package it up and be done
        package_details = self.dfu.package_for_download({
            'file_path': export_package_dir,
            'ws_refs': [params['pangenome_ref']]
        })

        return {'shock_id': package_details['shock_id']}
