#!/usr/bin/env python3
"""news-image-20261123: draw 'THE WORLD IN ONE DAY' — Monday 23 November 2026.
A newspaper front page, 1024x1024, Pillow, stdlib + Pillow only, no network.
Renders entry.png beside this file. Deterministic: same bytes every run.
Layout (1024x1024): masthead, stats strip, 3 leads, 12 grid, 18 briefs,
DATE CHECK box, footer. Legibility-first: 33 stories, large type, lots of air.
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 234)      # warm off-white newsprint
INK = (25, 25, 25)           # near-black ink
RED = (178, 28, 28)          # vintage red accent
MUTED = (90, 84, 74)         # grey-brown for labels
RULE = (60, 56, 48)          # rule lines
BOXBG = (238, 231, 216)      # date-check panel background
GRIDLINE = (200, 192, 176)   # thin separators
MARGIN = 28

SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    try:
        return ImageFont.truetype(path, size)
    except Exception:
        return ImageFont.load_default()


def wrap(draw, text, fnt, width):
    """Wrap text to fit width (pixels) using the font's metrics."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, text, fnt, width, fill=INK, leading=4):
    """Draw wrapped text, return y after the last line."""
    for line in wrap(draw, text, fnt, width):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + leading
    return y


def headline(draw, x, y, text, fnt, width, fill=INK):
    return text_block(draw, x, y, text, fnt, width, fill=fill, leading=2)


