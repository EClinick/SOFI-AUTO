# SOFI
1. Install Python
If you haven't already, you'll need to install Python.
https://www.python.org/downloads/


2. Clone the Repository
Clone this repository to your local machine.

git clone <https://github.com/EClinick/SOFI-AUTO>

3. Install Dependencies
Navigate to the project directory and install the required dependencies using pip:

```bash pip install -r requirements.txt ```
 

4. Set Up Environment Variables
Copy the .env.example file and rename the copy to .env. Then, open the .env file and replace the placeholders with your actual values:

Open .env file and update the variables:

USER='your_username'
PASSWORD='your_password'

Replace your_username and your_password with your actual username and password.

5. Run the Project
Finally, you can run the project with the following command:

```bash python main.py ORDER QUANTITY TICKER DRY ```

ORDER: The order type (buy or sell)
QUANTITY: The quantity of shares to buy or sell
TICKER: The stock ticker symbol
DRY: Set to TRUE to simulate the order (dry run mode) or FALSE to execute the order


It will ask you for a code from your phone, enter the code and you are good to go.

Don't worry if the code doesn't fit in one line, selenium will cut it off sometimes but it will still work.

Example:

```---------------------------------

Please enter code and press ENTER to continue:0Created TensorFlow Lite XNNPACK delegate for CPU.
89602 
```

# Example of running the program:

```bash python main.py buy 10 AAPL TRUE ```

This command will simulate (because of TRUE in dry run mode) buying 10 shares of AAPL
