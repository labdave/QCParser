from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException


class ClonotypeT(BaseParser):

	DESCRIPTION     = 'Parse Clonotype calling output for T loci'
	INPUT_FILE_DESC = 'Clonotype calling output'


	def __init__(self, sys_args):
		super(ClonotypeT, self).__init__(sys_args)


	def parse_input(self):
		# Parse clonotype calling
		first_line = True

		trb_count, tra_count, trg_count, trd_count = 0, 0, 0, 0
		trb_sequence, tra_sequence, trg_sequence, trd_sequence = '', '', '', ''
		trb_v, tra_v, trg_v, trd_v = '', '', '', ''
		trb_d, trd_d = '', ''
		trb_j, tra_j, trg_j, trd_j = '', '', '', ''
		trb_c, tra_c, trg_c, trd_c = '', '', '', ''

		with open(self.input_file, 'r') as f:
			for line in f:
				data = line.replace('\t', '|').strip().split('|')

				if first_line:
					first_line = False
					# check to make sure file actually clonotype calling file
					if 'clone' not in line:
						raise QCParseException('File provided is not output from Clonotype calling')

				if 'TRA' in line:
					tra_count = int(float(data[0]))
					tra_sequence = data[2]
					tra_v = data[3]
					tra_j = data[5]
					tra_c = data[6]

				if 'TRB' in line:
					trb_count = int(float(data[0]))
					trb_sequence = data[2]
					trb_v = data[3]
					trb_d = data[4]
					trb_j = data[5]
					trb_c = data[6]

				if 'TRG' in line:
					trg_count = int(float(data[0]))
					trg_sequence = data[2]
					trg_v = data[3]
					trg_j = data[5]
					trg_c = data[6]

				if 'TRD' in line:
					trd_count = int(float(data[0]))
					trd_sequence = data[2]
					trd_v = data[3]
					trd_d = data[4]
					trd_j = data[5]
					trd_c = data[6]

		# add clonotype fields
		self.add_entry('tra_count', tra_count)
		self.add_entry('trb_count', trb_count)
		self.add_entry('trg_count', trg_count)
		self.add_entry('trd_count', trd_count)
		self.add_entry('tra_sequence', tra_sequence)
		self.add_entry('trb_sequence', trb_sequence)
		self.add_entry('trg_sequence', trg_sequence)
		self.add_entry('trd_sequence', trd_sequence)
		self.add_entry('tra_v', tra_v)
		self.add_entry('trb_v', trb_v)
		self.add_entry('trg_v', trg_v)
		self.add_entry('trd_v', trd_v)
		self.add_entry('trb_d', trb_d)
		self.add_entry('trd_d', trd_d)
		self.add_entry('tra_j', tra_j)
		self.add_entry('trb_j', trb_j)
		self.add_entry('trg_j', trg_j)
		self.add_entry('trd_j', trd_j)
		self.add_entry('tra_c', tra_c)
		self.add_entry('trb_c', trb_c)
		self.add_entry('trg_c', trg_c)
		self.add_entry('trd_c', trd_c)

	def define_required_colnames(self):
		return [
			'tra_count', 'trb_count', 'trg_count', 'trd_count',
			'tra_sequence', 'trb_sequence', 'trg_sequence', 'trd_sequence',
			'tra_v', 'trb_v', 'trg_v', 'trd_v', 'trb_d', 'trd_d',
			'tra_j', 'trb_j', 'trg_j', 'trd_j', 'tra_c', 'trb_c', 'trg_c', 'trd_c']