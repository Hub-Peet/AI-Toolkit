# AI‑Transitie Toolkit (Streamlit)

Een praktische toolkit voor administratie- en belastingadvieskantoren om AI stapsgewijs te implementeren: diagnose → keuzeadvies → PoC → opschaling. Inclusief AI‑adviesgenerator (ChatGPT via OpenAI‑API) en export naar **Word (.docx)** en **Markdown (.md)**.

---

## 🚀 Snel starten (Windows)

1. Open **PowerShell** in je projectmap (bijv. `C:\Users\<jouwnaam>\AI-Toolkit`).
2. Voer éénmalig de setup uit (maakt venv, installeert packages, zet je API‑key):
   ```powershell
   .\setup.ps1
   ```
   > Tip: je kunt ook direct je sleutel meegeven en de app starten:
   ```powershell
   .\setup.ps1 -Key "sk-..." -Start
   ```
3. Volgende keren starten:
   ```powershell
   .\run.ps1
   ```

> **Melding over script‑policy?** Voer éénmalig uit:
>
> ```powershell
> Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
> ```

---

## 🧰 Handmatige installatie ( alternatief )

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt   # of: pip install streamlit openai python-docx
# API‑key instellen (kies 1 van 3):
# A) Tijdelijk voor huidig venster
$env:OPENAI_API_KEY = "sk-..."
# B) Permanent voor jouw account (nieuw venster openen!)
setx OPENAI_API_KEY "sk-..."
# C) Via secrets‑bestand (aanbevolen)
notepad .streamlit\secrets.toml   # voeg toe:  OPENAI_API_KEY = "sk-..."

# Start de app
streamlit run app.py
```

---

## 🔐 API‑key & secrets

De app zoekt je sleutel in deze volgorde:

1. `` → `OPENAI_API_KEY = "sk-..."`
2. **Omgevingsvariabele** → `OPENAI_API_KEY`

Op **Streamlit Cloud** zet je de sleutel in **Settings → Secrets** (geen bestanden nodig).

---

## 📁 Projectstructuur

```
AI-Toolkit/
├─ app.py                 # enige startfile van de app
├─ requirements.txt       # pakketten
├─ setup.ps1              # eenmalige setup (venv, deps, secrets)
├─ run.ps1                # snelle start (activeert venv en draait app)
├─ .streamlit/
│  └─ secrets.toml        # lokaal; NIET committen
├─ venv/                  # virtuele omgeving; in .gitignore
└─ archive/               # (optioneel) oudere prototypen
```

---

## 🖥️ Gebruik in de app

1. **Dashboard** → selecteer software, knelpunten en geef **weging (1–5)**.
2. **Keuzeadvies** → kies aanpak (*Zelf Doen / Laten Doen / Hybride*) en klik **Genereer Diagnose & Transitievoorstel (AI)**.
3. Exporteer advies als **.docx** of **.md**.

> Geen API‑key? Dan toont de app de samengestelde **prompt** als voorbeeld. Met key krijg je het volledige AI‑advies.

---

## ☁️ Deploy (Streamlit Cloud)

1. Push project naar **GitHub**.
2. In Streamlit Cloud: **New app** → kies je repo → `app.py`.
3. Zet in **Secrets**: `OPENAI_API_KEY = sk-...`.

---

## 🧪 Troubleshooting

- `` → installeer pakketten in de **actieve venv**: `venv\Scripts\activate` → `pip install -r requirements.txt`.
- **API‑key niet gevonden** → maak/controleer `.streamlit/secrets.toml` of gebruik `setx OPENAI_API_KEY ...` (nieuw venster openen).
- **Ziet oude app** → Stop vorige run (Ctrl+C), start opnieuw, doe een harde refresh (Ctrl+F5).
- **Word‑export ontbreekt** → installeer `python-docx` en start opnieuw: `pip install python-docx`.
- `` → zorg dat in `app.py` geen extra `}` staat in bestandsnamen of strings.

---

## 📦 Versies pinnen (optioneel)

In `requirements.txt` kun je vaste versies gebruiken:

```
streamlit==1.37.0
openai==1.42.0
python-docx==1.2.0
```

---

## 📄 Licentie & gebruik

- Gebruik op eigen risico. Controleer altijd exporten (compliance/AVG).
- Deel de app met klanten door hen hun **eigen API‑key** te laten instellen in `secrets.toml` of via Cloud‑Secrets.

Veel succes met jullie AI‑transitie! 🤝

