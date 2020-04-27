from twilio.rest import Client
import psycopg2
import subprocess


class Otp:
    # Twilio
    account_sid = "ACbd973a9fe06825ec2d3e27c06faf2346"
    auth_token = "52c72851ddd5365221d912a2d15159de"
    client = Client(account_sid, auth_token)
    service = client.verify.services('VA2bf14ed0efa4f4d15714fa5edfdaf0d7')

    def __init__(self, userpk, phonepk):
        conn = psycopg2.connect(
            user="admin",
            password="covid19",
            host="127.0.0.1",
            port="5432",
            database="covid19"
        )
        cursor = conn.cursor()

        query = "select * from auth_user where id = " + str(userpk)
        cursor.execute(query)
        records = cursor.fetchall()
        self.user = records[0][4]

        query = "select * from c19_server_userphone where owner_id = " + str(userpk) + " and id = " + str(phonepk)
        cursor.execute(query)
        records = cursor.fetchall()
        self.phone_number = records[0][2]

        cursor.close()
        conn.close()

    def send(self):
        verification = self.service.verifications.create(to=self.phone_number, channel='sms')

    def verify(self, otp):
        verification_check = self.service.verification_checks.create(to=self.phone_number, code=str(otp))
        if verification_check.status == 'approved':
            pr = subprocess.Popen(
                ['python', 'manage.py', 'drf_create_token', self.user, '-r'],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            out = pr.communicate()[0].decode().split(' ')[2]
            return out
        else:
            return 'gagal'
