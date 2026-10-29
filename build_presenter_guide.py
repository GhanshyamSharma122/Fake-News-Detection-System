from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "NewsLens_Presenter_Guide.pdf"


class GuideDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="normal")
        self.addPageTemplates([PageTemplate(id="guide", frames=frame, onPage=draw_page)])


def draw_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#D9E2EC"))
    canvas.line(doc.leftMargin, 0.58 * inch, A4[0] - doc.rightMargin, 0.58 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(doc.leftMargin, 0.36 * inch, "NewsLens Presenter Guide | AAT")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.36 * inch, f"Page {doc.page}")
    canvas.restoreState()


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CoverTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=25,
    leading=30, alignment=TA_CENTER, textColor=colors.HexColor("#102A43"), spaceAfter=12,
))
styles.add(ParagraphStyle(
    name="CoverSub", parent=styles["Normal"], fontName="Helvetica", fontSize=12,
    leading=17, alignment=TA_CENTER, textColor=colors.HexColor("#486581"), spaceAfter=18,
))
styles.add(ParagraphStyle(
    name="H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=17,
    leading=21, textColor=colors.HexColor("#102A43"), spaceBefore=10, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=12,
    leading=15, textColor=colors.HexColor("#243B53"), spaceBefore=8, spaceAfter=5,
))
styles.add(ParagraphStyle(
    name="BodyCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.5,
    leading=14, textColor=colors.HexColor("#243B53"), spaceAfter=6,
))
styles.add(ParagraphStyle(
    name="SmallCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=8.5,
    leading=12, textColor=colors.HexColor("#486581"), spaceAfter=4,
))
styles.add(ParagraphStyle(
    name="Callout", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=10,
    leading=14, textColor=colors.HexColor("#7C2D12"), backColor=colors.HexColor("#FFF7ED"),
    borderColor=colors.HexColor("#FDBA74"), borderWidth=0.7, borderPadding=8, spaceAfter=8,
))
styles.add(ParagraphStyle(
    name="CodeCustom", parent=styles["BodyText"], fontName="Courier", fontSize=8.5,
    leading=12, textColor=colors.HexColor("#102A43"), backColor=colors.HexColor("#F0F4F8"),
    borderColor=colors.HexColor("#D9E2EC"), borderWidth=0.5, borderPadding=7, spaceAfter=8,
))


def P(text, style="BodyCustom"):
    return Paragraph(text, styles[style])


def bullet(text):
    return P(f"&bull; {text}")


def section(title):
    return [P(title, "H1Custom")]


def table(rows, widths, header=True):
    converted = []
    for row_index, row in enumerate(rows):
        converted.append([P(str(cell), "SmallCustom" if row_index else "BodyCustom") for cell in row])
    t = Table(converted, colWidths=widths, repeatRows=1 if header else 0, hAlign="LEFT")
    commands = [
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]
    if header:
        commands += [
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#102A43")),
        ]
    t.setStyle(TableStyle(commands))
    return t


story = []

# Cover
story += [Spacer(1, 1.05 * inch), P("NewsLens", "CoverTitle"),
          P("Presenter preparation guide\nFake news language screening using NLP", "CoverSub"),
          Spacer(1, 0.3 * inch)]
story.append(table([
    ["Presenter", "USN"],
    ["Hitesh Sharma", "1BM23CS114"],
    ["Ghanshyam Sharma", "1BM23CS100"],
    ["Shreyash Shaurya", "1BM23CS354"],
    ["Utkrisht Umang", "1BM23CS355"],
    ["Guide", "Rajeshwari K"],
], [3.2 * inch, 2.1 * inch]))
story += [Spacer(1, 0.35 * inch), P("Use this document to understand the project and prepare your own explanation. Do not memorise every sentence; explain the flow in your own words.", "Callout"), PageBreak()]

# 1. Core explanation
story += section("1. The 60-second explanation")
story += [P("NewsLens is a web application that analyses the language of a news headline or article. It learns from the ISOT Fake and Real News Dataset, converts text into TF-IDF features, and uses Logistic Regression to estimate whether the language resembles the fake or real class in the training data."),
          P("The result is shown as a screening score with simple language signals. It is not a fact-checker and it does not prove that an article is true or false. A user must still verify the source, author, date and evidence."),
          P("A good short answer is: <b>\"Our project uses supervised NLP to identify patterns associated with labelled fake and real news. It helps decide what needs verification, but it cannot replace fact-checking.\"</b>", "Callout")]

