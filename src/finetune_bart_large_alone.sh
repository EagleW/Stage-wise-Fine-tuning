python finetune_bart.py \
--data_dir=pos \
--gpus 1 \
--learning_rate=3e-5 \
--output_dir=new_bart_large_results \
--num_train_epochs 3 \
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