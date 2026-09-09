from pathlib import Path
ROOT=Path(__file__).resolve().parent
ROLE_CREDS={}
for line in (ROOT/'DEMO_USER_CREDENTIALS.txt').read_text(encoding='utf-8').splitlines():
    if ' | ' not in line: continue
    parts=[x.strip() for x in line.split(' | ')]
    if len(parts)>=4:
        username,pin,display,role=parts[:4]
        ROLE_CREDS[role]=(username,pin)
def creds_for_role(role):
    if role not in ROLE_CREDS: raise KeyError(f'No individual synthetic validation account for role {role}')
    return ROLE_CREDS[role]
