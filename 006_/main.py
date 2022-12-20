# import os
from operations_with_paths import ChangeDir
from config import current
from monitoring_progress import monitor_add
from get_page import get_page_pagination, get_pages, run_page_async
from scrapper import get_pagination, get_info_book
from decor import spent_time

@spent_time
def main():
    ChangeDir(current)
    monitor_add()
    get_page_pagination()
    get_pagination()
    # get_pages()
    run_page_async()
    get_info_book()
    
if __name__ == '__main__':
    main()