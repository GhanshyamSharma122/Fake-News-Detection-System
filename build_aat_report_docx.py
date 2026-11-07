from copy import deepcopy
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree


ROOT = Path(__file__).resolve().parent
TEMPLATE = Path(r"C:\Users\shyam\Downloads\Batch_9_NP_AAT_Report (1).docx")
OUTPUT = ROOT / "NewsLens_AAT_Report.docx"

W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
XML_NS = "http://www.w3.org/XML/1998/namespace"
NS = {"w": W_NS, "r": R_NS}


def w(tag):
    return f"{{{W_NS}}}{tag}"


def rpr(font="Times New Roman", size=11, bold=False, italic=False, color=None):
    props = etree.Element(w("rPr"))
    fonts = etree.SubElement(props, w("rFonts"))
    fonts.set(w("ascii"), font)
    fonts.set(w("hAnsi"), font)
    fonts.set(w("cs"), font)
    sz = etree.SubElement(props, w("sz"))
    sz.set(w("val"), str(size * 2))
    szcs = etree.SubElement(props, w("szCs"))
    szcs.set(w("val"), str(size * 2))
    if bold:
        etree.SubElement(props, w("b"))
    if italic:
        etree.SubElement(props, w("i"))
    if color:
        c = etree.SubElement(props, w("color"))
        c.set(w("val"), color)
    return props


def run(text, size=11, bold=False, italic=False, font="Times New Roman", color=None):
    node = etree.Element(w("r"))
    node.append(rpr(font, size, bold, italic, color))
    t = etree.SubElement(node, w("t"))
    t.set(f"{{{XML_NS}}}space", "preserve")
    t.text = text
    return node


def paragraph(text="", size=11, bold=False, italic=False, align="left", style=None,
             before=0, after=120, first_line=0, page_break_before=False):
    node = etree.Element(w("p"))
    ppr = etree.SubElement(node, w("pPr"))
    if style:
        ps = etree.SubElement(ppr, w("pStyle"))
        ps.set(w("val"), style)
    if align:
        jc = etree.SubElement(ppr, w("jc"))
        jc.set(w("val"), align)
    spacing = etree.SubElement(ppr, w("spacing"))
    spacing.set(w("before"), str(before))
    spacing.set(w("after"), str(after))
    spacing.set(w("line"), "276")
    spacing.set(w("lineRule"), "auto")
    if first_line:
        ind = etree.SubElement(ppr, w("ind"))
        ind.set(w("firstLine"), str(first_line))
    if page_break_before:
        etree.SubElement(ppr, w("pageBreakBefore"))
    if text:
        node.append(run(text, size=size, bold=bold, italic=italic))
    return node


def page_break():
    node = etree.Element(w("p"))
    r = etree.SubElement(node, w("r"))
    br = etree.SubElement(r, w("br"))
    br.set(w("type"), "page")
    return node


def bullet(text):
    node = paragraph(text, style="ListBullet", after=60)
    return node


def replace_paragraph_text(node, text):
    texts = node.xpath(".//w:t", namespaces=NS)
    if not texts:
        node.append(run(text, size=11))
        return
    texts[0].text = text
    texts[0].set(f"{{{XML_NS}}}space", "preserve")
    for extra in texts[1:]:
        extra.getparent().remove(extra)


def cell(text, width, bold=False):
    tc = etree.Element(w("tc"))
    tcpr = etree.SubElement(tc, w("tcPr"))
    tcw = etree.SubElement(tcpr, w("tcW"))
    tcw.set(w("w"), str(width))
    tcw.set(w("type"), "dxa")
    tc.append(paragraph(text, size=9.5, bold=bold, after=0))
    return tc


def table(rows, widths):
    tbl = etree.Element(w("tbl"))
    tblpr = etree.SubElement(tbl, w("tblPr"))
    borders = etree.SubElement(tblpr, w("tblBorders"))
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        item = etree.SubElement(borders, w(edge))
        item.set(w("val"), "single")
        item.set(w("sz"), "4")
        item.set(w("space"), "0")
        item.set(w("color"), "B7C9D6")
    grid = etree.SubElement(tbl, w("tblGrid"))
    for width in widths:
        col = etree.SubElement(grid, w("gridCol"))
        col.set(w("w"), str(width))
    for row_index, values in enumerate(rows):
        tr = etree.SubElement(tbl, w("tr"))
        if row_index == 0:
            trpr = etree.SubElement(tr, w("trPr"))
            etree.SubElement(trpr, w("tblHeader"))
        for value, width in zip(values, widths):
            tr.append(cell(value, width, bold=row_index == 0))
    return tbl


