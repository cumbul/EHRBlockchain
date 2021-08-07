# EHRBlockchain
A project managing Electronic Health Records(EHR) of patients and giving permissions to audity using Solidity(Etherium Blockchain) with Truffle and Ganache GUI. Front-end is implemented with Flask and Web3.py is to connect Ethereum Blockchain.

It uses:
* Solidity which is an Ethereum Smart Contract programming language
* Truffle and Ganache to deploy smart contracts
* Web3.py is a python library to connect with deployed contracts and create new contracts, transaction calls etc.
* Flask to create a user GUI and Python backend for authorization and identification goals.

# Demo video

https://drive.google.com/file/d/1XLdGxWXVUpU96LJEla4rZF9Kot-fBKnF/view?usp=sharing

## Purpose

This project fully implements a Blockchain EHR(Electronic Health Record) DApp Website which is decentralized and immutable. The objectives of the system is:
- Privacy: Patient is always maintained. Unauthorized entities should not be able to access audit by using Ethereum Smart Contracts. The patient can add or remove audits/doctors who can view their Medical Records.
- Identification and authorization: All system users have to submit their information in the sign up page, and this sensitive info is encrypted and passwords are encrypted and hashed in a txt file. In the login page users need to enter correct credentials to login the system.
- Queries: Authorized entities which are decided by patient are able to query audit records of patients, and due to Ethereum blockchain running in background, everyone can see the changes made to the specific Medical Record.
- Immutability: Without detection, neither patients nor audits/doctors cannot modify the specific record. From starting the visit to updating medical records all of the changes to a specific Medical Record is written to a separate Ethereum block as a transaction. 
- Decentralization: Using smart contracts and deploying the project in Ethereum blockchain makes the system fully decentralized and itt does not  rely on a single trusted entity which ensures immutability.

## Installation

1. Install all python requirements. Libraries used are: flask, flask_boostrap, flask_wtf, wtforms, hashlib, pandas, cryptography, pyopenssl, datetime, dateutil, web3, json and clipboard (Discussed in next section). 
3. Install truffle using ```npm install truffle -g```
4. Install Ganache GUI from https://www.trufflesuite.com/ganache
5. Generate a fernet key using ```Fernet.generate_key()``` to data/enc_key.key file.

## Compile and Run

1. Open Ganache UI and connect truffle.js in settings
2. In terminal go to project folder and ```truffle compile && truffle migrate```
3. From another terminal ```FLASK_APP=main.py FLASK_ENV=development flask run```

## External Libraries/Tools Used

