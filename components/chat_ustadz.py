import streamlit as st
from urllib.parse import quote_plus

NAMA_USTADZ_1 = "Dr. Heri Iskandar, M.Pd"
NAMA_USTADZ_2 = "Sawi Sujarwo, M.Psi"

WA_LINK_1 = "+6289675674860"
WA_LINK_2 = "62xxxxxxxxxx"

DEFAULT_MESSAGE = (
    "Assalamu'alaikum Ustadz, saya ingin bertanya: "
)

# ---------------- util ----------------
def _normalize_wa_base(raw: str) -> str:
    if not raw:
        return ""
    raw = raw.strip()
    if raw.startswith("http://") or raw.startswith("https://"):
        return raw
    digits = ''.join(ch for ch in raw if ch.isdigit())
    if not digits:
        return ""
    return f"https://wa.me/{digits}"

def _with_prefill_message(base_url: str, message: str) -> str:
    if not base_url:
        return ""
    sep = '&' if ('?' in base_url) else '?'
    return f"{base_url}{sep}text={quote_plus(message or '')}"

# ---------------- card ustadz ----------------
def _ustadz_card(nama: str, wa_raw: str, key_prefix: str):
    base = _normalize_wa_base(wa_raw)

    with st.container(border=True):
        st.subheader(nama)
        msg = st.text_area(
            "Tulis pesan (akan diprefill di WhatsApp):",
            value=DEFAULT_MESSAGE,
            key=f"msg_{key_prefix}",
            height=120,
        )

        link = _with_prefill_message(base, msg)
        disabled = not bool(link)
        try:
            st.link_button(
                "💬 Chat via WhatsApp",
                link if link else "#",
                use_container_width=True,
                disabled=disabled
            )
        except Exception:
            if disabled:
                st.button("💬 Chat via WhatsApp (isi nomor dulu)", disabled=True, use_container_width=True)
            else:
                st.markdown(f"[💬 Chat via WhatsApp]({link})", unsafe_allow_html=True)

# ---------------- main tab ----------------
def show_chat_ustadz_tab():
    st.title("📞 Chat Ustadz")
    st.caption(
        "Tulis pesan lalu klik tombol untuk membuka WhatsApp. \n"
        "Catatan: aplikasi ini *tidak* mengirim pesan otomatis; tombol hanya membuka WA dengan pesan terisi."
    )

    _ustadz_card(NAMA_USTADZ_1, WA_LINK_1, key_prefix="u1")
    st.markdown("---")
    _ustadz_card(NAMA_USTADZ_2, WA_LINK_2, key_prefix="u2")
