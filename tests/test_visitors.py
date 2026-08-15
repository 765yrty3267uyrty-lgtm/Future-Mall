import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'python_modules'))

from visitors_analysis import VisitorsAnalyzer


class TestVisitorsAnalyzer:
    def setup_method(self):
        self.analyzer = VisitorsAnalyzer()

    def test_validate_visitor_count_valid(self):
        assert self.analyzer.validate_visitor_count("100") == 100
        assert self.analyzer.validate_visitor_count("0") == 0
        assert self.analyzer.validate_visitor_count("  250  ") == 250

    def test_validate_visitor_count_invalid(self):
        assert self.analyzer.validate_visitor_count("-10") is None
        assert self.analyzer.validate_visitor_count("abc") is None
        assert self.analyzer.validate_visitor_count("") is None

    def test_calculate_statistics(self):
        self.analyzer.visitor_data = [100, 150, 200, 180, 220, 300, 160]
        results = self.analyzer.calculate_statistics()

        assert results['total'] == 1310
        assert results['average'] == 187.14
        assert results['maximum'] == 300
        assert results['minimum'] == 100
        assert results['max_day'] == 'Saturday'
        assert results['min_day'] == 'Monday'
        assert results['days_recorded'] == 7
        assert results['median'] == 180
        assert results['range'] == 200
        assert results['pct_change_max_min'] == 200.0

    def test_calculate_statistics_single_day(self):
        self.analyzer.visitor_data = [100]
        results = self.analyzer.calculate_statistics()
        assert results['total'] == 100
        assert results['average'] == 100.0
        assert results['maximum'] == 100
        assert results['minimum'] == 100
        assert results['max_day'] == 'Monday'
        assert results['min_day'] == 'Monday'

    def test_calculate_statistics_zero_min(self):
        self.analyzer.visitor_data = [100, 0, 50]
        results = self.analyzer.calculate_statistics()
        assert results['minimum'] == 0
        assert results['pct_change_max_min'] == float('inf')

    def test_load_from_excel(self):
        excel_path = os.path.join(os.path.dirname(__file__), '..',
                                  'python_modules', 'data', 'visitors_data.xlsx')
        assert os.path.exists(excel_path)
        assert self.analyzer.load_from_excel(excel_path)
        assert len(self.analyzer.visitor_data) == 7
        assert len(self.analyzer.days) == 7

    def test_excel_busiest_quietest_day(self):
        excel_path = os.path.join(os.path.dirname(__file__), '..',
                                  'python_modules', 'data', 'visitors_data.xlsx')
        self.analyzer.load_from_excel(excel_path)
        results = self.analyzer.calculate_statistics()
        assert results['max_day'] == 'Saturday'
        assert results['min_day'] == 'Monday'

    def test_generate_chart_creates_png(self):
        excel_path = os.path.join(os.path.dirname(__file__), '..',
                                  'python_modules', 'data', 'visitors_data.xlsx')
        self.analyzer.load_from_excel(excel_path)
        self.analyzer.calculate_statistics()
        chart = self.analyzer.generate_chart()
        assert chart.endswith('.png')
        assert os.path.exists(chart)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])