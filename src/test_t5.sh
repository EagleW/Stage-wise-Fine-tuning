python finetune_t5_test.py \
--data_dir=pos \
--gpus 1 \
--learning_rate=3e-5 \
--output_dir=t5_large_pos_test_results \
--train_batch_size 6 --eval_batch_size 6 \
--max_source_length=120 \
--max_target_length=100 \
--val_max_target_length=100 \
--checkpoint=final_model_results/val_avg_bleu=61.9200-step_count=0.ckpt \
--test_max_target_length=100 \
--eval_max_gen_length=100 \
--model_name_or_path final_model_results/best_tfmr \
--task translation \
--early_stopping_patience 15 \
--warmup_steps 2 \
--do_predict \
--lr_scheduler cosine_w_restarts \
--eval_beams 3
 "$@"
