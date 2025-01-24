# devto-analytics

### data collection 
Use SQLlite to store the data and use cron job to run the script daily.

`0 * * * * cd /path/to/script/blog-stats/main.py && python3 main.py`