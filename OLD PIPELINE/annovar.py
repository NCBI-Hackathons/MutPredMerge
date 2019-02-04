
class annovar:
	def __init__(self, data_file):
		self.file_type = data_file.split(".")[-1]
		if self.file_type == "exonic_variant_function":
			self.line_index = 0
			self.mutation_type = 1
			self.annotations = 2
			self.chromosome = 3
			self.posStart = 4
			self.posEnd = 5
			self.ref = 6
			self.alt = 7
			self.gene = None
		elif self.file_type == "variant_function":
			self.line_index = None
			self.annotations = None
			self.mutation_type = 0
			self.gene = 1
			self.chromosome = 2
			self.posStart = 3
			self.posEnd = 4
			self.ref = 5
			self.alt = 6

class tools:
	def __init__(self, annovar, row):
		self.file_type = annovar.file_type
		self.line_index = annovar.line_index
		self.mutation_type = annovar.mutation_type
		self.annotations = annovar.annotations
		self.chromosome = annovar.chromosome
		self.posStart = annovar.posStart
		self.posEnd = annovar.posEnd
		self.ref = annovar.ref
		self.alt = annovar.alt
		self.gene = annovar.gene
		row = ''.join(row)
		self.row = row.split("\t")
		
	def get_mut(self):
		return self.row[self.mutation_type]
		
	def get_var_full(self):
		variant = (self.row[self.chromosome], self.row[ self.posStart], self.row[ self.posEnd], self.row[ self.ref], self.row[ self.alt])
		return variant
	
	def get_var(self):
		variant = (self.row[self.chromosome], self.row[ self.posStart], self.row[ self.ref], self.row[ self.alt])
		return variant
	def get_gene(self):
		if  self.file_type == "exonic_variant_function":
			gene = self.row[ self.annotations].split(":")
			gene = gene[0]
			return gene
		elif  self.file_type == "variant_function":
			return self.row[ self.gene]
