import logging

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
                if first_line:
                    # Check to make sure file actually samtools flagstat file
                    if "in total" not in line:
                        raise QCParseException("File provided is not output from samtools Flagstat")

                    # Get total reads in BAM file
                    tot_aligns = float(line.split()[0])
                    first_line = False

                elif "secondary" in line:
                    secondary_aligns = float(line.split()[0])

                elif "supplementary" in line:
                    supp_aligns = float(line.split()[0])

                elif "duplicates" in line:
                    # Get total duplicates
                    pcr_dups = float(line.split()[0])

                elif "mapped (" in line:
                    # Get number aligned reads
                    mapped_reads = float(line.split()[0])

                elif "paired in sequencing" in line:
                    # Get number, percent of properly paired reads
                    paired = float(line.split()[0])

                elif "properly paired" in line:
                    # Get number, percent of properly paired reads
                    prop_paired = float(line.split()[0])

                elif "singletons" in line:
                    # Get number, percent of singleton reads (mate doesn't map)
                    singletons = float(line.split()[0])

                elif "with mate mapped to a different chr" in line and "(mapQ" not in line:
                    # Get number, percent of reads where mates map to different chromosome
                    tot_mate_diff_chrom_lq = float(line.split()[0])

                elif "with mate mapped to a different chr" in line and "(mapQ" in line:
                    # Get number, percent of reads where mates map to different chromosome with high quality
                    tot_mate_diff_chrom_hq = float(line.split()[0])

            # Add basic samtools fields
            self.add_entry("Tot_aligns", int(tot_aligns))
            self.add_entry("Sec_aligns", int(secondary_aligns))
            self.add_entry("Supp_aligns", int(supp_aligns))
            self.add_entry("PCR_dups", int(pcr_dups))
            self.add_entry("Mapped_Reads", int(mapped_reads))
            self.add_entry("Proper_Paired", int(prop_paired))
            self.add_entry("Singletons", int(singletons))
            self.add_entry("Mate_Mapped_Diff_Chrom_LQ", int(tot_mate_diff_chrom_lq))
            self.add_entry("Mate_Mapped_Diff_Chrom_HQ", int(tot_mate_diff_chrom_hq))

            # Compute real mapping rates (number of actually good mappings / actual number of reads in bam)
            is_paired   = paired > 0
            total_reads = tot_aligns - secondary_aligns - supp_aligns
            if is_paired:
                logging.info("Paired in sequences detected for BAM: %s" % self.input_file)
                if total_reads:
                    self.add_entry("Real_Map_Rate", (prop_paired/total_reads) * 100)
                else:
                    self.add_entry("Real_Map_Rate", 0)

            else:
                logging.info("Single-end sequences detected for BAM: %s" % self.input_file)
                if total_reads:
                    self.add_entry("Real_Map_Rate", (mapped_reads/total_reads) * 100)
                else:
                    self.add_entry("Real_Map_Rate", 0)

    def define_required_colnames(self):
        return ["Tot_aligns", "Sec_aligns", "Supp_aligns", "PCR_dups", "Mapped_Reads",
                "Proper_Paired", "Singletons", "Mate_Mapped_Diff_Chrom_LQ",
                "Mate_Mapped_Diff_Chrom_HQ", "Real_Map_Rate"]
