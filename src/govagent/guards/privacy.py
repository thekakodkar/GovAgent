from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern
from presidio_anonymizer import AnonymizerEngine

class PrivacyGuard:
    """Article 9 Compliance: PII & Location Redaction."""
    def __init__(self, policy):
        self.analyzer = AnalyzerEngine()
        self.anonymizer = AnonymizerEngine()
        
        # INSTITUTIONAL FIX: Regex to capture street addresses (resolves '123 Main St' leak)
        address_regex = r"\d+\s+[A-Z][a-z]+\s+(St|Ave|Rd|Blvd|Street|Road|Lane)"
        address_pattern = Pattern(name="address_pattern", regex=address_regex, score=0.8)
        address_recognizer = PatternRecognizer(supported_entity="LOCATION", patterns=[address_pattern])
        
        self.analyzer.registry.add_recognizer(address_recognizer)
        self.target_entities = ["PERSON", "LOCATION", "PHONE_NUMBER", "EMAIL_ADDRESS"]

    def redact_task(self, text: str) -> str:
        results = self.analyzer.analyze(text=text, entities=self.target_entities, language='en')
        return self.anonymizer.anonymize(text=text, analyzer_results=results).text