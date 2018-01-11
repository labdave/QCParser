import logging
import json
import collections

class QCReportError(Exception):
    pass

class QCReport:

    def __init__(self):
        # Initialize report from existing dictionary or from empty dict
        self.report     = {}

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

    def add_entry(self, sample, module, source_file, colname, value):
        # Add a data column for a sample to a QCReport
        # Add sample if it doesn't exist in report
        if sample not in self.report:
            self.report[sample] = []

        # Add data column if it doesn't exist in report
        self.report[sample].append({"Module"     :module,
                                    "Source"     :source_file,
                                    "Name"       :colname,
                                    "Value"      :value})

    def add_entries(self, sample, data):
        # Add multiple data columns to a QCReport
        if sample not in self.report:
            self.report[sample] = []
        self.report[sample].extend(data)

    def validate_schema(self):
        # Determine whether QCReport is valid
        pass

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
        return json.dumps(self.report)



    def add_row(self, sample, entries):
        # Add a row of sample data to existing QCReport

        # Make sure sample isn't already in report
        if sample in self.report:
            logging.error("Attempt to add duplicate sample row to QCReport: %s!" % sample)
            raise IOError("Attempt to add duplicate sample row to QCReport.")

        # Check row contains same number of columns
        if len(entries) != len(self.get_colnames()):
            logging.error("Attempt to add row to QCReport with different number of columns (%s vs. %s)!" % (len(row), len(self.get_colnames())))
            raise IOError("Attempt to add row to QCReport with different number of columns!")

        # Check columns in same order
        col_order = [x["Name"] for x in entries]
        if "".join(self.get_colnames()) != "".join(col_order):
            logging.error("Attempt to add row to QCReport with different column order!")
            raise IOError("Attempt to add row to QCReport with different column order!")

        # Add sample data row to report
        self.report[sample] = entries

    def add_col(self, samples, entries):
        # Make sure column contains same number of rows
        if len(col_data) != len(self.get_rownames()):
            logging.error("Attempt to add column to QCReport with different number of samples (%s vs. %s)!" % (len(col_data.keys()), len(self.get_rownames())))
            raise IOError("Attempt to add column to QCReport with different number of samples!")

        # Make sure samples are in same order
        row_order = col_data.keys()
        if "".join(self.get_rownames()) != "".join(row_order):
            logging.error("Attempt to add col to QCReport with different sample order!")
            raise IOError("Attempt to add col to QCReport with different sample order!")

        for sample, data in col_data.iteritems():
            self.report[sample].append(data)

    def get_row(self, sample):
        return self.report[sample]

    def get_col(self, index):
        col_data = collections.OrderedDict()
        for sample, data in self.report.iteritems():
            col_data[sample] = data[index]
        return col_data

    def get_colnames_old(self):
        if self.n_cols() == 0:
            return []
        return [ x["Name"] for x in self.report[self.get_rownames()[0]]]

    def get_rownames(self):
        return self.report.keys()