story += section("2. What problem are we solving?")
story += [P("Misleading content is often shared quickly because it uses emotional or sensational language. Checking every article manually is difficult. NewsLens provides a first screening step before someone shares a claim."),
          P("The project is limited to English text and the patterns represented in the selected dataset. It does not perform live web searches, verify citations, detect images or videos, or determine the legal or political truth of a claim."),
          P("Say \"lower-risk language\" or \"needs verification\" instead of saying \"this news is true\" or \"this news is fake\".", "Callout")]

# 3. System flow
story += section("3. End-to-end system flow")
story += [table([
    ["Stage", "What happens", "What to say"],
    ["Dataset", "Fake.csv and True.csv are read and labelled from their source files.", "We use a genuine labelled dataset, not a hand-written toy dataset."],
    ["Split", "The data is divided into training and held-out test rows using stratification and random seed 42.", "The test rows are kept aside for offline evaluation."],
    ["Tokenization", "Text is split into tokens using the shared tokenizer.", "Tokens are the smaller units used by the vectorizer."],
    ["TF-IDF", "Words are converted into numerical features; common words receive less importance.", "The model cannot learn directly from raw sentences, so we create vectors."],
    ["Classifier", "Balanced Logistic Regression learns the relationship between vectors and labels.", "It estimates a probability for the fake/misleading class."],
    ["Artifact", "Both pipelines and metadata are saved in models/newslens.joblib.", "The server loads the saved model; it does not train during startup."],
    ["Inference", "The API validates text, selects a model, predicts, and returns score plus signals.", "Short and long inputs use different pipelines."],
], [1.05 * inch, 3.25 * inch, 2.15 * inch])]

story.append(P("Model routing: inputs with 60 words or fewer use the headline pipeline. Longer inputs use the article pipeline. The API response identifies the selected input mode and model.", "Callout"))

# 4. Vocabulary
story += section("4. Important vocabulary")
story += [table([
    ["Term", "Simple meaning"],
    ["NLP", "Natural Language Processing: using software to work with human language."],
    ["Tokenization", "Breaking text into words or other tokens."],
    ["Feature", "A numerical representation used by a machine-learning model."],
    ["TF-IDF", "A weighting method that highlights words useful for distinguishing documents."],
    ["Supervised learning", "Learning from examples that already have labels."],
    ["Logistic Regression", "A classification algorithm that estimates class probabilities."],
    ["Precision", "Among items predicted as fake, how many were actually fake in the test set."],
    ["Recall", "Among fake items in the test set, how many the model found."],
    ["F1-score", "A combined measure of precision and recall."],
    ["False positive", "Credible text incorrectly marked as higher risk."],
    ["False negative", "Misleading text incorrectly given a lower-risk result."],
    ["Data leakage", "Information from evaluation data or its source accidentally influencing training."],
], [1.55 * inch, 4.9 * inch])]

story.append(PageBreak())

# 5. Demonstration
story += section("5. Recommended live demonstration")
story += [P("Keep the demonstration short. The purpose is to show that the browser, API and trained artifact work together."),
          P("Step 1 - Check readiness", "H2Custom"),
          P("Open http://127.0.0.1:5000. The page should load. Optionally open /api/health and show that the model status is ready and metadata is available."),
          P("Step 2 - Analyse a short headline", "H2Custom"),
          P("Paste a headline from data/test_cases.csv. Point out the selected input mode, score, label, language signals and model name. Do not promise that the label is factually correct."),
          P("Step 3 - Analyse a longer article", "H2Custom"),
          P("Paste a longer sample. Show that the API routes it to the article model rather than the headline model."),
          P("Step 4 - Explain an unexpected result", "H2Custom"),
          P("If a teacher gives a new sample and the result is wrong, say that this is an expected limitation of a dataset-trained classifier. Discuss wording, topic shift, source bias and the difference between language patterns and truth."),
          P("Useful commands", "H2Custom"),
          P("python training/train_model.py --input data\npython server.py", "CodeCustom")]

