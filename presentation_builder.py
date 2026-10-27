from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_AUTO_SHAPE_TYPE, MSO_CONNECTOR
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.util import Inches, Pt

OUTPUT = "NewsLens_AAT_Presentation.pptx"
W, H = 13.333, 7.5
BG = RGBColor(16, 20, 26)
PANEL = RGBColor(28, 35, 44)
WHITE = RGBColor(238, 240, 243)
MUTED = RGBColor(174, 184, 196)
GREEN = RGBColor(198, 244, 50)
ORANGE = RGBColor(242, 169, 0)
RED = RGBColor(229, 56, 59)


def set_background(slide):
    fill = slide.background.fill
    fill.solid()
    fill.fore_color.rgb = BG


def add_text(slide, x, y, w, h, text, size=14, color=WHITE, font="Aptos", bold=False, align=PP_ALIGN.LEFT, valign=MSO_ANCHOR.TOP, margin=0.04):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(margin)
    frame.margin_right = Inches(margin)
    frame.margin_top = Inches(margin)
    frame.margin_bottom = Inches(margin)
    frame.vertical_anchor = valign
    paragraph = frame.paragraphs[0]
    paragraph.alignment = align
    run = paragraph.add_run()
    run.text = text
    run.font.name = font
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def add_rich_lines(slide, x, y, w, h, lines, size=12, color=WHITE, font="Aptos", line_spacing=1.15):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    frame = box.text_frame
    frame.clear()
    frame.word_wrap = True
    frame.margin_left = Inches(0.04)
    frame.margin_right = Inches(0.04)
    frame.margin_top = Inches(0.02)
    for index, line in enumerate(lines):
        paragraph = frame.paragraphs[0] if index == 0 else frame.add_paragraph()
        paragraph.space_after = Pt(8)
        paragraph.line_spacing = line_spacing
        run = paragraph.add_run()
        run.text = line
        run.font.name = font
        run.font.size = Pt(size)
        run.font.color.rgb = color
    return box


def add_panel(slide, x, y, w, h, fill=PANEL, line=None, radius=True):
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.ROUNDED_RECTANGLE if radius else MSO_AUTO_SHAPE_TYPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line or fill
    shape.line.width = Pt(0.7)
    return shape


def add_line(slide, x1, y1, x2, y2, color=MUTED, width=1):
    line = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    line.line.color.rgb = color
    line.line.width = Pt(width)
    return line