def rule(draw, x0, y, x1, weight=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=weight)


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    x0, x1 = MARGIN, W - MARGIN
    cw = x1 - x0  # content width = 968

    # ---------- masthead ----------
    y = 18
    f_title = font(SERIF_B, 47)
    title = "THE WORLD IN ONE DAY"
    tw = d.textlength(title, font=f_title)
    d.text(((W - tw) / 2, y), title, font=f_title, fill=INK)
    y += 56
    f_date = font(SANS_B, 21)
    date = "MONDAY 23 NOVEMBER 2026"
    tw = d.textlength(date, font=f_date)
    d.text(((W - tw) / 2, y), date, font=f_date, fill=RED)
    y += 30
    rule(d, x0, y, x1, 3)
    y += 6
    rule(d, x0, y, x1, 1)
    y += 12

    # ---------- stats strip ----------
    f_stat = font(SANS, 13)
    stats = ("KOSPI 4,736.98  \u22122.7%  (Mon close; intraday low \u22125.8%)   \u00b7   "
             "Hang Seng \u22121.5%   \u00b7   CSI 300 \u22121.0%   \u00b7   Nikkei CLOSED (holiday)   \u00b7   "
             "US futures: Nasdaq +3%, S&P +2%, Dow +700   \u00b7   S&P 500 6,910.39 \u22123.7% (Fri close)   \u00b7   "
             "Gold $3,517.24 \u22123.0% (Fri)   \u00b7   Brent $89.95 +0.6% (Fri)")
    y = text_block(d, x0, y, stats, f_stat, cw, fill=MUTED, leading=2)
    y += 4
    rule(d, x0, y, x1, 2)
    y += 12

    # ---------- leads ----------
    # Lead 1 left (wide), leads 2 & 3 stacked right.
    lead_w = 560
    right_x = x0 + lead_w + 24
    right_w = x1 - right_x
    leads_top = y

    f_lead_h = font(SERIF_B, 27)
    f_lead_b = font(SANS, 15)
    # Lead 1
    y1 = headline(d, x0, leads_top, "KYIV TOLL 12 \u2014 BOY, 7, PULLED ALIVE", f_lead_h, lead_w)
    y1 = text_block(d, x0, y1 + 2,
                    "Monday's toll from the overnight Russian strikes on the Kyiv region rose to 12 "
                    "\u2014 9 in Dymer, 2 in Vyshneve, 1 in Bila Tserkva. Rescuers pulled 7-year-old "
                    "David alive after 14 hours trapped in the rubble. Zelenskyy addressed the "
                    "nation on video Monday.",
                    f_lead_b, lead_w, leading=3)
    # Lead 2 (right, top)
    f_lead2_h = font(SERIF_B, 21)
    y2 = headline(d, right_x, leads_top, "ASIA SINKS AS AI FEARS SPREAD", f_lead2_h, right_w)
    y2 = text_block(d, right_x, y2 + 2,
                    "KOSPI plunged as much as 5.8% intraday \u2014 trading briefly halted \u2014 "
                    "before closing \u22122.7% at 4,736.98. Samsung \u22124.5%, SK Hynix \u22127.9%. "
                    "Seoul vowed stabilisation. US futures rebounded.",
                    f_lead_b, right_w, leading=3)
    # divider between lead 2 and lead 3
    y2 += 8
    rule(d, right_x, y2, x1, 1, fill=GRIDLINE)
    y2 += 10
    # Lead 3 (right, bottom)
    y3 = headline(d, right_x, y2, "NATO MEETS ON POLAND MISSILES", f_lead2_h, right_w)
    y3 = text_block(d, right_x, y3 + 2,
                    "The North Atlantic Council meets in Brussels today over the three Russian "
                    "Kh-101 cruise missiles that violated Polish airspace on Friday. Poland seeks "
                    "allied solidarity and stronger eastern-flank air defence. No Article 4 invoked.",
                    f_lead_b, right_w, leading=3)
    y = max(y1, y3) + 10
    rule(d, x0, y, x1, 2)
    y += 12

    # ---------- grid (12 stories, 3 cols x 4 rows) ----------
    grid = [
        ("24 DEAD IN JAVA FACTORY FIRE",
         "Indonesia confirmed Monday 24 died in the PT Fonusa Agung Mulia candy-factory fire in Cikande, Banten; ~30 still missing as the search resumed."),
        ("KOREA PASSES $1T IN EXPORTS",
         "Nov 1\u201320 exports hit a record $77.4B; cumulative exports reached $1.0076T. South Korea is the 4th country ever past $1T."),
        ("BELGIUM GROUNDED BY STRIKE",
         "Air-traffic controllers joined a national anti-austerity strike; nearly all flights cancelled \u2014 Brussels ~59,500 passengers on 429 flights hit."),
        ("UK TO HOST 2035 WOMEN'S CUP",
         "FIFA confirms the UK as 2035 host \u2014 first World Cup in the UK since 1966. 48 teams, 104 matches, 19 venues."),
        ("AFTER COP31: SAUDI BLAMED",
         "Monday analysis after Sunday's collapse: Riyadh loomed large, led resistance to fossil-fuel language; the EU and island states refused a text with no mention of oil, gas and coal."),
        ("M6.5 QUAKE ROCKS VANUATU",
         "A magnitude 6.5 quake struck the Vanuatu region at 02:40 UTC Monday, 598 km deep. No tsunami threat from a quake this deep."),
        ("US FUTURES BOUNCE AFTER ROUT",
         "Wall Street futures bounced Monday morning \u2014 Nasdaq 100 +3%, S&P 500 +2%, Dow +700 \u2014 after Friday's worst week in over six years."),
        ("PLOT TO KILL RAPPER TWICE",
         "Poland says Russia tried to assassinate Ukrainian rapper Kyivstoner twice; a plot at a Copenhagen concert was foiled on 25 Sept."),
        ("LIBYA 'READY' AFTER STRIKES",
         "Libya's military says Benghazi port is 'under control' and it is 'fully prepared' after the suspected Ukrainian drone strikes on the Russian corvette Merkury."),
        ("NHS TRIALS AI FOR BREAST CANCER",
         "The NHS launches the world's largest trial to find out whether AI can spot breast cancer earlier."),
        ("ARMY TO BLAST IOWA LEAD STORES",
         "The US Army plans to invoke emergency powers to detonate 4 tonnes of lead azide stored in an Iowa town, despite a court-ordered stay."),
        ("INDIA, CHINA TALK BORDER",
         "India and China hold 10-day talks to ease LAC tensions in Arunachal Pradesh. Nepal PM Balen Shah begins an India visit Monday."),
    ]
    f_grid_h = font(SANS_B, 15)
    f_grid_b = font(SANS, 12)
    cols, rows = 3, 4
    col_w = (cw - 2 * 20) // cols
    row_h = 68
    gy = y
    for i, (h, b) in enumerate(grid):
        r, c = divmod(i, cols)
        gx = x0 + c * (col_w + 20)
        gy2 = gy + r * row_h
        gy2 = headline(d, gx, gy2, h, f_grid_h, col_w)
        text_block(d, gx, gy2 + 1, b, f_grid_b, col_w, fill=MUTED, leading=1)
    y = gy + rows * row_h + 4
    rule(d, x0, y, x1, 2)
    y += 10

    # ---------- briefs (18, 3 cols x 6 rows) ----------
    briefs = [
        "Mets sign Tarik Skubal \u2014 9 years, $450M, a record deal.",
        "Red Wings trade ex-captain Dylan Larkin to Montreal in a blockbuster.",
        "US intel chief defends Trump's 'Putin my friend' remark as 'entirely appropriate'.",
        "WHO chief calls for peace amid heavy fighting in Ebola-hit DR Congo region.",
        "Israeli forces continue house demolitions in southern Lebanon.",
        "India: Congress MLA writes letter in blood to Haryana CM, claims brief detention.",
        "Nepal PM Balen Shah begins bilateral India visit \u2014 energy and connectivity on the agenda.",
        "India food regulator FSSAI orders prosecution of Bisleri over unsafe packaged water.",
        "Taiwan FSC bans short selling at or below flat price from today; export orders extend a 21-month rise.",
        "Anthropic shares retreat after record IPO \u2014 fell 9.1% Friday, down 7.1% more.",
        "China to cut margin requirement for leveraged share buys to 80% (from 100%) on 30 Nov.",
        "Don Toliver concert chaos: Manchester's Co-op Live arena evacuated after a suspected tear-gas release.",
        "Protests erupt at Seattle-Tacoma airport after ICE detained a father and daughter boarding a flight.",
        "Cameroon's ex-rebels caught between hiding and broken promises.",
        "India's GIFT Nifty points to a gap-up start; Nifty closed near 25,800 Friday.",
        "South Korea's finance minister pledges market stabilisation after the KOSPI plunge.",
        "Spain's S\u00e1nchez defends his record on TV: the Spanish people, not the press, will decide his future.",
        "Haas keeps Rafael Camara for the final two grands prix.",
    ]
    f_brief = font(SANS, 11)
    bcol_w = (cw - 2 * 20) // 3
    brow_h = 27
    by = y
    for i, b in enumerate(briefs):
        r, c = divmod(i, 3)
        bx = x0 + c * (bcol_w + 20)
        by2 = by + r * brow_h
        d.text((bx, by2), "\u2022", font=f_brief, fill=RED)
        text_block(d, bx + 12, by2, b, f_brief, bcol_w - 12, leading=1)
    y = by + 6 * brow_h + 2
    rule(d, x0, y, x1, 2)
    y += 10

    # ---------- DATE CHECK box ----------
    f_dc_h = font(SANS_B, 13)
    f_dc = font(SANS, 12)
    box_h = 56
    d.rectangle([x0, y, x1, y + box_h], fill=BOXBG, outline=RULE, width=1)
    d.text((x0 + 10, y + 7), "DATE CHECK \u2014 NOT TODAY:", font=f_dc_h, fill=RED)
    dc = ("COP31 collapse \u00b7 Riemann 'proof' \u00b7 Russian warship Merkury sunk \u00b7 Democrats' 258 House seats \u00b7 "
          "Trump 'bottom of the sea' dare \u00b7 Gaza mediator call \u00b7 El Chapo Isidro captured \u00b7 US AI sell-off \u2014 "
          "all Fri 20 \u2013 Sun 22 Nov, not Monday.")
    text_block(d, x0 + 10, y + 26, dc, f_dc, cw - 20, leading=2)
    y += box_h + 8

    # ---------- footer ----------
    f_foot = font(SANS, 10)
    foot = ("Sources: Reuters, BBC, Al Jazeera, CNBC, The Hindu, USGS, FIFA, Korea Customs Service \u2014 all dated Monday 23 November 2026.  "
            "Figures labelled with their as-of time; US closes shown are Friday 20 Nov, US futures are Monday morning.")
    text_block(d, x0, y, foot, f_foot, cw, fill=MUTED, leading=1)

    img.save("entry.png", format="PNG", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
