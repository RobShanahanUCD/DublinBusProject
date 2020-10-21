# DublinBusProject
Repository for UCD MSc. Conversion Research Practicum Project
- By Paihan Su, Rob Shanahan, John Parks, 

# Deployed Application:
- https://dublinbus-group11.herokuapp.com/ (Sorry the link is expired due to the RDS database exceed the credit)



## To run the code
### Step 1: Create and activate virtual environment using virtualenv
- In the terminal:
  - pip install virtualenv
  - virtualenv venv
  
  For MacOS/Linux
  - source venv/bin/activate
  
  For Windows
  - venv\Scripts\activate
  
### Step 2: Install requirements
- cd into the DublinBusProject folder
- run: pip install -r requirements.txt

### Step 3: Launch the application
- cd into the dublin_bus_time folder
- run: python3 manage.py runserver
