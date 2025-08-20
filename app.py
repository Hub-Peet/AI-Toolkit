
else:
    # Gratis/stub modus: toon de samengestelde opdracht i.p.v. AI-output
    _kn = st.session_state.get('knelpunten', [])
    _wg = st.session_state.get('weging', {})
    beschrijving = "\n".join([f"- {k} (weging {_wg.get(k, '—')})" for k in _kn]) if _kn else "- (geen geselecteerde knelpunten)"

    advies_tekst = (
        "🔒 AI staat uit of er is geen API-key.\n\n"
        f"**Software:** {st.session_state.get('software','—')}\n"
        f"**Knelpunten en weging:**\n{beschrijving}\n"
        f"**Toelichting:** {st.session_state.get('toelichting','—')}\n"
        f"**Voorkeursaanpak:** {st.session_state.get('voorkeur','Hybride')}\n\n"
        "Dit is de samengestelde opdracht (prompt) die normaal naar het model zou gaan."
    )
