import pandas as pd
from typing import Dict, List
import logging
from pathlib import Path
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from src.utils.config import GOOGLE_API_KEY, TEST_CASES_PATH, TEST_SCRIPTS_PATH
class SeleniumScriptGenerator:
    def __init__(self, test_cases_path: str = TEST_CASES_PATH):
        self.test_cases_path = test_cases_path
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.test_cases = self._load_test_cases()
        self.llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.3,
            verbose=True
        )

    def _load_test_cases(self) -> pd.DataFrame:
        """Load test cases from Excel file"""
        try:
            return pd.read_excel(self.test_cases_path)
        except Exception as e:
            self.logger.error(f"Failed to load test cases: {str(e)}")
            raise

    def create_selenium_script_prompt(self) -> str:
        """Create prompt for Selenium script generation"""
        prompt_template = """
        Generate a Python Selenium script for the following test case:

        Test Case ID: {test_case_id}
        Test Scenario: {test_scenario}
        Steps to Execute: {steps}
        Expected Result: {expected_result}

        Requirements:
        1. Use Python and Selenium WebDriver
        2. Include proper waits and error handling
        3. Use Page Object Model pattern
        4. Include documentation and comments
        5. Handle exceptions appropriately
        6. Include logging
        7. Return the complete script as a single string

        Generate a complete, runnable Python script that implements this test case.
        """
        return prompt_template

    def generate_selenium_script(self, test_case: Dict) -> str:
        """Generate Selenium script for a test case using Gemini"""
        try:
            prompt = PromptTemplate(
                template=self.create_selenium_script_prompt(),
                input_variables=["test_case_id", "test_scenario", "steps", "expected_result"]
            )

            chain = LLMChain(llm=self.llm, prompt=prompt)
            
            response = chain.run(
                test_case_id=test_case['Test_Case_ID'],
                test_scenario=test_case['Test_Scenario'],
                steps=test_case['Steps_to_Execute'],
                expected_result=test_case['Expected_Result']
            )
            
            return response.strip()

        except Exception as e:
            self.logger.error(f"Failed to generate Selenium script: {str(e)}")
            raise

    def export_to_excel(self, output_path: str = TEST_SCRIPTS_PATH) -> None:
        """Export generated scripts to Excel file"""
        try:
            scripts_data = []
            for _, test_case in self.test_cases.iterrows():
                selenium_script = self.generate_selenium_script(test_case)
                scripts_data.append({
                    'Test_Case_ID': test_case['Test_Case_ID'],
                    'Test_Scenario': test_case['Test_Scenario'],
                    'Selenium_Script': selenium_script
                })

            df = pd.DataFrame(scripts_data)
            
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            df.to_excel(output_path, index=False)
            self.logger.info(f"Successfully exported Selenium scripts to {output_path}")
        
        except Exception as e:
            self.logger.error(f"Failed to export Selenium scripts: {str(e)}")
            raise

if __name__ == "__main__":
    generator = SeleniumScriptGenerator()
    generator.export_to_excel()