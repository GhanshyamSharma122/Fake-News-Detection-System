from copy import deepcopy
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

from lxml import etree

import build_aat_report_docx as base


ROOT = Path(__file__).resolve().parent
TEMPLATE = base.TEMPLATE
OUTPUT = ROOT / "NewsLens_AAT_Report_Clean.docx"
NS = base.NS
table = base.table


def p(text="", size=11, bold=False, italic=False, align="left", style=None, after=120, first_line=360):
    return base.paragraph(text, size=size, bold=bold, italic=italic, align=align, style=style, after=after, first_line=first_line)


def heading(text, level=1):
    return base.paragraph(text, style="Heading1" if level == 1 else "Heading2", size=16 if level == 1 else 13, bold=True, after=180, first_line=0)


def page_break():
    return base.page_break()


def bullet(text):
    return base.paragraph(text, style="ListBullet", after=70, first_line=0)


def toc_line(title, page):
    node = p(f"{title}\t{page}", after=80, first_line=0)
    ppr = node.find(base.w("pPr"))
    tabs = etree.SubElement(ppr, base.w("tabs"))
    tab = etree.SubElement(tabs, base.w("tab"))
    tab.set(base.w("val"), "right")
    tab.set(base.w("pos"), "8666")
    return node


def chapter(title):
    return [page_break(), heading(title, 1)]


