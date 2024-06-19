import os
import pytest
import markdown
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from main import app

load_dotenv()

client = TestClient(app)

class TestMain:
    def setup_class(self):
        with open('tests/resources/diff_file.txt', 'r') as f:
            self.test_diff = f.read()

        self.prompt_types_present = True
        self.predef_prompt_types = [
            "package-vulnerabilities",
            "vulnerability-assessment",
            "pullrequest-review",
            "pullrequest-review-with-examples",
            "pullrequest-summary",
            "pullrequest-summary-perfile",
            "pullrequest-summary-with-work-item-context"
        ]

        self.headers_auth = {
            "X-API-CONSUMER": "system",
            "X-API-KEY": "system"
        }
        self.headers_noauth = {
            "X-API-CONSUMER": "system",
            "X-API-KEY": "wrong_key"
        }


    # test that the root endpoint returns 200 when authenticated
    def test_read_root_authenticated(self):
        response = client.get("/", headers=self.headers_auth)
        returned_prompt_types = [item['prompt_type'] for item in response.json() if 'prompt_type' in item]
        for prompt_type in self.predef_prompt_types:
            if prompt_type not in returned_prompt_types:
                self.prompt_types_present = False

        assert self.prompt_types_present
        assert response.status_code == 200


    # test that the root endpoint returns 401 when not authenticated
    def test_read_root_unauthenticated(self):
        response = client.get("/", headers=self.headers_noauth)

        assert response.status_code == 401


    # test that the predefined endpoint returns 200 when authenticated
    def test_pr_review_authenticated(self):
        response = client.post("/predefined", json={
            "prompt_type": "pullrequest-review",
            "prompt": f"{self.test_diff}"
        }, headers=self.headers_auth)

        assert markdown.markdown(response.json()) != ''
        assert response.status_code == 200


    # test that the pr review endpoint returns a 401 when not authenticated
    def test_pr_review_unauthenticated(self):
        response = client.post("/predefined", json={
            "prompt_type": "pullrequest-review",
            "prompt": f"{self.test_diff}"
        }, headers=self.headers_noauth)

        assert response.status_code == 401


    # test that the pr review with examples endpoint returns a 200 when authenticated
    def test_pr_review_with_examples_authenticated(self):
        response = client.post("/predefined", json={
            "prompt_type": "pullrequest-review-with-examples",
            "prompt": f"{self.test_diff}",
        }, headers=self.headers_auth)

        assert response.status_code == 200
        assert markdown.markdown(response.json()) != ''


    # test that the pr review with examples endpoint returns a 401 when not authenticated
    def test_pr_review_with_examples_unauthenticated(self):
        response = client.post("/predefined", json={
            "prompt_type": "pullrequest-review-with-examples",
            "prompt": f"{self.test_diff}",
        }, headers=self.headers_noauth)

        assert response.status_code == 401

 
    # test that the pr summary endpoint returns a 200 when authenticated
    def test_pr_summary_authenticated(self):
        response = client.post("/predefined", json={
            "prompt_type": "pullrequest-summary",
            "prompt": f"{self.test_diff}"
        }, headers=self.headers_auth)

        assert response.status_code == 200
        assert markdown.markdown(response.json()) != ''

    # test that the pr summary endpoint returns a 401 when not authenticated
    def test_pr_summary_unauthenticated(self):
        response = client.post("/predefined", json={
            "prompt_type": "pullrequest-summary",
            "prompt": f"{self.test_diff}"
        }, headers=self.headers_noauth)

        assert response.status_code == 401


    # test that the pr summary perfile endpoint returns a 200 when authenticated
    def test_pr_summary_perfile_authenticated(self):
        response = client.post("/predefined", json={
            "prompt_type": "pullrequest-summary-perfile",
            "prompt": f"{self.test_diff}"
        }, headers=self.headers_auth)

        assert response.status_code == 200
        assert markdown.markdown(response.json()) != ''


    # test that the pr summary perfile endpoint returns a 401 when not authenticated
    def test_pr_summary_perfile_unauthenticated(self):
        response = client.post("/predefined", json={
            "prompt_type": "pullrequest-summary-perfile",
            "prompt": f"{self.test_diff}"
        }, headers=self.headers_noauth)

        assert response.status_code == 401


if __name__ == "__main__":
    pytest.main()