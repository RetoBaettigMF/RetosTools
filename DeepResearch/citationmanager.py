class CitationManager:
    def __init__(self):
        self.sources = defaultdict(list)
    
    def add_source(self, fact_hash: str, source: dict):
        self.sources[fact_hash].append(source)
    
    def generate_citations(self, report: str) -> str:
        annotated_report = []
        for paragraph in report.split("\n\n"):
            facts = extract_facts(paragraph)
            citations = [self.sources[hash(fact)] for fact in facts]
            annotated_report.append(f"{paragraph}\nSources: {citations}")
        return "\n\n".join(annotated_report)