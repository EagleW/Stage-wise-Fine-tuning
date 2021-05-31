python finetune_t5.py \
--data_dir=wiki_pos \
--gpus 1 \
--learning_rate=3e-5 \
--output_dir=t5_base_wiki_pretrained_results \
--num_train_epochs 5 \
--train_batch_size 32 --eval_batch_size 32 \
--max_source_length=150 \
--max_target_length=100 \
--val_max_target_length=100 \
--test_max_target_length=100 \
--eval_max_gen_length=100 \
--model_name_or_path t5-base \
--task rdf2text \
--do_train \
--early_stopping_patience 15 \
--warmup_steps 2 \
--do_predict \
 "$@"

python finetune_t5.py \
--data_dir=pos \
--gpus 1 \
--learning_rate=3e-5 \
--output_dir=t5_base_wiki_final_results \
--num_train_epochs 10 \
--train_batch_size 32 --eval_batch_size 32 \
--max_source_length=150 \
--max_target_length=100 \
--val_max_target_length=100 \
--test_max_target_length=100 \
--eval_max_gen_length=100 \
--model_name_or_path t5_base_wiki_pretrained_results/best_tfmr \
--task rdf2text \
--do_train \
--early_stopping_patience 15 \
--warmup_steps 2 \
--do_predict \
--eval_beams 3 \
 "$@"