def add_header(slide, number, title, page):
    badge = add_panel(slide, 0.6, 0.3, 0.85, 0.48, GREEN, GREEN)
    add_text(slide, 0.6, 0.3, 0.85, 0.48, number, 12, BG, "Courier New", True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
    add_text(slide, 1.75, 0.31, 10.4, 0.5, title, 25, WHITE, "Cambria", True)
    add_text(slide, 11.95, 7.03, 0.65, 0.22, page, 9, MUTED, "Courier New", False, PP_ALIGN.RIGHT)


def add_label(slide, x, y, text, color=GREEN):
    add_text(slide, x, y, 5.6, 0.24, text.upper(), 9, color, "Courier New", True)


def add_arrow(slide, x, y, w=0.38, h=0.22, color=GREEN):
    shape = slide.shapes.add_shape(MSO_AUTO_SHAPE_TYPE.RIGHT_ARROW, Inches(x), Inches(y), Inches(w), Inches(h))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.color.rgb = color
    return shape


def slide_cover(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_text(slide, 0.72, 0.55, 4.5, 0.3, "NLP APPLICATION / AAT", 10, GREEN, "Courier New", True)
    add_text(slide, 0.72, 1.6, 7.2, 0.85, "NewsLens", 52, WHITE, "Cambria", True)
    add_text(slide, 0.76, 2.48, 6.5, 0.8, "Explainable fake news detection\nusing natural language processing", 22, MUTED, "Aptos", False)
    add_line(slide, 0.76, 3.65, 5.5, 3.65, GREEN, 2)
    add_text(slide, 0.76, 4.05, 2.2, 0.24, "PRESENTED BY", 9, GREEN, "Courier New", True)
    presenters = [
        ("Hitesh Sharma", "USN: __________", 0.76),
        ("Ghanshyam Sharma", "1BM23CS100", 2.18),
        ("Shreyash Shaurya", "1BM23CS354", 3.78),
        ("Utkrisht Umang", "1BM23CS355", 5.28),
    ]
    for name, usn, x in presenters:
        add_text(slide, x, 4.38, 1.45, 0.42, name, 10.5, WHITE, "Aptos", True)
        add_text(slide, x, 4.86, 1.45, 0.25, usn, 7.5, MUTED, "Courier New")
    add_text(slide, 0.76, 5.5, 5.5, 0.3, "Department of Computer Science and Engineering", 11, MUTED)
    add_text(slide, 0.76, 6.1, 5.5, 0.28, "BMS College of Engineering · 2026", 10, MUTED, "Courier New")
    add_panel(slide, 8.1, 1.1, 4.35, 5.35, PANEL, PANEL)
    add_text(slide, 8.55, 1.55, 3.3, 0.25, "THE QUESTION", 10, GREEN, "Courier New", True)
    add_text(slide, 8.55, 1.98, 3.25, 0.9, "Can language\nhelp us pause\nbefore sharing?", 25, WHITE, "Cambria", True)
    for i, (label, value, col) in enumerate((("INPUT", "headline / article", GREEN), ("MODEL", "TF-IDF + Logistic Regression", ORANGE), ("OUTPUT", "score + evidence", GREEN))):
        yy = 3.55 + i * 0.82
        add_line(slide, 8.55, yy - 0.12, 11.95, yy - 0.12, MUTED, 0.6)
        add_text(slide, 8.55, yy, 0.9, 0.2, label, 8, MUTED, "Courier New", True)
        add_text(slide, 9.55, yy - 0.02, 2.5, 0.27, value, 11, col, "Aptos", True)
    add_text(slide, 8.55, 5.95, 3.3, 0.25, "HUMAN-IN-THE-LOOP", 9, GREEN, "Courier New", True)
    add_text(slide, 8.55, 6.18, 3.35, 0.3, "A screening aid, never a truth verdict.", 10, MUTED)


def slide_problem(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, "01", "Problem statement and objectives", "2")
    add_label(slide, 0.6, 1.58, "PROBLEM")
    add_text(slide, 0.6, 1.98, 5.4, 1.25, "Identify language patterns that make a news headline or article deserve verification before it is shared.", 22, WHITE, "Cambria", True)
    add_text(slide, 0.6, 3.48, 5.2, 1.25, "A sensational claim can look persuasive, while legitimate reporting can be written in urgent language. The system must provide a signal with reasons—not an unsupported verdict.", 13, MUTED)
    add_label(slide, 6.95, 1.58, "OBJECTIVES")
    objectives = [
        "Train on a genuine labelled news dataset with reproducible evaluation.",
        "Route short headlines and longer articles through suitable models.",
        "Explain the result and keep a human responsible for verification.",
    ]
    for i, objective in enumerate(objectives, 1):
        yy = 2.05 + (i - 1) * 1.22
        add_line(slide, 6.95, yy - 0.12, 12.05, yy - 0.12, MUTED, 0.7)
        add_text(slide, 6.95, yy, 0.62, 0.35, f"0{i}", 16, GREEN, "Courier New", True)
        add_text(slide, 7.7, yy - 0.02, 4.35, 0.68, objective, 13, WHITE, "Aptos", False)
    add_panel(slide, 0.6, 5.75, 11.45, 0.78, PANEL, PANEL)
    add_text(slide, 0.9, 5.98, 10.9, 0.28, "Scope: English binary screening · local model artifact · Flask API · responsive browser interface", 12, GREEN, "Courier New", True)


def slide_related(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, "02", "Related work and research gap", "3")
    add_label(slide, 0.6, 1.58, "RELATED WORK", ORANGE)
    related = [
        ("LIAR benchmark", "12.8K manually labelled short statements from PolitiFact; useful for claim-level research."),
        ("FakeNewsNet", "News content plus social-context research data; collection is constrained by copyright and platform policies."),
        ("Text classifiers", "TF-IDF and linear models provide a fast, interpretable baseline for an academic deployment."),
    ]
    for i, (title, body) in enumerate(related):
        yy = 2.02 + i * 1.1
        add_line(slide, 0.6, yy - 0.12, 5.55, yy - 0.12, MUTED, 0.7)
        add_text(slide, 0.6, yy, 5.7, 0.28, title, 14, WHITE, "Cambria", True)
        add_text(slide, 0.6, yy + 0.34, 5.5, 0.54, body, 10, MUTED)
    add_panel(slide, 6.55, 1.55, 5.5, 4.95, PANEL, PANEL)
    add_text(slide, 6.95, 1.95, 4.6, 0.25, "OUR CONTRIBUTION", 10, GREEN, "Courier New", True)
    add_text(slide, 6.95, 2.45, 4.5, 0.35, "Project focus", 17, WHITE, "Cambria", True)
    add_text(slide, 6.95, 2.86, 4.55, 0.85, "A compact, explainable detector that distinguishes headline inputs from full article inputs and makes uncertainty visible.", 12, MUTED)
    add_line(slide, 6.95, 4.05, 11.65, 4.05, MUTED, 0.7)
    add_text(slide, 6.95, 4.38, 4.5, 0.35, "Our approach", 17, WHITE, "Cambria", True)
    add_text(slide, 6.95, 4.8, 4.55, 1.05, "Use the ISOT dataset, train separate TF-IDF + Logistic Regression pipelines, expose a Flask API, and require human source verification.", 12, MUTED)
    add_text(slide, 0.6, 6.75, 11.2, 0.28, "Gap addressed: many demos return a label; NewsLens pairs a model output with input-aware routing, provenance, metrics, and ethical guidance.", 10, GREEN, "Courier New", True)


def slide_architecture(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, "03", "System architecture and model flow", "4")
    add_label(slide, 0.6, 1.35, "TRAINING PIPELINE")
    steps = [("DATA", "Fake.csv\nTrue.csv"), ("NLP", "spaCy\ntokenization"), ("FEATURES", "bounded\nword TF-IDF"), ("MODELS", "headline +\narticle"), ("ARTIFACT", "joblib\nmetadata")]
    start_x = 0.65
    for i, (title, body) in enumerate(steps):
        x = start_x + i * 2.4
        add_panel(slide, x, 1.75, 1.85, 1.05, PANEL, GREEN)
        add_text(slide, x + 0.1, 1.9, 1.65, 0.2, title, 8, GREEN, "Courier New", True, PP_ALIGN.CENTER)
        add_text(slide, x + 0.1, 2.18, 1.65, 0.43, body, 11, WHITE, "Aptos", True, PP_ALIGN.CENTER)
        if i < len(steps) - 1:
            add_arrow(slide, x + 1.95, 2.17, 0.32, 0.2)
    add_label(slide, 0.6, 3.35, "INFERENCE PIPELINE", ORANGE)
    inference = [("USER TEXT", "headline\nor article"), ("VALIDATE", "type +\nlength"), ("ROUTE", "≤60 words\nheadline"), ("PREDICT", "probability\n+ signals"), ("VERIFY", "human\nsource check")]
    for i, (title, body) in enumerate(inference):
        x = start_x + i * 2.4
        fill = RGBColor(45, 39, 27) if i == 2 else PANEL
        line = ORANGE if i == 2 else MUTED
        add_panel(slide, x, 3.75, 1.85, 1.05, fill, line)
        add_text(slide, x + 0.1, 3.9, 1.65, 0.2, title, 8, ORANGE if i == 2 else GREEN, "Courier New", True, PP_ALIGN.CENTER)
        add_text(slide, x + 0.1, 4.18, 1.65, 0.43, body, 11, WHITE, "Aptos", True, PP_ALIGN.CENTER)
        if i < len(inference) - 1:
            add_arrow(slide, x + 1.95, 4.17, 0.32, 0.2, ORANGE if i == 2 else GREEN)
    add_panel(slide, 0.65, 5.45, 11.45, 0.78, PANEL, PANEL)
    add_text(slide, 0.95, 5.68, 10.8, 0.28, "API: GET /api/health  ·  POST /api/analyze  ·  Model loads a saved artifact; startup does not retrain.", 11, WHITE, "Courier New", True, PP_ALIGN.CENTER)


def slide_results(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    set_background(slide)
    add_header(slide, "04", "Results and conclusions", "5")
    add_label(slide, 0.6, 1.45, "MODEL RESULTS")
    cards = [("ARTICLE MODEL", "99.31%", "accuracy", "99.34% F1", GREEN), ("HEADLINE MODEL", "96.16%", "accuracy", "96.29% F1", ORANGE), ("DATASET", "44,898", "articles", "35,918 train · 8,980 test", GREEN)]
    for i, (label, value, small, detail, col) in enumerate(cards):
        x = 0.6 + i * 3.92
        add_panel(slide, x, 1.85, 3.52, 1.35, PANEL, PANEL)
        add_text(slide, x + 0.25, 2.08, 3.0, 0.2, label, 8, col, "Courier New", True)
        add_text(slide, x + 0.25, 2.36, 1.75, 0.38, value, 25, WHITE, "Cambria", True)
        add_text(slide, x + 2.0, 2.45, 1.15, 0.22, small, 9, MUTED, "Courier New")
        add_text(slide, x + 0.25, 2.92, 3.0, 0.2, detail, 9, MUTED)
    add_label(slide, 0.6, 3.65, "OBSERVATIONS", ORANGE)
    observations = [
        "Actual labelled rows from True.csv and Fake.csv produced the expected lower-risk and high-risk outcomes.",
        "Short inputs route to the headline model; full articles route to the article model.",
        "Random holdout metrics are not proof of real-world factual accuracy; publisher and topic leakage remain risks.",
    ]
    for i, text in enumerate(observations, 1):
        yy = 4.0 + (i - 1) * 0.52
        add_text(slide, 0.6, yy, 0.4, 0.23, f"0{i}", 10, GREEN, "Courier New", True)
        add_text(slide, 1.1, yy - 0.02, 5.45, 0.37, text, 10, WHITE)
    add_panel(slide, 6.95, 3.65, 5.1, 2.35, PANEL, PANEL)
    add_text(slide, 7.3, 3.95, 4.4, 0.2, "CONCLUSION", 9, GREEN, "Courier New", True)
    add_text(slide, 7.3, 4.3, 4.3, 0.88, "NewsLens turns NLP signals into a transparent verification aid—not an autonomous truth engine.", 18, WHITE, "Cambria", True)
    add_text(slide, 7.3, 5.35, 4.3, 0.38, "Pause · inspect the evidence · verify before sharing.", 11, ORANGE, "Courier New", True)


def build():
    prs = Presentation()
    prs.slide_width = Inches(W)
    prs.slide_height = Inches(H)
    slide_cover(prs)
    slide_problem(prs)
    slide_related(prs)
    slide_architecture(prs)
    slide_results(prs)
    prs.save(OUTPUT)


if __name__ == "__main__":
    build()
