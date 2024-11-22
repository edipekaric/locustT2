#Setup
*Locust is needed, download if you dont have it
*in cmd prompt / terminal, navigate to the project, example : cd t2-project
*After You are in the folder holding the project you need to pull this repository with *git clone https://github.com/edipekaric/locustT2.git*
*After the folder is cloned to the project You need to navigate into it, with *cd locustT2*
*Now, run the python script *locust -f testD.py*
*After running the script, leave the cmd prompt open, and navigate to website *http://localhost:8089/*
*Setup locust with following parameters:
    *Number of users(peak capacity) - 100
    *Ramp up(users started/second) - 100
    *Host - http://localhost:8080
*This ensures that the website in second 1 will have 100 users trying to browse products, add items to cart, and confirming order
