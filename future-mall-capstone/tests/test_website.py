import os

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

import pytest

WEBSITE_HTML = os.path.join(os.path.dirname(__file__), '..', 'website', 'index.html')


@pytest.fixture(scope='module')
def soup():
    with open(WEBSITE_HTML, encoding='utf-8') as f:
        return BeautifulSoup(f, 'html.parser')


@pytest.mark.skipif(not HAS_BS4, reason='BeautifulSoup not installed')
class TestWebsite:
    def test_html_structure(self, soup):
        assert soup.find('header') is not None
        assert soup.find('nav') is not None
        assert soup.find('main') is not None
        assert soup.find('footer') is not None

        assert soup.find('section', id='home') is not None
        assert soup.find('section', id='about') is not None
        assert soup.find('section', id='modules') is not None

    def test_accessibility(self, soup):
        skip_link = soup.find('a', class_='skip-link')
        assert skip_link is not None
        assert skip_link.get('href') == '#main'

        nav = soup.find('nav')
        assert nav.get('aria-label') == 'Main navigation'

        for img in soup.find_all('img'):
            assert img.get('alt') is not None

    def test_responsive_meta(self, soup):
        viewport = soup.find('meta', attrs={'name': 'viewport'})
        assert viewport is not None
        assert 'width=device-width' in viewport['content']

    def test_css_linked(self, soup):
        css_link = soup.find('link', href='style.css')
        assert css_link is not None
        assert css_link['rel'] == ['stylesheet']

    def test_title(self, soup):
        assert 'Future Mall' in soup.title.string

    def test_asset_files_present(self):
        for name in ['logo-primary.svg', 'logo-stacked.svg', 'logo-icon.svg']:
            path = os.path.join(os.path.dirname(WEBSITE_HTML), 'assets', name)
            assert os.path.isfile(path), f'Missing asset: {name}'

    def test_task4_logo_png_used(self, soup):
        """Interconnectivity criterion: the Task 4 logo PNG is used on the page."""
        srcs = [img.get('src', '') for img in soup.find_all('img')]
        assert any(s.endswith('logo-primary.png') for s in srcs)
        png_path = os.path.join(os.path.dirname(WEBSITE_HTML), 'assets', 'logo-primary.png')
        assert os.path.isfile(png_path)

    def test_five_stores_unnumbered_list(self, soup):
        store_list = soup.find('ul', class_='store-list')
        assert store_list is not None
        items = store_list.find_all('li')
        assert len(items) == 5


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
