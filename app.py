import os
import io
import math
import platform
from datetime import datetime
import streamlit as st

# Page config
st.set_page_config(page_title="AI-Transitie Toolkit", layout="wide")

# --- (Optioneel) OpenAI client ---
try:
    from openai import OpenAI
    _OPENAI_AVAILABLE = True
except Exception:
    _OPENAI_AVAILABLE = False

# --- (Optioneel) DOCX export ---
try:
    from docx import Document
    from docx.shared import Pt
    _DOCX_AVAILABLE = True
except Exception:
    _DOCX_AVAILABLE = False

# ========= Helpers =========
def approx_tokens(txt: str) -> int:
    if not txt:
        return 0
    return max(1, math.ceil(len(txt) / 4))

def make_docx_bytes(title: str, body_md: str) -> bytes:
    doc = Document()
    _ = doc.add_heading(title, level=1)
    for line in body_md.split("\n"):
        p = doc.add_paragraph()
        run = p.add_run(line)
        run.font.size = Pt(11)
    bio = io.BytesIO()
    doc.save(bio)
    bio.seek(0)
    return bio.read()

def get_openai_api_key() -> str | None:
    try:
        return st.secrets['OPENAI_API_KEY'] if 'OPENAI_API_KEY' in st.secrets else os.environ.get("OPENAI_API_KEY")
    except Exception:
        return os.environ.get("OPENAI_API_KEY")

def status_badge(ok: bool) -> str:
    return "✅" if ok else "⚠️"

def genereer_ai_advies(software, knelpunten, weging, toelichting, voorkeur, model: str, temperature: float = 0.4):
    punten = [f"- {k} (weging {weging.get(k, 3)})" for k in knelpunten]
    beschrijving = "\n".join(punten) if punten else "- (geen geselecteerde knelpunten)"
    system_msg = ("Je bent een nuchtere AI-implementatiecoach voor administratie- en belastingadvieskantoren. "
                  "Geef concrete, korte adviezen in duidelijk Nederlands; vermijd jargon; toon stappen en quick wins; "
                  "wees specifiek per software en knelpunt. Voeg indien relevant risico's en mitigaties toe.")
    user_msg = f"""
Kantoorsoftware: {software}
Knelpunten en weging:\n{beschrijving}
Toelichting: {toelichting or 'n.v.t.'}
Voorkeursaanpak: {voorkeur}

Maak een voorstel met:
1) Diagnose: analyse van de huidige situatie
2) Top 3 quick wins (met inschatting tijd/impact)
3) Aanpak per fase (diagnose, PoC, opschaling) met concrete acties
4) Benodigde tooling (heel concreet)
5) Indicatieve tijdslijn (weken) en betrokken rollen
6) Risico's + mitigatie
7) Heldere vervolgstap en call-to-action voor de klant
"""
    api_key = get_openai_api_key()
    if not _OPENAI_AVAILABLE or not api_key:
        return f"⚠️ Geen OpenAI-API geconfigureerd.\n\n**Systeemrol**:\n{system_msg}\n\n**Gebruikersinvoer**:\n{user_msg.strip()}"
    try:
        client = OpenAI(api_key=api_key)
        resp = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": system_msg}, {"role": "user", "content": user_msg}],
            temperature=temperature,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"❌ Fout bij genereren van advies ({type(e).__name__}): {e}"

# Sidebar instellingen
st.sidebar.title("AI-Transitie Toolkit")
menu = st.sidebar.radio("Navigatie", ["Dashboard", "Keuzeadvies", "Transitieplanner", "Proof-of-Concepts", "Feedback", "Handleiding"])

with st.sidebar.expander("Model & instellingen", expanded=False):
    model = st.selectbox("Model", ["gpt-4o-mini", "gpt-4o"], index=0)
    temperature = st.slider("Creativiteit (temperature)", 0.0, 1.0, 0.4, 0.1)

# Pagina: Dashboard
if menu == "Dashboard":
    st.title("AI-Transitie Toolkit voor Administratiekantoren")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Huidige Software en Knelpunten")
        software = st.selectbox("Selecteer software", ["Exact", "Nextens", "SnelStart", "AFAS", "Twinfield", "Multivers", "Minox", "Anders"])
        if software == "Anders":
            software = st.text_input("Voer de naam in van de gebruikte software")

        alle_knelpunten = [
            "Handmatig werk", "Trage communicatie", "Foutgevoeligheid", "Gebrekkig overzicht",
            "Duplicatie van gegevens", "Moeizame rapportages", "Veel tijd kwijt aan controles",
            "Onvoldoende koppelingen met andere software", "Compliance risico's",
        ]
        knelpunten = st.multiselect("Selecteer knelpunten", alle_knelpunten)
        toelichting = st.text_area("Toelichting of andere knelpunten")

        st.subheader("Weging van de problemen (1 = klein, 5 = groot)")
        probleemweging = {k: st.slider(f"Weging voor: {k}", 1, 5, 3) for k in knelpunten}

        if st.button("Advies voorbereiden"):
            st.session_state['software'] = software
            st.session_state['knelpunten'] = knelpunten
            st.session_state['toelichting'] = toelichting
            st.session_state['weging'] = probleemweging
            st.success("Invoer opgeslagen. Ga naar 'Keuzeadvies' om het voorstel te genereren.")

    with col2:
        st.subheader("AI-Oplossingen en Voorbeelden")
        st.markdown("""
        - **API-koppelingen** voor geautomatiseerde data-uitwisseling
        - **ChatGPT** voor diagnose en advies op maat
        - **OCR & RPA** voor documentverwerking en automatisering
        - **Zapier of Make** voor workflow-automatisering
        """)

        st.subheader("Invoerstatus")
        st.write("Software:", st.session_state.get('software', '—'))
        st.write("Knelpunten:", ", ".join(st.session_state.get('knelpunten', [])) or "—")
        st.write("Toelichting:", st.session_state.get('toelichting', '—') or "—")
        weging_dict = st.session_state.get('weging', {})
        if weging_dict:
            for k, v in weging_dict.items():
                st.write(f"{k}: {v}")
        else:
            st.write("Weging: —")
