from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException

class SamtoolsFlagstat(BaseParser):

    DESCRIPTION     = "Parse Samtools flagstat output (v1.3 and later)"
    INPUT_FILE_DESC = "Samtools flagstat output"

    def __init__(self, sys_args):
        super(SamtoolsFlagstat, self).__init__(sys_args)

    def parse_input(self):
        # Parse samtools flagstat
        first_line = True
        with open(self.input_file, "r") as fh:
            for line in fh:
                data = line.split()

                if first_line:
                    # Check to make sure file actually samtools flagstat file
                    if "in total" not in line:
                        raise QCParseException("File provided is not output from samtools Flagstat")

                    # Get total reads in BAM file
                    tot_aligns = int(data[0]) + int(data[2])
                    first_line = False

                elif "secondary" in line:
                    secondary_aligns = int(data[0]) + int(data[2])

                elif "supplementary" in line:
                    supp_aligns = int(data[0]) + int(data[2])

                elif "duplicates" in line:
                    # Get total duplicates
                    pcr_dups = int(data[0]) + int(data[2])

                elif "mapped (" in line:
                    # Get number aligned reads
                    mapped_reads = int(data[0]) + int(data[2])

                elif "paired in sequencing" in line:
                    # Get number, percent of properly paired reads
                    paired = int(data[0]) + int(data[2])

                elif "properly paired" in line:
                    # Get number, percent of properly paired reads
                    prop_paired = int(data[0]) + int(data[2])

                elif "singletons" in line:
                    # Get number, percent of singleton reads (mate doesn't map)
                    singletons = int(data[0]) + int(data[2])

                elif "with mate mapped to a different chr" in line and "(mapQ" not in line:
                    # Get number, percent of reads where mates map to different chromosome
                    tot_mate_diff_chrom_lq = int(data[0]) + int(data[2])

                elif "with mate mapped to a different chr" in line and "(mapQ" in line:
                    # Get number, percent of reads where mates map to different chromosome with high quality
                    tot_mate_diff_chrom_hq = int(data[0]) + int(data[2])

            # Add basic samtools fields
            self.add_entry("Tot_aligns", tot_aligns)
            self.add_entry("Sec_aligns", secondary_aligns)
            self.add_entry("Supp_aligns", supp_aligns)
            self.add_entry("PCR_dups", pcr_dups)
            self.add_entry("Mapped_Reads", mapped_reads)
            self.add_entry("Proper_Paired", prop_paired)
            self.add_entry("Singletons", singletons)
            self.add_entry("Mate_Mapped_Diff_Chrom_LQ", tot_mate_diff_chrom_lq)
            self.add_entry("Mate_Mapped_Diff_Chrom_HQ", tot_mate_diff_chrom_hq)

            # Compute real mapping rates (number of actually good mappings / actual number of reads in bam)
            total_reads = tot_aligns - secondary_aligns - supp_aligns
            total_mapped_reads = mapped_reads - secondary_aligns - supp_aligns
            if total_reads:
                self.add_entry("Real_Map_Rate", (total_mapped_reads * 100.0)/total_reads)
            else:
                self.add_entry("Real_Map_Rate", 0)

    def define_required_colnames(self):
        return ["Tot_aligns", "Sec_aligns", "Supp_aligns", "PCR_dups", "Mapped_Reads",
                "Proper_Paired", "Singletons", "Mate_Mapped_Diff_Chrom_LQ",
                "Mate_Mapped_Diff_Chrom_HQ", "Real_Map_Rate"]
