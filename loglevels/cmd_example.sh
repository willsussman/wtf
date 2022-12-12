python3 main.py \
	--filepath ./logs/example_log.txt \
	--pattern "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}) ([A-Z]*) .*" \
	--alpha 0.1 \
	--op gt \
	--beta 1.5 \
	--levels INFO WARN ERROR CRITICAL
