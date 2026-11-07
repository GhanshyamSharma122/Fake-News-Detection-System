from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import BaseDocTemplate, Frame, PageBreak, PageTemplate, Paragraph, Spacer, Table, TableStyle


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "NewsLens_Architecture_Model_Flow_Notes.pdf"


def footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(colors.HexColor("#CBD5E1"))
    canvas.line(doc.leftMargin, 0.55 * inch, A4[0] - doc.rightMargin, 0.55 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#64748B"))
    canvas.drawString(doc.leftMargin, 0.34 * inch, "NewsLens | Architecture and model-flow notes")
    canvas.drawRightString(A4[0] - doc.rightMargin, 0.34 * inch, f"Page {doc.page}")
    canvas.restoreState()


class NotesDocument(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        frame = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="main")
        self.addPageTemplates([PageTemplate(id="notes", frames=frame, onPage=footer)])


styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="TitleCustom", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=22, leading=27, alignment=TA_CENTER, textColor=colors.HexColor("#102A43"), spaceAfter=8))
styles.add(ParagraphStyle(name="Subtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=11, leading=15, alignment=TA_CENTER, textColor=colors.HexColor("#486581"), spaceAfter=14))
styles.add(ParagraphStyle(name="H1Custom", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=15, leading=18, textColor=colors.HexColor("#102A43"), spaceBefore=8, spaceAfter=6))
styles.add(ParagraphStyle(name="H2Custom", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=14, textColor=colors.HexColor("#243B53"), spaceBefore=6, spaceAfter=4))
styles.add(ParagraphStyle(name="BodyCustom", parent=styles["BodyText"], fontName="Helvetica", fontSize=9.2, leading=13, textColor=colors.HexColor("#243B53"), spaceAfter=5))
styles.add(ParagraphStyle(name="CodeCustom", parent=styles["BodyText"], fontName="Courier", fontSize=8.1, leading=11, textColor=colors.HexColor("#102A43"), backColor=colors.HexColor("#F0F4F8"), borderColor=colors.HexColor("#CBD5E1"), borderWidth=0.5, borderPadding=7, spaceAfter=7))
styles.add(ParagraphStyle(name="Callout", parent=styles["BodyText"], fontName="Helvetica-Bold", fontSize=9.4, leading=13, textColor=colors.HexColor("#7C2D12"), backColor=colors.HexColor("#FFF7ED"), borderColor=colors.HexColor("#FDBA74"), borderWidth=0.7, borderPadding=7, spaceAfter=7))


def P(text, style="BodyCustom"):
    return Paragraph(text, styles[style])


def bullets(items):
    return [P(f"&bull; {item}") for item in items]


def make_table(rows, widths):
    data = [[P(str(cell), "BodyCustom" if row == 0 else "BodyCustom") for cell in line] for row, line in enumerate(rows)]
    table = Table(data, colWidths=widths, repeatRows=1)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#CBD5E1")),
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#D9EAF7")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
    ]))
    return table


story = [
    Spacer(1, 0.35 * inch),
    P("NewsLens", "TitleCustom"),
    P("System architecture and model flow\nSpeaker notes for the AAT presentation", "Subtitle"),
    P("How to use this PDF: follow the numbered flow from left to right on the slide. The full explanation should take about 60-90 seconds.", "Callout"),
]

story += [P("1. Opening sentence", "H1Custom"), P("\"This slide shows two connected flows: first, how the models are trained and saved; second, how a user's text moves through the application during prediction.\"")]

