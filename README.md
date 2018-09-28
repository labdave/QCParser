# QCParser
**QCParser** is a command line tool for parsing information from popular bioinformatic output files and storing data in a common format (QCReport). Modular design allows users to add new modules to suit their specific needs.

## Feature Highlights

  * **Centralized Quality Control for you Workflow**
    * Parses unstructured QC data into standardized JSON format
    * Agglomeration functions allow combining all QC information into single report
    * Combine QC information across workflows for single QC reports for a project
  
  * **Built-in support for popular tools**
    * FastQC
    * Bedtools Intersect
    * Samtools Depth, Flagstat, Idxstat
    * Trimmomatic
    * Mosdepth
    * Picard CollectInsertSizeMetrics
  
  * **Modular/Extensible**
    * Easily add or customize modules to parse any unstructured data file

  * **Verbose type/error checking**
      * In-built checks to warn/quit when input data doesn't match expected structure
      * Clear errors if required datatypes aren't found


## Setting up your system
  
**QCParser** is currently designed only for *Linux* systems. 
You will need to install and configure the following tool:  

1. [Python](https://www.python.org/) v2.7.*

    You can check your Python version by running the following command in your terminal:

    ```sh
    $ python -V
    Python 2.7.10
    ```

    To install the correct version of Python, visit the official Python [website](https://www.python.org/downloads/).

2. Python packages: *numpy*, *scipy*, *pandas*, *matplotlib*

    You will need [pip](https://packaging.python.org/guides/installing-using-linux-tools/) to install the above packages.
    After installing *pip*, run the following commands in your terminal: 

    ``` sh
    # Upgrade pip
    sudo pip install -U pip
    
    pip install numpy
    pip install scipy
    pip install pandas
    pip install matplotlib
    ```

3. Clone the **QCParser** repo

    ``` sh
    # clone the repo
    git clone https://github.com/alexwaldrop/QCParser.git
    ```
## Usage
    
**QCParser** works by parsing a single input file using an available parser module
 and producing a single file called a QCReport. Available parsing modules can be seen by calling the top level QCParser.py program.
    
    ./QCParser.py <tool> [tool_args]
    Tools:
	    SamtoolsDepth		    Summarize coverage depth from Samtool depth output
	    Cbind		            Concatenate Two or more QCReports by COLUMN (e.g. merging multiple reports from same sample)
	    FastQC		            Parse Fastqc text output
	    PrintTable		        Print QCReport to tab-delimited table.
	    PicardInsertSize        Parse Picard InsertSize Metrics output.
	    MosdepthDist		    Parse read depth distribution output from Mosdepth
	    SamtoolsIdxstats	    Parse Samtools idxstats output (v1.3 and later)
	    TNADemuxReport		    Parse RNA/DNA report from TNA demux script
	    Rbind		            Concatenate Two or more QCReports by ROW (e.g. merging across samples)
	    BedtoolsIntersect	    Summarize overlap percentage from Bedtools Intersect output.
	    SamtoolsFlagstat	    Parse Samtools flagstat output (v1.3 and later)
	    GATKCollectReadCount	Count total number of reads mapping to genomic features.
	    Trimmomatic		        Parse Trimmomatic stderr log.


    Further tool level options can be found for each module.

Additionally, each parser module defines it's own command line arguments:

    ./QCParser.py FastQC --help
    
    
    Parse Fastqc text output
    

    optional arguments:
    -h, --help            show this help message and exit
    -v                    Increase verbosity of the program.Multiple -v's
                          increase the verbosity level: 0 = Errors 1 = Errors +
                          Warnings 2 = Errors + Warnings + Info 3 = Errors +
                          Warnings + Info + Debug
    -i INPUT_FILE, --input INPUT_FILE
        Path to FastQC output file (fastqc_data.txt).
    -s SAMPLE_NAME, --sample SAMPLE_NAME
        Sample name.
    -n NOTE, --note NOTE  
        Note about file being parsed.


## QCReport ouptut format

**QCParser** parses unstructured information into a unified JSON file called a QCReport.
In essence, QCReports are a JSON representation of a table with consistent column types.
Below, we'll define the formal and more intuitive definitions of the QCReport file produced by parser modules.


### QCReport Grammar Definition

    QCReport        ::= { QCSample* }
    QCSample        ::= "SampleName" : [ QCEntry+ ]
    QCEntry         ::= {   
                            "Module" : String,
                            "Name"   : String,
                            "Note"   : String,
                            "Source" : String,
                            "Value"  : Int | String
                        }

### Plainspeak definition
Any QCReport produced by **QCParser** are guaranteed to meet the following:

1. **QCReport** is a valid JSON object
2. **QCReport** contains a set of 0 or more **QCSamples**
3. **QCSamples** are lists containing 1 or more **QCEntries**
4. **QCEntries** are JSON objects containing the following information
    * Value: QC value parsed from a file
    * Name: QC value data type (e.g. "Raw Reads")
    * Source: Path to source file of QC value
    * Module: **QCParser** module used to parse source file
    * Note: Optional field for adding extra information
    
Additionally, **QCReports** satisfy the following properties:
1. Squareness
    
    All **QCSamples** contain the same number of **QCEntries**

2. Ordered

    All **QCSamples** contain the same **QCEntry** data types in the same order
    
    **QCEntries** are considered equivalent if they're produced by the same 'Module' and have the same 'Name' 

    
### Example QCReport

**QCReport**

    {
    "Sample_1": 
        [
            {
            "Module": "FastQC", 
            "Name": "Total_Reads", 
            "Note": "rna raw fastqs", 
            "Source": "/home/sample_1/fastqc_data.txt", 
            "Value": 18346
            }, 
            {
            "Module": "FastQC", 
            "Name": "LQ_Reads", 
            "Note": "rna raw fastqs", 
            "Source": "/home/sample_1/fastqc_data.txt", 
            "Value": 0
            }
        ],
    "Sample_2": 
        [
            {
            "Module": "FastQC", 
            "Name": "Total_Reads", 
            "Note": "rna raw fastqs", 
            "Source": "/home/sample_2/fastqc_data.txt", 
            "Value": 233990
            }, 
            {
            "Module": "FastQC", 
            "Name": "LQ_Reads", 
            "Note": "rna raw fastqs", 
            "Source": "/home/sample_2/fastqc_data.txt", 
            "Value": 59
            }
        ]
    }
    
**Tabular Format**
    
    Sample      Total_Reads LQ_Reads
    Sample_1    18346       0
    Sample_2    233990      59

## QCReport Manipulation functions
**QCParser** contains three functions for the basic manipulation of QCReports. 

These functions are useful for combining QCReports from multiple files, samples, or workflows into a single QCReport.

1. **PrintTable** Output QCReport to stdout in TSV table format


``` sh
    ./QCReport PrintTable -i sample_1.qc_report.txt
``` 


**QCParser** will often be used multiple times within a workflow to parse information from multiple output files.
To handle the issue of multiple QCReports, **QCParser** provides two convenience functions for safely combining QCReports
across modules, samples, or workflows. 


2. **Cbind** Concatenate columns of two or more QCReports with same samples.

    * Useful for combining QCReports from the same sample or samples into a single QCReport

    
``` sh
    ./QCReport Cbind -i sample_1.fastqc.qc_report.txt sample_1.trimmomatic.qc_report.txt
``` 


3. **Rbind** Concatenate samples of two or more QCReports with same QCEntries
    
    * Useful for combining QCReports from multiple samples into single report

``` sh
    ./QCReport Rbind -i sample_1.qc_report.txt sample_2.qc_report.txt
``` 


## Defining a custom parser module

A key strength of **QCParser** is its extensability, allowing it to parse nearly any data type.
This section discusses the process of defining your own custom module to create QCReports from new input types.

1. Create new python file in the QCModules/Parsers
2. Create constructor for your new class with the following properties:
    1. Extends the BaseParser module
    2. Takes only sys_args as its arguments
    3. Import QCParseException for throwing any parsing-related errors
    4. Override the BaseParser's DESCRIPTION field with a useful message to describe the parser module function. This gets printed by the CLI help message. 
    5. Override the BaseParser's INPUT_FILE_DESC field with a useful message to describe the type of input file expected. This gets printed by the CLI help message.  
    6. Call super() to instantiate base properties. 

    ```python
    
    from BaseParser import BaseParser
    from QCModules.BaseModule import QCParseException


    class MyNewParser(BaseParser):

        DESCRIPTION     = "This is a test class"
        INPUT_FILE_DESC = "Text output from Bioinformatics tool X"

        def __init__(self, sys_args):
            super(MyNewParser, self).__init__(sys_args)
    ```
    
    
   Inheriting from BaseParser provides the following to an extending class:
   1. Defines CLI that expects an input file, sample name, and optional note character
   2. Handles command line parsing and sets the input_file, sample_name, and note attributes of your parser class on instantiation.
    
   Without any additional code, your class is already incorporatd into the base CLI:
    
    
    ./QCParser.py --help
    Tools:
	    SamtoolsDepth		    Summarize coverage depth from Samtool depth output
	    ...
        MyNewParser             This is a test class
        
   And also inherits its own tool-specific CLI:
   
    ./QCParser.py MyNewParser --help
        usage: MyNewParser [-h] [-v] -i INPUT_FILE -s SAMPLE_NAME [-n NOTE]  
        
        This is a test class
        

        optional arguments:
        -h, --help            show this help message and exit
        -v                    Increase verbosity of the program.Multiple -v's
                              increase the verbosity level: 0 = Errors 1 = Errors +
                              Warnings 2 = Errors + Warnings + Info 3 = Errors +
                              Warnings + Info + Debug
        -i INPUT_FILE, --input INPUT_FILE
                Path to Text output from Bioinformatics tool X.
        -s SAMPLE_NAME, --sample SAMPLE_NAME
                Sample name.
        -n NOTE, --note NOTE  
                Note about file being parsed.
   

3. Implement the define_required_colnames() function

    * This function declares the types of data your class will parse from its expected input files.
    
   ```python
    
       # Define output data types for FastQC parser class
        def define_required_colnames(self):
            return ["FastQC_Tests", "Total_Reads", "LQ_Reads", "Read_Len", "GC"]
    ```
    
    * **QCParser** uses this function to check that all required data types were extracted from your input file.
    
    *  **QCParser** will exit with an error if one or more of these data types are missing from the QCReport parsed from the input file

3. Implement the parse_input() method
    
    Ideally, this function serves two purposes:
    
      1. Parses required data types from file and adds to QCReport
      2. Checks to make sure input file is correct format
        
    You certainly don't have to do any input_file checking, but it often helps. 
    If a file formatting error is detected, raise a QCParseException with a helpful message such as below:
    
    ```python
    
        # Check to make sure file is actually the correct filetype
       if first_line and "FastQC" not in line:
           raise QCParseException("FastQC file '%s' does not contain 'FastQC' in first line. Make sure it's the fastq_data.txt.")
       else:
           first_line = False
    ```
    
    To add a specific data point to the QCReport, use the add_entry() method as follows:
 
    ```python
       
       # Add number of reads to QCReport
       num_reads = line.split()[0]
       self.add_entry(colname= "Num_Reads", value=num_reads)
     
    ```
    
    **Note**: You'll notice this isn't a valid QCEntry because it's missing the *Module*, *Source*, and optional *Note* attributes.
    That's actually okay because these get set automatically by the class upon instantiation. 

### Advanced topic: Adding arguments to your module's CLI
 In some cases, you may want to pass additional command line arguments to your parser module to modify the way it parses the input at runtime.
 
 Here's a simple example where we want to specify depth intervals to include in a QCReport of SamtoolsDepth output:

    /QCParser.py SamtoolsDepth --help

    Summarize coverage depth from Samtool depth output

    optional arguments:
    -h, --help            show this help message and exit
    -v                    Increase verbosity of the program.Multiple -v's
                          increase the verbosity level: 0 = Errors 1 = Errors +
                          Warnings 2 = Errors + Warnings + Info 3 = Errors +
                          Warnings + Info + Debug
    -i INPUT_FILE, --input INPUT_FILE
        Path to Samtools depth output [Chr Pos Depth].
    -s SAMPLE_NAME, --sample SAMPLE_NAME
        Sample name.
    -n NOTE, --note NOTE  
        Note about file being parsed.
    --ct CUTOFFS         
            Determine percentage of bases covered above this depth
            (INT). Can be specified multiple times for multiple
            cutoffs.
            
  You'll notice that the --ct or cuttoffs option wasn't provided simply by extending the BaseParser module. 
  In this case, you'll need to override the configure_arg_parser() method to add additional options. 
  
  Here's an example for the SamtoolsDepth module:
  
      
```python
def configure_arg_parser(self, base_parser):

    base_parser = super(SamtoolsDepth, self).configure_arg_parser(base_parser)

    # Add additional option to get depth cutoffs
    base_parser.add_argument('--ct',
                            action='append',
                            dest='cutoffs',
                            default=[5],
                            type=int,
                            help="Determine percentage of bases covered above this depth (INT). Can be specified multiple times for multiple cutoffs.")
        return base_parser
    
```
   
Let's break down how this accomplishes our goal:

For some context, configure_arg_parser() is a BaseParser method that defines and returns and [ArgumentParser](https://docs.python.org/2/howto/argparse.html) object 

Knowing this, the new method first calls BaseParser's super() method to get the base arg parser.
 
```python
    base_parser = super(SamtoolsDepth, self).configure_arg_parser(base_parser)
```
Next, we add additional features we'd like as if this were a normal ArgumentParser object (because it is):
```python

    # Add additional option to get depth cutoffs
    base_parser.add_argument('--ct',
                            action='append',
                            dest='cutoffs',
                            default=[5],
                            type=int,
                            help="Determine percentage of bases covered above this depth (INT). Can be specified multiple times for multiple cutoffs.")
```
Finally, make sure the function returns the modified arg parser and the changes will be reflected in the CLI.

## Docker Support

**QCParser** is maintained as a docker image and can be ported anywhere Docker is available.

The only pre-requisite here is the [Docker] client. Please execute the following command line to see if your system 
already have Docker-client installed or not.

```bash
$ sudo docker --version
``` 

If Docker is not installed on your system, you can get it from [Docker-client]. 

After the Docker set up, please pull the **QCParser** Docker image from the [Docker Hub]. To do so, please run 
the following command line:

```bash
$ sudo docker pull alexwaldrop/qcparser:latest
```

You can run **QCParser** as Docker container as follows:

```bash
$ sudo docker run --rm --user root alexwaldrop/qcparser:latest "./QCParser.py --help"
``` 

[Docker]: https://www.docker.com/
[Docker-client]: https://docs.docker.com/install/
[Docker Hub]: https://hub.docker.com/


## Project Status

**QCParser** is actively under development. To request features, please contact the author listed below.

## Authors

* [Alex Waldrop](https://github.com/alexwaldrop)



