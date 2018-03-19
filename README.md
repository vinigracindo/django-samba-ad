# Django Samba Active Directory 

Web management application for Samba Active Directory

## Features

1. Create, list, delete and update domains Users.

## Setup

Add rule in sudoers file (sudo visudo): **myuser ALL=(ALL) NOPASSWD:ALL**

## Getting started

```console
git clone https://github.com/vinigracindo/django-samba-ad.git dsad
cd dsad
python -m venv .dsad
source .dsad/bin/activate #Unix CMD
pip install -r requirements.txt
cp contrib/env-sample .env
python manage.py test
```
