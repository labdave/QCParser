import logging
import json

class QCReportError(Exception):
    pass

class QCReport:

    def __init__(self, report=None):
        # Initialize report from existing dictionary or from empty dict
        self.report     = {} if report is None else report
        self.validate()

    def add_entry(self, sample, module, source_file, colname, value, note=""):
        # Add a data column for a sample to a QCReport
        # Add sample if it doesn't exist in report
        if sample not in self.report:
            self.report[sample] = []

        # Add data column if it doesn't exist in report
        self.report[sample].append({"Module"     :module,
                                    "Source"     :source_file,
                                    "Name"       :colname,
                                    "Value"      :value,
                                    "Note"       :note})

    def add_entries(self, sample, data):
        # Add multiple data columns to a QCReport
        if sample not in self.report:
            self.report[sample] = []
        self.report[sample].extend(data)

    def rbind(self, qc_report):
        # Append all Samples from another QCReport
        # Check to make sure Reports contain same number of columns
        if self.n_columns() != qc_report.n_columns():
            logging.error("Rbind error: QCReports have differing number of columns (%s vs %s)" % (self.n_columns(), qc_report.n_columns()))
            raise QCReportError("Unable to rbind QCReports!")

        for sample in qc_report.get_sample_names():
            # Make sure sample doesn't already exist
            if sample in self.get_sample_names():
                logging.error("Rbind error: Duplicate sample: %s" % sample)
                raise QCReportError("Unable to rbind QCReports!")
            # Add data from sample to existing QCReport
            self.add_entries(sample, data=qc_report.get_sample_data(sample))

        # Validate to make sure QCReport is still valid
        self.validate()

    def cbind(self, qc_report):
        # Append all columns from another QCReport
        # Check to make sure reports contain same number of rows
        if self.n_samples() != qc_report.n_samples():
            logging.error("Cbind error: QCReports have differing number of samples (%s vs %s)" % (self.n_samples(), qc_report.n_samples()))
            raise QCReportError("Unable to rbind QCReports!")

        for sample in qc_report.get_sample_names():
            # Check to make sure sample exists in current report
            if sample not in self.get_sample_names():
                logging.error("Cbind error: Sample '%s' doesn't appear in both reports!" % sample)
                raise QCReportError("Unable to cbind QCReports!")

            # Add data from sampe to existing QCReport
            self.add_entries(sample, data=qc_report.get_sample_data(sample))

        # Validate to make sure QCReport is still valid
        self.validate()

    def get_sample_names(self):
        return self.report.keys()

    def get_colnames(self, sample):
        # Get data colnames associated with a sample
        return [x["Name"] for x in self.get_sample_data(sample)]

    def get_sample_data(self, sample):
        if sample not in self.get_sample_names():
            logging.error("Sample '%s' not found in QCReport!")
            raise QCReportError("Cannot get data of non-existant sample!")
        return self.report[sample]

    def get_entry(self, sample, index):
        sample_data = self.get_sample_data(sample)
        if index >= len(sample_data) or index < 0:
            logging.error("Invalid QCReport column index: %s" % index)
            raise QCReportError("Invalid QCReport column index!")
        return sample_data[index]

    def n_samples(self):
        return len(self.get_sample_names())

    def n_columns(self):
        if len(self.get_sample_names()) == 0:
            return 0
        return len(self.get_colnames(self.get_sample_names()[0]))

    def validate(self):
        # Determine whether QCReport is valid
        for sample_name, sample_data in self.report.iteritems():
            # Make sure every data point in every sample row contains only the required fields
            for sample_column in sample_data:
                if not "".join(sorted(sample_column.keys())) == "ModuleNameNoteSourceValue":
                    logging.error("Entry in QCReport for sample %s does not contain required columns!" % sample_name)
                    raise QCReportError("Invalid QCReport schema.")

        # Check to make sure QCReport is square
        if not self.is_square():
            # Check if
            logging.error("QCReport is not square! Not all rows have same number of columns!")
            raise QCReportError("Invalid QCReport! Not all rows have same number of columns!")

        # Check to make sure all rows in QCReport have columns in same order
        if not self.is_ordered():
            logging.error("QCReport is not ordered! Data columns are not same for every sample or are not in same order!")
            raise QCReportError("Invalid QCReport! Data columns are not same for every sample or are not in same order!")

    def is_square(self):
        # Return True if all rows have same number of columns
        row_len = -1
        for sample in self.get_sample_names():
            if row_len == -1:
                row_len = len(self.get_colnames(sample))
            else:
                if len(self.get_colnames(sample)) != row_len:
                    return False
        return True

    def is_ordered(self):
        # Return True if columns in every row are in same order
        row_order = ""
        for sample in self.get_sample_names():
            if row_order == "":
                row_order = "_".join(self.get_colnames(sample))
            elif "_".join(self.get_colnames(sample)) != row_order:
                return False
        return True

    def __str__(self):
        return json.dumps(self.report, indent=4, sort_keys=True)



