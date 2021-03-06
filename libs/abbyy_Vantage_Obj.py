import requests
import sys
import time

class Abbyy_Vantage_Obj:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.accessToken = ""
        self.skills = ""

    def requestToken(self):

        if not self.accessToken:
            data = {"grant_type":"password", 
                    "scope":"openid permissions", 
                    "username":f"{self.username}", 
                    "password":f"{self.password}", 
                    "client_id":"ABBYY.Vantage", 
                    "client_secret":"f3ec6136-6ccc-75a1-3780-caeef723e998"}
            
            r = requests.post("https://vantage-us.abbyy.com/auth/connect/token", data=data)
            
            if (r.status_code == 200):
                a = r.json()
                self.accessToken = a["access_token"]
        
        # return(self.accessToken)

    def getSkills(self):

        headers = {"Authorization": f"Bearer {self.accessToken}"}

        if not (self.skills):

            r = requests.get("https://vantage-us.abbyy.com/api/publicapi/v1/skills", headers=headers)

            if r.status_code == 200:
                a = r.json()
                self.skills = a
        
        return(self.skills)

    def transaction(self, skillId, fileToRead):

        headers = {"accept":"text/plain", "Authorization": f"Bearer {self.accessToken}"}

        files = {
            "Files": open(fileToRead, 'rb')
        }


        r = requests.post(f"https://vantage-us.abbyy.com/api/publicapi/v1/transactions/launch?skillId={skillId}", headers=headers, files=files)
        a = r.json()
        print(a)
        transactionId = a["transactionId"]

        status = ""
        fileId = ""

        headers = {"Authorization": f"Bearer {self.accessToken}"}

        while not (status == "Processed"):

            
            r = requests.get(f"https://vantage-us.abbyy.com/api/publicapi/v1/transactions/{transactionId}", headers=headers)
            a = r.json()
            status = a["status"]

            time.sleep(5)

        fileId = a["documents"][0]["resultFiles"][0]["fileId"]

        r = requests.get(f"https://vantage-us.abbyy.com/api/publicapi/v1/transactions/{transactionId}/files/{fileId}/download", headers=headers)

        lastResult = r.content.decode()
        return (lastResult)

