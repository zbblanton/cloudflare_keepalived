'''
TODO:
-Add checks to every API call on, check if success is true, if not email the error.
-Move auth_email, api_key, and zone_id to an init method to make script more modular.
'''

import os
import requests

cloudflare_api_key = ''
cloudflare_email = ''
cloudflare_domain = ''
cloudflare_zone_id = ''

sendmail_api_key = ''
sendmail_mail_to = ''
sendmail_mail_from = ''

ip_list = ['1.1.1.1','2.2.2.2','3.3.3.3']

#Send mail using sendgrid API
def send_mail(mail_to, mail_from, mail_subject, mail_content):
    api_key = sendmail_api_key
    json_data={
      "personalizations": [
        {
          "to": [
            {
              "email": mail_to
            }
          ],
          "subject": mail_subject
        }
      ],
      "from": {
        "email": mail_from
      },
      "content": [
        {
          "type": "text/plain",
          "value": mail_content
        }
      ]
    }
    api_url = 'https://api.sendgrid.com/v3/mail/send'
    header_info = {"Authorization": "Bearer " + api_key, "Content-type": "application/json"}
    ret = requests.post(api_url,headers=header_info,json=json_data)
    return

#CLoudflare API
class Cloudflare_api:
    auth_email = cloudflare_email
    api_base_url = 'https://api.cloudflare.com/client/v4/zones/'
    api_key = cloudflare_api_key
    zone_id = cloudflare_zone_id
    header_info = {"X-Auth-Email": auth_email, "X-Auth-Key": api_key, "Content-type": "application/json"}

    def dns_list(self, dns_record_name):
        api_url = Cloudflare_api.api_base_url + Cloudflare_api.zone_id + '/dns_records?type=A&name=' + dns_record_name    
        ret = requests.get(api_url,headers=Cloudflare_api.header_info)
        return ret.json()

    def dns_delete(self, dns_id):
        api_url = Cloudflare_api.api_base_url + Cloudflare_api.zone_id + '/dns_records/' + dns_id    
        ret = requests.delete(api_url,headers=Cloudflare_api.header_info)
        return ret.json()

    def dns_add(self, dns_record_name, dns_record_ip):
        api_url = Cloudflare_api.api_base_url + Cloudflare_api.zone_id + '/dns_records'
        post_data = {'type':'A','name':dns_record_name,'content':dns_record_ip,'ttl':'1','proxied':True}
        ret = requests.post(api_url,headers=Cloudflare_api.header_info,json=post_data)
        return ret.json()

cf_api = Cloudflare_api()
dns_list_json = cf_api.dns_list(cloudflare_domain)


dns_list = []
for i in range(0, dns_list_json['result_info']['count']):
    dns_list.append(dns_list_json['result'][i]['content'])


for i in range(len(ip_list)):
 if os.name == 'nt': #Windows
     response = os.system("ping -n 1 " + ip_list[i]) 
 else: #Linux
     response = os.system("ping -c 3 -W 3 " + ip_list[i])
     
 if response == 0:
  #Check if api dns list contains this ip, if not add it back to dns, the server should be back up, send an email
  if ip_list[i] not in dns_list:
      cf_api.dns_add(cloudflare_domain, ip_list[i])
      send_mail(sendmail_mail_to, sendmail_mail_from, 'Server up: ' + ip_list[i], ip_list[i] + ' is up and has been added to DNS')        
 else:
  #Check if api dns list contains this ip, if it does, remove it, the server is down, send an email
  if ip_list[i] in dns_list:
      cf_api.dns_delete(dns_list_json['result'][dns_list.index(ip_list[i])]['id'])
      send_mail(sendmail_mail_to, sendmail_mail_from, 'Server down: ' + ip_list[i], ip_list[i] + ' is down and has been removed from DNS')     

