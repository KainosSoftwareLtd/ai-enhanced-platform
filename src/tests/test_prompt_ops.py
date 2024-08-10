import os
import pytest
from dotenv import load_dotenv
from helpers import prompts
import re

load_dotenv()

class TestPromptOps:
    def setup_class(self):
        self.expected_prompts = [
            "package-vulnerabilities",
            "vulnerability-assessment",
            "pullrequest-review",
            "pullrequest-review-with-examples",
            "pullrequest-review-with-work-context",
            "pullrequest-summary",
            "pullrequest-summary-perfile",
            "pullrequest-summary-with-work-item-context"
        ]

        self.prompt = '''
        I want you to act as a cyber security specialist...
        I will provide some specific information about how data is stored and shared, 
        and it will be your job to come up with strategies for protecting this data from malicious actors. 
        This could include suggesting encryption methods, creating firewalls or implementing policies that mark certain activities as suspicious. 
        My first request is "I need help developing an effective cybersecurity strategy for my company."'''

    def test_retrieve_prompts(self):
        prompt_types = prompts.retrieve_prompts()
        prompt_items = [item['prompt_type'] for item in prompt_types if 'prompt_type' in item]

        known_p_set = set(self.expected_prompts)
        found_p_set = set(prompt_items)

        assert known_p_set == found_p_set

    def test_read_prompt(self):
        print("Test read prompt")
        prompt = prompts.read_prompt("pullrequest-review", "test", self.prompt)
        print(prompt)
        assert prompt is not None


    def test_prompt_compression(self):
        compressed_prompt = prompts.reduce_prompt_tokens(self.prompt)

        # check for comments
        pattern = r'#.*'
        match = re.search(pattern, compressed_prompt)
        assert match is None

        # check for 2 or more consecutive spaces
        pattern = r'  +'
        match = re.search(pattern, compressed_prompt)
        assert match is None

        # check that special chars have been removed
        pattern = r'\.{2,}'
        match = re.search(pattern, compressed_prompt)
        print(compressed_prompt)
        assert match is None

    def test_prompt_injection_detection(self):
        # Generate a prompt with more than 100000 unicode characters
        prompt = "a"*100001

        # Check for prompt injection
        result = prompts.check_for_prompt_inj(prompt)
        
        # Assert that the function returns False
        assert not result

    def test_retrieve_prompts_exc(self):
        # rename prompt file to force an exception
        os.rename('system_prompts/prompts.json', 'system_prompts/prompts.json.test')
        prompt_types = prompts.retrieve_prompts()
        assert len(prompt_types) == 0

        os.rename('system_prompts/prompts.json.test', 'system_prompts/prompts.json')

    def test_read_prompt_exc(self):
        print("Test read prompt exc")

        # rename prompt file to force an exception  
        os.rename('system_prompts/prompts.json', 'system_prompts/prompts.json.test')

        prompt = prompts.read_prompt("pullrequest-review", "test", self.prompt)

        assert prompt['system'] == ''

        os.rename('system_prompts/prompts.json.test', 'system_prompts/prompts.json')




