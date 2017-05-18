import os
import Exceptions as ex
import sys
import pandas as pd
import numpy as np



################################################################# Parsing Functions ################################################################


#parse text-based output from fastqc
def parse_fastqc(summary_file, fastq_type="", is_paired=True, omit_num_reads=False, omit_num_low_qual=False, omit_seq_len=False, omit_gc=False, omit_test_results=False, omit_filename=False):

    #initialize empty summary
    summary = []

    if not os.path.isfile(summary_file):
        raise ex.MissingSummaryFileError("FastQC", summary_file)

    # add underscore to name so type can be added to end of underscore delimited headers
    if fastq_type is not "":
        fastq_type = "_" + fastq_type


    # open summary file
    fastqc = open(summary_file, "r")
    first_line = True

    # results of FASTQC tests
    test_results = []

    # parse summary file and store results
    for line in fastqc:
        # strip newlines
        line = line.strip()

        # check to make sure file is actually the correct filetype
        if first_line:
            if "FastQC" not in line:
                raise ex.SummaryParseError("FastQC", summary_file,
                                           "File provided is not fastqc_data.txt file from FASTQC")
            first_line = False

        if ("Total Sequences" in line) and not omit_num_reads:
            key = "Total_Read_Pairs"
            if is_paired:
                value = int(line.split()[2]) * 2
            else:
                value = int(line.split()[2])

        elif ("Filename" in line) and not omit_filename:
            key   = "Fastq_Filename"
            value = line.split()[1]

        elif ("flagged as poor quality" in line) and not omit_num_low_qual:
            key = "Num_Low_Quality_Reads"
            if is_paired:
                value = int(line.split()[5]) * 2
            else:
                value = int(line.split()[5]) * 2

        elif ("Sequence length") in line and not omit_seq_len:
            key = "Read_Length"
            value = line.split()[2]

        elif ("%GC") in line and not omit_gc:
            key = "%GC"
            value = float(line.split()[1])


        # case: header line for summary test
        elif ((">>" in line) and ("END_MODULE" not in line)):
            # strip delimiter
            line = line[2:]
            test_results.append(line.split()[-1])

        else:
            key = None
            value = None

        # add to summary summary if necessary
        if ((key is not None) and (value is not None)):
            summary.append((key + fastq_type, value))

    # add FASTQC test results as a single entry if desired
    if not omit_test_results:
        summary.append(("FastQC_Test_Results" + fastq_type, ';'.join(test_results)))

    fastqc.close()

    #return summary
    return summary


#parse samtools flagstat for PCR duplicates, Aligned reads, and alignment rate
def parse_flagstat(summary_file, omit_pcr_dup_percent=False, omit_num_align_reads=False, omit_aligned_percent=False):

    #init empty summary
    summary = []

    # check to see if file exists
    if not os.path.isfile(summary_file):
        raise ex.MissingSummaryFileError("Samtools Flagstat BAM", summary_file)

    # open input file
    samtools_file = open(summary_file, "r")
    count = 0
    for line in samtools_file:
        if count == 0:
            # check to make sure file actually samtools flagstat file
            if "in total" not in line:
                raise ex.SummaryParseError("Samtools Flagstat", summary_file,
                                           "File provided is not output from samtools Flagstat")
            # get total reads
            tot_reads = float(line.split()[0])
        elif ("duplicates" in line) and not omit_pcr_dup_percent:
            # get total duplicates
            tot_dups = float(line.split()[0])
            percent_dups = (tot_dups / tot_reads) * 100.0
            summary.append(("PCR_Duplicates", int(tot_dups)))
            summary.append(("Percent_PCR_Duplicates", percent_dups))
        elif "mapped (" in line:
            mapped_reads = float(line.split()[0])
            align_perc   = mapped_reads/tot_reads
            if not omit_num_align_reads:
                summary.append(("Aligned_Reads", int(mapped_reads)))

            if not omit_aligned_percent:
                summary.append(("Align_Perc", align_perc))

        count += 1

    samtools_file.close()
    return summary



