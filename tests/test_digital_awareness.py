import os

try:
    from bs4 import BeautifulSoup
    HAS_BS4 = True
except ImportError:
    HAS_BS4 = False

import pytest

BASE = os.path.join(os.path.dirname(__file__), '..', 'digital_awareness')


def read_html(name):
    with open(os.path.join(BASE, name), encoding='utf-8') as f:
        return BeautifulSoup(f, 'html.parser')


@pytest.mark.skipif(not HAS_BS4, reason='BeautifulSoup not installed')
class TestDigitalAwareness:
    def test_threats_page_structure(self):
        soup = read_html('threats.html')
        threats = soup.find_all('article', class_='threat-card')
        assert len(threats) == 8

        for threat in threats:
            assert threat.find('h3', class_='threat-title') is not None
            assert threat.find('span', class_='threat-severity') is not None

    def test_password_checker_elements(self):
        soup = read_html('password.html')
        assert soup.find('input', id='password-input') is not None
        assert soup.find('button', id='toggle-visibility') is not None
        assert soup.find('button', id='generate-btn') is not None
        assert soup.find('div', id='meter-fill') is not None

    def test_quiz_page_structure(self):
        soup = read_html('quiz.html')
        assert soup.find('button', id='start-quiz') is not None
        assert soup.find('div', id='quiz-area') is not None
        assert soup.find('button', id='next-btn') is not None

    def test_posters_page_structure(self):
        soup = read_html('posters.html')
        posters = soup.find_all('article', class_='poster-card')
        assert len(posters) == 6

    def test_posters_have_download_buttons(self):
        soup = read_html('posters.html')
        download_btns = soup.find_all('button', attrs={'data-poster': True})
        assert len(download_btns) >= 6

    def test_all_pages_link_shared_css(self):
        for name in ['index.html', 'threats.html', 'password.html', 'quiz.html', 'posters.html']:
            soup = read_html(name)
            css_link = soup.find('link', href='style.css')
            assert css_link is not None, f'{name} missing style.css'

    def test_navigation_is_present(self):
        for name in ['index.html', 'threats.html', 'password.html', 'quiz.html', 'posters.html']:
            soup = read_html(name)
            assert soup.find('header') is not None, f'{name} missing header'
            assert soup.find('footer') is not None, f'{name} missing footer'


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
