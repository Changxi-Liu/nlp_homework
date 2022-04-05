f = open("./train.txt","r")
lines = f.readlines();
wf_4 = open('4.txt','w')
wf_1_4 = open('14.txt','w')
wf_1_2 = open('12.txt','w')
wf_2 = open('2.txt','w')

ec = []
ec_blocks = []
ec_word_counter = 0
for line in lines:
	if '<EOS>' in line:
		ec_word_counter = 0
	if 'B-X' in line:
		ec_word_counter += 1
	if '\n' == line:
		ec.append(ec_word_counter)
		ec_word_counter = 0

ec_block = []
counter = 0
for line in lines:
	ec_block.append(line)
	if '\n' == line:
		number_ec_lines = ec[counter]
		if number_ec_lines != 0:
			ec_words = ec_block[-ec[counter]:]
			# once get the ec_words, we can try to handle them

			# for example, double
			ec_block.pop()
			ec_block += ec_words
		for i in ec_block:
			wf_2.writelines(i)



		ec_block = []
		counter += 1
ec_block = []
counter = 0
for line in lines:
	ec_block.append(line)
	if '\n' == line:
		number_ec_lines = ec[counter]
		if number_ec_lines != 0:
			ec_words = ec_block[-ec[counter]:]

			# # quadra
			ec_block.pop() #remove /n
			ec_block += ec_words

			ec_block.pop() #remove /n
			ec_block += ec_words

		for i in ec_block:
			wf_4.writelines(i)

		ec_block = []
		counter += 1


ec_block = []
counter = 0
for line in lines:
	ec_block.append(line)
	if '\n' == line:
		number_ec_lines = ec[counter]
		if number_ec_lines != 0:
			ec_words = ec_block[-ec[counter]:]
			# for example, half
			ec_block.pop()
			ec_block = ec_block[:-(int(ec[counter]/2))]
			ec_block.append('\n')
		for i in ec_block:
			wf_1_2.writelines(i)

		ec_block = []
		counter += 1

ec_block = []
counter = 0
for line in lines:
	ec_block.append(line)
	if '\n' == line:
		number_ec_lines = ec[counter]
		if number_ec_lines != 0:
			ec_words = ec_block[-ec[counter]:]
			# for example, quater
			ec_block.pop()
			ec_block = ec_block[:-(int(ec[counter]/4*3))]
			ec_block.append('\n')
		for i in ec_block:
			wf_1_4.writelines(i)

		ec_block = []
		counter += 1
# for line in lines:
# 	wf.writelines()