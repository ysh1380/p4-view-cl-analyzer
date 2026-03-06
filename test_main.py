import unittest
from unittest.mock import patch
import main  # type: ignore
from main import get_template_view_lines, get_changes_with_desc, Change  # type: ignore

class TestP4Analyzer(unittest.TestCase):

    @patch('main.run_p4')
    def test_get_template_view_lines(self, mock_run_p4):
        # p4 client -t template -o 출력 모사
        mock_run_p4.return_value = """
Client: product_template
View:
	//depot/project/main/... //product_template/main/...
	//depot/project/release/... //product_template/release/...
"""
        paths = get_template_view_lines("product_template")
        
        expected = ["//depot/project/main/...", "//depot/project/release/..."]
        self.assertEqual(paths, expected)

    @patch('main.run_p4')
    def test_get_changes_with_desc(self, mock_run_p4):
        # p4 changes -l 출력 모사
        mock_run_p4.return_value = """
Change 1500123 on 2026/02/28 14:35:22 by dev.kim@client
	[UI] 버튼 색상 피드백 반영
	추가 설명 부분...

Change 1500156 on 2026/03/01 09:12:45 by tester.park@client
	린트 에러 전체 수정
"""
        changes = get_changes_with_desc("//depot/project/main/...", 1500000, 1505000)
        
        self.assertEqual(len(changes), 2)
        self.assertEqual(changes[0].cl, 1500123)
        self.assertEqual(changes[0].user, "dev.kim")
        self.assertEqual(changes[0].desc, "[UI] 버튼 색상 피드백 반영")
        
        self.assertEqual(changes[1].cl, 1500156)
        self.assertEqual(changes[1].user, "tester.park")
        self.assertEqual(changes[1].desc, "린트 에러 전체 수정")

if __name__ == '__main__':
    unittest.main()