* [Truffle](https://github.com/trufflesuite/truffle#:~:text=Truffle%20is%20a%20development%20environment,linking%2C%20deployment%20and%20binary%20management): Truffle Suite is a development environment based on Ethereum Blockchain, used to develop DApps (Distributed Applications). Truffle is a one-stop solution for building DApps: Compiling Contracts, Deploying Contracts, Injecting it into a web app, Creating front-end for DApps and Testing.
* [Ganache GUI](https://www.trufflesuite.com/ganache): Ganache GUI is a visual interface for Ganache CLI that works as a blockchain explorer. It is used to show blocks/events/transaction in the blockchain we deployed through truffle. After real deployment to Ethereum blockchain, everyone would be able to query whatever is shown in this Ganache GUI.
* [Web3.py](https://web3py.readthedocs.io/en/stable/): a Python library built for interacting with the Ethereum blockchain. All interaction to Ethereum blockchain deployed in port 7545 is done from main.py using Web3.py.
* [Flask](https://github.com/pallets/flask):  Flask is a lightweight WSGI web application framework, (flask, flask_boostrap, flask_wtf, wtforms) used for Website front end implementation and python is used in the server side.
* [Hashlib](https://docs.python.org/3/library/hashlib.html): Used to hash passwords and file names in /data/
* [Cryptography](https://pypi.org/project/cryptography/): Used for fernet encryption/decryption and generation of key.
* [Pyopenssl](https://pypi.org/project/pyOpenSSL/): Used to create an SSL certificate for EHR website.
* [Pandas](https://pandas.pydata.org/) and [JSON](https://docs.python.org/3/library/json.html): Used to store into csv file and read from csv file while encrypting and decrypting.
* [Datetime](https://docs.python.org/3/library/datetime.html) and [Dateutil](https://dateutil.readthedocs.io/en/stable/): to get/change date from epoch to any datetime format and vice versa.
* [Clipboard](https://pypi.org/project/clipboard/): Used for copying a unique patient record into clipboard.. Patient record is not selectable on the audit front end side, so only the copy function can copy it.

## Source Files

* [main.py](https://github.com/cumbul/EHRBlockchain/blob/main/main.py): All the user interface is implemented here using Flask and other than solidity files, all blockchain connections and other encryption/decryption/hashing is implemented here. This file will be deployed to the server.
* [model.py](https://github.com/cumbul/EHRBlockchain/blob/main/model.py): GUI forms for login signup and all patient and user actions model classes defined here. This file will be deployed to the server.
* [abi.json](https://github.com/cumbul/EHRBlockchain/blob/main/abi.json): JSON file that describes the deployed solidity contracts and its functions.
* [bytecode.json](https://github.com/cumbul/EHRBlockchain/blob/main/bytecode.json): Solidity files get compiled to the EVM bytecode which gets deployed to the Ethereum blockchain.
* [build/contracts/Migrations.json](https://github.com/cumbul/EHRBlockchain/blob/main/build/contracts/Migrations.json): After compilation Migration.sol turns into js file
* [build/contracts/Patient.json](https://github.com/cumbul/EHRBlockchain/blob/main/build/contracts/Patient.json): After compiling using truffle Migration.sol turns into js
* [contracts/Migrations.sol](https://github.com/cumbul/EHRBlockchain/blob/main/contracts/Migrations.sol): Solidity file which includes implementation of Migrations contract keeping track of which migrations were done on the current network. Implemented in truffle projects automatically, I did not change the file.
* [contracts/Patient.sol](https://github.com/cumbul/EHRBlockchain/blob/main/contracts/Patient.sol): Solidity contract for creating a new patient and all of the health records of the patient as well as their authorized audit/doctor info.
* [data/3f91fb273e0c… .csv](https://github.com/cumbul/EHRBlockchain/blob/main/data/3f91fb273e0cc5729c0e3c6379c3439c1369f987c29705146771707a.csv): Hashed name of “signin_data” where encrypted patient and audit signin data is stored. This file will be stored in the server or ideally a new encrypted db will be created for this purpose.
* [data/enc_key.key](https://github.com/cumbul/EHRBlockchain/blob/main/data/enc_key.key): Fernet encryption key is stored here. This file should be hidden securely in server.
* [data/f415ea3131a... . csv](http://f415ea3131a706b7d59e47c93b748932660f10d747cfa34f5868d469.csv): Hashed name of “uniqueid_data” where encrypted unique medical record id and patient id is stored. This file will be stored in the server or ideally a new encrypted db will be created for this purpose.
* [migrations/1_initial_migration.js](https://github.com/cumbul/EHRBlockchain/blob/main/migrations/1_initial_migration.js): First task to do after compiling both Migrations.sol and Patient.sol. It migrates the and keeps track of migrations to the Ethereum blockchain. Implemented in the truffle project automatically, I did not change the file.
* [migrations/2_deploy_contract.js](https://github.com/cumbul/EHRBlockchain/blob/main/migrations/2_deploy_contract.js): Second task to do after compilation of both solidity files. Fully implemented by me and creates the first Patient contract and deploys into the Ethereum network.
* [static/css](https://github.com/cumbul/EHRBlockchain/tree/main/static/css) and [static/img](https://github.com/cumbul/EHRBlockchain/tree/main/static/img) : CSS and image files for the EHR website.
* [templates/audit.html](https://github.com/cumbul/EHRBlockchain/blob/main/templates/audit.html): Flask template showing client side audit actions webpage. Built using HTML/CSS, Bootstrap and Jinja(embedded python code).
* [templates/auditreg.html](https://github.com/cumbul/EHRBlockchain/blob/main/templates/auditreg.html): Flask template showing client side audit signup webpage. Built using HTML/CSS, Bootstrap and Jinja(embedded python code).
* [templates/index.html](https://github.com/cumbul/EHRBlockchain/blob/main/templates/index.html): Flask template showing client side index webpage. Built using HTML/CSS, Bootstrap and Jinja(embedded python code).
* [templates/login.html](https://github.com/cumbul/EHRBlockchain/blob/main/templates/login.html): Flask template showing client side login webpage for both patients - audits. Built using HTML/CSS, Bootstrap and Jinja(embedded python code).
* [templates/patient.html](https://github.com/cumbul/EHRBlockchain/blob/main/templates/patient.html): Flask template showing client side patient actions webpage. Built using HTML/CSS, Bootstrap and Jinja(embedded python code).
* [templates/patientreg.html](https://github.com/cumbul/EHRBlockchain/blob/main/templates/patientreg.html): Flask template showing client side patient signup webpage. Built using HTML/CSS, Bootstrap and Jinja(embedded python code).
* [templates/result.html](https://github.com/cumbul/EHRBlockchain/blob/main/templates/result.html): Flask template showing client side result web page after sign in. Built using HTML/CSS, Bootstrap and Jinja(embedded python code).
* [test/](https://github.com/cumbul/EHRBlockchain/tree/main/test): Test files for deployed solidity contract. Empty in this project
* [truffle-config.js](https://github.com/cumbul/EHRBlockchain/blob/main/truffle-config.js):  Truffle configuration file is a Javascript file and can execute any code necessary to create configuration. In our case we connect Ganache GUI to truffle using this file.

## Cryptographic Components Used
* Fernet Encryption/Decryption:
  - Used in the authentication system. All sensitive info of audits and patients are encrypted file getting written into a csv file. 
  - While checking their credentials in login page
  - All unique id and patient id pairs are encrypted while stored in a csv file
  - While list button is used all info gets decrypted first, then using pandas DF functions related unique id’s are listed.
* SHA 256 Salted Hashing:
  - All passwords are hashed and salt is used before hashing.
  - No actual password storage is implemented and the system just compares pass hashes.
* SSL and TLS
  - System runs through HTTPS and uses SSL certificates as well as leveraging TLS.
* Ethereum Blockchain
  - The whole system is immutable and decentralized using a Ethereum Blockchain backend.


