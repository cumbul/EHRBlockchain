# app.py
#!bin/python
# to run truffle migrate after opening Ganache UI
# to run in development FLASK_APP=main.py FLASK_ENV=development flask run
# to run with ssl -->

from flask import Flask, request, render_template, redirect
from model import AuditRegForm, AuditActions
from model import PatientRegForm, PatientActions
from model import LogForm
from flask_bootstrap import Bootstrap
import hashlib
import pandas as pd
import cryptography
from cryptography.fernet import Fernet
from datetime import datetime
from dateutil import parser
import clipboard

from web3 import Web3
import json

# install ganache using https://www.trufflesuite.com/ganache

# connect to ganache
ganache_url = "HTTP://127.0.0.1:7545"
# pass in http url
web3 = Web3(Web3.HTTPProvider(ganache_url))
print("Web3 is connected = " + str(web3.isConnected()))

# connect to remix
f = open('abi.json',)
abi = json.load(f)
f = open('bytecode.json',)
bytecode = json.load(f)['object']
contract = web3.eth.contract(abi=abi, bytecode=bytecode)

# default account to send money from default account in each user creation
# account_def = "0xa39c1505c345cc50C19924861659BbB242B9F6d8"
# pk_def = "f1f6e43d6e69d645805581739225db9e256377745fde1041aabf2e3357621386"

app = Flask(__name__)
app.config.from_mapping(
    SECRET_KEY=b'\xd6\x04\xbdj\xfe\xed$c\x1e@\xad\x0f\x13,@G')
Bootstrap(app)
# Encryption of authorization data
# Generate once use all time
#enc_key = Fernet.generate_key()
# get key
file = open('data/enc_key.key', 'rb') # rb = read bytes
enc_key  = file.read()
file.close()
fernet = Fernet(enc_key)

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
global count_acc
@app.route('/patientreg', methods=['GET', 'POST'])
def patient_registration():
    form = PatientRegForm(request.form)
    global count_acc
    if request.method == 'POST' and form.validate_on_submit():
        ################## CREATE GANACHE ACCOUNT #################
#                 #get nonce of default account
#                 nonce = web3.eth.getTransactionCount(account_def)
#
#                 # create ganache accounts
#                 account= web3.eth.account.create()
#                 account_num = account.address
#                 account_pk = account.privateKey
#                 print("new account created: " +  str(account_num))
#
#                 #build a transaction
#                 tx = {
#                     'nonce': nonce,
#                     'to': account_num,
#                     'value': web3.toWei(1, 'ether'),
#                     'gas': 2000000,
#                     'gasPrice': web3.toWei('50', 'gwei'),
#                 }
#
#                 #sign transaction
#                 signed_tx = web3.eth.account.signTransaction(tx, pk_def)
#
#                 #send transaction
#                 tx_hash = web3.eth.sendRawTransaction(signed_tx.rawTransaction)
#
#                 print("new account balance: " + str(web3.eth.getBalance(str(account_num))))

        ###################### USE EXITING GANACHE ACCOUNT ###################################
            try:
                account_num= web3.eth.accounts[int(form.account_number.data)]
            except:
                print("Account number failed")
        ###################### RECORD ACCOUNT DETAILS TO A FILE ##############################
            fname = hashlib.sha224(b"signin_data").hexdigest()
            f = open("data/"+fname+".csv", "a")
            pass_hash = hashlib.sha224(bytes("loremipsum"+form.password.data,encoding='utf-8')).hexdigest()
            encrypted_data = "patient" + ", " + str(fernet.encrypt(bytes("patient",encoding='utf-8'))) + ", " +\
                    str(fernet.encrypt(bytes(form.name_first.data,encoding='utf-8'))) + ", " +\
                    str(fernet.encrypt(bytes(form.name_last.data,encoding='utf-8'))) + ", " +\
                    str(fernet.encrypt(bytes(form.email.data,encoding='utf-8')))  + ", " +\
                    str(fernet.encrypt(bytes(form.phone.data,encoding='utf-8')))  + ", " +\
                    str(fernet.encrypt(bytes(form.city.data,encoding='utf-8')))  + ", " +\
                    str(fernet.encrypt(bytes(form.zip_code.data,encoding='utf-8')))  + ", " +\
                    str(fernet.encrypt(bytes(form.insurance.data,encoding='utf-8')))  + ", " +\
                    str(fernet.encrypt(bytes(pass_hash,encoding='utf-8'))) + "\n"
            f.write(encrypted_data)
            f.close()

            ################## CONSTRUCTOR OF SMART CONTRACT -- DEPLOY #############################
            try:
                web3.eth.defaultAccount = account_num
            except:
                print("Account number failed")
            #construct
            tx_hash = contract.constructor(str(form.name_first.data),str(form.name_last.data),str(form.insurance.data),"bdate", str(form.email.data),str(form.phone.data),str(form.zip_code),str(form.city.data),"ekey").transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

            username = form.name_first.data + " " + form.name_last.data
            address = account_num
            pk = "no need for demo but will be sent in actual app as email"
            result = "We have emailed you a key pair and contract address! "+"\nNormally it will be emailed using emailing API:"
            patient_qr = "https://api.qrserver.com/v1/create-qr-code/?data="+ str(account_num) +"&size=150x150"
            return render_template('result.html', result=result, username = username, address = address, pk=pk, tx_hash = tx_hash.hex(), tx_receipt = tx_receipt,audit_qr=patient_qr)
    return render_template('patientreg.html', form=form)

