from copy import deepcopy
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

from build_aat_report_docx import NS, paragraph, table, w


ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / "NewsLens_AAT_Report.docx"
OUTPUT = ROOT / "NewsLens_AAT_Report_expanded.docx"


def text_of(node):
    return "".join(node.xpath(".//w:t/text()", namespaces=NS)).strip()


def extra_sections():
    return {
        "Chapter 4  Literature Review": [
            paragraph("4.1 Comparison of Approaches", style="Heading2", size=13, bold=True),
            paragraph("A rule-based system can identify fixed words such as shocking or urgent, but it is easy to bypass and cannot learn from examples. A TF-IDF classifier learns a larger vocabulary from the dataset while remaining fast enough for local deployment. Deep neural models may capture more context, but they also require careful tuning, more computation and stronger validation."),
            paragraph("4.2 Position of the Present Work", style="Heading2", size=13, bold=True),
            paragraph("The present work is positioned as an explainable baseline and an end-to-end application. The aim is not to claim state-of-the-art factual verification. The aim is to show how an NLP model can be trained, evaluated, saved, exposed through an API and presented responsibly to a user."),
        ],
        "Chapter 8  Performance Evaluation": [
            paragraph("8.3 Metric Meaning", style="Heading2", size=13, bold=True),
            table([
                ["Metric", "Meaning in this project"],
                ["Accuracy", "The proportion of all held-out rows classified correctly."],
                ["Precision", "Among rows predicted as fake/misleading, the proportion that had the fake label in the test set."],
                ["Recall", "Among fake/misleading rows in the test set, the proportion found by the model."],
                ["F1-score", "The harmonic mean of precision and recall, useful when both types of error matter."],
            ], [1900, 5400]),
            paragraph("8.4 Error Analysis and Generalisation", style="Heading2", size=13, bold=True),
            paragraph("A model can be wrong even when its held-out score is high. A credible article may use dramatic language and become a false positive. A misleading article may imitate a formal news style and become a false negative. New events, new publishers, satire, opinion writing and different political topics can differ from the training distribution."),
            paragraph("The random split is useful for a reproducible classroom experiment, but it may be optimistic if related articles, publishers or repeated writing patterns occur in both training and testing data. A future evaluation should consider time-based and publisher-independent splits."),
            paragraph("8.5 Evaluation Boundary", style="Heading2", size=13, bold=True),
            paragraph("The reported values describe the current ISOT dataset experiment only. They should not be converted into a claim that the system is accurate for every real-world news article. During a demonstration, an unexpected prediction should be treated as an error case to discuss rather than hidden."),
        ],
        "Chapter 9  Output and Results": [
            paragraph("9.1 User Interface Flow", style="Heading2", size=13, bold=True),
            paragraph("The user opens the browser interface, enters text and selects the analysis action. JavaScript sends a JSON request to the Flask endpoint. The response is rendered as a score card, a cautious label, a description, the selected model and a list of language signals. The page also communicates that the result requires verification."),
            paragraph("9.2 Demonstration Scenarios", style="Heading2", size=13, bold=True),
            table([
                ["Scenario", "Expected system behaviour"],
                ["Short credible-style headline", "Use the headline pipeline and return a lower or mixed screening signal."],
                ["Short sensational headline", "Use the headline pipeline and may display risk vocabulary or emphasis signals."],
                ["Long article text", "Use the article pipeline because the input is longer than 60 words."],
                ["Empty input", "Reject the request with a validation message instead of predicting."],
                ["Very long input", "Reject text above the 10,000-character limit."],
            ], [2500, 4800]),
            paragraph("9.3 Interpretation of Signals", style="Heading2", size=13, bold=True),
            paragraph("The signals shown by the interface are additional indicators: sensational vocabulary, exclamation-mark emphasis, evidence-related vocabulary and simple token/sentence statistics. They are not a formal explanation of every Logistic Regression decision and they do not override the model probability."),
            paragraph("9.4 Reproducibility", style="Heading2", size=13, bold=True),
            paragraph("Repeatable headline examples are stored in data/test_cases.csv. The project also records model metadata, class distribution and dataset hash in the saved artifact metadata. This allows the team to identify which training input produced the current evaluation result."),
        ],
        "Chapter 10 Conclusion": [
            paragraph("10.1 Project Contribution", style="Heading2", size=13, bold=True),
            paragraph("The project connects data preparation, NLP feature extraction, supervised learning, evaluation and web deployment in one application. The separate headline and article pipelines demonstrate a simple form of input-aware model selection. The saved artifact makes the application usable without retraining on every launch."),
            paragraph("10.2 Practical Learning", style="Heading2", size=13, bold=True),
            paragraph("The main practical lesson is that a classifier output must be interpreted together with its data and evaluation boundary. A high test score does not remove the need for source checking. Responsible deployment therefore includes uncertainty, limitation reporting and a human decision-maker."),
        ],
    }


def build():
    if not SOURCE.exists():
        raise FileNotFoundError(SOURCE)
    with ZipFile(SOURCE) as source:
        root = etree.fromstring(source.read("word/document.xml"))
        body = root.find(w("body"))
        additions = extra_sections()
        for heading, nodes in additions.items():
            target = None
            for child in body:
                if child.tag == w("p") and text_of(child) == heading:
                    target = child
                    break
            if target is None:
                raise ValueError(f"Heading not found: {heading}")
            position = body.index(target)
            for node in nodes:
                body.insert(position, deepcopy(node))
                position += 1
        document_xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")

        with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as target:
            for item in source.infolist():
                payload = source.read(item.filename)
                if item.filename == "word/document.xml":
                    payload = document_xml
                target.writestr(item, payload)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build()
