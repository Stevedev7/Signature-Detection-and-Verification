# SIGNATURE DETECTION AND VERIFICATION API

### Installation
1. clone this repository and move to the project directory.
2. Install requirements
```bash
pip install -r reuirements.txt
```
3. Download the service account credential file and edit the properties.py file.
4. Run the server
```bash
uvicorn main:app --reload
```
### API
**Signature Detection**
----
Returns a json object with the bucket location of the detections. If signature is not detected, returns a json object with message "Signature not detected".

* **URL**
/detect

* **METHOD**
`POST`

*  **URL Params**

   None

* **Data Params**

```json
{
  "document": {
    "location": <bucket-location>[string]
  }
}
```
* **Success Response:**
  
  * **Code:** 200 <br />
    
    **Content:** `{"detections": "<bucket-location>"}`
    OR

  * **Code:** 200 <br />
    
    **Content:** `{"message": "Signature not detected"}`


* **URL**
/verify

* **METHOD**
`POST`

*  **URL Params**

   None

* **Data Params**

```json
{
  "sign_1": {
    "location": <bucket-location>[string]
  },
  "sign_2": {
    "location": <bucket-location>[string]
  }
}
```
* **Success Response:**
  
  * **Code:** 200 <br />
    
    **Content:** `{"score": [float]}`