def chapter(title):
    return [page_break(), paragraph(title, style="Heading1", size=16, bold=True, after=180)]


def body_content():
    out = []
    out += [paragraph("Table of Contents", style="Heading1", size=16, bold=True, align="center", after=240)]
    toc = [
        "Chapter 1  Abstract",
        "Chapter 2  Objectives",
        "Chapter 3  Introduction",
        "Chapter 4  Literature Review",
        "Chapter 5  Research Gap",
        "Chapter 6  Problem Statement",
        "Chapter 7  Methodology and Implementation",
        "Chapter 8  Performance Evaluation",
        "Chapter 9  Output and Results",
        "Chapter 10 Conclusion",
        "Chapter 11 References",
    ]
    for item in toc:
        out.append(paragraph(item, size=11, after=80, first_line=360))

    out += chapter("Chapter 1  Abstract")
    out += [
        paragraph("NewsLens is a Natural Language Processing application that screens the language of news headlines and articles. It uses the ISOT Fake and Real News Dataset distributed through Kaggle, word-level TF-IDF features, and Logistic Regression classifiers. The system contains separate pipelines for short headlines and longer article text because these inputs provide different amounts of context."),
        paragraph("The trained models are saved in a joblib artifact and served through a Flask API. A browser interface accepts text, validates the request, selects the appropriate pipeline, and displays a probability-derived screening score with language signals. The result is deliberately presented as a verification aid rather than a final truth judgement."),
        paragraph("Keywords: Natural Language Processing, fake news detection, tokenization, TF-IDF, Logistic Regression, text classification, precision, recall, F1-score, Flask, explainable screening.", italic=True),
    ]

    out += chapter("Chapter 2  Objectives")
    out += [paragraph("The objectives of this AAT project are:")]
    for item in [
        "Study how NLP can be applied to a socially relevant misinformation-screening problem.",
        "Use a genuine labelled dataset instead of a small manually created sample.",
        "Build a reproducible training pipeline with a stratified held-out evaluation split.",
        "Train a headline model and an article model for different input lengths.",
        "Implement a working Flask API and browser interface for end-to-end analysis.",
        "Return a score, selected model, input mode and understandable language signals.",
        "Evaluate the models using accuracy, precision, recall and F1-score.",
        "Document limitations, bias, privacy and the need for human source verification.",
    ]:
        out.append(bullet(item))

    out += chapter("Chapter 3  Introduction")
    out += [
        paragraph("3.1 Background", style="Heading2", size=13, bold=True),
        paragraph("News is consumed through websites, social platforms and messaging applications. A headline can be seen and shared before the reader checks the original source. Misleading content may use emotional vocabulary, unsupported claims, excessive emphasis or imitation of a news-writing style."),
        paragraph("Natural Language Processing provides methods for representing written language as data. A supervised classifier can learn patterns from labelled examples and provide a first screening signal for new text."),
        paragraph("3.2 Project Scope", style="Heading2", size=13, bold=True),
        paragraph("NewsLens supports English headline and article inputs. It does not perform live web searches, verify citations, analyse images or videos, detect every type of satire or opinion, or make decisions about people. It should not be used for censorship, punishment or automatic content removal."),
        paragraph("3.3 Dataset", style="Heading2", size=13, bold=True),
        paragraph("The project uses Fake.csv with 23,481 rows and True.csv with 21,417 rows, giving 44,898 usable articles. Each file contains title, text, subject and date fields. The trainer derives the binary label from the source file name. Subject and date are retained in the source files but are not used as direct model features."),
    ]

    out += chapter("Chapter 4  Literature Review")
    out += [
        paragraph("Research on misinformation classification includes claim-level datasets, article-level datasets, social-context datasets, linguistic feature models and transformer-based methods. The LIAR benchmark is commonly used for short labelled claims, while FakeNewsNet combines news content with social-context information. These resources support research but may have access, copyright, collection and reproducibility constraints."),
        paragraph("Traditional text classification methods such as bag-of-words, TF-IDF and linear classifiers remain useful baselines because they are fast, relatively interpretable and easy to deploy. More complex neural models can capture broader language context, but they require careful comparison, larger resources and stronger validation."),
        paragraph("For this AAT implementation, TF-IDF with balanced Logistic Regression was selected as a practical baseline. The choice allows the team to demonstrate the complete lifecycle: data preparation, tokenization, feature extraction, training, evaluation, artifact saving, API inference and responsible interpretation."),
        table([
            ["Area", "Typical approach", "Relevance to NewsLens"],
            ["Claim datasets", "Short statements with truth-related labels", "Useful comparison for headline-sized inputs"],
            ["Social-context research", "News plus shares, comments or network signals", "Outside the current text-only scope"],
            ["Text classification", "TF-IDF, linear models and neural models", "TF-IDF and Logistic Regression are used here"],
        ], [1700, 3000, 2600]),
    ]

    out += chapter("Chapter 5  Research Gap")
    out += [
        paragraph("Many classroom demonstrations produce only a binary label from a small dataset. That makes it difficult to reproduce the training process, understand which input was analysed, or explain what happens when a model is unavailable."),
        paragraph("NewsLens addresses this course-scale gap by connecting a genuine labelled dataset to two saved text-classification pipelines, a Flask API, a browser interface, metadata, validation and an explicit human-verification message. The system also makes the input-aware routing decision visible to the user."),
        paragraph("The project does not claim to solve the general fact-checking problem. Its contribution is a compact and reproducible NLP application that demonstrates the full path from labelled text to a cautious screening result."),
    ]

    out += chapter("Chapter 6  Problem Statement")
    out += [
        paragraph("Design and implement an NLP-based web application that analyses a news headline or article and identifies whether its language resembles real/credible or fake/misleading examples in a labelled dataset. The application must validate input, use a saved model, show the selected model and communicate uncertainty and ethical limitations."),
        paragraph("Functional Requirements", style="Heading2", size=13, bold=True),
        table([
            ["Requirement", "Implementation response"],
            ["Dataset loading", "Read Fake.csv and True.csv from the data directory and derive labels from file names."],
            ["Preprocessing", "Tokenize input text using the shared NLP utility."],
            ["Feature extraction", "Use bounded word-level TF-IDF features."],
            ["Classification", "Use balanced Logistic Regression pipelines."],
            ["Input routing", "Use the headline pipeline for inputs of 60 words or fewer; otherwise use the article pipeline."],
            ["API service", "Expose GET /api/health and POST /api/analyze through Flask."],
            ["Responsible output", "Return a cautious label and advise source verification."],
        ], [1900, 5400]),
    ]

    out += chapter("Chapter 7  Methodology and Implementation")
    out += [
        paragraph("7.1 High-Level Architecture", style="Heading2", size=13, bold=True),
        paragraph("The system is divided into a training side and an inference side. The training side reads the reviewed dataset, validates labels, splits the rows and trains two pipelines. The inference side loads the saved artifact, accepts user text through the browser, routes the text and returns a result."),
        paragraph("Reviewed dataset -> validation -> stratified split -> tokenization -> TF-IDF -> two Logistic Regression pipelines -> joblib artifact -> Flask API -> browser result -> human source verification.", style="MacroText", size=10, after=120),
        paragraph("7.2 Dataset Preparation", style="Heading2", size=13, bold=True),
        paragraph("For the article pipeline, the title and body are combined. For the headline pipeline, only the title is used. The labels are mapped as 0 for real/credible and 1 for fake/misleading. A stratified 80/20 split with random seed 42 is used so both classes are represented in training and testing."),
        paragraph("7.3 NLP and Feature Extraction", style="Heading2", size=13, bold=True),
        paragraph("Tokenization breaks a sentence into smaller units. TfidfVectorizer then converts the token sequences into numerical vectors. The implementation uses word unigrams, minimum document frequency 3, maximum document frequency 0.98, a maximum of 50,000 features and sublinear term frequency scaling."),
        paragraph("7.4 Model Training", style="Heading2", size=13, bold=True),
        paragraph("The same pipeline structure is fitted twice with different input values. Each pipeline contains a tokenizer-aware TF-IDF vectorizer followed by Logistic Regression using class_weight=balanced, the liblinear solver, max_iter=200 and random_state=42. The resulting article_pipeline and headline_pipeline objects are stored together in models/newslens.joblib."),
        paragraph("7.5 Inference and Model Routing", style="Heading2", size=13, bold=True),
        paragraph("The browser sends JSON containing text to POST /api/analyze. The server rejects empty input and text above 10,000 characters. If the word count is 60 or fewer, headline_pipeline is selected; otherwise pipeline is selected. The selected pipeline returns a probability for class 1, which is converted into a screening score."),
        paragraph("7.6 Low-Level Components", style="Heading2", size=13, bold=True),
        table([
            ["File", "Responsibility"],
            ["training/train_model.py", "Load data, create pipelines, train, evaluate and save the artifact."],
            ["nlp_utils.py", "Shared tokenization and token-counting utilities."],
            ["server.py", "Load the artifact, validate requests, route models and return JSON."],
            ["index.html", "Provide the user interface and project explanation."],
            ["app.js", "Send requests and display scores, labels and signals."],
            ["styles.css", "Define the responsive visual layout."],
            ["models/newslens.joblib", "Store both fitted pipelines and metadata."],
        ], [2400, 4900]),
        paragraph("7.7 Ethical and Operational Safeguards", style="Heading2", size=13, bold=True),
        paragraph("The application does not train when the server starts, does not present the result as proof, and reports model readiness through /api/health. A credible article can be flagged and a false claim can pass. Users should verify the publisher, author, date, supporting evidence and independent reporting."),
    ]

    out += chapter("Chapter 8  Performance Evaluation")
    out += [
        paragraph("8.1 Evaluation Setup", style="Heading2", size=13, bold=True),
        paragraph("The dataset contains 44,898 usable articles. The stratified split produced 35,918 training rows and 8,980 held-out test rows. The evaluation reports accuracy, precision, recall and F1-score. These values describe the current dataset experiment and are not guaranteed real-world accuracy."),
        table([
            ["Measure", "Article pipeline", "Headline pipeline"],
            ["Accuracy", "99.31%", "96.16%"],
            ["Precision", "99.57%", "97.32%"],
            ["Recall", "99.11%", "95.27%"],
            ["F1-score", "99.34%", "96.29%"],
        ], [2500, 2500, 2500]),
        paragraph("8.2 Interpretation", style="Heading2", size=13, bold=True),
        paragraph("Precision indicates how often predictions for the fake/misleading class were correct in the test set. Recall indicates how much of the fake/misleading class was found. F1-score combines precision and recall. A new sample from a different topic, publisher, time period or writing style may produce a wrong result."),
    ]

    out += chapter("Chapter 9  Output and Results")
    out += [
        paragraph("The user interface accepts a headline or article and displays the score, label, model name, input mode, description and language signals. The language signals include sensational vocabulary, emphasis patterns, evidence vocabulary and basic text statistics. These signals are transparency aids and do not override the classifier."),
        table([
            ["Input condition", "Selected model", "Output"],
            ["Headline with 60 words or fewer", "Headline TF-IDF + Logistic Regression", "Score, label, signals and headline metrics"],
            ["Article longer than 60 words", "Article TF-IDF + Logistic Regression", "Score, label, signals and article metrics"],
            ["Empty input", "No model", "HTTP 400 validation response"],
            ["Text over 10,000 characters", "No model", "HTTP 413 validation response"],
        ], [2500, 3000, 2000]),
        paragraph("The smoke-test examples in data/test_cases.csv provide repeatable headline inputs. They should be used to demonstrate the interface, while the presenter should clearly state that the output is a screening signal and not a factual verdict."),
    ]

    out += chapter("Chapter 10  Conclusion")
    out += [
        paragraph("NewsLens demonstrates a complete NLP application for screening the language of news headlines and articles. It uses a genuine labelled dataset, tokenization, TF-IDF feature extraction, two Logistic Regression pipelines, evaluation metrics, a saved model artifact, a Flask API and a browser interface."),
        paragraph("The two-model design matches the difference between short headlines and longer articles. The API exposes the selected input mode and returns a cautious result with supporting signals. The project is useful for education and preliminary review, but it cannot establish truth without independent human verification."),
        paragraph("Future work could include time-based evaluation, publisher-independent splits, multilingual support, transformer comparisons, source retrieval with citations, authentication, rate limiting, monitoring and an approved data-retention policy."),
    ]

    out += chapter("Chapter 11  References")
    references = [
        "Kaggle, ISOT Fake and Real News Dataset, https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset?resource=download, accessed October 2026.",
        "H. Ahmed, I. Traore and S. Saad, Detection of Online Fake News Using N-Gram Analysis and Machine Learning Techniques, Security and Privacy, 2017.",
        "W. Y. Wang, \"Liar, Liar Pants on Fire\": A New Benchmark Dataset for Fake News Detection, Proceedings of ACL, 2017.",
        "H. A. A. K. Shu et al., FakeNewsNet: A Data Repository with News Content, Social Context and Spatiotemporal Information for Studying Fake News on Social Media, Big Data, 2020.",
        "F. Pedregosa et al., Scikit-learn: Machine Learning in Python, Journal of Machine Learning Research, 2011.",
        "spaCy Documentation, Linguistic Features and Tokenization, https://spacy.io/usage/linguistic-features, accessed October 2026.",
        "Flask Documentation, https://flask.palletsprojects.com/, accessed October 2026.",
    ]
    for index, ref in enumerate(references, 1):
        out.append(paragraph(f"[{index}] {ref}", size=10, after=100, first_line=0))
    return out


