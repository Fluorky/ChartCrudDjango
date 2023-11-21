# ChartCrudDjango

PoC Chart App in python using django framework with this functionalities:

*Charts chartJS with CRUD and LOGS,

*CRUD with database,

*Multiple charts on one chart with CHARTJS library,

*Network hosts scanner,

*Realtime Modbus sensors dashborad,

*JSON responses


# To run this app:
1. git clone https://github.com/Fluorky/ChartCrudDjango
2. Go to ChartCrundDjango-main folder
3. Create and run virual venv using these commands in cmd 

## Windows
py -3 -m venv venv
.\\venv\\Scripts\\activate

## macOS or Linux
python3 -m venv venv
source ./venv/bin/activate

4.  Use this command to install requirements packages
pip install -r requirements.txt
5. Use this command to create sqlite database from model
python manage.py migrate
6. To run app write in cmd
python manage.py runserver 0.0.0.0:8000 
7. Open this address yourIPAdress:8000 in browser
for example: 127.0.0.1:8000