#parse trimmomatic output
def parse_trimmomatic(summary_file, omit_reads_before_trimming=False, omit_reads_after_trimming=False, omit_percent_trimmed=False):

    #initialize summary list
    summary = []

    # check to see if file exists
    if not os.path.isfile(summary_file):
        raise ex.MissingSummaryFileError("Trimmomatic", summary_file)


    # open input file
    trimmomatic_file = open(summary_file, "r")
    count = 0
    is_paired = True
    for line in trimmomatic_file:
        #find line with number of reads input and surviving trimming
        if count == 0:
            if "TrimmomaticSE" in line:
                is_paired = False
            elif "TrimmomaticPE" not in line:
                raise ex.SummaryParseError("Trimmomatic", summary_file,
                                           "File provided is not output from trimmomatic")
        elif "Surviving" in line:
            if is_paired:
                #paired-end output
                input_reads   = int(line.strip().split()[3])
                trimmed_reads = int(line.strip().split()[6])
            else:
                #single-end output
                input_reads = int(line.strip().split()[2])
                trimmed_reads = int(line.strip().split()[4])

            if not omit_reads_before_trimming:
                summary.append(("Reads_Before_Trimming", input_reads))

            if not omit_reads_after_trimming:
                summary.append(("Reads_After_Trimming", trimmed_reads))

            if not omit_percent_trimmed:
                summary.append(("Percent_Passed_Trimming", float(trimmed_reads)/input_reads))
            break
        #increment count
        count += 1

    trimmomatic_file.close()
    return summary


#parses output from picard insert size metrics to determine the median insert size
def parse_picard_insert_size_metrics(summary_file):

    #init new summary
    summary = []

    # check to see if file exists
    if not os.path.isfile(summary_file):
        raise ex.MissingSummaryFileError("Picard insert size", summary_file)

    # open input file
    insert_size_file = open(summary_file, "r")
    for line in insert_size_file:
        # find line with number of reads input and surviving trimming
        if "FR" in line:
            line = line.strip().split()

            median_insert_size  = float(line[0])
            mean_insert_size    = float(line[4])
            sd_insert_size      = float(line[5])
            min_insert_size     = float(line[2])
            max_insert_size     = float(line[3])

            summary.append(("Mean_Insert_Size", mean_insert_size))
            summary.append(("Median_Insert_Size", median_insert_size))
            summary.append(("SD_Insert_Size", sd_insert_size))
            summary.append(("Min_Insert_Size", min_insert_size))
            summary.append(("Max_Insert_Size", max_insert_size))

    insert_size_file.close()
    return summary






#parse output from samtools depth to summarize read coverage for a target region
def parse_samtools_depth(summary_file, cutoffs=[]):
    #inputs: samtools depth summary file
    #cutoffs: list of cutoffs to determine the number of reads covered at or above each cutoff

    summary = []

    # check and format cutoffs provided by user
    cutoffs = format_samtools_depth_cutoffs(cutoffs)

    # check to see if file exists
    if not os.path.isfile(summary_file):
        raise ex.MissingSummaryFileError("Samtools Coverage Depth BAM", summary_file)

    # check input file format
    check_samtools_depth_format(summary_file)

    # get input table as pandas data frame
    input_table = pd.read_table(summary_file, names=["chr", "pos", "depth"], header=None, usecols=["depth"])

    # summarize depth column
    results = input_table["depth"].describe()

    # iterate through key/value pairs and store results
    keys      = ['mean', 'std', 'min', '25%', '50%', '75%', 'max']
    key_names = ['mean_cov_dp', 'stdev_cov_dp', 'min_cov_dp', 'Q1_cov_dp', 'median_cov_dp',
            'Q3_cov_dp', 'max_cov_dp']

    for i in range(len(keys)):
        value = results[[keys[i]]][0]
        summary.append((key_names[i], value))

    # get percent of bases covered above varying depth cutoffs
    for cutoff in cutoffs:
        key = "pct_bases_dp_%d" % cutoff
        value = get_pct_bases_covered_above_cutoff(input_table, cutoff)
        summary.append((key, value))

    return summary










