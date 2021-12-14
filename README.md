# Scan-to-pdf

Maintainers:
- Mikaël Ferreira de Almeida
- Jérémie Henrion

## Managing app
- Build app : `docker-compose build`
- Run server : `docker-compose up [-d]`

## Access to Web Interface (app_1)
[http://127.0.0.1:5000/project/scan_to_pdf/](http://127.0.0.1:5000/project/scan_to_pdf/)

### Create you Account
```sh
curl -X POST "http://127.0.0.1:5000/project/scan_to_pdf/account/{{YOU PSEUDO}}/{{YOUR EMAIL}}" -H "accept: application/json"
```

### Get your account informations
```sh
curl -X GET "http://127.0.0.1:5000/project/scan_to_pdf/account/{{YOUR PSEUDO}}" -H "accept: application/json"
```

### Upload your Files
```sh
curl -X PUT "http://127.0.0.1:5000/project/scan_to_pdf/PDF/upload/{{YOUR PSEUDO}}" -H "accept: application/json" -H "Content-Type: multipart/form-data" -F "file=@{{YOUR FILE PATH}}"
```

### List your uploaded Files
```sh
curl -X GET "http://127.0.0.1:5000/project/scan_to_pdf/PDF/{{YOUR PSEUDO}}/_all" -H "accept: application/json"
```
### Download your transformed Files
```sh
curl -X GET "http://127.0.0.1:5000/project/scan_to_pdf/PDF/download/{{YOUR PSEUDO}}/{{FILE TO DOWNLOAD}}" -H "accept: application/json"
```