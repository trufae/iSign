# Better Than Fastlane



## How to use
```sh
$ ./rscript -a <APP IDENTIFIER> -c <CLIENT ID>  -v <VERSION> ... 
```

| Parameter | Value |
| ------ | ------ |
| -a | App identifier |
| -c | Client ID |
| -v | App version |
| -m | Maestro Token |
| -g | GitHub Token |
| -s3 | S3 access key | 
| -s3secret | S3 secret key | 
| -s3bucket | S3 bucket |  
| -s3region | S3 region |
| -s3endpoint | S3 endpoint |
| -sheet | Google Sheet ID |

By default S3 Region/endpoint value is s3-website-us-east-1.amazonaws.com
A endpoint list is available in [AWS Docs](http://docs.aws.amazon.com/pt_br/general/latest/gr/rande.html)
99627-6680

## Dependencies
requests, zipfile, plistlib, boto3, gspread and isign


## Methods

### getRepositories()
Load all user repositories, search for PROJECT_NAME and get release url

### OhOBichoVindo(releaseUrl)
Receive Release URL from getRepositories and download IPA

### zipdir(path, ziph)
Compress directory (Payload) to a new IPA

### modifyIPA()
Modify AppConfigs.plist

### resign()
Resign IPA

### sheetsHappen()
Update Google Spreadsheet

### generateMetadata
Generate index.html, version.json and manifest.plist

### vaiFilhao()
Upload IPA to Amazon S3

### updateMaestro()
Update client version in Maestro