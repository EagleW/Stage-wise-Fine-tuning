# base.txt pos pos+wiki wiki
python parent.py --predictions ../dev/t5_large/base.txt \
--references ../pos/val.target_eval ../pos/val.target2_eval ../pos/val.target3_eval \
--tables webnlg.jl \
--avg_results 