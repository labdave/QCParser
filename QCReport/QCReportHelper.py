import logging
import json

from QCReport import QCReport

class QCReportHelper:

    @staticmethod
    def load(qc_report_file):
        try:
            return QCReport(json.load(open(qc_report_file,"r")))
        except BaseException, e:
            logging.error("Unable to load QCReport from file: %s" % qc_report_file)
            if e.message != "":
                logging.error("Received following error msg:\n%s" % e.message)
                raise