def replace_cover_content(body):
    children = list(body)
    cover = [deepcopy(item) for item in children[:42]]
    replacements = {
        1: "B.M.S. COLLEGE OF ENGINEERING",
        2: "(Autonomous Institute, Affiliated to VTU)",
        3: "Bull Temple Road, Basavanagudi, Bengaluru - 560019",
        6: "Presentation Report under Alternate Assessment Tool (AAT)",
        7: "NewsLens: Explainable Fake News Detection using Natural Language Processing",
        13: "HITESH SHARMA                         1BM23CS114",
        14: "GHANSHYAM SHARMA             1BM23CS100",
        15: "SHREYASH SHAURYA                 1BM23CS354",
        16: "UTKRISHT UMANG                    1BM23CS355",
        21: "Under the guidance of",
        22: "Rajeshwari K",
        23: "Assistant Professor",
        25: "Department of Computer Science and Engineering",
        26: "2026-2027",
        33: "C E R T I F I C A T E",
        35: "This is to certify that the Presentation Report under Alternate Assessment Tool entitled ‘NewsLens: Explainable Fake News Detection using Natural Language Processing’ is a bona-fide work carried out by Hitesh Sharma (1BM23CS114), Ghanshyam Sharma (1BM23CS100), Shreyash Shaurya (1BM23CS354) and Utkrisht Umang (1BM23CS355) in partial fulfilment of the requirements for the award of the degree of Bachelor of Engineering in Computer Science and Engineering during the academic year 2026-2027.",
        40: "Rajeshwari K                                             Dr. Shubha Rao V",
        41: "Assistant Professor                                      Professor and HOD",
    }
    for index, text in replacements.items():
        if index < len(cover) and cover[index].tag == w("p"):
            replace_paragraph_text(cover[index], text)
    return cover


