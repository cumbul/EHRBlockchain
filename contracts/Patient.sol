pragma solidity ^0.6.6;

contract Patient{
    
    /////////// VARIABLES ///////////////////
    
    // address
    address owner;
    
    //identity
    string private firstName;
    string private lastName;
    string private IID;
    
    //birthday
    string private bdate;
    
    //contract
    string private email;
    string private phone;
    string private zip;
    string private city;
    
    // keys
    string encryption_key;
    
    /////////// VARIABLES END ///////////////

    
    
    /////////// DECLARATIONS ////////////
    
    struct medical_record{
        bool is_uid_generated;
        uint256 record_id;
        string record_msg;
        uint record_status; // 0-Created, 1-Deleted, 2-Changed, 3-Queried, 4-Printed, 5-Copied
        
        // all images files etc will be stored here
        string record_details;
        
        address patient_address;
        uint record_time;
        
        address doctor;
        uint doctor_time;
        
        address audit;
        uint audit_time;
    }
    
    /////////// DECLARATIONS END////////
    
    
    ////////// MAPPINGS ////////////////
    
    mapping (address => medical_record) public record_mapping; 
    mapping (address => bool) public doctors;
    mapping (address => bool) public audits;
    ////////// MAPPINGS END ////////////
    
    
    ////////// MODIFIERS ///////////////////
    
    // initiate  patient data
    constructor (string memory _firstName, string memory _lastName, string memory _IID, 
                string memory _bdate, string memory _email, string memory _phone, 
                string memory _zip, string memory _city, string memory _encryption_key) public
    {
        owner = msg.sender;
        firstName = _firstName ;
        lastName = _lastName;
        IID = _IID;
        bdate = _bdate;
        email = _email;
        phone = _phone;
        zip = _zip;
        city = _city;
        encryption_key = _encryption_key;
    }
    
    // make the patient using this contractt only owner
    modifier only_owner(){
        require(owner == msg.sender);
        _;
    }
    
    ////////// MODIFIERS END////////////////

    ////////////// EVENTS ////////////////////
    event event_start_visit(
        address record_unique_id,
        string record_msg,
        uint record_status,
        uint record_time
        );
        
    event event_add_doctor(
        string return_msg,
        address doctor_address,
        uint record_time
        );
    event event_remove_doctor(
        string return_msg,
        address doctor_address,
        uint record_time
        );
    event event_add_audit(
        string return_msg,
        address audit_address,
        uint record_time
        );
    event event_remove_audit(
        string return_msg,
        address audit_address,
        uint record_time
        );
    event event_patient_print(
        string record_msg,
        uint record_status,
        uint record_time
        );
    event event_patient_delete(
        string record_msg,
        uint record_status,
        uint record_time
        );
    event event_doctor_delete(
        string record_msg,
        uint record_status,
        uint record_time
        );
    event event_doctor_print(
        string record_msg,
        uint record_status,
        uint record_time
        );
    event event_doctor_copy(
        string record_msg,
        uint record_status,
        uint record_time
        );
    event event_doctor_query(
        string record_msg,
        uint record_status,
        uint record_time
        );
    event event_doctor_update(
        string record_msg,
        uint record_status,
        uint record_time
        );
    
    ////////////// EVENTS END////////////////
    
    ////////// PATIENT FUNCTIONS //////////////
    
    // create a medical record with unique id
    // patient makes appointment
    function start_visit(uint _time) public only_owner returns (address){
        address unique_id = address(uint256(sha256(abi.encodePacked(msg.sender, now))));
        record_mapping[unique_id].is_uid_generated = true;
        record_mapping[unique_id].record_id = uint256(unique_id);
        record_mapping[unique_id].record_msg = "New Medical Record is created";
        record_mapping[unique_id].record_status = 0;
        
        record_mapping[unique_id].record_details = "Visit initiate";
        
        record_mapping[unique_id].patient_address = msg.sender;
        record_mapping[unique_id].record_time = _time;
        emit event_start_visit(
            unique_id,
            record_mapping[unique_id].record_msg,
            record_mapping[unique_id].record_status, 
            record_mapping[unique_id].record_time);
        return unique_id;
    }
    
    // give permissions to doctors -- authorize doctors
    function addDoctors(address _doctor_address) public only_owner returns (string memory) {
       
        // if doctor is not authorized yet
        if(!doctors[_doctor_address]){
            doctors[_doctor_address] = true;
        }
        emit event_add_doctor("A doctor is added.", _doctor_address, now);
        return "A doctor is added.";
    }
    
    // take back permissions -- delete authorization of doctors
    function removeDoctors(address _doctor_address) public only_owner returns (string memory) {
       
        // if doctor is authorized 
        if(doctors[_doctor_address]){
            doctors[_doctor_address] = false;
        }
        emit event_remove_doctor("A doctor is removed.", _doctor_address, now);
        return "A doctor is removed.";
    }
    
    // Give permissions to audits
    // give permissions to doctors -- authorize doctors
    function addAudit(address _audit_address) public only_owner returns (string memory) {
       
        // if doctor is not authorized yet
        if(!audits[_audit_address]){
            audits[_audit_address] = true;
        }
        emit event_add_audit("An audit is added.", _audit_address, now);
        return "An audit is added.";
    }
    
    // take back permissions -- delete authorization of doctors
    function removeAudit(address _audit_address) public only_owner returns (string memory) {
       
        // if doctor is authorized 
        if(audits[_audit_address]){
            audits[_audit_address] = false;
        }
        emit event_remove_audit("An audit is removed.", _audit_address, now);
        return "A doctor is removed.";
    }
    
    //////////// PATIENT FUNCTIONS END ///////////
    
    /////////// GET MEDICAL RECORDS /////////////
    function get_record_details(address _unique_id) view public returns (string memory) {
        require(record_mapping[_unique_id].is_uid_generated == true);
        require(record_mapping[_unique_id].record_status!=1);
        if(record_mapping[_unique_id].patient_address == msg.sender){
            require(record_mapping[_unique_id].patient_address == msg.sender);
            return record_mapping[_unique_id].record_details;
        }
        if(doctors[msg.sender]){
            require(doctors[msg.sender], "Not working");
            return record_mapping[_unique_id].record_details;
        }
         if(audits[msg.sender]){
            require(audits[msg.sender], "Not working");
            return record_mapping[_unique_id].record_details;
        }
        return "You have no authorization.";
    }
    
    /////////// END GET MEDICAL RECORDS /////////

    
    /////////// MODIFICATION OF MEDICAL DATA  /////////////////
    
    // patient can delete his/her medical record
    function delete_record(address _unique_id) public returns (string memory){
        require(record_mapping[_unique_id].is_uid_generated == true);
        require(record_mapping[_unique_id].patient_address == msg.sender);
        require(record_mapping[_unique_id].record_status!=1);
         
        record_mapping[_unique_id].record_details = "";
        record_mapping[_unique_id].record_time = now;

        
        record_mapping[_unique_id].record_status = 1;
        record_mapping[_unique_id].record_msg = "Record is deleted by patient.";
        emit event_patient_delete(
            record_mapping[_unique_id].record_msg,
            record_mapping[_unique_id].record_status,
            record_mapping[_unique_id].record_time
        );
        return "Record is deleted by patient.";
        
    }
    
    // patient can print his/her medical record
    function print_record(address _unique_id) public returns (string memory){
        require(record_mapping[_unique_id].is_uid_generated == true);
        require(record_mapping[_unique_id].patient_address == msg.sender);
        require(record_mapping[_unique_id].record_status!=1);
         
        record_mapping[_unique_id].record_time = now;

        record_mapping[_unique_id].record_status = 4;
        record_mapping[_unique_id].record_msg = "Record is printed by patient.";
        emit event_patient_print(
            record_mapping[_unique_id].record_msg,
            record_mapping[_unique_id].record_status,
            record_mapping[_unique_id].record_time
        );
    }
    
    // check
    // doctor deletes medical record
    function doctor_delete_record(address _unique_id) public returns (string memory){
        require(record_mapping[_unique_id].is_uid_generated);
        require(doctors[msg.sender]);
        require(record_mapping[_unique_id].record_status!=1);
    
        record_mapping[_unique_id].doctor = msg.sender;
        record_mapping[_unique_id].doctor_time = now;
        
        record_mapping[_unique_id].record_details = "";
        record_mapping[_unique_id].record_status = 1;
        record_mapping[_unique_id].record_msg = "Record is deleted by doctor/audit.";
        emit event_doctor_delete(
            record_mapping[_unique_id].record_msg,
            record_mapping[_unique_id].record_status,
            record_mapping[_unique_id].record_time
        );
    }
    
    // doctor prints medical record
    function doctor_print_record(address _unique_id) public returns (string memory){
        require(record_mapping[_unique_id].is_uid_generated);
        require(doctors[msg.sender]);
        require(record_mapping[_unique_id].record_status!=1);
    
        record_mapping[_unique_id].doctor = msg.sender;
        record_mapping[_unique_id].doctor_time = now;
        
        record_mapping[_unique_id].record_status = 4;
        record_mapping[_unique_id].record_msg = "Record is printed by doctor/audit.";
        emit event_doctor_print(
            record_mapping[_unique_id].record_msg,
            record_mapping[_unique_id].record_status,
            record_mapping[_unique_id].record_time
        );
    }
    
    // doctor query medical record
    function doctor_query_record(address _unique_id) public returns (string memory){
        require(record_mapping[_unique_id].is_uid_generated);
        require(doctors[msg.sender]);
        require(record_mapping[_unique_id].record_status!=1);
    
        record_mapping[_unique_id].doctor = msg.sender;
        record_mapping[_unique_id].doctor_time = now;
        
        record_mapping[_unique_id].record_status = 3;
        record_mapping[_unique_id].record_msg = "Record is queried by doctor/audit.";
        emit event_doctor_query(
            record_mapping[_unique_id].record_msg,
            record_mapping[_unique_id].record_status,
            record_mapping[_unique_id].record_time
        );
    }
    
    // doctor copy medical record
    function doctor_copy_record(address _unique_id) public returns (string memory){
        require(record_mapping[_unique_id].is_uid_generated);
        require(doctors[msg.sender] || audits[msg.sender], "Not working");
        require(record_mapping[_unique_id].record_status!=1);
    
        record_mapping[_unique_id].doctor = msg.sender;
        record_mapping[_unique_id].doctor_time = now;
        
        record_mapping[_unique_id].record_status = 5;
        record_mapping[_unique_id].record_msg = "Record is copied by doctor/audit.";
        emit event_doctor_copy(
            record_mapping[_unique_id].record_msg,
            record_mapping[_unique_id].record_status,
            record_mapping[_unique_id].record_time
        );
    }
    
     // doctor update medical record
    function doctor_update_record(address _unique_id, string memory _update) public returns (string memory){
        require(record_mapping[_unique_id].is_uid_generated);
        require(doctors[msg.sender]);
        require(record_mapping[_unique_id].record_status!=1);
    
        record_mapping[_unique_id].doctor = msg.sender;
        record_mapping[_unique_id].doctor_time = now;
        record_mapping[_unique_id].record_details = _update;
        record_mapping[_unique_id].record_status = 5;
        record_mapping[_unique_id].record_msg = "Record is updated by doctor/audit.";
        emit event_doctor_update(
            record_mapping[_unique_id].record_msg,
            record_mapping[_unique_id].record_status,
            record_mapping[_unique_id].record_time
        );
    }
    ////////////MODIFICATION OF MEDICAL DATA END ///////////////
    
}