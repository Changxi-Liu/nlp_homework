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
        ext_sent = dict()
        count = 0
        
        flag = True
        for line in d:
            if line.startswith('\n'):
                flag = True
                count += 1
                orig_sent[count] = []
            
            if line.startswith('<EOS>'):
                flag = False
                ext_sent[count] = []
                
            if not line.startswith('-DOCSTART-'):
                if flag:
                    orig_sent[count].append(line)
                else:
                    ext_sent[count].append(line)
            
        doc_dict[n]= {
            'orig': orig_sent,
            'ext': ext_sent
        }
    
    return doc_dict

# merge two sequential sentences as one
def output(doc_dict, output_file):
    for n, d in doc_dict.items():
        for i in range(1, len(d['orig'])):

            for sent in d['orig'][i]:
                output_file.write(sent)
            
            for sent in d['orig'][i+1]:
                if sent != '\n':
                    output_file.write(sent)
            
            if i in d['ext']:
                for sent in d['ext'][i]:
                    output_file.write(sent)
            
            if i+1 in d['ext']:
                for sent in d['ext'][i+1]:
                    if sent.startswith('<EOS>'):
                        sent = sent.replace('<EOS>', '')
                    output_file.write(sent)

#===============================================================
def main():
    input_file_path = '../CLNER_datasets/conll_03_bertscore_eos_doc_full/dev.txt'
    f = open(input_file_path, "r")
    data = f.readlines()
    output_file_path = '../CLNER_datasets/conll_03_bertscore_eos_doc_full/merge_two_dev.txt'
    output_file = open(output_file_path, "a")

    doc_dict = get_doc(data)
    output(doc_dict, output_file)

if __name__ == '__main__':
    main()

