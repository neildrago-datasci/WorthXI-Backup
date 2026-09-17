
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
import requests
from pathlib import Path

# ============================================================
# WORTHXI — PREMIUM PLAYER PERFORMANCE DASHBOARD
# ============================================================

st.set_page_config(
    page_title="WorthXI | Player Intelligence",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# PREMIUM UI
# -----------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(circle at 85% 5%, rgba(99,102,241,.13), transparent 28%),
        radial-gradient(circle at 8% 35%, rgba(16,185,129,.09), transparent 25%),
        #070a12;
}

[data-testid="stHeader"] {
    background: rgba(7,10,18,.75);
}

.block-container {
    max-width: 1500px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0b1020 0%, #080b13 100%);
    border-right: 1px solid rgba(255,255,255,.08);
}

[data-testid="stSidebar"] * {
    color: #e8ecf5;
}

.worth-brand {
    display:flex;
    align-items:center;
    gap:14px;
    margin-bottom: 2rem;
}

.worth-ball {
    width:52px;
    height:52px;
    border-radius:16px;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:26px;
    background:linear-gradient(135deg,#6366f1,#22c55e);
    box-shadow:0 12px 35px rgba(99,102,241,.28);
}

.worth-brand-title {
    font-size:25px;
    font-weight:900;
    letter-spacing:-1px;
    line-height:1;
}

.worth-brand-sub {
    font-size:11px;
    color:#8992a8;
    margin-top:5px;
    letter-spacing:1.5px;
    text-transform:uppercase;
}

.hero {
    position:relative;
    overflow:hidden;
    border:1px solid rgba(255,255,255,.09);
    border-radius:28px;
    padding:36px 40px;
    margin-bottom:22px;
    background:
        radial-gradient(circle at 85% 15%, rgba(99,102,241,.28), transparent 32%),
        radial-gradient(circle at 70% 100%, rgba(34,197,94,.14), transparent 28%),
        linear-gradient(135deg, rgba(17,24,39,.96), rgba(9,12,21,.98));
    box-shadow:0 25px 70px rgba(0,0,0,.28);
}

.hero:after {
    content:"WORTHXI";
    position:absolute;
    right:-20px;
    bottom:-45px;
    font-size:110px;
    font-weight:900;
    letter-spacing:-7px;
    color:rgba(255,255,255,.025);
    pointer-events:none;
}

.hero-kicker {
    color:#8b9cff;
    text-transform:uppercase;
    font-size:12px;
    font-weight:800;
    letter-spacing:2px;
    margin-bottom:10px;
}

.hero h1 {
    font-size:clamp(42px,6vw,76px);
    line-height:.92;
    letter-spacing:-5px;
    margin:0;
    font-weight:900;
    color:#fff;
}

.hero p {
    color:#aab3c5;
    max-width:700px;
    font-size:16px;
    line-height:1.7;
    margin:18px 0 0;
}

.pill {
    display:inline-flex;
    align-items:center;
    gap:7px;
    margin-top:20px;
    padding:8px 13px;
    border-radius:999px;
    background:rgba(34,197,94,.10);
    border:1px solid rgba(34,197,94,.22);
    color:#86efac;
    font-size:12px;
    font-weight:700;
}

.section-title {
    display:flex;
    align-items:end;
    justify-content:space-between;
    margin:30px 0 14px;
}

.section-title h2 {
    font-size:22px;
    margin:0;
    color:#f7f8fb;
    letter-spacing:-.5px;
}

.section-title span {
    color:#747f95;
    font-size:12px;
}

.player-card {
    border:1px solid rgba(255,255,255,.09);
    border-radius:24px;
    padding:25px;
    background:linear-gradient(145deg, rgba(20,26,42,.94), rgba(11,15,25,.96));
    box-shadow:0 18px 50px rgba(0,0,0,.18);
    margin-bottom:18px;
}


.player-profile {
    display:grid;
    grid-template-columns:140px 1fr auto;
    gap:24px;
    align-items:center;
    border:1px solid rgba(255,255,255,.09);
    border-radius:26px;
    padding:22px 25px;
    margin-bottom:20px;
    background:
        radial-gradient(circle at 10% 20%, rgba(99,102,241,.12), transparent 30%),
        linear-gradient(145deg,rgba(18,24,39,.98),rgba(9,13,22,.98));
    box-shadow:0 20px 60px rgba(0,0,0,.22);
}

.profile-photo-wrap {
    width:140px;
    height:160px;
    border-radius:20px;
    overflow:hidden;
    background:linear-gradient(135deg,#151b31,#0c101c);
    border:1px solid rgba(255,255,255,.1);
    display:flex;
    align-items:center;
    justify-content:center;
}

.player-photo {
    width:100%;
    height:100%;
    object-fit:cover;
    object-position:center top;
}

.player-photo-fallback {
    font-size:38px;
    font-weight:900;
    color:#c7d2fe;
    letter-spacing:-2px;
}

.profile-eyebrow {
    color:#818cf8;
    font-size:10px;
    font-weight:900;
    letter-spacing:2px;
    margin-bottom:8px;
}

.dot {
    color:#4b5563;
    padding:0 5px;
}

.profile-tags {
    display:flex;
    flex-wrap:wrap;
    gap:8px;
    margin-top:17px;
}

.profile-tags span {
    color:#aeb8cb;
    background:rgba(255,255,255,.045);
    border:1px solid rgba(255,255,255,.07);
    border-radius:999px;
    padding:7px 10px;
    font-size:11px;
    font-weight:700;
}

.profile-value {
    min-width:190px;
    padding-left:24px;
    border-left:1px solid rgba(255,255,255,.08);
}

.value-mini-label {
    color:#69758b;
    font-size:9px;
    font-weight:800;
    letter-spacing:1.4px;
}

.profile-price {
    color:#fff;
    font-size:37px;
    font-weight:900;
    letter-spacing:-2px;
    margin:5px 0 2px;
}

.compare-name {
    color:#fff;
    font-size:23px;
    font-weight:900;
    margin-top:7px;
}

@media (max-width: 800px) {
    .player-profile {
        grid-template-columns:90px 1fr;
    }
    .profile-photo-wrap {
        width:90px;
        height:110px;
    }
    .profile-value {
        grid-column:1 / -1;
        border-left:0;
        border-top:1px solid rgba(255,255,255,.08);
        padding:15px 0 0;
    }
}

.player-name {
    font-size:31px;
    font-weight:900;
    letter-spacing:-1.3px;
    color:#fff;
    margin-bottom:5px;
}

.player-meta {
    color:#8994a9;
    font-size:13px;
}

.position-badge {
    display:inline-block;
    padding:5px 10px;
    border-radius:999px;
    background:rgba(99,102,241,.15);
    color:#a5b4fc;
    font-weight:800;
    font-size:11px;
    margin-left:6px;
}

.metric-card {
    background:linear-gradient(145deg,rgba(19,25,40,.95),rgba(10,14,23,.96));
    border:1px solid rgba(255,255,255,.075);
    border-radius:18px;
    padding:17px 18px;
    min-height:100px;
    box-shadow:0 12px 35px rgba(0,0,0,.13);
}

.metric-label {
    color:#7f8ba3;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:1.15px;
    font-weight:700;
}

.metric-value {
    color:#f8fafc;
    font-size:27px;
    font-weight:850;
    margin-top:7px;
    letter-spacing:-1px;
}

.metric-accent {
    color:#8b9cff;
}

.value-card {
    border-radius:22px;
    padding:24px;
    border:1px solid rgba(255,255,255,.09);
    background:linear-gradient(145deg,rgba(19,25,40,.97),rgba(9,13,22,.97));
}

.value-label {
    color:#7f8ba3;
    font-size:11px;
    text-transform:uppercase;
    letter-spacing:1.2px;
    font-weight:800;
}

.value-number {
    color:white;
    font-size:38px;
    font-weight:900;
    letter-spacing:-1.8px;
    margin-top:5px;
}

.value-sub {
    color:#8994a9;
    font-size:12px;
    margin-top:4px;
}

.status-good {
    color:#86efac;
    background:rgba(34,197,94,.08);
    border:1px solid rgba(34,197,94,.18);
}

.status-watch {
    color:#fcd34d;
    background:rgba(245,158,11,.08);
    border:1px solid rgba(245,158,11,.18);
}

.status-neutral {
    color:#cbd5e1;
    background:rgba(148,163,184,.08);
    border:1px solid rgba(148,163,184,.18);
}

.status-box {
    border-radius:18px;
    padding:15px 18px;
    margin:18px 0;
    font-size:13px;
    line-height:1.55;
}

.insight {
    border-left:3px solid #6366f1;
    padding:13px 17px;
    background:rgba(99,102,241,.07);
    border-radius:0 14px 14px 0;
    color:#b7c0d3;
    font-size:13px;
    line-height:1.65;
    margin:14px 0;
}

.footer {
    margin-top:45px;
    padding-top:22px;
    border-top:1px solid rgba(255,255,255,.07);
    color:#667085;
    font-size:11px;
    text-align:center;
}

div[data-testid="stMetric"] {
    background:transparent;
}

.stTabs [data-baseweb="tab-list"] {
    gap:7px;
    background:rgba(255,255,255,.025);
    padding:6px;
    border-radius:14px;
}

.stTabs [data-baseweb="tab"] {
    border-radius:10px;
    color:#8d98ad;
    font-weight:700;
}

.stTabs [aria-selected="true"] {
    background:rgba(99,102,241,.15);
    color:#c7d2fe;
}

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background:rgba(255,255,255,.045);
    border-color:rgba(255,255,255,.10);
    border-radius:12px;
}

.stSlider > div > div > div {
    color:#6366f1;
}

button[kind="secondary"] {
    border-radius:10px;
}

hr {
    border-color:rgba(255,255,255,.07);
}


.visual-stat {
    border:1px solid rgba(255,255,255,.075);
    background:rgba(255,255,255,.025);
    border-radius:16px;
    padding:15px;
    margin-bottom:10px;
}
.small-note {
    color:#69758b;
    font-size:11px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD MODEL + DATA
# -----------------------------
@st.cache_resource
def load_assets():
    model = joblib.load("worthxi_model.pkl")
    encoder = joblib.load("worthxi_position_encoder.pkl")
    features = joblib.load("worthxi_features.pkl")
    data = pd.read_csv("WorthXI_expanded_player_data.csv")
    return model, encoder, features, data

model, position_encoder, model_features, df = load_assets()

df["Position"] = df["Position"].fillna("").astype(str).str.strip()
df["Season"] = df["Season"].fillna("").astype(str).str.strip()
df["Player"] = df["Player"].fillna("Unknown").astype(str).str.strip()

# -----------------------------
# HELPERS
# -----------------------------
def money(v):
    return f"€{v/1_000_000:.1f}M"

def metric_card(label, value, accent=False):
    cls = "metric-value metric-accent" if accent else "metric-value"
    st.markdown(
        f'<div class="metric-card"><div class="metric-label">{label}</div>'
        f'<div class="{cls}">{value}</div></div>',
        unsafe_allow_html=True
    )

def chart_layout(fig, height=430):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#aab3c5"),
        title_font=dict(size=17, color="#f8fafc"),
        margin=dict(l=20, r=25, t=65, b=25),
        xaxis=dict(
            gridcolor="rgba(148,163,184,.09)",
            zerolinecolor="rgba(148,163,184,.12)",
        ),
        yaxis=dict(
            gridcolor="rgba(148,163,184,.09)",
            zerolinecolor="rgba(148,163,184,.12)",
        ),
    )
    return fig


# -----------------------------
# PLAYER IMAGE + EXTRA HELPERS
# -----------------------------
@st.cache_data(ttl=7 * 24 * 60 * 60, show_spinner=False)
def get_player_image(player_name, club_name=""):
    """
    Identity-safe footballer photo resolver.

    IMPORTANT DESIGN RULE:
    A wrong photo is worse than no photo.  This resolver therefore prefers
    verified Wikidata footballer identities and FAILS CLOSED when confidence
    is too low instead of showing a random same-name person, stadium, badge,
    stamp, or another sport.

    Priority:
    1. Explicit local player image, if supplied.
    2. Exact canonical identity overrides for known ambiguous/high-profile names.
    3. Wikidata identity search, requiring an association-football occupation
       and scoring the player's club against the selected dataset club.
    4. Wikipedia page image only after the Wikidata identity is established.
    """
    name = str(player_name).strip()
    club = str(club_name).strip()

    # These are deliberate identity overrides for names that are commonly
    # ambiguous.  The dataset itself supplies the club, so Pedro -> Pedro
    # Rodriguez is unambiguous here because every Pedro record is Chelsea.
    CANONICAL = {
        "marc guehi": "Marc Guéhi",
        "matheus nunes": "Matheus Nunes",
        "mohamed salah": "Mohamed Salah",
        "pedro": "Pedro Rodríguez",
        "petr cech": "Petr Čech",
        "rodri": "Rodri (footballer, born 1996)",
        "romeo lavia": "Roméo Lavia",
        "sadio mane": "Sadio Mané",
        "thiago alcantara": "Thiago Alcântara",
        "vincent kompany": "Vincent Kompany",
        "yaya toure": "Yaya Touré",
        "zlatan ibrahimovic": "Zlatan Ibrahimović",
        "cesc fabregas": "Cesc Fàbregas",
        "achraf hakimi": "Achraf Hakimi",
    }

    # 1) Optional local images always win.
    image_dir = Path(__file__).resolve().parent / "player_images"
    normalized = name.lower().replace(".", "").strip()
    local_names = [name, name.replace(" ", "_"), CANONICAL.get(normalized, "")]
    if image_dir.exists():
        for candidate_name in local_names:
            if not candidate_name:
                continue
            for ext in (".jpg", ".jpeg", ".png", ".webp"):
                candidate = image_dir / f"{candidate_name}{ext}"
                if candidate.exists():
                    return str(candidate)

    headers = {
        "User-Agent": "WorthXI/3.0 (student football analytics research project)"
    }

    def get_json(url, params, timeout=10):
        try:
            r = requests.get(url, params=params, headers=headers, timeout=timeout)
            r.raise_for_status()
            return r.json()
        except Exception:
            return None

    def norm_text(value):
        import unicodedata
        value = unicodedata.normalize("NFKD", str(value)).encode("ascii", "ignore").decode("ascii")
        return " ".join(value.lower().replace("-", " ").replace("_", " ").split())

    target = norm_text(name)
    canonical = CANONICAL.get(normalized, name)
    canonical_norm = norm_text(canonical)
    club_norm = norm_text(club)

    # Common club aliases in the dataset versus Wikidata/Wikipedia.
    club_aliases = {
        "manchester city": ["manchester city", "manchester city fc"],
        "manchester united": ["manchester united", "manchester united fc"],
        "liverpool": ["liverpool", "liverpool fc"],
        "chelsea": ["chelsea", "chelsea fc"],
        "arsenal": ["arsenal", "arsenal fc"],
        "crystal palace": ["crystal palace", "crystal palace fc"],
    }
    club_terms = club_aliases.get(club_norm, [club_norm]) if club_norm else []

    # 2) Wikidata: identity + occupation + club + image.
    # Association football player is Wikidata Q937857.
    wd_search = get_json("https://www.wikidata.org/w/api.php", {
        "action": "wbsearchentities",
        "search": canonical,
        "language": "en",
        "uselang": "en",
        "format": "json",
        "limit": 10,
        "type": "item",
    })

    candidates = (wd_search or {}).get("search", [])
    ids = [c.get("id") for c in candidates if c.get("id", "").startswith("Q")]
    if ids:
        entity_data = get_json("https://www.wikidata.org/w/api.php", {
            "action": "wbgetentities",
            "ids": "|".join(ids),
            "format": "json",
            "languages": "en",
            "props": "labels|aliases|descriptions|claims",
        }, timeout=15)
        entities = (entity_data or {}).get("entities", {})

        # Collect all referenced club/occupation IDs, then fetch their labels.
        referenced_ids = set()
        for ent in entities.values():
            for claim in ent.get("claims", {}).get("P54", []):
                try:
                    referenced_ids.add(claim["mainsnak"]["datavalue"]["value"]["id"])
                except Exception:
                    pass
            for claim in ent.get("claims", {}).get("P106", []):
                try:
                    referenced_ids.add(claim["mainsnak"]["datavalue"]["value"]["id"])
                except Exception:
                    pass

        label_map = {}
        if referenced_ids:
            ref_data = get_json("https://www.wikidata.org/w/api.php", {
                "action": "wbgetentities",
                "ids": "|".join(list(referenced_ids)[:50]),
                "format": "json",
                "languages": "en",
                "props": "labels",
            }, timeout=15)
            for qid, ent in (ref_data or {}).get("entities", {}).items():
                label_map[qid] = ent.get("labels", {}).get("en", {}).get("value", "")

        scored = []
        for qid in ids:
            ent = entities.get(qid, {})
            label = ent.get("labels", {}).get("en", {}).get("value", "")
            aliases = [a.get("value", "") for a in ent.get("aliases", {}).get("en", [])]
            desc = ent.get("descriptions", {}).get("en", {}).get("value", "")
            label_norm = norm_text(label)
            alias_norms = [norm_text(a) for a in aliases]
            desc_norm = norm_text(desc)

            # Require football identity. P106 is the strongest signal.
            occupation_ids = set()
            for claim in ent.get("claims", {}).get("P106", []):
                try:
                    occupation_ids.add(claim["mainsnak"]["datavalue"]["value"]["id"])
                except Exception:
                    pass
            occupation_labels = [norm_text(label_map.get(q, "")) for q in occupation_ids]
            football_occupation = (
                "Q937857" in occupation_ids
                or any("association football" in x or "football player" in x or "footballer" in x or "soccer player" in x for x in occupation_labels)
                or "footballer" in desc_norm
                or "soccer player" in desc_norm
                or "football player" in desc_norm
            )
            if not football_occupation:
                continue

            # Club membership is a powerful disambiguator for short/common names.
            team_labels = []
            for claim in ent.get("claims", {}).get("P54", []):
                try:
                    team_qid = claim["mainsnak"]["datavalue"]["value"]["id"]
                    team_labels.append(norm_text(label_map.get(team_qid, "")))
                except Exception:
                    pass
            club_match = any(term and any(term in team for team in team_labels) for term in club_terms)

            score = 0
            if label_norm == canonical_norm or label_norm == target:
                score += 70
            elif target and (target in label_norm or label_norm in target):
                score += 45
            elif any(target == a for a in alias_norms):
                score += 55
            elif any(target in a or a in target for a in alias_norms if a):
                score += 30

            if club_match:
                score += 45
            elif club_terms:
                score -= 10

            # Prefer a real image claim. A verified identity without an image
            # is still preferable to a wrong image, but it should not display one.
            image_claims = ent.get("claims", {}).get("P18", [])
            image_file = None
            if image_claims:
                try:
                    image_file = image_claims[0]["mainsnak"]["datavalue"]["value"]
                except Exception:
                    pass
            if image_file:
                score += 10

            scored.append((score, label, qid, image_file, club_match, desc))

        scored.sort(key=lambda x: x[0], reverse=True)
        if scored:
            score, label, qid, image_file, club_match, desc = scored[0]
            # High-confidence rule. Club match is required for highly ambiguous
            # names such as Pedro; otherwise exact footballer identity is enough.
            exact_identity = norm_text(label) in {target, canonical_norm}
            if image_file and score >= 80 and (club_match or exact_identity):
                encoded = requests.utils.quote(str(image_file), safe="")
                return f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded}?width=700"

            # For a non-exact but strong candidate, require club match.
            if image_file and score >= 90 and club_match:
                encoded = requests.utils.quote(str(image_file), safe="")
                return f"https://commons.wikimedia.org/wiki/Special:FilePath/{encoded}?width=700"

    # 3) Exact Wikipedia page, but ONLY for our verified canonical title.
    # This prevents random search results from becoming photos.
    wiki_title = canonical
    encoded_title = requests.utils.quote(wiki_title.replace(" ", "_"), safe="")
    rest_url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded_title}"
    try:
        r = requests.get(rest_url, headers=headers, timeout=8)
        if r.ok:
            data = r.json()
            desc = norm_text(data.get("description", ""))
            thumb = data.get("thumbnail", {}).get("source")
            football_desc = any(k in desc for k in ["footballer", "football player", "soccer player"])
            if thumb and football_desc:
                return thumb
    except Exception:
        pass

    # FAIL CLOSED: do not return a random image.
    return None