def parse_bedtools_intersect(summary_file, target_type="Target"):
    # parses output from bedtools intersect (-c option) to determine the number of reads mapping to a target region

    summary = []

    # check to see if file exists
    if not os.path.isfile(summary_file):
        raise ex.MissingSummaryFileError("Bedtools Intersect BAM", summary_file)

    # get input table as pandas data frame
    input_table = pd.read_table(summary_file,
                                names=["chr", "start", "end", "header", "mq", "strand", "start2", "end2", "color",
                                       "passed", "length", "dummy", "mapped"], header=None, usecols=["mapped"])

    # replace '.' with 0 for unmapped reads
    input_table.mapped.replace(".","0",inplace=True)

    # convert everything to int
    input_table.mapped = input_table.mapped.apply(np.int16)

    # get percent of reads mapping to exon
    reads_mapped, pct_mapped = get_pct_reads_mapped(input_table)
    summary.append(("Reads_mapped_to_%s" % target_type, reads_mapped))
    summary.append(("Pct_mapped_to_%s" % target_type, pct_mapped))

    return summary






def merge_summary_files(summary_files, sample_name=None, multisample=False, delim='\t'):
    #merges multiple summary file into a single summary

    if multisample:
        #case: concat summary files from multiple samples into a single file (merge by row)
        summary = concat_summary_files_by_row(summary_files)

    else:
        #case: concat summary files for a single sample into a single file (merge by col)
        summary = concat_summary_files_by_sample(summary_files, sample_name, delim)

    return summary





################################################################# I/O Functions ################################################################


def print_summary(summary, delim='\t'):
    # return delimited text version of summary

    # separate headers and data into two lists
    header_line = [x for (x, y) in summary]
    data_line   = [str(y) for (x, y) in summary]

    # join into delimited string
    header_line = delim.join(header_line)
    data_line   = delim.join(data_line)

    # collapse with newline
    print >> sys.stdout, header_line + "\n" + data_line




################################################################# Helper Functions ################################################################

def get_pct_reads_mapped(input_table):
    #helper function used by parse_bedtools intersect to determine the percentage of reads mapping to a target region
    #takes a pandas dataframe as input
    total_bases = len(input_table) * 1.0
    covered_bases = len(input_table[input_table.mapped > 0]) * 1.0
    return (int(covered_bases), (covered_bases / total_bases) * 100)



def get_pct_bases_covered_above_cutoff(input_table, cutoff):
    #helper function used by parse_samtools_depth to determine the nubmer of reference bases covered at or above some cutoff
    #takes a pandas dataframe as input
    total_bases = len(input_table) * 1.0
    covered_bases = len(input_table[input_table.depth >= cutoff])
    return (covered_bases / total_bases) * 100




def concat_summary_files_by_row(summary_files):
    # merges summary files from multiple sample into a single summary list where each column is a tuple (header, data)

    header = None
    data   = ""

    #loop through summary files
    for summary_file in summary_files:
        header_line = True

        #open summary file
        with open(summary_file, "r") as ft:
            for line in ft:
                if header_line:
                    if header is None:
                        # get header line if not already gotten
                        header = line.strip()
                    header_line = False
                else:
                    #get data line as array
                    data += line
                    break

    return [(header, data)]




def concat_summary_files_by_sample(summary_files, sample_name=None, delim='\t'):
    #merges multilpe summary files from a single sample into a single summary list where each column is a tuple (header, data)
    summary = []

    #add sample name if necessary
    if sample_name is not None:
        summary.append(("Sample", sample_name))

    #loop through summary files
    for summary_file in summary_files:
        header = []
        data   = []
        header_line = True

        #open summary file
        with open(summary_file, "r") as ft:
            for line in ft:
                if header_line:
                    #get header line as array
                    header = line.strip().split(delim)
                    header_line = False
                else:
                    #get data line as array
                    data   = line.strip().split(delim)
                    break

            #append to summary as a list of tuples (header, data)
            summary += zip(header, data)

    #return concatenated list of columns from multiple files
    return summary


def check_samtools_depth_format(summary_file):
    #check to make sure samtools depth file conforms to output before parsing file
    # open input file
    coverage_file = open(summary_file, "r")

    # check format to make sure input file contains 3 columns as expected
    first_line = coverage_file.readline()
    first_line = first_line.split()

    if len(first_line) != 3:
        raise ex.SummaryParseError("Samtools Coverage Depth", summary_file,
                                   "File provided is not output from samtools depth")
    coverage_file.close()


def format_samtools_depth_cutoffs(cutoffs):
    # formats cutoffs used in parsing samtools depth output
    if len(cutoffs) == 0:
        return cutoffs
    # return sorted list of unique cutoffs
    return sorted(list(set(cutoffs)))











