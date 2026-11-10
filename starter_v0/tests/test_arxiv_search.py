import unittest
from unittest.mock import patch, MagicMock
from tools.arxiv_search.tool import run as arxiv_search_run

class TestArxivSearch(unittest.TestCase):

    @patch("tools.arxiv_search.tool.requests.get")
    def test_arxiv_search_success(self, mock_get):
        # 1. Chuẩn bị dữ liệu XML mẫu trả về từ arXiv API
        sample_xml = b"""<?xml version="1.0" encoding="UTF-8"?>
        <feed xmlns="http://www.w3.org/2005/Atom">
            <entry>
                <id>http://arxiv.org/abs/2301.00001</id>
                <title>Test Arxiv Paper Title</title>
                <summary>This is a test summary of the paper.</summary>
            </entry>
        </feed>
        """
        
        # Giả lập phản hồi thành công của requests.get
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = sample_xml
        mock_get.return_value = mock_response

        # 2. Gọi hàm arxiv_search
        result = arxiv_search_run(query="machine learning", max_results=1)

        # 3. Kiểm tra kết quả
        self.assertIn("results", result)
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0]["title"], "Test Arxiv Paper Title")
        self.assertEqual(result["results"][0]["link"], "http://arxiv.org/abs/2301.00001")
        self.assertEqual(result["results"][0]["summary"], "This is a test summary of the paper.")

    def test_arxiv_search_empty_query(self):
        # Truyền query rỗng để kiểm tra điều kiện validate đầu vào
        result = arxiv_search_run(query="")
        
        # Kiểm tra kết quả trả về phải chứa key "error"
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Query cannot be empty")

    @patch("tools.arxiv_search.tool.requests.get")
    def test_arxiv_search_network_error(self, mock_get):
        # Giả lập requests.get ném ra ngoại lệ (ví dụ: lỗi mạng / ConnectionError)
        mock_get.side_effect = Exception("Network connection failed")

        # Gọi hàm
        result = arxiv_search_run(query="quantum computing")

        # Kiểm tra xử lý lỗi an toàn, kết quả trả về phải chứa key "error"
        self.assertIn("error", result)
        self.assertEqual(result["error"], "Network connection failed")

if __name__ == "__main__":
    unittest.main()