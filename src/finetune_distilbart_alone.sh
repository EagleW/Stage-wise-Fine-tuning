python finetune.py \
--data_dir=pos \
--gpus 1 \
--learning_rate=3e-5 \
--output_dir=distillbart_results \
--num_train_epochs 10 \
--train_batch_size 4 --eval_batch_size 4 \
--max_source_length=150 \
--max_target_length=100 \
--val_max_target_length=100 \
--test_max_target_length=100 \
--model_name_or_path sshleifer/distilbart-xsum-12-6 \
--task  rdf2text \
--do_train \
--early_stopping_patience 15 \
--eval_beams 5 \
--do_predict \
 "$@"