def content():
    # The reference cover/certificate already ends with its page break.
    out = [heading("Table of Contents", 1)]
    out.append(toc_line("Chapter 1  Abstract", 4))
    out.append(toc_line("Chapter 2  Objectives", 5))
    out.append(toc_line("Chapter 3  Introduction", 6))
    out.append(toc_line("Chapter 4  Literature Review", 8))
    out.append(toc_line("Chapter 5  Research Gap", 10))
    out.append(toc_line("Chapter 6  Problem Statement", 11))
    out.append(toc_line("Chapter 7  Methodology and Implementation", 12))
    out.append(toc_line("Chapter 8  Performance Evaluation", 15))
    out.append(toc_line("Chapter 9  Output and Results", 16))
    out.append(toc_line("Chapter 10  Conclusion", 18))
    out.append(toc_line("Chapter 11  References", 19))
    out.append(p("Note: page numbers follow the fixed page breaks in this report and can be refreshed in Word if the text is later edited.", italic=True, size=9, first_line=0, after=80))

    out += chapter("Chapter 1  Abstract")
    out += [
        p("NewsLens is a Natural Language Processing application for screening the language of news headlines and articles. The project uses the ISOT Fake and Real News Dataset, word-level TF-IDF feature extraction and Logistic Regression classification. Since a headline contains less context than an article, the system trains separate pipelines for short headline inputs and longer article inputs."),
        p("The trained pipelines are stored in one joblib artifact and served through a Flask API. The browser interface accepts text, validates it, selects the appropriate pipeline and displays a probability-derived screening score with language signals. The result is deliberately presented as a verification aid rather than a final decision about factual truth."),
        p("The application demonstrates the complete path from data to deployment. During training, the source files are checked, the labels are converted into two classes and the rows are separated into training and held-out test sets. During inference, the saved vectorizer and classifier are applied to the same type of text representation used during training. This prevents the web application from using a different preprocessing process from the training script."),
        p("The project also records the selected model and evaluation metadata in its response. This makes it possible to explain whether a headline or article pipeline was used and to distinguish an offline dataset result from a real-world factual judgement. The final decision to trust and share a claim remains with the user."),
        p("Keywords: Natural Language Processing, fake news detection, tokenization, TF-IDF, Logistic Regression, text classification, precision, recall, F1-score, Flask and responsible AI.", italic=True),
    ]

    out += chapter("Chapter 2  Objectives")
    out += [p("The project objectives are to study the problem, implement a complete NLP workflow and validate the result through a working web application. The objectives also include explaining the limits of a text classifier so that the system is not presented as an automatic fact-checker.", first_line=360), p("The specific objectives are:", first_line=0)]
    for item in [
        "Study the use of NLP for misinformation screening and understand why language patterns alone cannot establish factual truth.",
        "Use a genuine labelled dataset instead of a manually written toy dataset and record its source and label definition.",
        "Build a reproducible training and evaluation pipeline with a fixed random seed and a held-out test split.",
        "Train separate pipelines for headline and article input because the two input types provide different amounts of context.",
        "Develop a working Flask API and browser interface that can be run locally by the project team.",
        "Return a score, selected model, input mode, description and language signals for each valid request.",
        "Measure accuracy, precision, recall and F1-score and describe exactly what the measurements do and do not mean.",
        "Document limitations, bias, privacy, false positives, false negatives and the need for human source verification.",
    ]:
        out.append(bullet(item))

    out += chapter("Chapter 3  Introduction")
    out += [
        heading("3.1 Background", 2),
        p("News is consumed through websites, social platforms and messaging applications. A reader may see a headline before checking the original publisher, author, date or evidence. Misleading content can use emotional language, unsupported claims, excessive emphasis or the appearance of formal reporting."),
        p("Natural Language Processing represents written language in a form that a computer can analyse. A supervised classifier learns from examples that already have labels and then estimates how a new input resembles those examples."),
        heading("3.2 Motivation", 2),
        p("Checking every online claim manually is difficult. NewsLens provides a first screening step that encourages the user to pause and verify. It is designed to show the complete lifecycle of a college NLP application: data preparation, model training, evaluation, deployment and responsible interpretation."),
        heading("3.3 Scope", 2),
        p("The system supports English headlines and articles. It does not perform live web searches, verify citations, analyse images or videos, identify every kind of satire or opinion, or make decisions about people. It should not be used for automatic censorship or punishment."),
        heading("3.4 Dataset Summary", 2),
        p("The project uses Fake.csv with 23,481 rows and True.csv with 21,417 rows, giving 44,898 usable articles. Each source file contains title, text, subject and date fields. The trainer derives the binary label from the file name; subject and date are not used as direct model features."),
        page_break(),
        heading("Chapter 3  Introduction (continued)", 1),
        heading("3.5 Important NLP Concepts", 2),
        p("Tokenization divides a sentence into smaller units such as words. TF-IDF then represents the input as a vector. Term frequency reflects how often a word appears in a document, while inverse document frequency reduces the importance of words that occur in many documents. The resulting vector is suitable for a linear classifier."),
        p("Supervised classification means that the algorithm learns from examples with known labels. Logistic Regression produces a probability for the selected class. In this project, class 1 represents the fake/misleading label. The probability is converted into a screening score for the interface, but it is not a percentage of factual truth."),
        heading("3.6 Responsible Problem Framing", 2),
        p("The phrase fake news can be misunderstood as a final judgement about an article or a person. In this report, the output is described as language risk or need for verification. The model may learn correlations related to source, topic or writing style. Therefore, the application is an assistive screening tool and not an authority that should remove or punish content."),
        p("A responsible workflow is: read the result, inspect the original source, compare the claim with independent reporting, check the date and author, and then make a human decision. This framing is part of the system design rather than an optional note added after implementation."),
    ]

    out += chapter("Chapter 4  Literature Review")
    out += [
        p("Research on misinformation classification includes claim-level datasets, article-level datasets, social-context datasets, linguistic features and neural language models. The LIAR benchmark is frequently used for short labelled claims, while FakeNewsNet includes news content with social-context information. These resources are useful for research, but access, copyright, collection and reproducibility must be considered."),
        p("Traditional methods such as bag-of-words, TF-IDF and linear classifiers are still useful baselines because they are fast, auditable and inexpensive to deploy. Neural and transformer models can represent broader context, but they require careful tuning, more computational resources and stronger validation."),
        p("For this AAT, TF-IDF with balanced Logistic Regression was selected as a practical baseline. This choice allows the team to demonstrate tokenization, feature extraction, supervised learning, evaluation, saved artifacts, API inference and ethical limitations in one working application."),
        heading("4.1 Dataset-Oriented Research", 2),
        p("A dataset is not a neutral list of facts. Its labels depend on the collection process, the definition used by the dataset creators and the sources from which the examples were obtained. A model can therefore learn both useful language patterns and unwanted shortcuts, such as publication style or topic vocabulary."),
        p("This concern is important for NewsLens because the real and fake files do not necessarily have identical subjects, publishers or dates. A strong random-split result should be interpreted as evidence that the model separates the available examples, not as evidence that it can judge every future article."),
        heading("4.2 Model Choice", 2),
        p("A linear TF-IDF model was chosen because the project needs a clear baseline that can be trained on a college computer and loaded quickly by a local Flask service. The vectorizer and classifier can be inspected as separate pipeline stages, and the same fitted pipeline is reused during inference."),
        page_break(),
        heading("Chapter 4  Literature Review (continued)", 1),
        heading("4.3 Explainability and Deployment", 2),
        p("Explainability in this project has two levels. First, the TF-IDF and Logistic Regression pipeline is structurally understandable: text becomes weighted features and the classifier combines those features to estimate a class probability. Second, the application displays additional language signals such as sensational words and emphasis patterns. These signals help a user review the text, but they are not a complete causal explanation of every prediction."),
        p("Deployment research also highlights the difference between a notebook experiment and an application. NewsLens loads a versioned artifact, exposes readiness through a health endpoint, validates requests and gives the client a structured response. This makes the model behaviour easier to demonstrate and reproduce than an isolated training cell."),
        p("The literature and implementation together support a modest project claim: NewsLens is a practical, explainable baseline for language screening. It is not presented as a state-of-the-art fact-checker or as a replacement for professional verification."),
        table([
            ["Approach", "Strength", "Relation to NewsLens"],
            ["Rule-based keywords", "Simple and easy to implement", "Used only for supporting language signals, not the main classifier"],
            ["TF-IDF and linear models", "Fast and inspectable", "Selected for the current baseline"],
            ["Neural language models", "Can capture richer context", "Possible future comparison, not required for this AAT"],
        ], [1900, 2600, 4166]),
    ]

    out += chapter("Chapter 5  Research Gap")
    out += [
        p("Many classroom demonstrations return only a label from a small sample. They may not show how the training data was prepared, how the model is selected for different inputs, or how the application behaves when a model is unavailable."),
        p("NewsLens addresses this course-scale gap by connecting a genuine dataset to two saved pipelines, a Flask API and a browser interface. It records evaluation metadata, validates requests and identifies whether the headline or article pipeline was used."),
        p("The project does not claim to solve general fact-checking. Its contribution is a compact, reproducible and explainable screening workflow from labelled text to a cautious result."),
        p("The selected gap is therefore practical rather than a claim of a new machine-learning algorithm. The project brings together components that are often shown separately: a documented data contract, repeatable training, an artifact that can be loaded by a server, input-aware routing, structured API output and an ethical explanation for the user."),
        p("This scope is suitable for the AAT because it demonstrates several NLP mechanisms while remaining small enough to run locally. It also gives the team a clear basis for discussion: the quality of the result depends on the labels and distribution of the dataset, and deployment does not remove the need for human judgement."),
    ]

    out += chapter("Chapter 6  Problem Statement")
    out += [
        p("Design and implement an NLP-based web application that analyses a news headline or article and identifies whether its language resembles real/credible or fake/misleading examples in a labelled dataset. The application must validate input, use a saved model, expose its selected input mode and communicate uncertainty."),
        p("The system receives plain English text as its input. It must return a structured response that can be understood by a browser client: a screening score, a cautious label, a description, the selected model, the input mode, evaluation metadata and supporting language signals. If the input is invalid or the model artifact is missing, the system must return an error rather than inventing a result."),
        heading("Functional Requirements", 2),
        table([
            ["Requirement", "Implementation response"],
            ["Dataset loading", "Read Fake.csv and True.csv from the data directory."],
            ["Preprocessing", "Tokenize text through the shared NLP utility."],
            ["Feature extraction", "Generate bounded word-level TF-IDF features."],
            ["Classification", "Use balanced Logistic Regression pipelines."],
            ["Input routing", "Use headline_pipeline for 60 words or fewer; otherwise use pipeline."],
            ["API service", "Expose GET /api/health and POST /api/analyze through Flask."],
            ["Responsible output", "Return a cautious label and source-verification guidance."],
        ], [2000, 6666]),
        heading("Non-Functional Requirements", 2),
        table([
            ["Property", "Requirement"],
            ["Reproducibility", "Use a recorded dataset source, fixed random seed and saved model metadata."],
            ["Usability", "Provide a simple browser form with a readable result and verification guidance."],
            ["Safety", "Do not expose a prediction when input validation or model loading fails."],
            ["Maintainability", "Keep training, shared NLP utilities, server code and frontend code separated."],
        ], [2000, 6666]),
    ]

    out += chapter("Chapter 7  Methodology and Implementation")
    out += [
        heading("7.1 High-Level Architecture", 2),
        p("The training side reads and validates the dataset, creates a stratified split and trains two pipelines. The inference side loads the saved artifact, accepts browser input, validates the request, routes the input and returns a result."),
        p("Reviewed data -> validation -> split -> tokenization -> TF-IDF -> two Logistic Regression pipelines -> joblib artifact -> Flask API -> browser result -> human verification.", style="MacroText", size=10, first_line=0),
        heading("7.2 Dataset Preparation", 2),
        p("For the article pipeline, the title and body are combined. For the headline pipeline, only the title is used. The labels are mapped to 0 for real/credible and 1 for fake/misleading. The rows are divided using an 80/20 stratified split with random seed 42."),
        heading("7.3 NLP and Feature Extraction", 2),
        p("Tokenization divides text into smaller units. TfidfVectorizer converts the tokens into numerical features. The implementation uses word unigrams, minimum document frequency 3, maximum document frequency 0.98, at most 50,000 features and sublinear term-frequency scaling."),
        heading("7.4 Model Training", 2),
        p("The same pipeline structure is fitted twice. Each pipeline contains a tokenizer-aware TF-IDF vectorizer followed by Logistic Regression with class_weight=balanced, the liblinear solver, max_iter=200 and random_state=42. The two fitted objects are saved under pipeline and headline_pipeline in models/newslens.joblib."),
    ]
    out.append(page_break())
    out += [
        heading("Chapter 7  Methodology and Implementation (continued)", 1),
        heading("7.5 Inference and Model Routing", 2),
        p("The browser sends JSON containing text to POST /api/analyze. The server rejects empty input and text above 10,000 characters. If the word count is 60 or fewer, headline_pipeline is selected; otherwise pipeline is selected. The selected model returns the probability of class 1, which is converted into a screening score."),
        heading("7.6 Low-Level Components", 2),
        table([
            ["File", "Responsibility"],
            ["training/train_model.py", "Load data, train, evaluate and save both pipelines."],
            ["nlp_utils.py", "Provide tokenization and token-counting utilities."],
            ["server.py", "Load the artifact, validate input, route models and return JSON."],
            ["index.html", "Provide the browser interface and project explanation."],
            ["app.js", "Send analysis requests and display the response."],
            ["styles.css", "Define the responsive visual layout."],
            ["models/newslens.joblib", "Store both fitted pipelines and metadata."],
        ], [2700, 5966]),
        heading("7.7 Output Signals", 2),
        p("The API returns the score, label, description, selected model, input mode and language signals. The signals identify sensational vocabulary, exclamation-mark emphasis, evidence-related vocabulary and basic token/sentence statistics. They are supporting indicators and do not override the trained model."),
        heading("7.8 Running the System", 2),
        p("The model is trained explicitly with python training/train_model.py --input data. The server is started with python server.py or run.bat. When a trained artifact already exists, run.bat skips training and loads the existing model. This prevents unnecessary retraining during a demonstration."),
    ]
    out.append(page_break())
    out += [
        heading("Chapter 7  Methodology and Implementation (continued)", 1),
        heading("7.9 Training Lifecycle and Artifact", 2),
        p("The training script first checks that the input path exists and that the selected input contains enough usable rows. For the ISOT directory, it reads Fake.csv and True.csv, combines the relevant text fields and creates the binary labels. The same train/test indices are used when evaluating the article and headline pipelines so that the comparison is based on the same held-out rows."),
        p("After fitting, the artifact stores the article pipeline, the headline pipeline and metadata. The metadata includes the dataset name, dataset hash, creation time, class distribution, training and test sizes, and the classification metrics. A separate JSON metadata file makes the evaluation information easy to inspect without loading the model object."),
        heading("7.10 API Contract", 2),
        table([
            ["Endpoint", "Request or response"],
            ["GET /api/health", "Reports ready/not_ready status and model metadata."],
            ["POST /api/analyze", "Accepts JSON such as {\"text\": \"headline or article\"}."],
            ["Successful response", "Returns score, label, description, signals, model, input_mode and metrics."],
            ["HTTP 400", "Returned for missing or empty text."],
            ["HTTP 413", "Returned when text exceeds 10,000 characters."],
            ["HTTP 503", "Returned when the saved model artifact is unavailable or invalid."],
        ], [2300, 6366]),
        heading("7.11 Screening Labels", 2),
        p("The current interface uses three cautious bands. Scores below 38 are shown as lower-risk language, scores from 38 to 64 require verification, and scores of 65 or above are shown as high-risk language. These labels describe the model signal and are not factual truth categories."),
        heading("7.12 Ethical Safeguards", 2),
        p("The output is not proof of truth. A credible article can be flagged and a polished false claim can pass. The application should not be used to censor, punish or deny services. Users should check the original source, author, date, evidence and independent reporting."),
    ]

    out += chapter("Chapter 8  Performance Evaluation")
    out += [
        heading("8.1 Evaluation Setup", 2),
        p("The dataset contains 44,898 usable articles. A stratified split produced 35,918 training rows and 8,980 held-out test rows. The same held-out labels are used to calculate accuracy, precision, recall and F1-score for both pipelines."),
        p("The class counts are 23,481 fake/misleading rows and 21,417 real/credible rows. The classifier uses class_weight=balanced so that the difference in class frequency has less influence on the fitted decision boundary."),
        p("The evaluation is performed after fitting the vectorizer and classifier only on the training portion. The test rows are then transformed by the already-fitted vectorizer and passed to the classifier. This keeps the held-out evaluation separate from the learning step."),
        table([
            ["Metric", "Article pipeline", "Headline pipeline"],
            ["Accuracy", "99.31%", "96.16%"],
            ["Precision", "99.57%", "97.32%"],
            ["Recall", "99.11%", "95.27%"],
            ["F1-score", "99.34%", "96.29%"],
        ], [2700, 2983, 2983]),
        heading("8.2 Metric Interpretation", 2),
        p("Accuracy is the proportion of all held-out rows classified correctly. Precision describes how often fake/misleading predictions were correct in the test set. Recall describes how much of the fake/misleading class was found. F1-score combines precision and recall."),
        heading("8.3 Evaluation Limitation", 2),
        p("These numbers describe the current dataset experiment, not guaranteed real-world performance. A random split can be optimistic if related articles, publishers or repeated writing patterns appear in both training and testing data. A future evaluation should consider time-based and publisher-independent splits."),
        p("The most important evaluation question is therefore not only whether the score is high, but whether the test design resembles the way the system will be used. A teacher's new headline may come from a different event, source or writing style. Such an input is useful for demonstrating generalisation limits."),
    ]

    out += chapter("Chapter 9  Output and Results")
    out += [
        heading("9.1 User Interface Output", 2),
        p("The user interface accepts a headline or article and displays the score, label, model name, input mode, description and language signals. The interface also reminds the user that the result requires source verification."),
        p("A short input is labelled as headline mode when it contains 60 words or fewer. The response then reports Headline TF-IDF + Logistic Regression and the headline metrics. A longer input reports Article TF-IDF + Logistic Regression and the article metrics. This makes the routing decision visible during a demonstration."),
        p("The score is probability-derived and scaled to a 0-100 display value. A lower score means that the selected pipeline found fewer patterns associated with the fake/misleading class in its learned vocabulary. It does not mean that the article has been checked against an authoritative source."),
        heading("9.2 Demonstration Scenarios", 2),
        table([
            ["Scenario", "Expected behaviour"],
            ["Short headline", "Use the headline pipeline and return headline metrics in the response."],
            ["Long article", "Use the article pipeline because the input is longer than 60 words."],
            ["Empty input", "Return a validation response instead of a prediction."],
            ["Very long input", "Reject text above the 10,000-character limit."],
        ], [2700, 5966]),
        heading("9.3 Test Cases", 2),
        p("The file data/test_cases.csv contains repeatable headline examples. The application can be tested with lower-risk language, sensational language and invalid input. The observed score is associated with the current model artifact and may change after retraining."),
        p("The demonstration file demo_inputs.txt contains two short headline examples, two sensational headline examples and two longer paragraphs. The longer paragraphs are useful for showing that the word-count rule selects the article pipeline. The examples are for software demonstration and should not be described as independent fact-checking evidence."),
        p("A successful demonstration should show at least one lower-risk result, one higher-risk result, one longer input and one validation error. The presenter should identify the model selected in each case and explain that a surprising prediction is an error case that the system must acknowledge."),
    ]
    out.append(page_break())
    out += [
        heading("Chapter 9  Output and Results (continued)", 1),
        heading("9.4 Interpreting an Unexpected Result", 2),
        p("If a teacher gives a new sample and the model predicts incorrectly, this is a valid limitation to discuss. The model learns patterns from the dataset; it does not check the internet or understand factual context. Topic shift, source style, satire, opinion writing and adversarial wording can produce errors."),
        heading("9.5 Responsible Demonstration", 2),
        p("During a demonstration, the presenter should identify the selected model, show the score and explain that the result is a screening signal. The presenter should not claim that a high score proves an article is false or that a low score proves it is true."),
        heading("9.6 Reproducibility", 2),
        p("The training script records model metadata, class distribution, evaluation metrics and a dataset hash. This provides evidence of which data and settings produced the current artifact. The saved model is loaded by the server without retraining on startup."),
        p("For a repeatable run, the team should use the same dataset directory, the same training command and the same model artifact. If the dataset or preprocessing code changes, the metrics should be regenerated and the report should identify the new artifact rather than reusing old numbers."),
    ]

    out += chapter("Chapter 10  Conclusion")
    out += [
        p("NewsLens demonstrates a complete NLP application for screening the language of news headlines and articles. It uses a genuine labelled dataset, tokenization, TF-IDF feature extraction, two Logistic Regression pipelines, evaluation metrics, a saved artifact, a Flask API and a browser interface."),
        p("The two-model design matches the difference between short headlines and longer articles. The API exposes the selected input mode and returns a cautious result with supporting signals. The project is suitable as an educational verification aid, but it cannot establish truth without independent human review."),
        p("The implementation also demonstrates the importance of separating training from inference. Training is an explicit operation that produces a reusable artifact. The running web service loads that artifact, validates requests and applies the same fitted transformations to new text. This makes the behaviour easier to explain than a system that silently retrains whenever it starts."),
        p("The main limitations are dataset bias, possible source and topic leakage, lack of live evidence retrieval, English-only input and the possibility of false positives and false negatives. These limitations are not defects to hide; they define the conditions under which the current system should be used."),
        p("Future work may include time-based evaluation, publisher-independent splits, multilingual support, transformer comparisons, source retrieval with citations, authentication, rate limiting and monitoring."),
    ]

    out += chapter("Chapter 11  References")
    for index, ref in enumerate([
        "Kaggle, ISOT Fake and Real News Dataset, https://www.kaggle.com/datasets/clmentbisaillon/fake-and-real-news-dataset?resource=download, accessed October 2026.",
        "H. Ahmed, I. Traore and S. Saad, Detection of Online Fake News Using N-Gram Analysis and Machine Learning Techniques, Security and Privacy, 2017.",
        "W. Y. Wang, \"Liar, Liar Pants on Fire\": A New Benchmark Dataset for Fake News Detection, Proceedings of ACL, 2017.",
        "H. A. A. K. Shu et al., FakeNewsNet: A Data Repository with News Content, Social Context and Spatiotemporal Information for Studying Fake News on Social Media, Big Data, 2020.",
        "F. Pedregosa et al., Scikit-learn: Machine Learning in Python, Journal of Machine Learning Research, 2011.",
        "C. D. Manning, P. Raghavan and H. Schütze, Introduction to Information Retrieval, Cambridge University Press, 2008.",
        "T. Joachims, Text Categorization with Support Vector Machines: Learning with Many Relevant Features, Proceedings of ECML, 1998.",
        "K. Shu, A. Sliva, S. Wang, J. Tang and H. Liu, Fake News Detection on Social Media: A Data Mining Perspective, ACM SIGKDD Explorations Newsletter, 2017.",
        "S. Bird, E. Klein and E. Loper, Natural Language Processing with Python, O'Reilly Media, 2009.",
        "spaCy Documentation, Linguistic Features and Tokenization, https://spacy.io/usage/linguistic-features, accessed October 2026.",
        "Flask Documentation, https://flask.palletsprojects.com/, accessed October 2026.",
    ], 1):
        out.append(p(f"[{index}] {ref}", size=10, first_line=0, after=100))
    return out


def build():
    with ZipFile(TEMPLATE) as source:
        original_root = etree.fromstring(source.read("word/document.xml"))
        original_body = original_root.find(base.w("body"))
        cover_nodes = base.replace_cover_content(original_body)
        root = etree.fromstring(source.read("word/document.xml"))
        body = root.find(base.w("body"))
        section = deepcopy(body.find(base.w("sectPr")))
        for child in list(body):
            body.remove(child)
        for child in cover_nodes:
            body.append(child)
        for child in content():
            body.append(child)
        body.append(section)
        document_xml = etree.tostring(root, xml_declaration=True, encoding="UTF-8", standalone="yes")
        with ZipFile(OUTPUT, "w", ZIP_DEFLATED) as target:
            for item in source.infolist():
                payload = source.read(item.filename)
                if item.filename == "word/document.xml":
                    payload = document_xml
                elif item.filename == "docProps/core.xml":
                    payload = base.update_core_properties(payload)
                elif item.filename == "docProps/app.xml":
                    payload = payload.replace(
                        b"Socket Level Lightweight Detection of TCP Flooding Attacks in Edge Network",
                        b"NewsLens Fake News Detection System",
                    )
                target.writestr(item, payload)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    build()
