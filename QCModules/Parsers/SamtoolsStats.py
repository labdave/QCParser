from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class SamtoolsStats(BaseParser):

    DESCRIPTION     = "Parse Samtools stats output (v1.3 and later)"
    INPUT_FILE_DESC = "Samtools stats output"

    def __init__(self, sys_args):
        super(SamtoolsStats, self).__init__(sys_args)

    def parse_input(self):
        # Parse samtools stats
        with open(self.input_file, "r") as fh:
            for line in fh:
                # remove the trailing new line character
                line = line.rstrip()

                if line.startswith("SN"):
                    data = line.split('\t')
                    if "raw total sequences:" in data:
                        self.add_entry("Raw_Total_Sequences", data[2])
                    elif "filtered sequences:" in data:
                        self.add_entry("Filtered_Sequences", data[2])
                    elif "sequences:" in data:
                        self.add_entry("Sequences", data[2])
                    # elif "1st fragments:" in data:
                    #     self.add_entry("First_Fragments", data[2])
                    # elif "last fragments:" in data:
                    #     self.add_entry("Last_Fragments", data[2])
                    elif "reads mapped:" in data:
                        self.add_entry("Reads_Mapped", data[2])
                    elif "reads mapped and paired:" in data:
                        self.add_entry("Reads_Mapped_And_Paired", data[2])
                    # elif "reads unmapped:" in data:
                    #     self.add_entry("Reads_Unmapped", data[2])
                    elif "reads properly paired:" in data:
                        self.add_entry("Reads_Properly_Paired", data[2])
                    elif "reads paired:" in data:
                        self.add_entry("Reads_Paired", data[2])
                    # elif "reads duplicated:" in data:
                    #     self.add_entry("Reads_Duplicated", data[2])
                    elif "reads MQ0:" in data:
                        self.add_entry("Reads_MQ0", data[2])
                    # elif "reads QC failed:" in data:
                    #     self.add_entry("Reads_QC_Failed", data[2])
                    elif "non-primary alignments:" in data:
                        self.add_entry("Non_Primary_Alignments", data[2])
                    # elif "total length:" in data:
                    #     self.add_entry("Total_Length", data[2])
                    # elif "total first fragment length:" in data:
                    #     self.add_entry("Total_First_Fragment_Length", data[2])
                    # elif "total last fragment length:" in data:
                    #     self.add_entry("Total_Last_Fragment_Length", data[2])
                    elif "bases mapped:" in data:
                        self.add_entry("Bases_Mapped", data[2])
                    elif "bases mapped (cigar):" in data:
                        self.add_entry("Bases_Mapped_Cigar", data[2])
                    # elif "bases trimmed:" in data:
                    #     self.add_entry("Bases_Trimmed", data[2])
                    # elif "bases duplicated:" in data:
                    #     self.add_entry("Bases_Duplicated", data[2])
                    elif "mismatches:" in data:
                        self.add_entry("Mismatches", data[2])
                    elif "error rate:" in data:
                        self.add_entry("Error_Rate", data[2])
                    # elif "average length:" in data:
                    #     self.add_entry("Average_Length", data[2])
                    # elif "average first fragment length:" in data:
                    #     self.add_entry("Average_First_Fragment_Length", data[2])
                    # elif "average last fragment length:" in data:
                    #     self.add_entry("Average_Last_Fragment_Length", data[2])
                    # elif "maximum length:" in data:
                    #     self.add_entry("Maximum_Length", data[2])
                    # elif "maximum first fragment length:" in data:
                    #     self.add_entry("Maximum_First_Fragment_Length", data[2])
                    # elif "maximum last fragment length:" in data:
                    #     self.add_entry("Maximum_Last_Fragment_Length", data[2])
                    elif "average quality:" in data:
                        self.add_entry("Average_Quality", data[2])
                    elif "insert size average:" in data:
                        self.add_entry("Insert_Size_Average", data[2])
                    elif "insert size standard deviation:" in data:
                        self.add_entry("Insert_Size_Standard_Deviation", data[2])
                    elif "inward oriented pairs:" in data:
                        self.add_entry("Inward_Oriented_Pairs", data[2])
                    elif "outward oriented pairs:" in data:
                        self.add_entry("Outward_Oriented_Pairs", data[2])
                    elif "pairs with other orientation:" in data:
                        self.add_entry("Pairs_With_Other_Orientation", data[2])
                    elif "pairs on different chromosomes:" in data:
                        self.add_entry("Pairs_On_Different_Chromosomes", data[2])
                    elif "percentage of properly paired reads (%):" in data:
                        self.add_entry("Percentage_Of_Properly_Paired_Reads", data[2])
                    else:
                        continue

    def define_required_colnames(self):
        return ["Raw_Total_Sequences","Filtered_Sequences","Sequences","Reads_Mapped","Reads_Mapped_And_Paired",
                "Reads_Properly_Paired","Reads_Paired","Reads_MQ0","Non_Primary_Alignments","Bases_Mapped",
                "Bases_Mapped_Cigar","Mismatches","Error_Rate","Average_Quality","Insert_Size_Average",
                "Insert_Size_Standard_Deviation","Inward_Oriented_Pairs","Outward_Oriented_Pairs",
                "Pairs_With_Other_Orientation","Pairs_On_Different_Chromosomes","Percentage_Of_Properly_Paired_Reads"]
