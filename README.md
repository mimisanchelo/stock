# Stock Market Helper
<img width="40px" align="left" src="https://github.com/mimisanchelo/stock/assets/80426185/23c2fe40-b0a0-416b-a4be-ce1fb2f00553"/>
<img width="40px" align="left" src="https://github.com/mimisanchelo/stock/assets/80426185/eca4fe62-ab93-4b24-a00a-c6102555b06b"/>
<img width="40px" align="left" src="https://github.com/mimisanchelo/stock/assets/80426185/9de01f2c-70d7-4a26-8050-866cc7aaf946"/>

<br></br>

This is a Python-based stock market Helper project built using the Qt framework. The application uses a MySQL database. Passwords are hashed and salted using sha256 to protect sensitive data.
<br></br>
## Features

Registered and logged-in users can track the ticker of interest, monitor daily price changes, calculate entry and exit point with desired precentages, set alarm that will be send by email when price or percentage reaches the deasired user ticker mark.

## Preview
** images**

## Installation

1. Clone the repository:</br>
    ```python
   https://github.com/mimisanchelo/stock.git
    ```
   
1. Create virtual environment:
   
    ```python
   py -m venv venv
    ```
    ```python
    source venv/Scripts/activate
    ```

1. Install the required packages:
   
    ```python
   pip install -r requirements.txt
    ```
1. Create a MySQL database.
1. Change environmental variables to your own database URL.
1. Run the application.

