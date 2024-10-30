'''Used third party if email is real or not'''
import requests

def verfy_mail(email):
     if outlook_classfication(email) == 'outlook':
          return True
     elif outlook_classfication(email) == 'gmail':
          return  verify_email_hunter(email)
     else:
          return  False

def verify_email_hunter(email):
        api_key = "1a667a59ddba2ddb85debf8d388418c6eb07b2b0"  # Replace with your Hunter.io API key
        url = f"https://api.hunter.io/v2/email-verifier?email={email}&api_key={api_key}"
        response = requests.get(url)
        data = response.json()
        
        # Check if the result is 'deliverable'
        return data['data']['result'] == "deliverable"

def outlook_classfication(email):
    try:
        local_part, domain_part = email.split('@')
        if domain_part == 'outlook.com':
           return 'outlook'
        else:
            return 'gmail'
    except ValueError:
        return False