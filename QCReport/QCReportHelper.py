from QCReport import QCReport

class QCReportHelper:

    @staticmethod
    def read_report_from_file(qc_report_file):
        pass

    @staticmethod
    def write_report_to_table(qc_report, delim="\t", include_cols=None, col_headers=None):
        pass

    @staticmethod
    def rbind(qc_reports):
        # Bind on or more QCReports into single report
        new_qc_report = QCReport()
        for qc_report in qc_reports:
            for sample in qc_report.get_rownames():
                new_qc_report.add_row(sample, qc_report.get_row(sample))

        return new_qc_report

    @staticmethod
    def cbind(qc_reports):
        new_qc_report = QCReport()
        for qc_report in qc_reports:
            for i in range(len(qc_report.get_colnames)):
                new_qc_report.add_col(qc_report.get_col(i))
        return new_qc_report