python3 main.py \
	--filepath ./data/raw_example.txt \
	--pattern "(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.\d{6}) ([A-Z]*) .*" \
	--alpha 0.1 \
	--op gt \
	--beta 1.5 \
	--levels INFO WARN ERROR CRITICAL \
	-t "2022-12-16 04:22:38.338809" \
	-m 15
