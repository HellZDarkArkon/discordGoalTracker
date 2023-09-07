# config.py

#Bot token
with open("token.txt", "r") as token_file:
    BOT_TOKEN = token_file.read().strip()
BOT_SECRET = "Sx2MRIU1O5AxzIDrm_dHHbXB6S-MB-ye"
BOT_ID = "1147911186537517056"

#Bot command prefix
BOT_PREFIX = "/"

#API keys

BOT_KEY = "c5847989b340bd09fdcadcaaaf48f01b81cecfa22c13bdb4504b3a88bbdc41bb"

#PayPal tokens
PP_TOKEN = 'AU_7e1cE_5LGW3gb5Z2bVNO7fRFE28d-xXajndnkog7QTuv8_S0zOyjggYxIhAZ4PV0rJ7C5GF2gEsrm'
PP_SECRET = 'EI1Zx1ly_fC9B_hGda3KZDeymTncX-Al2SybwOS92Sg3Dphd68W7odoyP4X3m2ipxhS4mt3ttAQroLCX'
PP_EMAIL = " "

#Localization settings
DEFAULT_LANG = "en_us"
SUPPORTED_LANG = ["en_us", "en_gb", "es_cu", "jpn"]