#ModelName=first_epoch
#CUDA_VISIBLE_DEVICES=0 python train.py   --config config/wnut17_doc2.yaml 2>&1|tee ${ModelName}
#CUDA_VISIBLE_DEVICES=0 python train.py --test --gen  --config config/wnut17_doc2.yaml 
#
###prapare data
#cp resources/taggers/${ModelName}/test.tsv CLNER_datasets/wnut17_bertscore_eos_doc_full3/train.txt
#ModelName=second_epoch
#CUDA_VISIBLE_DEVICES=0 python train.py   --config config/wnut17_doc3.yaml 2>&1|tee ${ModelName}
#CUDA_VISIBLE_DEVICES=0 python train.py --test --gen  --config config/wnut17_doc3.yaml 
###prapare data
#cp resources/taggers/${ModelName}/test.tsv CLNER_datasets/wnut17_bertscore_eos_doc_full4/train.txt
#ModelName=third_epoch
#CUDA_VISIBLE_DEVICES=0 python train.py   --config config/wnut17_doc4.yaml 2>&1|tee ${ModelName}
##CLNER_datasets/wnut17_bertscore_eos_doc_full2/train.txt


#cp resources/taggers/${ModelName}/test.tsv CLNER_datasets/wnut17_bertscore_eos_doc_full4/train.txt
ModelName=third_epoch
#CUDA_VISIBLE_DEVICES=0 python train.py   --config config/wnut17_doc4.yaml 2>&1|tee ${ModelName}
##CLNER_datasets/wnut17_bertscore_eos_doc_full2/train.txt
cp -r CLNER_datasets/wnut17_bertscore_eos_doc_full4/ CLNER_datasets/wnut17_bertscore_eos_doc_full5
CUDA_VISIBLE_DEVICES=0 python train.py --gen --test   --config config/wnut17_doc4.yaml 

cp resources/taggers/${ModelName}/test.tsv CLNER_datasets/wnut17_bertscore_eos_doc_full5/train.txt
ModelName=epoch_4
CUDA_VISIBLE_DEVICES=0 python train.py   --config config/wnut17_doc5.yaml 2>&1|tee ${ModelName}
#CLNER_datasets/wnut17_bertscore_eos_doc_full2/train.txt