def initials(name):
    parts = [p for p in str(name).split() if p]
    if not parts:
        return "⚽"
    return "".join(p[0] for p in parts[:2]).upper()

def money_exact(v):
    return f"€{v/1_000_000:.2f}M"

def get_player_history(player_name):
    h = df[df["Player"] == player_name].copy()
    if h.empty:
        return h
    h = h.sort_values("Season")
    return h

def predict_row(row):
    x = pd.DataFrame({
        "Goal_Contribution": [row["Goal_Contribution"]],
        "Shot_Accuracy": [row["Shot_Accuracy"]],
        "Defensive_Contribution": [row["Defensive_Contribution"]],
        "Minutes_Per_Appearance": [row["Minutes_Per_Appearance"]],
        "Discipline_Score": [row["Discipline_Score"]],
        "Age": [row["Age"]],
    })
    enc = position_encoder.transform([[row["Position"]]])
    for i, pos in enumerate(position_encoder.classes_):
        x[f"Position_{pos}"] = enc[0][i]
    x = x.reindex(columns=model_features, fill_value=0)
    return float(model.predict(x)[0])

# -----------------------------
# SIDEBAR
# -----------------------------
with st.sidebar:
    st.markdown("""
    <div class="worth-brand">
        <div class="worth-ball">⚽</div>
        <div>
            <div class="worth-brand-title">WorthXI</div>
            <div class="worth-brand-sub">Player Intelligence</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Explore Players")

    positions = ["All Positions", "FW", "MF", "DF", "GK"]
    seasons = sorted(df["Season"].dropna().unique())
    min_age = int(df["Age"].dropna().min())
    max_age = int(df["Age"].dropna().max())

    selected_position = st.selectbox("Position", positions)
    selected_age_range = st.slider(
        "Age range",
        min_value=min_age,
        max_value=max_age,
        value=(min_age, max_age)
    )
    selected_season = st.selectbox(
        "Season",
        ["All Seasons"] + seasons
    )

    st.markdown("---")
    st.markdown("### Dataset")
    st.markdown(
        f"**{len(df):,}** player-season records  \n"
        f"**{df['Player'].nunique():,}** unique players  \n"
        f"**{df['Season'].nunique():,}** seasons"
    )

    st.markdown("---")
    st.caption("WorthXI • Football Performance × Market Value")
    st.caption("Machine-learning assisted analysis")
    st.caption("Player photos: Wikimedia + optional local images")

# -----------------------------
# HERO
# -----------------------------
st.markdown("""
<div class="hero">
    <div class="hero-kicker">Football analytics · player intelligence</div>
    <h1>WORTHXI</h1>
    <p>
        Go beyond the headline price. Explore player performance, compare
        market value with a machine-learning estimate, and understand the
        statistical profile behind the number.
    </p>
    <div class="pill">● Linear Regression valuation engine</div>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# FILTER DATA
# -----------------------------
filtered_df = df.copy()

if selected_position != "All Positions":
    filtered_df = filtered_df[filtered_df["Position"] == selected_position]

filtered_df = filtered_df[
    (filtered_df["Age"] >= selected_age_range[0]) &
    (filtered_df["Age"] <= selected_age_range[1])
]

if selected_season != "All Seasons":
    filtered_df = filtered_df[filtered_df["Season"] == selected_season]

if filtered_df.empty:
    st.error("No players match these filters. Try widening the age range or changing the position.")
    st.stop()

players = sorted(filtered_df["Player"].unique())

st.markdown('<div class="section-title"><h2>Find a player</h2><span>Filter → select → analyse</span></div>', unsafe_allow_html=True)

selected_player = st.selectbox(
    "Player",
    players,
    label_visibility="collapsed"
)

# Selected player row: respect season filter, otherwise use latest season.
player_rows = filtered_df[filtered_df["Player"] == selected_player].copy()
if player_rows.empty:
    player_rows = df[df["Player"] == selected_player].copy()

player_rows = player_rows.sort_values("Season")
player = player_rows.iloc[-1]

# -----------------------------
# QUICK DATASET STATS
# -----------------------------
q1, q2, q3, q4 = st.columns(4)
with q1:
    metric_card("Players in current view", f"{len(players):,}")
with q2:
    metric_card("Records in current view", f"{len(filtered_df):,}")
with q3:
    metric_card("Selected season", str(player["Season"]))
with q4:
    metric_card("Position", str(player["Position"]), accent=True)

# -----------------------------
# PLAYER HEADER — WOW PROFILE
# -----------------------------
st.markdown('<div class="section-title"><h2>Player Intelligence</h2><span>Scouting profile</span></div>', unsafe_allow_html=True)

club = str(player["Club"])
player_image = get_player_image(selected_player, club)
position = str(player["Position"])
age = int(player["Age"])
season = str(player["Season"])

if player_image:
    image_html = f'<img src="{player_image}" class="player-photo" alt="{selected_player}">'
else:
    image_html = f'<div class="player-photo-fallback">{initials(selected_player)}</div>'

st.markdown(
    f"""
    <div class="player-profile">
        <div class="profile-photo-wrap">{image_html}</div>
        <div class="profile-main">
            <div class="profile-eyebrow">PLAYER PROFILE</div>
            <div class="player-name">{selected_player}</div>
            <div class="player-meta">
                {club} <span class="dot">•</span> Age {age}
                <span class="dot">•</span> {season}
                <span class="position-badge">{position}</span>
            </div>
            <div class="profile-tags">
                <span>⚽ {int(player['Goals'])} goals</span>
                <span>🎯 {int(player['Assists'])} assists</span>
                <span>📈 {int(player['Goal_Contribution'])} contributions</span>
            </div>
        </div>
        <div class="profile-value">
            <div class="value-mini-label">MARKET VALUE</div>
            <div class="profile-price">{money_exact(float(player['Market_Value_EUR']))}</div>
            <div class="value-mini-label">OBSERVED VALUE</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# PREDICTION
# -----------------------------
prediction_input = pd.DataFrame({
    "Goal_Contribution": [player["Goal_Contribution"]],
    "Shot_Accuracy": [player["Shot_Accuracy"]],
    "Defensive_Contribution": [player["Defensive_Contribution"]],
    "Minutes_Per_Appearance": [player["Minutes_Per_Appearance"]],
    "Discipline_Score": [player["Discipline_Score"]],
    "Age": [player["Age"]],
})

position_data = position_encoder.transform([[player["Position"]]])
position_columns = position_encoder.classes_

for i, position in enumerate(position_columns):
    prediction_input[f"Position_{position}"] = position_data[0][i]

prediction_input = prediction_input.reindex(columns=model_features, fill_value=0)
predicted_value = float(model.predict(prediction_input)[0])
actual_value = float(player["Market_Value_EUR"])
value_gap = actual_value - predicted_value

# -----------------------------
# TABS
# -----------------------------
tab_overview, tab_value, tab_performance, tab_visuals, tab_history, tab_compare, tab_model = st.tabs([
    "Overview",
    "💰 Valuation",
    "📊 Performance",
    "📉 Visualizations",
    "📈 History",
    "⚔️ Compare",
    "🧠 Model"
])

# ============================================================
# OVERVIEW
# ============================================================
with tab_overview:
    st.markdown('<div class="section-title"><h2>Performance snapshot</h2><span>Core match metrics</span></div>', unsafe_allow_html=True)

    cols = st.columns(4)
    overview_metrics = [
        ("Goals", f"{int(player['Goals'])}"),
        ("Assists", f"{int(player['Assists'])}"),
        ("Goal contribution", f"{int(player['Goal_Contribution'])}"),
        ("Shot accuracy", f"{player['Shot_Accuracy']:.1f}%"),
    ]
    for col, (label, value) in zip(cols, overview_metrics):
        with col:
            metric_card(label, value, accent=True)

    cols = st.columns(3)
    overview_metrics_2 = [
        ("Defensive contribution", f"{int(player['Defensive_Contribution'])}"),
        ("Minutes / appearance", f"{player['Minutes_Per_Appearance']:.1f}"),
        ("Discipline score", f"{player['Discipline_Score']:.1f}"),
    ]
    for col, (label, value) in zip(cols, overview_metrics_2):
        with col:
            metric_card(label, value)

    st.markdown('<div class="section-title"><h2>At a glance</h2><span>Actual vs model estimate</span></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(
            f'<div class="value-card"><div class="value-label">Actual market value</div>'
            f'<div class="value-number">{money(actual_value)}</div>'
            f'<div class="value-sub">Observed value in the dataset</div></div>',
            unsafe_allow_html=True
        )
    with c2:
        st.markdown(
            f'<div class="value-card"><div class="value-label">WorthXI estimate</div>'
            f'<div class="value-number">{money(predicted_value)}</div>'
            f'<div class="value-sub">Linear Regression estimate</div></div>',
            unsafe_allow_html=True
        )
    with c3:
        direction = "above" if value_gap > 0 else "below" if value_gap < 0 else "aligned with"
        st.markdown(
            f'<div class="value-card"><div class="value-label">Model gap</div>'
            f'<div class="value-number">{money(abs(value_gap))}</div>'
            f'<div class="value-sub">Actual value is {direction} the estimate</div></div>',
            unsafe_allow_html=True
        )

    st.markdown(
        '<div class="insight"><b>WorthXI lens:</b> The estimate is generated from the performance '
        'features used by the trained model. It should be read as a statistical estimate, not a '
        'replacement for real-world transfer-market judgement.</div>',
        unsafe_allow_html=True
    )

# ============================================================
# VALUATION
# ============================================================
with tab_value:
    st.markdown('<div class="section-title"><h2>Market value intelligence</h2><span>Actual × predicted</span></div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        metric_card("Actual market value", money(actual_value), accent=True)
    with c2:
        metric_card("WorthXI estimated", money(predicted_value), accent=True)
    with c3:
        metric_card("Absolute gap", money(abs(value_gap)))

    if value_gap > 0:
        st.markdown(
            f'<div class="status-box status-good"><b>Actual value is higher than the model estimate.</b><br>'
            f'The observed market value exceeds the WorthXI estimate by <b>{money(value_gap)}</b>.</div>',
            unsafe_allow_html=True
        )
    elif value_gap < 0:
        st.markdown(
            f'<div class="status-box status-watch"><b>Model estimate is higher than the actual value.</b><br>'
            f'The WorthXI estimate exceeds the observed market value by <b>{money(abs(value_gap))}</b>.</div>',
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            '<div class="status-box status-neutral"><b>Values are approximately aligned.</b><br>'
            'The model estimate and observed market value are effectively equal.</div>',
            unsafe_allow_html=True
        )

    value_chart = pd.DataFrame({
        "Value": ["Actual Market Value", "WorthXI Estimate"],
        "Market Value (€M)": [actual_value/1e6, predicted_value/1e6]
    })

    fig = px.bar(
        value_chart,
        x="Value",
        y="Market Value (€M)",
        text="Market Value (€M)",
        title=f"{selected_player} · Value comparison",
    )
    fig.update_traces(
        texttemplate="€%{text:.1f}M",
        textposition="outside",
        marker_line_width=0
    )
    chart_layout(fig, 470)
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ============================================================
# PERFORMANCE
# ============================================================
with tab_performance:
    st.markdown('<div class="section-title"><h2>Performance profile</h2><span>Percentile vs dataset</span></div>', unsafe_allow_html=True)

    profile_metrics = {
        "Goal Contribution": "Goal_Contribution",
        "Shot Accuracy": "Shot_Accuracy",
        "Defensive Contribution": "Defensive_Contribution",
        "Minutes / Appearance": "Minutes_Per_Appearance",
        "Discipline Score": "Discipline_Score"
    }

    profile_values = []
    for display_name, column_name in profile_metrics.items():
        valid = df[column_name].dropna()
        rank_pct = valid.rank(pct=True) * 100
        matches = rank_pct[valid == player[column_name]]
        score = float(matches.mean()) if not matches.empty else 0.0
        profile_values.append((display_name, score, float(player[column_name])))

    profile_df = pd.DataFrame(profile_values, columns=["Metric", "Score", "Raw"])

    theta = profile_df["Metric"].tolist()
    values = profile_df["Score"].tolist()

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=values + [values[0]],
        theta=theta + [theta[0]],
        fill="toself",
        name="Percentile",
        hovertemplate="<b>%{theta}</b><br>Percentile: %{r:.1f}<extra></extra>"
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor="rgba(0,0,0,0)",
            radialaxis=dict(
                visible=True,
                range=[0,100],
                tickvals=[20,40,60,80,100],
                gridcolor="rgba(148,163,184,.12)",
                linecolor="rgba(148,163,184,.18)"
            ),
            angularaxis=dict(
                gridcolor="rgba(148,163,184,.10)",
                linecolor="rgba(148,163,184,.16)"
            )
        ),
        showlegend=False,
        title=f"{selected_player} · Performance percentile profile"
    )
    chart_layout(fig_radar, 610)
    st.plotly_chart(fig_radar, use_container_width=True, config={"displayModeBar": False})

    st.markdown('<div class="section-title"><h2>Metric breakdown</h2><span>Raw value + percentile</span></div>', unsafe_allow_html=True)

    breakdown = profile_df.copy()
    breakdown["Percentile"] = breakdown["Score"].map(lambda x: f"{x:.1f}%")
    breakdown["Raw Value"] = breakdown["Raw"].map(lambda x: f"{x:.1f}")
    st.dataframe(
        breakdown[["Metric", "Raw Value", "Percentile"]],
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '<div class="small-note">Percentiles compare the selected player with the complete player dataset. '
        'They describe relative standing, not causal impact on market value.</div>',
        unsafe_allow_html=True
    )

# ============================================================
# VISUALIZATIONS
# ============================================================
with tab_visuals:
    st.markdown(
        '<div class="section-title"><h2>Visual analytics</h2>'
        '<span>Explore the dataset from multiple angles</span></div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="insight"><b>Analytics lab:</b> These views use the full WorthXI '
        'dataset to reveal relationships between performance, age, position and market value. '
        'Use the hover tools to inspect individual observations.</div>',
        unsafe_allow_html=True
    )

    # 1. Performance vs market value
    scatter_df = df[[
        "Goal_Contribution", "Market_Value_EUR", "Position", "Age", "Player"
    ]].dropna().copy()
    scatter_df["Market Value (€M)"] = scatter_df["Market_Value_EUR"] / 1e6

    fig_scatter = px.scatter(
        scatter_df,
        x="Goal_Contribution",
        y="Market Value (€M)",
        size="Age",
        hover_name="Player",
        hover_data=["Position", "Age"],
        title="Goal contribution vs market value",
        opacity=0.65
    )
    fig_scatter.update_layout(
        xaxis_title="Goal contribution",
        yaxis_title="Market value (€M)"
    )
    chart_layout(fig_scatter, 500)
    st.plotly_chart(fig_scatter, use_container_width=True, config={"displayModeBar": False})

    # 2. Market value distribution
    st.markdown(
        '<div class="section-title"><h2>Market value distribution</h2>'
        '<span>How player values are spread</span></div>',
        unsafe_allow_html=True
    )
    dist_df = df[["Market_Value_EUR"]].dropna().copy()
    dist_df["Market Value (€M)"] = dist_df["Market_Value_EUR"] / 1e6

    fig_dist = px.histogram(
        dist_df,
        x="Market Value (€M)",
        nbins=35,
        title="Distribution of player market values"
    )
    fig_dist.update_layout(xaxis_title="Market value (€M)", yaxis_title="Player-season records")
    chart_layout(fig_dist, 430)
    st.plotly_chart(fig_dist, use_container_width=True, config={"displayModeBar": False})

    # 3. Market value by position
    st.markdown(
        '<div class="section-title"><h2>Value by position</h2>'
        '<span>Distribution across playing roles</span></div>',
        unsafe_allow_html=True
    )
    box_df = df[["Position", "Market_Value_EUR"]].dropna().copy()
    box_df["Market Value (€M)"] = box_df["Market_Value_EUR"] / 1e6

    fig_box = px.box(
        box_df,
        x="Position",
        y="Market Value (€M)",
        points=False,
        title="Market value distribution by position"
    )
    chart_layout(fig_box, 470)
    st.plotly_chart(fig_box, use_container_width=True, config={"displayModeBar": False})

    # 4. Age vs market value
    age_df = df[["Age", "Market_Value_EUR", "Player", "Position"]].dropna().copy()
    age_df["Market Value (€M)"] = age_df["Market_Value_EUR"] / 1e6

    fig_age = px.scatter(
        age_df,
        x="Age",
        y="Market Value (€M)",
        hover_name="Player",
        hover_data=["Position"],
        title="Age vs market value",
        opacity=0.55,
        trendline="ols"
    )
    fig_age.update_layout(xaxis_title="Age", yaxis_title="Market value (€M)")
    chart_layout(fig_age, 500)
    st.plotly_chart(fig_age, use_container_width=True, config={"displayModeBar": False})

    # 5. Average performance metrics by position
    st.markdown(
        '<div class="section-title"><h2>Performance by position</h2>'
        '<span>Average profile across the dataset</span></div>',
        unsafe_allow_html=True
    )
    pos_perf = df.groupby("Position", as_index=False)[[
        "Goals", "Assists", "Goal_Contribution",
        "Shot_Accuracy", "Defensive_Contribution"
    ]].mean()

    metric_choice = st.selectbox(
        "Choose a metric",
        ["Goals", "Assists", "Goal_Contribution", "Shot_Accuracy", "Defensive_Contribution"],
        key="visual_metric"
    )

    fig_pos = px.bar(
        pos_perf.sort_values(metric_choice, ascending=False),
        x="Position",
        y=metric_choice,
        text=metric_choice,
        title=f"Average {metric_choice.replace('_', ' ')} by position"
    )
    fig_pos.update_traces(texttemplate="%{text:.1f}", textposition="outside")
    chart_layout(fig_pos, 430)
    st.plotly_chart(fig_pos, use_container_width=True, config={"displayModeBar": False})

# ============================================================
# HISTORY
# ============================================================
with tab_history:
    history = get_player_history(selected_player)
    st.markdown('<div class="section-title"><h2>Career trajectory</h2><span>Available player-season records</span></div>', unsafe_allow_html=True)

    if len(history) >= 2:
        history = history.copy()
        history["WorthXI Estimate"] = history.apply(predict_row, axis=1)
        history["Market Value (€M)"] = history["Market_Value_EUR"] / 1e6
        history["WorthXI Estimate (€M)"] = history["WorthXI Estimate"] / 1e6

        hist = history[["Season", "Market Value (€M)", "WorthXI Estimate (€M)"]]

        fig_hist = go.Figure()
        fig_hist.add_trace(go.Scatter(
            x=hist["Season"], y=hist["Market Value (€M)"],
            mode="lines+markers", name="Actual market value",
            line=dict(width=3), marker=dict(size=7)
        ))
        fig_hist.add_trace(go.Scatter(
            x=hist["Season"], y=hist["WorthXI Estimate (€M)"],
            mode="lines+markers", name="WorthXI estimate",
            line=dict(width=3, dash="dot"), marker=dict(size=7)
        ))
        fig_hist.update_layout(title=f"{selected_player} · Market value trajectory")
        chart_layout(fig_hist, 500)
        st.plotly_chart(fig_hist, use_container_width=True, config={"displayModeBar": False})

        st.dataframe(
            history[[
                "Season", "Age", "Goals", "Assists",
                "Goal_Contribution", "Market_Value_EUR", "WorthXI Estimate"
            ]].rename(columns={
                "Market_Value_EUR": "Actual Value (€)",
                "WorthXI Estimate": "WorthXI Estimate (€)"
            }),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.markdown(
            '<div class="status-box status-neutral"><b>History is limited for this player.</b><br>'
            'The dataset contains only one player-season record matching this profile.</div>',
            unsafe_allow_html=True
        )

# ============================================================
# COMPARE
# ============================================================
with tab_compare:
    st.markdown('<div class="section-title"><h2>Head-to-head comparison</h2><span>Same dataset · same model lens</span></div>', unsafe_allow_html=True)

    compare_candidates = [p for p in players if p != selected_player]
    if compare_candidates:
        comparison_player = st.selectbox(
            "Compare with",
            compare_candidates,
            key="comparison_player"
        )
        other_rows = df[df["Player"] == comparison_player].sort_values("Season")
        other = other_rows.iloc[-1]

        other_pred = predict_row(other)
        other_actual = float(other["Market_Value_EUR"])

        left, right = st.columns(2)
        for col, name, row, pred, actual in [
            (left, selected_player, player, predicted_value, actual_value),
            (right, comparison_player, other, other_pred, other_actual)
        ]:
            with col:
                img = get_player_image(name, row.get("Club", "") if isinstance(row, pd.Series) else "")
                if img:
                    st.image(img, width=170)
                st.markdown(
                    f'<div class="compare-name">{name}</div>'
                    f'<div class="player-meta">{row["Club"]} · {row["Position"]} · Age {int(row["Age"])}</div>',
                    unsafe_allow_html=True
                )

        compare_metrics = pd.DataFrame({
            "Metric": [
                "Goals", "Assists", "Goal Contribution",
                "Shot Accuracy", "Defensive Contribution",
                "Minutes / Appearance", "Actual Value (€M)", "WorthXI (€M)"
            ],
            selected_player: [
                float(player["Goals"]), float(player["Assists"]), float(player["Goal_Contribution"]),
                float(player["Shot_Accuracy"]), float(player["Defensive_Contribution"]),
                float(player["Minutes_Per_Appearance"]), actual_value/1e6, predicted_value/1e6
            ],
            comparison_player: [
                float(other["Goals"]), float(other["Assists"]), float(other["Goal_Contribution"]),
                float(other["Shot_Accuracy"]), float(other["Defensive_Contribution"]),
                float(other["Minutes_Per_Appearance"]), other_actual/1e6, other_pred/1e6
            ]
        })
        st.dataframe(compare_metrics, use_container_width=True, hide_index=True)

        comp_chart = pd.DataFrame({
            "Metric": ["Goals", "Assists", "Goal Contribution", "Shot Accuracy"],
            selected_player: [
                float(player["Goals"]), float(player["Assists"]),
                float(player["Goal_Contribution"]), float(player["Shot_Accuracy"])
            ],
            comparison_player: [
                float(other["Goals"]), float(other["Assists"]),
                float(other["Goal_Contribution"]), float(other["Shot_Accuracy"])
            ]
        })
        fig_comp = px.bar(
            comp_chart, x="Metric", y=[selected_player, comparison_player],
            barmode="group", title="Performance comparison"
        )
        chart_layout(fig_comp, 450)
        st.plotly_chart(fig_comp, use_container_width=True, config={"displayModeBar": False})
    else:
        st.info("Choose a broader filter to compare this player with another player.")

# ============================================================
# MODEL
# ============================================================
with tab_model:
    st.markdown('<div class="section-title"><h2>Model intelligence</h2><span>Standardized feature influence</span></div>', unsafe_allow_html=True)

    numerical_features = [
        "Goal_Contribution",
        "Shot_Accuracy",
        "Defensive_Contribution",
        "Minutes_Per_Appearance",
        "Discipline_Score",
        "Age"
    ]

    position_lists = df["Position"].fillna("").str.split(",")
    position_columns = ["DF", "FW", "GK", "MF"]
    position_data_all = pd.DataFrame(index=df.index)

    for pos in position_columns:
        position_data_all[f"Position_{pos}"] = position_lists.apply(
            lambda x: int(pos in [i.strip() for i in x])
        )

    analysis_features = pd.concat(
        [df[numerical_features].copy(), position_data_all],
        axis=1
    )

    if hasattr(model, "feature_names_in_"):
        model_feature_names = list(model.feature_names_in_)
    else:
        model_feature_names = list(model_features)

    analysis_features = analysis_features[model_feature_names]
    feature_std = analysis_features.std()
    coefficients = pd.Series(model.coef_, index=model_feature_names)
    standardized_effect = coefficients * feature_std

    feature_analysis = pd.DataFrame({
        "Feature": model_feature_names,
        "Standardized Effect": standardized_effect
    })
    feature_analysis["Absolute Effect"] = feature_analysis["Standardized Effect"].abs()
    total_effect = feature_analysis["Absolute Effect"].sum()
    feature_analysis["Relative Influence"] = (
        feature_analysis["Absolute Effect"] / total_effect * 100
        if total_effect != 0 else 0
    )
    feature_analysis["Direction"] = np.where(
        feature_analysis["Standardized Effect"] >= 0, "Positive", "Negative"
    )

    feature_name_map = {
        "Goal_Contribution": "Goal Contribution",
        "Shot_Accuracy": "Shot Accuracy",
        "Defensive_Contribution": "Defensive Contribution",
        "Minutes_Per_Appearance": "Minutes / Appearance",
        "Discipline_Score": "Discipline Score",
        "Age": "Age",
        "Position_DF": "Position — DF",
        "Position_FW": "Position — FW",
        "Position_GK": "Position — GK",
        "Position_MF": "Position — MF"
    }

    feature_analysis["Feature"] = feature_analysis["Feature"].map(feature_name_map)
    feature_analysis = feature_analysis.sort_values("Relative Influence", ascending=True)

    fig_inf = px.bar(
        feature_analysis,
        x="Relative Influence",
        y="Feature",
        orientation="h",
        text="Relative Influence",
        title="Relative influence of modelling features",
    )
    fig_inf.update_traces(
        texttemplate="%{text:.1f}%",
        textposition="outside",
        marker_line_width=0
    )
    chart_layout(fig_inf, 570)
    fig_inf.update_xaxes(range=[0, max(10, feature_analysis["Relative Influence"].max()*1.25)])
    st.plotly_chart(fig_inf, use_container_width=True, config={"displayModeBar": False})

    display_influence = feature_analysis[["Feature","Relative Influence","Direction"]].copy()
    display_influence["Relative Influence"] = display_influence["Relative Influence"].map(lambda x: f"{x:.1f}%")
    st.dataframe(display_influence, use_container_width=True, hide_index=True)

    st.markdown(
        '<div class="insight"><b>How to read this:</b> Relative influence is calculated from '
        'standardized model effects so differently scaled features can be compared more fairly. '
        'It represents model behaviour and does not establish causation.</div>',
        unsafe_allow_html=True
    )

# -----------------------------
# FOOTER
# -----------------------------
st.markdown(
    '<div class="footer">WORTHXI · Football Player Performance × Market Value · '
    'Built with Python, Streamlit, Plotly and Machine Learning</div>',
    unsafe_allow_html=True
)
