import os
import requests
from dotenv import load_dotenv

load_dotenv()

def send_mail(email: str, med: str, doc: str):
    r = requests.post(
		f"https://api.mailgun.net/v3/{os.getenv('MAILGUN_DOMAIN')}/messages",
		auth=("api", os.getenv("MAILGUN_API")),
		data={"from": os.getenv("MAILGUN_ADDRESS"),
			"to": [email],
			"subject": f"DTCM 處方 - {doc}醫師",
			"text": f"""
以下為您的處方：
{med}
開立者：{doc}醫師
本信由系統自動發送，請勿回覆。
"""},
			timeout=5
        )
    print("Mail sent successfully to " + email + ".")
    return r
