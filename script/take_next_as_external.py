"""
# transform data to dictionary doc_dict into the following format
# {
    0:[ --> doc id
        {0:{ --> sentence id
            'orig': [], --> original sentence
            'ext': [] --> correspondent external sentence
        }}
#   ],
#   1: [
    ...
]
# }
"""
def get_doc(data):
    doc = dict()
    doc_count = 0
    for line in data:
        if line.startswith('-DOCSTART-'):
            doc_count += 1
            doc[doc_count] = []
        
        doc[doc_count].append(line)
    
    doc_dict = dict()
    for n, d in doc.items():
        orig_sent = dict()
        count_sent = 0
        for line in d:
            if line.startswith('\n'):
                count_sent += 1
                orig_sent[count_sent] = []
            
            if not line.startswith('-DOCSTART-'):
                orig_sent[count_sent].append(line)
        doc_dict[n] = orig_sent
    
    return doc_dict

# replace pos chunk ner with B-X
def repalce_b_x(sent):
    sent = sent.split(' ')
    sent[1] = 'B-X'
    sent[2] = 'B-X'
    sent[3] = 'B-X\n'
    return ' '.join(sent)

# merge two sequential sentences as one
def output(doc_dict, output_file):
    for n, d in doc_dict.items():
        for i in range(1, len(d)):
            for sent in d[i]:
                output_file.write(sent)
            
            # previous and next sentence as external context
            output_file.write('<EOS> B-X B-X B-X\n')
            
            for sent in d[i+1]:
                if sent != '\n':
                    # replace pos chunk ner with B-X
                    sent = repalce_b_x(sent)
                    output_file.write(sent)

#===============================================================
def main():
    input_file_path = '../CLNER_datasets/conll_03_english/testb.txt'
    f = open(input_file_path, "r")
    data = f.readlines()
    output_file_path = '../CLNER_datasets/conll_03_english/new_testb.txt'
    output_file = open(output_file_path, "a")

    doc_dict = get_doc(data)
    output(doc_dict, output_file)

if __name__ == '__main__':
    main()