story += section("6. What the returned score means")
story += [table([
    ["Score range", "Current interface label", "Correct explanation"],
    ["0-37", "Lower-risk language", "Fewer learned misleading-language patterns were found. This does not prove truth."],
    ["38-64", "Needs verification", "The signals are mixed or uncertain. Check reliable sources."],
    ["65-100", "High-risk language", "The language resembles higher-risk training examples. Verify before sharing."],
], [1.0 * inch, 1.65 * inch, 3.8 * inch])]

story.append(P("The score is probability-derived and depends on the model, vocabulary and training data. It is not a percentage of factual truth.", "Callout"))

# 7. Results and limitations
story += section("7. How to discuss the evaluation numbers")
story += [P("The current offline experiment reports 99.31% accuracy and 99.34% F1 for the article pipeline, and 96.16% accuracy and 96.29% F1 for the headline pipeline. These values are calculated on a random held-out split of the same dataset."),
          P("Do not say: \"The system is 99% accurate for all news.\" Say: <b>\"On our held-out split, the article pipeline reached 99.31% accuracy. This is not a guarantee on new real-world articles.\"</b>"),
          P("A teacher's sample can be classified incorrectly. The model may learn publisher, topic or dataset-specific patterns. New events, satire, opinion, different writing styles and adversarial wording can reduce performance."),
          P("If asked why the score is high or low, explain that it comes from learned TF-IDF patterns and not from checking the internet.", "Callout")]

story += section("8. Ethics and responsible use")
story += [bullet("Do not use the result to censor, punish, deny services or label a person."),
          bullet("Do not store submitted article text unnecessarily."),
          bullet("A credible article can be flagged, and a polished false claim can pass."),
          bullet("Always inspect the original publisher, author, date, evidence and independent reporting."),
          bullet("Mention dataset bias, class labels and the difference between language screening and fact-checking.")]

# 9. Questions
story += section("9. Likely questions and safe answers")
story += [table([
    ["Question", "Answer to understand and explain"],
    ["Why did you use TF-IDF?", "It is fast, easy to inspect and suitable for a practical college baseline. It turns text into weighted numerical features."],
    ["Why not TensorFlow or PyTorch?", "They are optional for this project. We selected a lighter, interpretable scikit-learn pipeline instead of adding libraries without a clear need."],
    ["Does the model check Google or news websites?", "No. It only uses the saved model and the submitted text. It does not perform live fact-checking."],
    ["Why two models?", "Headlines are short and have less context. Full articles contain more text, so the project trains a separate pipeline and routes by word count."],
    ["What if the prediction is wrong?", "That is possible. The model identifies dataset-related language patterns, not truth. The user must verify the source."],
    ["What is a false positive?", "A credible article receives a higher-risk prediction. This is one reason not to use the system for automatic removal or punishment."],
    ["What happens when the server starts?", "It loads the saved joblib artifact. It does not retrain unless the user explicitly runs the training command."],
    ["What is your main limitation?", "The dataset may contain source, topic and time-period bias, and random splitting may produce optimistic results."],
], [2.2 * inch, 4.25 * inch])]

# 10. Final checklist
story += section("10. Final presenter checklist")
for item in [
    "Run the application before the presentation and confirm the model is available.",
    "Keep one short headline and one longer article ready for demonstration.",
    "Know what the selected model, score, label and signals mean.",
    "Do not claim that the model determines truth or guarantees accuracy.",
    "Explain the held-out metrics with the words 'on this dataset split'.",
    "Be ready to discuss one false positive, one false negative and one ethical risk.",
    "Each team member should explain at least one module they actually understand.",
    "If the teacher asks something outside the implementation, say it is outside the current scope rather than inventing an answer.",
]:
    story.append(bullet(item))


doc = GuideDocTemplate(
    str(OUTPUT), pagesize=A4, rightMargin=0.65 * inch, leftMargin=0.65 * inch,
    topMargin=0.65 * inch, bottomMargin=0.75 * inch,
    title="NewsLens Presenter Guide", author="NewsLens team",
)
doc.build(story)
print(f"Created {OUTPUT}")
