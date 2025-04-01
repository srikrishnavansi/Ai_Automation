import json
import pandas as pd
from typing import List, Dict
import logging
from pathlib import Path
import sys
import os
from datetime import datetime

# Add the project root directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from langchain_google_genai import GoogleGenerativeAI
from langchain.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from src.utils.config import GOOGLE_API_KEY, ELEMENTS_JSON_PATH, TEST_CASES_PATH

# Configure verbose logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

class TestCaseGenerator:
    def __init__(self, elements_json_path: str = ELEMENTS_JSON_PATH):
        self.elements_json_path = elements_json_path
        self.logger = logging.getLogger(__name__)
        self.elements = self._load_elements()
        
        if not GOOGLE_API_KEY:
            raise ValueError("GOOGLE_API_KEY not found in environment variables")
            
        self.llm = GoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=GOOGLE_API_KEY,
            temperature=0.7,
            verbose=True
        )
        
        self.logger.info(f"Initialized TestCaseGenerator at {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC")
        self.logger.info(f"Current user: {os.getlogin()}")

    def _load_elements(self) -> Dict:
        """Load elements from JSON file"""
        try:
            if not os.path.exists(self.elements_json_path):
                raise FileNotFoundError(f"Elements JSON file not found at {self.elements_json_path}")
                
            with open(self.elements_json_path, 'r') as f:
                elements = json.load(f)
                self.logger.debug(f"Loaded elements from {self.elements_json_path}: {json.dumps(elements, indent=2)}")
                return elements
        except IOError as e:
            self.logger.error(f"Failed to load elements JSON: {str(e)}")
            raise

    def create_test_case_prompt(self) -> str:
        """Create prompt for test case generation"""
        return """
        You are a test automation expert. Based on the following website UI elements, generate 5 detailed test cases.

        Website UI Elements:
        {elements}

        Generate exactly 5 test cases in a valid JSON array format. Each test case should be a JSON object with these exact keys:
        - Test_Case_ID (format: TC001, TC002, etc.)
        - Test_Scenario (clear description of what is being tested)
        - Steps_to_Execute (numbered steps)
        - Expected_Result (clear success criteria)

        Focus areas:
        1. User authentication flows
        2. Navigation and menu interactions
        3. Form submissions and validations
        4. Error handling scenarios
        5. Data validation checks

        IMPORTANT: Return ONLY the JSON array without any additional text or explanation.
        Example format:
        [
            {{
                "Test_Case_ID": "TC001",
                "Test_Scenario": "Verify user login with valid credentials",
                "Steps_to_Execute": "1. Navigate to login page\\n2. Enter valid username\\n3. Enter valid password\\n4. Click login button",
                "Expected_Result": "User should be successfully logged in and redirected to dashboard"
            }}
        ]
        """

    def generate_test_cases(self) -> List[Dict]:
        """Generate test cases using Gemini"""
        try:
            self.logger.info("Starting test case generation")
            
            prompt = PromptTemplate(
                template=self.create_test_case_prompt(),
                input_variables=["elements"]
            )

            # Create the chain using the new syntax
            chain = prompt | self.llm

            # Invoke the chain
            self.logger.debug("Invoking LLM chain")
            response = chain.invoke({
                "elements": json.dumps(self.elements, indent=2)
            })
            
            self.logger.debug(f"Raw LLM response: {response}")

            # Clean and parse the response
            test_cases = self._format_response(response)
            
            self.logger.info(f"Successfully generated {len(test_cases)} test cases")
            self.logger.debug(f"Generated test cases: {json.dumps(test_cases, indent=2)}")
            
            return test_cases

        except Exception as e:
            self.logger.error(f"Failed to generate test cases: {str(e)}")
            raise

    def _format_response(self, response: str) -> List[Dict]:
        """Format and clean the LLM response"""
        try:
            self.logger.debug(f"Formatting response: {response}")
            
            # Clean the response text to ensure it's valid JSON
            response_str = str(response).strip()
            start_idx = response_str.find('[')
            end_idx = response_str.rfind(']') + 1
            
            if start_idx == -1 or end_idx == 0:
                raise ValueError("Could not find JSON array in response")
                
            json_str = response_str[start_idx:end_idx]
            self.logger.debug(f"Extracted JSON string: {json_str}")
            
            test_cases = json.loads(json_str)
            
            # Validate the structure
            for test_case in test_cases:
                required_keys = ["Test_Case_ID", "Test_Scenario", "Steps_to_Execute", "Expected_Result"]
                missing_keys = [key for key in required_keys if key not in test_case]
                if missing_keys:
                    raise ValueError(f"Test case missing required keys: {missing_keys}")
            
            return test_cases
            
        except Exception as e:
            self.logger.error(f"Failed to format response: {str(e)}")
            self.logger.error(f"Raw response: {response}")
            raise

    def export_to_excel(self, output_path: str = TEST_CASES_PATH) -> None:
        """Export test cases to Excel file"""
        try:
            self.logger.info(f"Starting export to Excel: {output_path}")
            
            test_cases = self.generate_test_cases()
            
            if not test_cases:
                raise ValueError("No test cases were generated")
                
            df = pd.DataFrame(test_cases)
            
            # Create output directory if it doesn't exist
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            df.to_excel(output_path, index=False)
            self.logger.info(f"Successfully exported test cases to {output_path}")
            self.logger.debug(f"Excel file contents:\n{df.to_string()}")
        
        except Exception as e:
            self.logger.error(f"Failed to export test cases: {str(e)}")
            raise

if __name__ == "__main__":
    try:
        generator = TestCaseGenerator()
        generator.export_to_excel()
    except Exception as e:
        logging.error(f"Script failed: {str(e)}")
        logging.error(f"Current UTC time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}")
        logging.error(f"Current user: {os.getlogin()}")
        sys.exit(1)