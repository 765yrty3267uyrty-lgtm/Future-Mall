#!/usr/bin/env python3
"""Generate Task 3 - Protection Plan PDF using reportlab.

Matches the capstone specification exactly:
  - Protection table for the 3 mall systems:
        Free Wi-Fi, Cashier Device, Mall Website
    (risk + protection method for each).
  - Awareness sign with 3 simple security tips for employees.
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (BaseDocTemplate, Frame, PageTemplate, Paragraph,
                                Spacer, Table, TableStyle, PageBreak, HRFlowable)

BRAND = {
    "primary": colors.HexColor("#2563EB"),
    "primary_dark": colors.HexColor("#1D4ED8"),
    "secondary": colors.HexColor("#0D9488"),
    "accent": colors.HexColor("#F97316"),
    "danger": colors.HexColor("#EF4444"),
    "warning": colors.HexColor("#F59E0B"),
    "success": colors.HexColor("#10B981"),
    "ink": colors.HexColor("#0F172A"),
    "text": colors.HexColor("#1E293B"),
    "muted": colors.HexColor("#64748B"),
    "surface": colors.HexColor("#F8FAFC"),
    "border": colors.HexColor("#E2E8F0"),
    "white": colors.white,
}

OUT = os.path.join(os.path.dirname(__file__), "..", "Task3_Protection_Plan.pdf")


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(BRAND["muted"])
    canvas.setFont("Helvetica", 8)
    canvas.drawString(16 * mm, 10 * mm, "Task 3 - Protection Plan | Future Mall")
    canvas.drawRightString(194 * mm, 10 * mm, f"Page {doc.page}")
    canvas.setStrokeColor(BRAND["border"])
    canvas.setLineWidth(0.5)
    canvas.line(16 * mm, 13 * mm, 194 * mm, 13 * mm)
    canvas.restoreState()


class CoverPageTemplate(PageTemplate):
    def beforeDrawPage(self, canvas, doc):
        canvas.saveState()
        canvas.setFillColor(BRAND["ink"])
        canvas.rect(0, A4[1] - 70 * mm, A4[0], 70 * mm, stroke=0, fill=1)
        canvas.setFillColor(BRAND["accent"])
        canvas.rect(0, A4[1] - 74 * mm, A4[0], 2 * mm, stroke=0, fill=1)
        canvas.restoreState()


def styles():
    s = {}
    s["title"] = ParagraphStyle("title", fontName="Helvetica-Bold", fontSize=26,
                                leading=30, textColor=BRAND["white"], alignment=TA_CENTER)
    s["cover_sub"] = ParagraphStyle("cover_sub", fontName="Helvetica", fontSize=13,
                                    leading=18, textColor=BRAND["white"], alignment=TA_CENTER)
    s["h1"] = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=18, leading=22,
                             textColor=BRAND["primary_dark"], spaceBefore=10, spaceAfter=6)
    s["h2"] = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=14, leading=18,
                             textColor=BRAND["primary_dark"], spaceBefore=8, spaceAfter=4)
    s["h3"] = ParagraphStyle("h3", fontName="Helvetica-Bold", fontSize=11.5, leading=15,
                             textColor=BRAND["ink"], spaceBefore=6, spaceAfter=2)
    s["body"] = ParagraphStyle("body", fontName="Helvetica", fontSize=10, leading=14.5,
                               textColor=BRAND["text"], alignment=TA_JUSTIFY,
                               spaceAfter=5)
    s["bullet"] = ParagraphStyle("bullet", parent=s["body"], leftIndent=12,
                                 bulletIndent=2, spaceAfter=3)
    s["small"] = ParagraphStyle("small", fontName="Helvetica", fontSize=8.5,
                                leading=12, textColor=BRAND["muted"])
    s["cell"] = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.5,
                               leading=11.5, textColor=BRAND["text"])
    s["cell_head"] = ParagraphStyle("cell_head", fontName="Helvetica-Bold",
                                    fontSize=9, leading=12, textColor=BRAND["white"])
    return s


def make_table(header, rows, col_widths=None, header_bg=None, styles=None):
    def _wrap(cell):
        if isinstance(cell, Paragraph):
            return cell
        if not cell:
            return ""
        return Paragraph(cell, styles["cell"])

    data = [[Paragraph(h, styles["cell_head"]) for h in header]]
    data += [[_wrap(c) for c in row] for row in rows]
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), header_bg or BRAND["primary"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), BRAND["white"]),
        ("VALIGN", (0, 0), (-1, 0), "MIDDLE"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [BRAND["white"], BRAND["surface"]]),
        ("GRID", (0, 0), (-1, -1), 0.5, BRAND["border"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 5),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("RIGHTPADDING", (0, 0), (-1, -1), 6),
    ]))
    return t


def build():
    st = styles()
    doc = BaseDocTemplate(OUT, pagesize=A4,
                          leftMargin=16 * mm, rightMargin=16 * mm,
                          topMargin=16 * mm, bottomMargin=18 * mm)
    body = Frame(doc.leftMargin, doc.bottomMargin,
                 doc.width, doc.height, id="body")
    doc.addPageTemplates([CoverPageTemplate(id="cover", frames=[Frame(0, 0, A4[0], A4[1], id="coverframe")]),
                          PageTemplate(id="normal", frames=[body], onPage=footer)])

    # ---------------- COVER ----------------
    cover = []
    cover.append(Spacer(1, 22 * mm))
    cover.append(Paragraph("PROTECTION PLAN", st["title"]))
    cover.append(Spacer(1, 6 * mm))
    cover.append(Paragraph("Future Mall Capstone - Task 3", st["cover_sub"]))
    cover.append(Spacer(1, 2 * mm))
    cover.append(Paragraph("Protecting the mall's most exposed systems & its people",
                           st["cover_sub"]))
    cover.append(Spacer(1, 30 * mm))

    meta = [
        ["Project", "Future Mall - Shopping for Tomorrow (Capstone)"],
        ["Document", "Task 3 - Protection Plan"],
        ["Scope", "Table for 3 mall systems: Free Wi-Fi, Cashier Device, Mall Website"],
        ["", "Awareness sign with 3 simple tips for employees"],
        ["Audience", "Mall staff, IT team, and management"],
        ["Format", "PDF (this file)"],
    ]
    cover.append(make_table(["Field", "Value"], meta, col_widths=[50 * mm, 108 * mm],
                            header_bg=BRAND["primary_dark"], styles=st))
    cover.append(Spacer(1, 12 * mm))
    cover.append(Paragraph("Prepared by the Future Mall team - Capstone Project 2026.",
                           st["small"]))
    cover.append(PageBreak())

    # ---------------- PART A : protection table for 3 systems ----------------
    parta = []
    parta.append(Paragraph("Protection Table - Three Mall Systems", st["h1"]))
    parta.append(Paragraph(
        "The three most exposed systems of Future Mall are the public Free Wi-Fi "
        "network, the cashier devices that handle daily sales, and the mall website "
        "customers use to browse and order. For each system the table lists its main "
        "risk and the protection method applied to reduce that risk.", st["body"]))
    parta.append(HRFlowable(width="100%", thickness=1, color=BRAND["primary"]))

    systems = [
        ["Mall System", "Main Risk", "Protection Method"],
        ["Free Wi-Fi",
         "Rogue devices / 'evil twin' access points trick users into "
         "connecting to a fake network and stealing their passwords and "
         "payment details (man-in-the-middle).",
         "Use WPA2/WPA3 enterprise authentication with per-user login; "
         "encrypt all traffic with captive-portal HTTPS plus a VPN option for "
         "sensitive browsing; isolate the guest network with VLAN segmentation "
         "so guests cannot reach mall devices; block peer-to-peer client "
         "traffic (client isolation)."],
        ["Cashier Device",
         "POS malware or a USB key infect the cashier, and staff leaving the "
         "device logged in lets others modify prices or leak customer payment "
         "data.",
         "Lock the cashier to a single restricted POS user, auto-lock after "
         "90 seconds; whitelist USB devices and scan them on insertion; keep "
         "the OS and POS software updated, run up-to-date antivirus, and "
         "disable side-loaded payments; record an audit log of every "
         "transaction and price change."],
        ["Mall Website",
         "SQL injection / XSS let attackers deface the site, steal customer "
         "logins, or inject phishing pages; brute force on the admin panel.",
         "Use HTTPS with TLS across the whole site; parameterise every SQL "
         "query; validate and encode all user input; enforce strong admin "
         "passwords (12+ chars) with MFA and IP allow-listing; keep CMS and "
         "plugins updated; take nightly backups and do weekly restore tests."],
    ]
    parta.append(make_table(systems[0], systems[1:],
                            col_widths=[26 * mm, 58 * mm, 74 * mm],
                            header_bg=BRAND["primary"], styles=st))
    parta.append(Spacer(1, 6 * mm))
    parta.append(Paragraph(
        "The table above is the deliverable table for Task 3. Every system has at "
        "least one realistic risk and one concrete protection method.", st["body"]))
    parta.append(PageBreak())

    # ---------------- PART B : awareness sign ----------------
    partb = []
    partb.append(Paragraph("Awareness Sign - 3 Simple Tips for Employees", st["h1"]))
    partb.append(Paragraph(
        "A poster/sign design that will be hung in the mall's staff areas "
        "(break room and back office). It contains three simple, easy-to-remember "
        "security tips.", st["body"]))
    partb.append(HRFlowable(width="100%", thickness=1, color=BRAND["primary"]))
    partb.append(Spacer(1, 4 * mm))

    sign_w, sign_h = 178 * mm, 96 * mm
    sign = Table(
        [[Paragraph("<b>Awareness Sign</b>", ParagraphStyle(
            "sh1", fontName="Helvetica-Bold", fontSize=9, textColor=BRAND["white"],
            alignment=TA_CENTER))]],
        colWidths=[sign_w], rowHeights=[6 * mm],
    )
    sign.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), BRAND["ink"]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))

    tip_style = ParagraphStyle("tip", fontName="Helvetica-Bold", fontSize=10.5,
                               leading=14, textColor=colors.black, alignment=TA_LEFT)
    sub_style = ParagraphStyle("sub", fontName="Helvetica", fontSize=8.5,
                               leading=11.5, textColor=BRAND["muted"], alignment=TA_LEFT)

    def tip_cell(num, headline, body, bg):
        inner = [
            [Paragraph(f"<font color='white'><b>{num}</b></font>",
                       ParagraphStyle("n", fontName="Helvetica-Bold", fontSize=14,
                                      alignment=TA_CENTER)),
             Paragraph(f"<b>{headline}</b>", tip_style)],
            ["", Paragraph(body, sub_style)],
        ]
        t = Table(inner, colWidths=[14 * mm, 46 * mm])
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, 0), bg),
            ("SPAN", (0, 0), (0, 1)),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 8),
            ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ("BOX", (0, 0), (-1, -1), 0.6, BRAND["border"]),
        ]))
        return t

    tips = [
        tip_cell("1", "Think before you click",
                 "Never open links or attachments from unknown senders - "
                 "if it is urgent, verify on another channel.", BRAND["accent"]),
        tip_cell("2", "Lock, then walk",
                 "Lock your screen whenever you leave your device - "
                 "even for a minute. An unattended cashier is an open door.",
                 BRAND["primary"]),
        tip_cell("3", "Never share your password",
                 "No real IT team will ever ask for your password or OTP. "
                 "Keep codes private, use a password manager and MFA.",
                 BRAND["secondary"]),
    ]
    body_row = Table([[tips[0], tips[1], tips[2]]],
                     colWidths=[60 * mm, 60 * mm, 60 * mm - 2 * mm])
    body_row.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 1),
        ("RIGHTPADDING", (0, 0), (-1, -1), 1),
    ]))

    banner = Paragraph("<b>FUTURE MALL - STAY SAFE, STAY SMART</b>",
                       ParagraphStyle("banner", fontName="Helvetica-Bold",
                                      fontSize=12, leading=16,
                                      textColor=BRAND["white"], alignment=TA_CENTER))

    partb.append(Table([[sign]], colWidths=[sign_w], rowHeights=[6 * mm]))
    partb.append(Spacer(1, 2 * mm))
    banner_table = Table([[banner]], colWidths=[sign_w], rowHeights=[8 * mm])
    banner_table.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), BRAND["primary"]),
                                      ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                                      ("LEFTPADDING", (0, 0), (-1, -1), 4),
                                      ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    partb.append(banner_table)
    partb.append(body_row)
    partb.append(Spacer(1, 3 * mm))
    partb.append(Paragraph(
        "Read the full three-system protection table on the previous page. "
        "For anything unusual, contact the IT help desk immediately.",
        ParagraphStyle("closing", parent=st["body"], alignment=TA_CENTER,
                       textColor=BRAND["muted"])))

    partb.append(Spacer(1, 8 * mm))
    partb.append(Paragraph(
        "Future Mall capstone project - Protection Plan (Task 3). Educational use. 2026.",
        st["small"]))

    flow = cover + parta + partb
    doc.build(flow)
    print("PDF created:", OUT)


if __name__ == "__main__":
    build()