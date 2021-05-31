
python finetune_bart.py \
--data_dir=wiki_pos \
--gpus 1 \
--learning_rate=3e-5 \
--output_dir=bart_large_wiki_pretrained_results \
--num_train_epochs 10 \
--train_batch_size 16 --eval_batch_size 16 \
--max_source_length=150 \
--max_target_length=100 \
--val_max_target_length=100 \
--test_max_target_length=100 \
--sortish_sampler \
--model_name_or_path facebook/bart-large  \
--task  rdf2text \
--do_train \
--early_stopping_patience 15 \
--warmup_steps 2 \
--eval_beams 5 \
--do_predict \
 "$@"


python finetune_bart.py \
--data_dir=pos \
--gpus 1 \
--learning_rate=3e-5 \
--output_dir=bart_large_wiki_final_results \
--num_train_epochs 5 \
--train_batch_size 16 --eval_batch_size 32 \
--max_source_length=150 \
--max_target_length=100 \
--val_max_target_length=100 \
--test_max_target_length=100 \
--model_name_or_path  bart_large_wiki_pretrained_results/best_tfmr \
--task  rdf2text \
--do_train \
--early_stopping_patience 20 \
--warmup_steps 2 \
--eval_beams 3 \
--do_predict \
 "$@"
