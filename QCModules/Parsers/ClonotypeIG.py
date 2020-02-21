from BaseParser import BaseParser
from QCModules.BaseModule import QCParseException


class ClonotypeIG(BaseParser):

	DESCRIPTION     = 'Parse Clonotype calling output for IG loci'
	INPUT_FILE_DESC = 'Clonotype calling output'


	def __init__(self, sys_args):
		super(ClonotypeIG, self).__init__(sys_args)


	def parse_input(self):
		# Parse clonotype calling
		first_line = True

		igh_count, igk_count, igl_count = 0, 0, 0
		igh_sequence, igk_sequence, igl_sequence = '', '', ''
		igh_v, igk_v, igl_v = '', '', ''
		igh_d = ''
		igh_j, igk_j, igl_j = '', '', ''
		igh_c, igk_c, igl_c = '', '', ''

		with open(self.input_file, 'r') as f:
			for line in f:
				data = line.replace('\t', '|').strip().split('|')

				if first_line:
					first_line = False
					# check to make sure file actually clonotype calling file
					if 'clone' not in line:
						raise QCParseException('File provided is not output from Clonotype calling')

				if 'IGH' in line:
					igh_count = int(float(data[0]))
					igh_sequence = data[2]
					igh_v = data[3]
					igh_d = data[4]
					igh_j = data[5]
					igh_c = data[6]

				if 'IGK' in line:
					igk_count = int(float(data[0]))
					igk_sequence = data[2]
					igk_v = data[3]
					igk_j = data[5]
					igk_c = data[6]

				if 'IGL' in line:
					igl_count = int(float(data[0]))
					igl_sequence = data[2]
					igl_v = data[3]
					igl_j = data[5]
					igl_c = data[6]

		# add clonotype fields
		self.add_entry('igh_count', igh_count)
		self.add_entry('igk_count', igk_count)
		self.add_entry('igl_count', igl_count)
		self.add_entry('igh_sequence', igh_sequence)
		self.add_entry('igk_sequence', igk_sequence)
		self.add_entry('igl_sequence', igl_sequence)
		self.add_entry('igh_v', igh_v)
		self.add_entry('igk_v', igk_v)
		self.add_entry('igl_v', igl_v)
		self.add_entry('igh_d', igh_d)
		self.add_entry('igh_j', igh_j)
		self.add_entry('igk_j', igk_j)
		self.add_entry('igl_j', igl_j)
		self.add_entry('igh_c', igh_c)
		self.add_entry('igk_c', igk_c)
		self.add_entry('igl_c', igl_c)

	def define_required_colnames(self):
		return [
			'igh_count', 'igk_count', 'igl_count',
			'igh_sequence', 'igk_sequence', 'igl_sequence',
			'igh_v', 'igk_v', 'igl_v', 'igh_d',
			'igh_j', 'igk_j', 'igl_j', 'igh_c', 'igk_c', 'igl_c']