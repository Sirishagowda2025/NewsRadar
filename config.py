"""
NewsRadar — Configuration
==========================
All sensitive values are loaded from environment variables.
Copy .env.example → .env, fill in your values, and you're good to go.

CATEGORIES define the "intelligence beats" the scraper monitors.
You can adapt these to any industry — just update search_queries,
RELEVANCE_KEYWORDS, and EXCLUDE_KEYWORDS to match your domain.

FIRST RUN : set time_window_hours = 720  (~1 month backfill)
DAILY RUN : set time_window_hours = 24

FILTER PHILOSOPHY:
  - Only DIRECT-impact articles pass: fee changes, policy mandates,
    compliance deadlines, API/integration changes, logistics rate changes,
    global events with concrete cost or compliance impact.
  - EXCLUDED: expansion news, general market growth, funding rounds,
    IPOs, executive hires, opinion pieces, how-to guides.
"""

import os

# ─────────────────────────────────────────────────────────────────────────────
# EMAIL  — values come from environment variables, never hardcoded
# ─────────────────────────────────────────────────────────────────────────────

def _env_list(key: str) -> list[str]:
    """Split a comma-separated env var into a clean list."""
    raw = os.environ.get(key, "")
    return [v.strip() for v in raw.split(",") if v.strip()]


EMAIL_CONFIG = {
    "smtp_server":    os.environ.get("SMTP_SERVER", "smtp.gmail.com"),
    "smtp_port":      int(os.environ.get("SMTP_PORT", "587")),
    "sender_email":   os.environ.get("SENDER_EMAIL", ""),
    "sender_password": os.environ.get("SMTP_PASSWORD", ""),   # Gmail App Password
    "recipients":     _env_list("RECIPIENTS"),
    "cc_recipients":  _env_list("CC_RECIPIENTS"),
    "subject":        os.environ.get("EMAIL_SUBJECT", "NewsRadar Intelligence — {date}"),
}

# ─────────────────────────────────────────────────────────────────────────────
# SYSTEM
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_CONFIG = {
    "time_window_hours":     168,   # how far back to fetch (hours). 24 = daily, 720 = monthly
    "articles_per_category": 20,    # max articles kept per category after AI ranking
    "articles_per_query":    12,    # max articles pulled per RSS feed query
    "excel_file":            "newsradar_report.xlsx",
    "preview_before_send":   True,
}

# ─────────────────────────────────────────────────────────────────────────────
# AI CONFIG  (Ollama — runs locally, no API key needed)
# ─────────────────────────────────────────────────────────────────────────────

OLLAMA_CONFIG = {
    # Model to use for scoring + summarisation. qwen3:4b is fast and free.
    # Pull it with:  ollama pull qwen3:4b
    "model":   os.environ.get("OLLAMA_MODEL", "qwen3:4b"),

    # Articles scoring below this threshold are dropped from the report.
    # 7 = only direct, actionable business impact passes.
    # Lower to 5 to get more articles; raise to 9 for tighter filtering.
    "min_relevance_score": int(os.environ.get("MIN_RELEVANCE_SCORE", "7")),

    # Set to False to skip AI entirely (faster, no Ollama needed).
    "enabled": os.environ.get("AI_ENABLED", "true").lower() == "true",
}

# ─────────────────────────────────────────────────────────────────────────────
# CATEGORIES
# ─────────────────────────────────────────────────────────────────────────────
# Each category defines:
#   html_section   — the CSS id used in the report
#   color          — the accent colour for that section
#   description    — subtitle shown in the report
#   search_queries — list of Google News RSS queries to run
#
# To adapt to a different industry, replace the search_queries lists
# and update RELEVANCE_KEYWORDS / EXCLUDE_KEYWORDS below.
# ─────────────────────────────────────────────────────────────────────────────

