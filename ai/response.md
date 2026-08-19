### FILE: routes/auth.py [PATCH]
### REPLACE
    if whatsapp == ADMIN_WHATSAPP and code == ADMIN_CODE:
### WITH
    if whatsapp == normalize_whatsapp(ADMIN_WHATSAPP) and code == ADMIN_CODE:
### END FILE