def update_core_properties(data):
    root = etree.fromstring(data)
    cp = {"dc": "http://purl.org/dc/elements/1.1/", "cp": "http://schemas.openxmlformats.org/package/2006/metadata/core-properties"}
    title = root.find("dc:title", cp)
    subject = root.find("dc:subject", cp)
    creator = root.find("dc:creator", cp)
    if title is not None:
        title.text = "NewsLens: Explainable Fake News Detection using Natural Language Processing"
    if subject is not None:
        subject.text = "Alternate Assessment Tool Report"
    if creator is not None:
        creator.text = ""
    return etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")


def build():
    if not TEMPLATE.exists():
        raise FileNotFoundError(f"Reference template not found: {TEMPLATE}")
    with ZipFile(TEMPLATE) as source:
        document_root = etree.fromstring(source.read("word/document.xml"))
        body = document_root.find(w("body"))
        section = deepcopy(body.find(w("sectPr")))
        for child in list(body):
            body.remove(child)
        for child in replace_cover_content(etree.fromstring(source.read("word/document.xml")).find(w("body"))):
            body.append(child)
        body.append(page_break())
        for child in body_content():
            body.append(child)
        body.append(section)
        document_xml = etree.tostring(document_root, xml_declaration=True, encoding="UTF-8", standalone="yes")

        with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as target:
            for item in source.infolist():
                payload = source.read(item.filename)
                if item.filename == "word/document.xml":
                    payload = document_xml
                elif item.filename == "docProps/core.xml":
                    payload = update_core_properties(payload)
                elif item.filename == "docProps/app.xml":
                    payload = payload.replace(
                        b"Socket Level Lightweight Detection of TCP Flooding Attacks in Edge Network",
                        b"NewsLens Fake News Detection System",
                    )
                target.writestr(item, payload)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build()