CATEGORIES = {

    "India": {
        "html_section": "s-india",
        "color": "#2563eb",
        "description": "Amazon India, Flipkart, Meesho, Blinkit, Swiggy Instamart — fee & policy changes only",
        "search_queries": [
            # Amazon India
            "Amazon India referral fee change 2026",
            "Amazon India FBA fee rate update 2026",
            "Amazon India seller policy mandate 2026",
            "Amazon India account suspension policy 2026",
            "Amazon India listing compliance deadline 2026",
            "Amazon India seller central policy update 2026",
            "Amazon India Easy Ship rate change 2026",
            "Amazon India storage fee update 2026",
            "Amazon India category restriction update 2026",
            "Amazon India GST TCS rate change seller 2026",
            # Flipkart
            "Flipkart commission rate change 2026",
            "Flipkart seller fee revision 2026",
            "Flipkart listing compliance mandate 2026",
            "Flipkart GSTIN KYC deadline seller 2026",
            "Flipkart shipping fee policy change 2026",
            "Flipkart account health policy update 2026",
            "Flipkart fulfilment fee change 2026",
            "Flipkart category policy restriction 2026",
            # Quick commerce
            "Zepto seller commission policy change 2026",
            "Blinkit seller fee rate update 2026",
            "Swiggy Instamart seller policy change 2026",
            "BigBasket seller listing compliance 2026",
            "JioMart seller fee policy change 2026",
            "Meesho seller fee commission change 2026",
            "quick commerce platform fee change India 2026",
            "dark store compliance regulation India 2026",
            # Regulatory
            "BIS certificate mandatory ecommerce India 2026",
            "FSSAI licence ecommerce mandatory India 2026",
            "EPR registration deadline ecommerce India 2026",
            "GST ecommerce compliance change India 2026",
            "ecommerce seller TDS TCS compliance India 2026",
        ],
    },

    "Global": {
        "html_section": "s-global",
        "color": "#7c3aed",
        "description": "Amazon global, UAE, US tariffs, EU compliance, payment policy changes",
        "search_queries": [
            # Amazon global
            "Amazon Global Selling fee rate change 2026",
            "Amazon Global Selling export compliance mandate India 2026",
            "Amazon FBA international fee rate change 2026",
            "Amazon UAE seller fee update 2026",
            "Amazon US seller policy change 2026",
            "Amazon UK EU fee change 2026",
            "Amazon Pan-EU fulfilment rate update 2026",
            # UAE / Middle East
            "Noon marketplace seller fee policy change 2026",
            "UAE ecommerce seller compliance mandate 2026",
            "Dubai customs ecommerce import rule 2026",
            "UAE VAT ecommerce change 2026",
            # US tariffs & trade
            "US tariff India ecommerce export impact 2026",
            "US import duty India goods change 2026",
            "US Section 301 tariff India ecommerce 2026",
            "de minimis threshold change US ecommerce 2026",
            "US customs ecommerce small parcel rule change 2026",
            # EU
            "EU ecommerce compliance mandate India seller 2026",
            "EU customs rule ecommerce India 2026",
            "EU VAT ecommerce OSS rule change 2026",
            "EU Digital Services Act ecommerce seller 2026",
            "EU import duty change India goods 2026",
            # Trade war / geopolitical with direct cost impact
            "trade war tariff India ecommerce cost impact 2026",
            "India US trade deal ecommerce impact 2026",
            # Payments
            "RBI payment aggregator cross border India rate change 2026",
            "Razorpay international payment fee change 2026",
            "FEMA ecommerce remittance rule change India 2026",
            "cross border payment compliance deadline India 2026",
            "PayPal India cross border fee change 2026",
            "Stripe India payment fee update 2026",
        ],
    },

    "Cross-Border & Export": {
        "html_section": "s-crossborder",
        "color": "#0891b2",
        "description": "India export customs rules, duty changes, DGFT mandates, logistics rate changes",
        "search_queries": [
            # Customs & duties
            "India ecommerce export customs rule change 2026",
            "customs duty rate change ecommerce India 2026",
            "export duty change India ecommerce 2026",
            "India import tariff rate change ecommerce 2026",
            "CBIC ecommerce export notification 2026",
            "India HS code change ecommerce 2026",
            "India customs valuation rule ecommerce 2026",
            # DGFT & IEC
            "DGFT export policy mandate change India 2026",
            "IEC ecommerce export compliance India 2026",
            "DGFT notification ecommerce export 2026",
            "RoDTEP rate change ecommerce export India 2026",
            "MEIS SEIS export incentive change India 2026",
            "export promotion scheme change India 2026",
            # Logistics & courier
            "cross border logistics rate increase India 2026",
            "courier export rule change India ecommerce 2026",
            "India air cargo export rate change 2026",
            "India sea freight export rate change 2026",
            "DHL FedEx UPS India export rate change 2026",
            "courier aggregator export rule India 2026",
            # FTAs
            "India FTA trade agreement tariff change ecommerce 2026",
            "India UAE CEPA ecommerce export 2026",
            "India UK FTA ecommerce impact 2026",
            "India EU FTA negotiation ecommerce 2026",
            "India GCC trade agreement ecommerce 2026",
            # Returns & compliance
            "cross border ecommerce return policy India 2026",
            "India export packaging compliance change 2026",
        ],
    },

    "Trade & Logistics": {
        "html_section": "s-trade",
        "color": "#d97706",
        "description": (
            "Global trade wars, shipping rate changes, port disruptions, freight indexes, "
            "sanctions — anything affecting cost or timeline of goods moving to/from India"
        ),
        "search_queries": [
            # Shipping rates & indexes
            "container shipping rate India 2026",
            "freight rate increase Asia Europe 2026",
            "Drewry World Container Index 2026",
            "SCFI Shanghai Container Freight Index 2026",
            "global shipping cost surge India exporter 2026",
            "India sea freight rate change 2026",
            "air freight rate India export 2026",
            "LCL FCL shipping rate change India 2026",
            # Port congestion & disruptions
            "port congestion India ecommerce delay 2026",
            "Nhava Sheva JNPT port delay 2026",
            "Red Sea shipping disruption India 2026",
            "Suez Canal shipping India impact 2026",
            "Panama Canal congestion India freight 2026",
            "port strike shipping delay India 2026",
            "global port congestion freight delay 2026",
            # Trade wars & tariffs with transport impact
            "US China trade war India shipping impact 2026",
            "US tariff increase global freight diversion India 2026",
            "trade route change India export cost 2026",
            "India export rerouting shipping cost 2026",
            # Carrier & logistics companies
            "Maersk shipping rate India 2026",
            "MSC container line rate India 2026",
            "CMA CGM freight rate India 2026",
            "COSCO shipping India rate 2026",
            "carrier surcharge India export 2026",
            # Fuel & BAF
            "bunker fuel surcharge India shipping 2026",
            "BAF bunker adjustment factor shipping India 2026",
            "IMO fuel regulation shipping cost 2026",
            # Sanctions & trade restrictions with logistics impact
            "Russia sanctions India shipping alternative route 2026",
            "trade restriction shipping route India 2026",
            "OFAC sanctions India goods transport 2026",
            # Last mile & express courier global
            "DHL express rate surcharge India 2026",
            "FedEx international rate increase India 2026",
            "UPS cross border delivery cost India 2026",
        ],
    },

    "Competitors": {
        "html_section": "s-competitors",
        "color": "#dc2626",
        "description": "Unicommerce, EasyEcom, Vinculum, Shiprocket, Delhivery — pricing & feature changes only",
        "search_queries": [
            # OMS/WMS
            "Unicommerce pricing plan change 2026",
            "Unicommerce platform feature update 2026",
            "Unicommerce new integration update 2026",
            "EasyEcom pricing fee update 2026",
            "EasyEcom platform feature change 2026",
            "Vinculum OMS pricing update 2026",
            "Vinculum new feature integration 2026",
            "Increff WMS pricing update 2026",
            "Browntape pricing update 2026",
            "SellerApp pricing feature update 2026",
            "Fynd platform fee update 2026",
            # Logistics
            "Shiprocket shipping rate change 2026",
            "Shiprocket policy update 2026",
            "Delhivery freight rate change 2026",
            "Delhivery service policy update 2026",
            "Clickpost platform fee update 2026",
            "Ecom Express rate policy change 2026",
            "XpressBees rate policy change 2026",
            "Shadowfax rate update 2026",
            "Blue Dart rate change ecommerce 2026",
            "DTDC ecommerce rate update 2026",
        ],
    },

    "Others": {
        "html_section": "s-others",
        "color": "#059669",
        "description": "ONDC policy changes, API integration updates, ad cost changes, India ecommerce policy",
        "search_queries": [
            # ONDC
            "ONDC seller fee compliance mandate 2026",
            "ONDC network policy rule change 2026",
            "ONDC buyer app seller integration update 2026",
            "ONDC transaction fee change 2026",
            "ONDC new category launch mandate 2026",
            # WMS / OMS / integration
            "warehouse management compliance ecommerce India 2026",
            "Amazon Flipkart API integration change 2026",
            "multichannel integration compliance change India 2026",
            "ecommerce ERP integration update India 2026",
            "inventory management compliance India ecommerce 2026",
            # Ads
            "Amazon sponsored ads policy fee change India 2026",
            "Flipkart ads cost rate change 2026",
            "ecommerce advertising rate increase India 2026",
            "Amazon PPC cost increase India 2026",
            "Flipkart sponsored product rate change 2026",
            # Supply chain & fulfilment
            "D2C fulfilment cost change India 2026",
            "India supply chain disruption ecommerce 2026",
            "3PL fulfilment rate change India 2026",
            "ecommerce returns cost change India 2026",
            # Policy
            "India ecommerce policy regulation change 2026",
            "consumer protection ecommerce rule India 2026",
            "India FDI ecommerce rule change 2026",
            "ecommerce data localisation rule India 2026",
        ],
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# IRRELEVANT_SOURCES — Gate 0 domain blocklist
# ─────────────────────────────────────────────────────────────────────────────

IRRELEVANT_SOURCES = [
    "buzzfeed.com", "indiatimes.com", "scoopwhoop.com",
    "mensxp.com", "femina.in", "filmfare.com",
    "pinkvilla.com", "bollywoodhungama.com",
    "tradingview.com",
    "Markets Mojo", "scanx.trade",
    "Whalesbook", "Prittle Prattle News",
    "cricinfo.com", "espncricinfo.com", "cricbuzz.com",
    "sportskeeda.com", "Construction World",
    "Exchange4Media", "Brand Equity",
    "naukri.com", "shine.com", "timesjobs.com",
    "foundit.in", "freshersworld.com",
    "prnewswire.com", "businesswire.com",
    "globenewswire.com", "einpresswire.com",
    "youtube.com", "instagram.com", "facebook.com", "twitter.com",
    "quora.com", "reddit.com", "medium.com",
    "slideshare.net", "scribd.com",
    "amazonaws.com", "cloudfront.net",
]


def is_irrelevant_source(source_name: str, url: str = "") -> bool:
    """Return True if the source domain is on the blocklist — article is skipped."""
    check = (source_name + " " + url).lower()
    return any(domain in check for domain in IRRELEVANT_SOURCES)


# ─────────────────────────────────────────────────────────────────────────────
# KEYWORD FILTERS
#
# RELEVANCE_KEYWORDS  — article must contain at least one to reach AI scoring.
# EXCLUDE_KEYWORDS    — article is dropped immediately if it contains any of these.
# TRADE_IMPACT_KEYWORDS — flags articles with direct transport/cost consequences
#                         (used in the Trade & Logistics AI scoring prompt).
# ─────────────────────────────────────────────────────────────────────────────

RELEVANCE_KEYWORDS = [
    # Platforms
    "amazon india", "flipkart", "meesho", "myntra", "jiomart",
    "noon", "zepto", "instamart", "bigbasket", "blinkit",
    "talabat", "swiggy instamart", "ondc",
    # Direct-impact operational terms
    "seller fee", "commission rate", "referral fee", "fba fee",
    "listing compliance", "account health", "policy change", "policy update",
    "mandate", "deadline", "compliance requirement", "penalty", "suspension",
    "rate change", "rate increase", "rate revision", "fee revision",
    "api update", "integration change", "platform update",
    # Logistics & fulfilment cost
    "shipping rate", "freight rate", "logistics cost", "last mile rate",
    "fulfilment cost", "warehouse compliance", "order management update",
    "container rate", "air freight", "sea freight", "ocean freight",
    "carrier surcharge", "bunker surcharge", "port congestion",
    "shipping disruption", "freight index", "container shortage",
    # Regulatory / compliance
    "bis certification", "fssai", "epr registration", "gst change", "gstin mandate",
    "customs duty", "import duty", "export duty", "tariff change",
    "dgft", "iec mandate", "cbic", "fema", "rbi circular",
    "payment aggregator", "cross border payment rule",
    # Global direct-impact trade events
    "trade war", "us tariff", "eu tariff", "import ban", "export ban",
    "sanctions", "trade restriction", "duty hike", "de minimis",
    "red sea", "suez canal", "panama canal",
    "maersk", "msc shipping", "cma cgm", "cosco shipping",
    "drewry", "scfi", "freight index",
    "india fta", "india us trade", "india eu trade", "india uae cepa",
    # Competitor platform changes (pricing/feature only)
    "unicommerce", "shiprocket rate", "delhivery rate", "clickpost fee",
    "easeecom", "vinculum pricing", "ecom express rate",
    "xpressbees rate", "shadowfax rate",
]

EXCLUDE_KEYWORDS = [
    # Funding / corporate
    "ipo", "share price", "fundraising", "series a", "series b",
    "venture capital", "valuation", "investment round", "funding round",
    "nse", "bse", "sensex", "quarterly earnings", "annual report",
    # Executive / org changes
    "ceo appointed", "ceo resigns", "board of directors",
    "chief executive", "co-founder", "leadership team", "appoints ceo",
    # Competitor expansion news (not pricing/policy)
    "expands to", "launches in", "enters market", "new city launch",
    "opens warehouse", "new hub", "geographic expansion",
    "market share", "valuation hits", "gmv crosses", "revenue grows",
    # Legal / IP noise
    "trademark infringement", "counterfeit", "patent lawsuit",
    # Geopolitical noise without direct transport/ecommerce cost impact
    "diplomatic talks", "foreign policy", "bilateral summit",
    "peace talks", "military", "defence deal",
    # Entertainment / lifestyle
    "bollywood", "celebrity", "cricket", "ipl",
    "food delivery restaurant", "zomato restaurant",
    # Finance products
    "mutual fund", "insurance premium", "home loan", "stock recommendation",
    "equity market", "bond yield",
    # Jobs
    "job opening", "hiring alert", "internship", "we are hiring",
    # Generic opinion / how-to
    "how to sell", "tips for sellers", "guide to ecommerce",
    "opinion:", "market size by 2030", "forecast 2030", "projected to grow",
    "industry report", "whitepaper", "listicle",
    # Agriculture / packaging unrelated to ecommerce logistics
    "aqua farming", "bubble wrap market", "corrugated box market",
    "agricultural output",
]

TRADE_IMPACT_KEYWORDS = [
    # Rate signals
    "rate increase", "rate surge", "rate spike", "surcharge", "price hike",
    "freight cost", "shipping cost", "cost increase", "cost impact",
    # Route disruption
    "port congestion", "port delay", "port strike", "route disruption",
    "canal disruption", "rerouting", "transit time", "delay",
    # Tariff / trade war with shipping consequence
    "tariff hike", "duty increase", "trade war impact", "export ban",
    "import restriction", "sanctions impact", "trade route",
    # Carrier / index
    "container shortage", "blank sailing", "carrier", "vessel",
    "freight index", "drewry", "scfi", "bdi", "baltic index",
]


def has_trade_impact(text: str) -> bool:
    """
    Return True if the article text contains direct trade/transport impact keywords.
    Used to flag Trade & Logistics articles that actually change cost or delivery time.
    """
    t = text.lower()
    return any(kw in t for kw in TRADE_IMPACT_KEYWORDS)
