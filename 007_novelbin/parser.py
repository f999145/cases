from bs4 import BeautifulSoup as BS
from typing import Iterator

def _pars_urls(urls_page: str) -> Iterator[str]:
    soup = BS(urls_page, 'html.parser')
    option = soup.find_all('option')
    for op in option:
        yield op.get('value')

