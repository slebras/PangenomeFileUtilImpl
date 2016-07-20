/*
*/
module PangenomeFileUtil {

    /* A boolean - 0 for false, 1 for true.
       @range (0, 1)
    */
    typedef int boolean;

    typedef structure {
        string genomes_path;
        string orthologs_path;
        string shock_id;
    } PangenomeTsvFiles;

    typedef structure {
        string pangenome_name;
        string workspace_name;
    } PangenomeToFileParams;


    funcdef pangenome_to_tsv_file(PangenomeToFileParams params)
                returns(PangenomeTsvFiles files) authentication required;


    typedef structure {
        string path;
        string shock_id;
    } PangenomeExcelFile;

    funcdef pangenome_to_excel_file(PangenomeToFileParams params)
                returns(PangenomeExcelFile file) authentication required;


    typedef structure {
        string input_ref;
    } ExportParams;

    typedef structure {
        string shock_id;
    } ExportOutput;

    funcdef export_pangenome_as_tsv_file(ExportParams params)
                returns (ExportOutput output) authentication required;

    funcdef export_pangenome_as_excel_file(ExportParams params)
                returns (ExportOutput output) authentication required;

};