@app.route('/auditreg', methods=['GET', 'POST'])
def audit_registration():
    form = AuditRegForm(request.form)
    global account_num
    account_num = 0
    if request.method == 'POST' and form.validate_on_submit():
        try:
            account_num= web3.eth.accounts[int(form.account_number.data)]
        except:
             print("Account number failed")
        fname = hashlib.sha224(b"signin_data").hexdigest()
        f = open("data/"+fname+".csv", "a")
        pass_hash = hashlib.sha224(bytes("loremipsum"+form.password.data,encoding='utf-8')).hexdigest()
        encrypted_data = "audit" + ", " +str(fernet.encrypt(bytes("audit",encoding='utf-8'))) + ", " +\
                str(fernet.encrypt(bytes(form.name_first.data,encoding='utf-8'))) + ", " +\
                str(fernet.encrypt(bytes(form.name_last.data,encoding='utf-8'))) + ", " +\
                str(fernet.encrypt(bytes(form.email.data,encoding='utf-8')))  + ", " +\
                str(fernet.encrypt(bytes(form.employee_id.data,encoding='utf-8')))  + ", " +\
                str(fernet.encrypt(bytes("n/a",encoding='utf-8')))  + ", " +\
                str(fernet.encrypt(bytes("00008",encoding='utf-8')))  + ", " +\
                str(fernet.encrypt(bytes("0000000000",encoding='utf-8')))  + ", " +\
                str(fernet.encrypt(bytes(pass_hash,encoding='utf-8'))) + "\n"
        f.write(encrypted_data)
        f.close()
        username = form.name_first.data + " " + form.name_last.data
        address = account_num
        pk = "no need for demo but will be sent in actual app as email"
        result = "We have emailed you a key pair! "+"\nNormally it will be emailed using emailing API:"
        audit_qr = "https://api.qrserver.com/v1/create-qr-code/?data="+ str(account_num) +"&size=150x150"
        return render_template('result.html', result=result, username = username, address = address, pk=pk, tx_hash =0, tx_receipt=0, audit_qr=audit_qr)
    return render_template('auditreg.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    fname = hashlib.sha224(b"signin_data").hexdigest()
    form = LogForm(request.form)
    form2 = PatientActions(request.form)
    form3 = AuditActions(request.form)
    address = form.user_name.data
    encrypt_address = fernet.encrypt(bytes(address,encoding='utf-8'))
    hashed_pass = hashlib.sha224(bytes("loremipsum"+form.password.data,encoding='utf-8')).hexdigest()
    hashed_ecrypt_pass = fernet.encrypt(bytes(hashed_pass,encoding='utf-8'))
    if request.method == 'POST' and form.validate_on_submit():
        df=pd.read_csv("data/"+fname+".csv")
        row = df.loc[df['address'] == str(encrypt_address)]
        if(row[password] == str(hashed_pass)):
#         if form.password.data != '':
            error = 'Invalid Credentials. Please try again.'
        else:
            if str(form.contract_address.data) != "0":
                return redirect('patient?'+"address=" + str(form.user_name.data) + "&contract=" + str(form.contract_address.data) )
            else:
                return redirect('audit?'+ "address=" + form.user_name.data + "&contract=0")
    return render_template('login.html', form=form, error=error)

@app.route('/patient', methods=['GET', 'POST'])
def patientdash():
    form = PatientActions(request.form)
    account_address  = request.args.get("address")
    contract_address = request.args.get("contract")
    isCard = False
    if request.method == 'POST':
        if request.form.get('action1') == 'VALUE1':
            isCard  = True
            appointment_date = form.start_visit.data
            result = "Patient initiated visit."


            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            date_obj = parser.parse(form.start_visit.data)
            date_epoch = date_obj.timestamp()
            tx_hash  = contract.functions.start_visit(int(date_epoch)).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_start_visit.getLogs()
            qr_code = "https://api.qrserver.com/v1/create-qr-code/?data="+event_logs[0]['args']['record_unique_id']+"&size=150x150"
#             changes = filter.get_new_entries()
            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")
#             print(tx_receipt)
#             contract.functions.record_mapping()
            ################## End Solidity TRansaction ###############
            ###################### ENCRYPT & RECORD ACCOUNT DETAILS TO A FILE ##############################
            fname = hashlib.sha224(b"uniqueid_data").hexdigest()
            f = open("data/"+fname+".csv", "a")
            encrypted_data = str(fernet.encrypt(bytes(contract_address,encoding='utf-8')))\
            +","+str(fernet.encrypt(bytes(event_logs[0]['args']['record_unique_id'],encoding='utf-8')))+"\n"
            f.write(encrypted_data)
            f.close()
            ###################### END RECORD ACCOUNT DETAILS TO A FILE ########################

            return render_template("patient.html", form=form, isStart = True, isCard  = isCard, username=account_address,contract_address=contract_address, date = appointment_date, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs, qr_code=qr_code)
        elif  request.form.get('action2') == 'VALUE2':
            isCard  = True
            dr_id = form.add_doctors.data
            result = "Patient added a doctor to audit their medical records."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.addDoctors(dr_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_add_doctor.getLogs()
#             changes = filter.get_new_entries()
            print("--------------------changes-------------")
            print(event_logs[0]['args']['return_msg'])
            print("--------------------end changes-------------")
#             print(tx_receipt)
#             contract.functions.record_mapping()
            ################## End Solidity TRansaction ###############
            return render_template("patient.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs)
        elif  request.form.get('action3') == 'VALUE3':
            isCard  = True
            dr_id = form.remove_doctors.data
            result = "Patient removed a doctor to audit their medical records."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.removeDoctors(dr_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_remove_doctor.getLogs()
#             changes = filter.get_new_entries()
            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")
#             print(tx_receipt)
#             contract.functions.record_mapping()
            ################## End Solidity TRansaction ###############
            return render_template("patient.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs)
        elif  request.form.get('action4') == 'VALUE4':
            isCard  = True
            audit_id = form.add_audits.data
            result = "Patient added an audit to view/change their medical records."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.addAudit(audit_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_add_audit.getLogs()

            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")

            ################## End Solidity TRansaction ###############
            return render_template("patient.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs)

        elif  request.form.get('action5') == 'VALUE5':
            isCard  = True
            audit_id = form.remove_audits.data
            result = "Patient removed an audit to prohibit view/change their medical records."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.removeAudit(audit_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_remove_audit.getLogs()

            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")

            ################## End Solidity TRansaction ###############
            return render_template("patient.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs)


        elif  request.form.get('action6') == 'VALUE6':
            isCard  = True
            unique_id = form.print_record.data
            unique_id = unique_id.lower()
            unique_id = Web3.toChecksumAddress(unique_id)
            result = "Patient printed their medical records."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.print_record(unique_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_patient_print.getLogs()
            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")

            # get medical record details
            record_details  = contract.functions.get_record_details(unique_id).call()
            print(record_details)

            ################## End Solidity TRansaction ###############
            return render_template("patient.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs, record_details = record_details)

        elif  request.form.get('action7') == 'VALUE7':
            isCard  = True
            unique_id = form.delete_record.data
            unique_id = unique_id.lower()
            unique_id = Web3.toChecksumAddress(unique_id)
            result = "Patient deleted their medical record."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.delete_record(unique_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_patient_delete.getLogs()
            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")

            ################## End Solidity TRansaction ###############
            return render_template("patient.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs)
        else:
            pass # unknown
    return render_template('patient.html', form=form, isCard  = isCard, username=account_address,contract_address=contract_address )

@app.route('/audit', methods=['GET', 'POST'])
def auditdash():
    account_address  = request.args.get("address")
    contract_address = request.args.get("contract")
    form = AuditActions(request.form)
    if request.method == 'POST':
        if request.form.get('action10') == 'VALUE10':
            contract_address  = form.contract_address.data
            return redirect('audit?'+"address=" + str(account_address) + "&contract=" + str(form.contract_address.data) )
        if request.form.get('action1') == 'VALUE1':
            print("-------------contract address  = " +contract_address)
            isCard  = True
            unique_id = form.print_record.data
            unique_id = unique_id.lower()
            unique_id = Web3.toChecksumAddress(unique_id)
            result = "Audit printed patient medical records."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.doctor_print_record(unique_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_doctor_print.getLogs()
            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")

            # get medical record details
            record_details  = contract.functions.get_record_details(unique_id).call()
            print(record_details)

            ################## End Solidity TRansaction ###############
            return render_template("audit.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs, record_details = record_details)

        elif  request.form.get('action2') == 'VALUE2':
            isCard  = True
            unique_id = form.update_record_id.data
            unique_id = unique_id.lower()
            unique_id = Web3.toChecksumAddress(unique_id)
            result = "Audit updated patient medical records."
            new_record = form.update_record_rec.data
            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.doctor_update_record(unique_id,new_record).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_doctor_update.getLogs()
            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")

            # get medical record details
            record_details  = contract.functions.get_record_details(unique_id).call()
            print(record_details)
            return render_template("audit.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs, record_details = record_details)

        elif  request.form.get('action3') == 'VALUE3':
            isCard  = True
            unique_id = form.query.data
            unique_id = unique_id.lower()
            unique_id = Web3.toChecksumAddress(unique_id)
            result = "Audit queried one of the patient medical records."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.doctor_query_record(unique_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_doctor_query.getLogs()
            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")

            # get medical record details
            record_details  = contract.functions.get_record_details(unique_id).call()
            print(record_details)

            ################## End Solidity TRansaction ###############
            return render_template("audit.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs, record_details = record_details)

        elif  request.form.get('action30') == 'VALUE30':
            fname = hashlib.sha224(b"uniqueid_data").hexdigest()
            df = pd.read_csv('data/'+fname+'.csv')
            print(df)
            token3 = df.applymap(lambda x: bytes(x[2:-1],'utf-8'))
            token4 = token3.applymap(lambda x: fernet.decrypt(x))
            decrypted_df = token4.applymap(lambda x: x.decode('utf-8'))
            print(decrypted_df)
            filtered_df = decrypted_df[decrypted_df['contract_address']==contract_address]
            filtered_dict = filtered_df.to_dict()
            print(filtered_dict)
            return render_template("audit.html", form=form, username=account_address,contract_address=contract_address,isDF = True, filtered_df=filtered_df)
        elif  request.form.get('action4') == 'VALUE4':
            isCard  = True
            unique_id = form.copy_record.data
            unique_id = unique_id.lower()
            unique_id = Web3.toChecksumAddress(unique_id)
            result = "Audit copied patient medical records."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.doctor_copy_record(unique_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_doctor_copy.getLogs()
            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")

            # get medical record details
            record_details  = contract.functions.get_record_details(unique_id).call()
            print(record_details)
            clipboard.copy(record_details)

            return render_template("audit.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs, record_details = record_details)
        elif  request.form.get('action5') == 'VALUE5':
            isCard  = True
            unique_id = form.delete_record.data
            unique_id = unique_id.lower()
            unique_id = Web3.toChecksumAddress(unique_id)
            result = "Audit deleted patient medical records."

            ################## Solidity Transaction ###################
            #find deployed contract
            contract = web3.eth.contract(address = contract_address, abi = abi)
            # assign default address
            web3.eth.defaultAccount = account_address
            tx_hash  = contract.functions.doctor_delete_record(unique_id).transact()
            tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)
            event_logs = contract.events.event_doctor_delete.getLogs()
            print("--------------------changes-------------")
            print(event_logs)
            print("--------------------end changes-------------")

            ################## End Solidity TRansaction ###############
            return render_template("audit.html", form=form, isCard  = isCard, username=account_address,contract_address=contract_address, result=result, tx_receipt = tx_receipt, tx_hash=tx_hash.hex(), event_logs = event_logs)

        else:
            pass # unknown
    return render_template('audit.html', form=form, username=account_address)


if __name__ == '__main__':
    # add ssl certificate
    app.run(ssl_context='adhoc')