story += [P("2. Training pipeline - explain from left to right", "H1Custom"),
          make_table([
              ["Block", "What happens", "Say this"],
              ["DATA", "The project reads data/Fake.csv and data/True.csv.", "The labels come from the source file names: fake/misleading and real/credible."],
              ["NLP", "The shared tokenizer breaks the title and article into tokens.", "This converts raw language into units that the vectorizer can process."],
              ["FEATURES", "A word-level TF-IDF vectorizer creates numerical features.", "TF-IDF gives more importance to words that help distinguish documents."],
              ["MODELS", "Two Logistic Regression pipelines are fitted.", "The article model uses title plus body; the headline model uses title only."],
              ["ARTIFACT", "Both fitted pipelines and metadata are saved in models/newslens.joblib.", "The server loads this saved artifact instead of training every time it starts."],
          ], [1.0 * inch, 2.7 * inch, 2.8 * inch]),
          P("The data is split into training and held-out test rows using a stratified 80/20 split with random seed 42. This is used for offline evaluation.", "Callout")]

story += [P("3. Inference pipeline - explain from left to right", "H1Custom"),
          make_table([
              ["Block", "What happens", "Say this"],
              ["USER TEXT", "The user enters a headline or article in the browser.", "The frontend sends the text to the Flask API."],
              ["VALIDATE", "The API checks that the input is non-empty and within the 10,000-character limit.", "Invalid input is rejected instead of being sent to the model."],
              ["ROUTE", "Inputs of 60 words or fewer use the headline pipeline; longer inputs use the article pipeline.", "The response tells us which input mode and model were selected."],
              ["PREDICT", "The selected pipeline returns the probability of the fake/misleading class.", "The probability is converted into a 0-100 screening score and a cautious label."],
              ["VERIFY", "The interface displays signals and a verification message.", "The user must still check the original source; this is not automatic fact-checking."],
          ], [1.0 * inch, 2.7 * inch, 2.8 * inch])]

story += [PageBreak(), P("4. Technical details to remember", "H1Custom"),
          make_table([
              ["Item", "Project value"],
              ["Backend", "Flask in server.py"],
              ["Analysis endpoint", "POST /api/analyze"],
              ["Health endpoint", "GET /api/health"],
              ["Headline routing", "60 words or fewer"],
              ["Maximum input", "10,000 characters"],
              ["Model file", "models/newslens.joblib"],
              ["Metadata file", "models/newslens.json"],
              ["Classifier", "Balanced Logistic Regression"],
              ["Features", "Word-level TF-IDF"],
          ], [1.8 * inch, 4.7 * inch]),
          P("5. Short script to memorise", "H1Custom"),
          P("\"The training flow starts with the labelled Fake and True CSV files. We tokenize the text and convert it into word-level TF-IDF vectors. Then we train two Logistic Regression pipelines: one on headlines and one on full article text. Both pipelines are saved in one joblib artifact. During inference, the Flask API validates the input and routes short text to the headline pipeline and longer text to the article pipeline. The result is a probability-derived screening score, not a guarantee of factual truth.\"", "Callout"),
          P("6. Commands if the teacher asks how to run it", "H1Custom"),
          P("python training/train_model.py --input data\npython server.py\nOpen: http://127.0.0.1:5000", "CodeCustom"),
          P("7. Questions you may be asked", "H1Custom"),
          make_table([
              ["Question", "Safe answer"],
              ["Why two models?", "Headlines have very little context, while full articles contain more text. Separate pipelines match those two input types."],
              ["Where are the models?", "They are stored as two pipeline objects inside models/newslens.joblib: pipeline and headline_pipeline."],
              ["Does it verify the internet?", "No. It only analyses the submitted text using the saved model."],
              ["Can it be wrong?", "Yes. Dataset patterns do not guarantee real-world truth, so every result needs source verification."],
              ["What does the accuracy mean?", "It is performance on the held-out dataset split, not guaranteed accuracy for a new sample."],
          ], [1.7 * inch, 4.8 * inch]),
          P("Do not say that the system proves an article is fake or real. Say that it identifies language patterns associated with the dataset labels and helps decide what needs verification.", "Callout")]

doc = NotesDocument(str(OUTPUT), pagesize=A4, rightMargin=0.65 * inch, leftMargin=0.65 * inch, topMargin=0.6 * inch, bottomMargin=0.72 * inch, title="NewsLens Architecture and Model Flow Notes")
doc.build(story)
print(f"Created {OUTPUT}")
