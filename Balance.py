import requests
import json
import datetime
from bs4 import BeautifulSoup

def time():
    current_time = datetime.datetime.now()
    print(current_time.strftime("%I:%M:%S %p"))
time()

user_name = input("What is your school email? ")
#user_name = "Deron.mcguire@morehouse.edu"
#password = "Playstation8"
password = input("what is your password? ")
print("Logging in now...... ")
session = requests.session()
request_url = "https://morehouse.my.centrify.com/my?customerId=TH523%25252Fmyportaliwa"
post_url_1 = "https://morehouse.my.centrify.com/Security/StartAuthentication?antixss="
post_url_2 = "https://morehouse.my.centrify.com/Security/AdvanceAuthentication?antixss="
black_board_url = "https://blackboard.morehouse.edu/webapps/portal/execute/tabs/tabAction?tab_tab_group_id=_7_1"

session.get("https://morehouse.my.centrify.com/my?customerId=TH523%25252Fmyportaliwa")

antixss = session.cookies.get_dict()

ending = antixss.get("antixss")
ending_1 = str(ending)
new_ending = ending_1.replace('-', '')

login_user_data = {"TenantId": "th523%252fmyportaliwa",
"User": user_name,
"Version": "1.0",
"AssociatedEntityType": "Portal",
"AssociatedEntityName": "Portal",
"ExtIdpAuthChallengeState": "",
"ZsoSessionId": ""}


#Posts user name
user_name_login = session.post(post_url_1 + new_ending, data=json.dumps(login_user_data))

data = user_name_login.json()
session_id = data["Result"]["SessionId"]
mechanism_id = (data.get('Result', {}).get('Challenges', [{}])[0].get('Mechanisms', [{}])[0].get('MechanismId'))



login_pass_data = {"Action":"Answer",
"Answer":password,
"MechanismId": mechanism_id,
"PersistentLogin":"true",
"SessionId": session_id,
"TenantId": "TH523"}

#Posts password and logs in
password_login = session.post(post_url_2, data=json.dumps(login_pass_data))

name = password_login.json()
full_name = name["Result"]["DisplayName"]
print("Success! " + "Welcome to Morehouse College User Portal " + full_name)
print("Logging into Tiger Pay to view account......")


#Next step
#blackboard = session.get("black_board_url")

banner_key = "https://eis-prod.ec.morehouse.edu/cas/login?service=https%3A%2F%2Fssb-prod.ec.morehouse.edu%3A443%2Fssomanager%2Fc%2FSSB"
banner = session.get(banner_key)
soup = BeautifulSoup(banner.text, "html.parser")

tag_key = soup.find('input', {"name":"sessionDataKey"})
tag = tag_key["value"]


banner_web = "https://eis-prod.ec.morehouse.edu/authenticationendpoint/login.do?commonAuthCallerPath=%252Fcas%252Flogin&forceAuth=false&passiveAuth=false&tenantDomain=carbon.super&sessionDataKey=" +tag+ "&relyingParty=SSB_SSO&type=cassso&sp=SSB_SSO&isSaaSApp=false&authenticators=BasicAuthenticator:LOCAL"

banner_get = session.get(banner_web)

banner_user = input("What is your Banner Web user name? ")
banner_pass = input("What is your password? ")
print("Logging you into Banner Web......")

print("Here are the details of your student account: ")

banner_data = {"username":banner_user,
"password": banner_pass,
"sessionDataKey":tag}


banner_site = "https://eis-prod.ec.morehouse.edu/commonauth"
banner_login = session.post(banner_site, data=banner_data)

web_banner = session.get("https://ssb-prod.ec.morehouse.edu/MC/twbkwbis.P_GenMenu?name=bmenu.P_MainMnu")

#tiger_pay_url = "https://commerce.cashnet.com/cashnetg/selfserve/ebilllogin.aspx?client=MOREHOUSE_PROD&eusername=ecbc0219924e19cdc34fb5049719a15093cbeb7d2af3c1f502da77384a6abff3"
tiger_pay_url = "https://ssb-prod.ec.morehouse.edu/MC/CASHNet_sso.p_CASHNet_login"
tiger_pay = session.get(tiger_pay_url)

soup_2 = BeautifulSoup(tiger_pay.text, "html.parser")

tag_numb = soup_2.find("div", class_="title2")

numb = tag_numb.find_all("tr")

prev_bal = numb[0].text
current_bal = numb[1].text
current_aid = numb[2].text
total_amount = numb[6].text


print(prev_bal)
print(current_bal)
print(current_aid)
print(total_amount)
