"""
Feature extraction service for plumbing job descriptions.

This module uses OpenAI's ChatGPT API to extract structured features from
natural language descriptions of plumbing jobs. The extracted features are
compatible with the PlumbingPredictor model for cost and time estimation.
"""

import os
import json
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Try to import OpenAI, but don't fail if not installed yet
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    print("Warning: openai package not installed. Install with: pip install openai")


class FeatureExtractor:
    """
    Extract plumbing job features from natural language using ChatGPT.

    This class interfaces with OpenAI's ChatGPT API to convert natural language
    descriptions of plumbing jobs into structured feature dictionaries that can
    be used with the PlumbingPredictor model.

    Attributes:
        client (OpenAI): OpenAI API client instance
        model (str): ChatGPT model to use (default: gpt-4)

    Example:
        >>> extractor = FeatureExtractor()
        >>> job_desc = "I need a luxury bathroom with 2 toilets and a big shower"
        >>> features = extractor.extract_features(job_desc)
        >>> print(features['toilet'])  # 2
        >>> print(features['showerCabinType'])  # "Luxury_Enclosure"
    """

    # System instructions for ChatGPT feature extraction
    SYSTEM_PROMPT = """You are a feature extraction system for a plumbing cost estimation model. Your task is to extract structured data from natural language descriptions of plumbing jobs.

USER INPUT: Natural language description of a plumbing job
YOUR OUTPUT: A JSON object with exactly 17 features

REQUIRED OUTPUT FORMAT:
Return ONLY a valid JSON object with these exact keys (case-sensitive):

{
  "boilerSize": "<value>",
  "radiator": <integer>,
  "radiatorType": "<value>",
  "toilet": <integer>,
  "toileType": "<value>",
  "washbasin": <integer>,
  "washbasinType": "<value>",
  "bathhub": <integer>,
  "bathhubType": "<value>",
  "showerCabin": <integer>,
  "showerCabinType": "<value>",
  "Bidet": <integer>,
  "BidetType": "<value>",
  "waterHeater": <integer>,
  "waterHeaterType": "<value>",
  "sinkTypeQuality": "<value>",
  "sinkCategorie": "<value>"
}

FEATURE DEFINITIONS AND VALID VALUES:

1. boilerSize (string):
   Valid values: "small", "medium", "big"
   Default: "medium"
   Extract from: mentions of boiler size

2. radiator (integer):
   Valid range: 0-16
   Default: 5
   Extract from: number of radiators mentioned

3. radiatorType (string):
   Valid values: "COPA_Aluminium", "FONDITAL_ARDENTE_C2", "GLOBAL_ISEO_350", "Helyos_Evo", "Primavera_H500", "Samochauf_SAHD", "Sira_Alice_Royal"
   Default: "Primavera_H500"
   Extract from: specific radiator model/brand mentioned, or infer from quality level

4. toilet (integer):
   Valid range: 0-3
   Default: 2
   Extract from: number of toilets mentioned

5. toileType (string):
   Valid values: "Basic-Ceramic", "One-Piece", "Wall-Hung"
   Default: "One-Piece"
   Extract from: toilet type/style mentioned, or infer from quality indicators

6. washbasin (integer):
   Valid range: 0-3
   Default: 2
   Extract from: number of washbasins/sinks mentioned

7. washbasinType (string):
   Valid values: "Countertop", "Pedestal", "Wall-Mounted"
   Default: "Pedestal"
   Extract from: washbasin style mentioned

8. bathhub (integer):
   Valid range: 0-2
   Default: 1
   Extract from: number of bathtubs mentioned (note: if only showers mentioned, set to 0)

9. bathhubType (string):
   Valid values: "Standard", "Luxury"
   Default: "Standard"
   Extract from: bathtub quality mentioned

10. showerCabin (integer):
    Valid range: 0-2
    Default: 1
    Extract from: number of showers mentioned

11. showerCabinType (string):
    Valid values: "Basic_Enclosure", "Luxury_Enclosure"
    Default: "Basic_Enclosure"
    Extract from: shower quality/type mentioned

12. Bidet (integer):
    Valid range: 0-2
    Default: 0
    Extract from: number of bidets mentioned (0 if not mentioned)

13. BidetType (string):
    Valid values: "Bidet-Ceramic", "Bidet-Mixer-Tap", "Wall-Hung"
    Default: "Bidet-Mixer-Tap"
    Extract from: bidet type mentioned

14. waterHeater (integer):
    Valid range: 0-2
    Default: 1
    Extract from: number of water heaters mentioned

15. waterHeaterType (string):
    Valid values: "Electric-30liters", "Electric-50liters", "GAS-6liters", "GAS-11liters"
    Default: "Electric-50liters"
    Extract from: water heater capacity/fuel type mentioned

16. sinkTypeQuality (string):
    Valid values: "poor", "high"
    Default: "high"
    Extract from: overall quality indicators (budget/economy → "poor", premium/quality → "high")

17. sinkCategorie (string):
    Valid values: "single", "double"
    Default: "single"
    Extract from: whether kitchen sink is single or double basin

EXTRACTION RULES:

1. QUANTITY EXTRACTION:
   - Look for explicit numbers: "3 toilets", "5 radiators", "two bathrooms"
   - Infer from context: "master bathroom" (1 toilet, 1 washbasin, 1 shower/bath)
   - Home size clues: "2-bedroom apartment" → fewer fixtures, "5-bedroom house" → more fixtures

2. QUALITY INFERENCE:
   - Keywords "luxury", "premium", "high-end", "designer" → use Luxury types, "high" quality
   - Keywords "basic", "standard", "economy", "budget" → use Standard/Basic types, may use "poor" quality
   - Keywords "cheap", "minimal", "builder-grade" → use poor quality
   - No quality mentioned → use defaults (moderate quality)

3. TYPE MAPPING:
   - "wall-mounted toilet" → "Wall-Hung"
   - "modern toilet" / "one-piece toilet" → "One-Piece"
   - "standard toilet" → "Basic-Ceramic"
   - "pedestal sink" → "Pedestal"
   - "vessel sink" / "countertop sink" → "Countertop"
   - "floating sink" → "Wall-Mounted"
   - "double kitchen sink" → sinkCategorie: "double"
   - "tankless water heater" → interpret size/fuel type mentioned
   - "electric water heater" → default to "Electric-50liters"
   - "gas water heater" → default to "GAS-11liters"

4. CONTEXT CLUES:
   - "full bathroom" = toilet + washbasin + bathtub/shower
   - "half bath" = toilet + washbasin
   - "master bathroom" = typically includes bathtub AND shower
   - "en-suite" = private bathroom (1 toilet, 1 washbasin, 1 shower/bath)
   - "powder room" = half bath

5. DEFAULT BEHAVIOR:
   - If a fixture is not mentioned, use the default count and type
   - If quality is not mentioned, assume standard/moderate quality
   - All 17 fields MUST be present in the output
   - Never return null or undefined values

6. VALIDATION:
   - Ensure all string values exactly match the valid values (case-sensitive)
   - Ensure all integers are within valid ranges
   - Return only the JSON object, no additional text or explanation

EXAMPLES:

Input: "I need to install a luxury bathroom with a wall-hung toilet, luxury shower, and a pedestal sink"
Output:
{
  "boilerSize": "medium",
  "radiator": 5,
  "radiatorType": "Primavera_H500",
  "toilet": 1,
  "toileType": "Wall-Hung",
  "washbasin": 1,
  "washbasinType": "Pedestal",
  "bathhub": 0,
  "bathhubType": "Standard",
  "showerCabin": 1,
  "showerCabinType": "Luxury_Enclosure",
  "Bidet": 0,
  "BidetType": "Bidet-Mixer-Tap",
  "waterHeater": 1,
  "waterHeaterType": "Electric-50liters",
  "sinkTypeQuality": "high",
  "sinkCategorie": "single"
}

Input: "Complete plumbing for a 3-bedroom house: 3 bathrooms, kitchen with double sink, big boiler, 8 radiators"
Output:
{
  "boilerSize": "big",
  "radiator": 8,
  "radiatorType": "Primavera_H500",
  "toilet": 3,
  "toileType": "One-Piece",
  "washbasin": 3,
  "washbasinType": "Pedestal",
  "bathhub": 2,
  "bathhubType": "Standard",
  "showerCabin": 1,
  "showerCabinType": "Basic_Enclosure",
  "Bidet": 0,
  "BidetType": "Bidet-Mixer-Tap",
  "waterHeater": 1,
  "waterHeaterType": "Electric-50liters",
  "sinkTypeQuality": "high",
  "sinkCategorie": "double"
}

Input: "Budget bathroom renovation: basic fixtures, 1 toilet, 1 shower, 1 sink, small electric water heater"
Output:
{
  "boilerSize": "medium",
  "radiator": 5,
  "radiatorType": "Primavera_H500",
  "toilet": 1,
  "toileType": "Basic-Ceramic",
  "washbasin": 1,
  "washbasinType": "Pedestal",
  "bathhub": 0,
  "bathhubType": "Standard",
  "showerCabin": 1,
  "showerCabinType": "Basic_Enclosure",
  "Bidet": 0,
  "BidetType": "Bidet-Mixer-Tap",
  "waterHeater": 1,
  "waterHeaterType": "Electric-30liters",
  "sinkTypeQuality": "poor",
  "sinkCategorie": "single"
}

CRITICAL: Return ONLY the JSON object. Do not include explanations, markdown formatting, or any other text."""

    # Required feature keys for validation
    REQUIRED_FEATURES = [
        'boilerSize', 'radiator', 'radiatorType', 'toilet', 'toileType',
        'washbasin', 'washbasinType', 'bathhub', 'bathhubType', 'showerCabin',
        'showerCabinType', 'Bidet', 'BidetType', 'waterHeater', 'waterHeaterType',
        'sinkTypeQuality', 'sinkCategorie'
    ]

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize the FeatureExtractor with OpenAI API credentials.

        Parameters:
            api_key (str, optional): OpenAI API key. If not provided, will load from
                                    OPENAI_API_KEY environment variable (conda env or .env file).
            model (str, optional): ChatGPT model to use. If not provided, will load
                                  from OPENAI_MODEL environment variable or default to 'gpt-4'.

        Raises:
            ImportError: If openai package is not installed
            ValueError: If no API key is provided or found in environment

        Environment Variables:
            You can set OPENAI_API_KEY using either:
            - Conda: conda env config vars set OPENAI_API_KEY=your_key
            - .env file: Create models/.env with OPENAI_API_KEY=your_key
            - Shell: export OPENAI_API_KEY=your_key
        """
        if not OPENAI_AVAILABLE:
            raise ImportError(
                "OpenAI package is not installed. "
                "Install it with: pip install openai"
            )

        # Load environment variables from .env file (won't override conda/shell vars)
        load_dotenv()

        # Get API key from parameter or environment (conda env, .env file, or shell)
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "No OpenAI API key provided. Set it using:\n"
                "  - Parameter: FeatureExtractor(api_key='your_key')\n"
                "  - Conda env: conda env config vars set OPENAI_API_KEY=your_key\n"
                "  - .env file: Create models/.env with OPENAI_API_KEY=your_key\n"
                "  - Shell: export OPENAI_API_KEY=your_key"
            )

        # Initialize OpenAI client
        self.client = OpenAI(api_key=self.api_key)

        # Get model from parameter or environment
        self.model = model or os.getenv("OPENAI_MODEL", "gpt-4")

    def extract_features(self, job_description: str) -> Dict[str, Any]:
        """
        Extract structured features from natural language job description.

        This method sends the job description to ChatGPT with specific instructions
        to extract the 17 required features for the plumbing cost prediction model.

        Parameters:
            job_description (str): Natural language description of the plumbing job

        Returns:
            dict: Dictionary with 17 features required by PlumbingPredictor:
                - boilerSize (str): "small", "medium", or "big"
                - radiator (int): Number of radiators
                - radiatorType (str): Type of radiator
                - toilet (int): Number of toilets
                - toileType (str): Type of toilet
                - washbasin (int): Number of washbasins
                - washbasinType (str): Type of washbasin
                - bathhub (int): Number of bathtubs
                - bathhubType (str): Type of bathtub
                - showerCabin (int): Number of shower cabins
                - showerCabinType (str): Type of shower cabin
                - Bidet (int): Number of bidets
                - BidetType (str): Type of bidet
                - waterHeater (int): Number of water heaters
                - waterHeaterType (str): Type of water heater
                - sinkTypeQuality (str): "poor" or "high"
                - sinkCategorie (str): "single" or "double"

        Raises:
            ValueError: If job_description is empty or invalid
            RuntimeError: If ChatGPT API call fails
            json.JSONDecodeError: If ChatGPT response is not valid JSON
            KeyError: If required features are missing from response

        Example:
            >>> extractor = FeatureExtractor()
            >>> features = extractor.extract_features(
            ...     "Renovate bathroom with luxury fixtures: 1 wall-hung toilet, 1 shower"
            ... )
            >>> features['toilet']
            1
            >>> features['toileType']
            'Wall-Hung'
            >>> features['showerCabinType']
            'Luxury_Enclosure'
        """
        # Validate input
        if not job_description or not job_description.strip():
            raise ValueError("Job description cannot be empty")

        try:
            # Call ChatGPT API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self.SYSTEM_PROMPT},
                    {"role": "user", "content": job_description}
                ],
                temperature=0.1,  # Low temperature for consistent extraction
                max_tokens=500,   # Sufficient for JSON response
                response_format={"type": "json_object"}  # Ensure JSON response
            )

            # Extract response content
            content = response.choices[0].message.content

            # Parse JSON response
            features = json.loads(content)

            # Validate all required features are present
            missing_features = [f for f in self.REQUIRED_FEATURES if f not in features]
            if missing_features:
                raise KeyError(
                    f"ChatGPT response missing required features: {missing_features}"
                )

            return features

        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Failed to parse ChatGPT response as JSON: {e.msg}",
                e.doc,
                e.pos
            )
        except Exception as e:
            raise RuntimeError(f"ChatGPT API call failed: {str(e)}")

    def extract_features_with_fallback(
        self,
        job_description: str,
        default_features: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Extract features with fallback to defaults if API call fails.

        This is a safer alternative to extract_features() that won't raise exceptions
        if the API call fails. Instead, it returns default feature values.

        Parameters:
            job_description (str): Natural language description of the plumbing job
            default_features (dict, optional): Custom default features to use on failure.
                                              If not provided, uses standard defaults.

        Returns:
            dict: Extracted features or defaults if extraction fails

        Example:
            >>> extractor = FeatureExtractor()
            >>> features = extractor.extract_features_with_fallback(
            ...     "Install 2 toilets and a shower"
            ... )
            # Returns extracted features or defaults on error
        """
        try:
            return self.extract_features(job_description)
        except Exception as e:
            print(f"Warning: Feature extraction failed ({str(e)}), using defaults")

            # Return provided defaults or standard defaults
            if default_features:
                return default_features

            return {
                "boilerSize": "medium",
                "radiator": 5,
                "radiatorType": "Primavera_H500",
                "toilet": 2,
                "toileType": "One-Piece",
                "washbasin": 2,
                "washbasinType": "Pedestal",
                "bathhub": 1,
                "bathhubType": "Standard",
                "showerCabin": 1,
                "showerCabinType": "Basic_Enclosure",
                "Bidet": 0,
                "BidetType": "Bidet-Mixer-Tap",
                "waterHeater": 1,
                "waterHeaterType": "Electric-50liters",
                "sinkTypeQuality": "high",
                "sinkCategorie": "single"
            }


# Example usage
if __name__ == "__main__":
    # Example: Extract features from natural language
    extractor = FeatureExtractor()

    # Example job descriptions
    examples = [
        "I need a luxury bathroom with a wall-hung toilet, luxury shower, and a pedestal sink",
        "Complete plumbing for a 3-bedroom house: 3 bathrooms, kitchen with double sink, big boiler, 8 radiators",
        "Budget bathroom renovation: basic fixtures, 1 toilet, 1 shower, 1 sink, small electric water heater"
    ]

    for desc in examples:
        print(f"\n{'='*80}")
        print(f"Job Description: {desc}")
        print(f"{'='*80}")

        try:
            features = extractor.extract_features(desc)
            print(json.dumps(features, indent=2))
        except Exception as e:
            print(f"Error: {e}")
