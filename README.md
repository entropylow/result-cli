<!-- ABOUT THE PROJECT -->
## About The Project

This is a simple command line script which aims to access the result data from sgbau.ucanapply.com/result-details for a given range of roll numbers efficiently. 

<!-- GETTING STARTED -->
## Installation

1. Clone the repo and cd into result-cli

   ```sh
   git clone https://github.com/entropylow/result-cli.git
   cd result-cli
   ```
2. Create a virtual environment inside the project directory and activate it 

   **Linux**:

   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
   **Windows**:

   ```sh
   py -m venv .venv
   ```
   for powershell:
   
   ```sh
   .venv\Scripts\Activate
   ```
   for commmand prompt:
   
   ```sh
   .venv\Scripts\activate
   ``` 

3. Install the required packages

   **Linux**:

   ```sh
   python3 -m pip install lxml bs4 argparse asyncio aiohttp tqdm 
   ```
   **Windows**:

   ```sh
   py -m pip install lxml bs4 argparse asyncio aiohttp tqdm
   ```

<!-- USAGE EXAMPLES -->
## Usage

The script needs the following arguments to function as intended:

   `--session SESSION`    17:W22, 18:S23, ... , 21:W24 
 
   `--course COURSE`      UG/PG/PHD 
 
   `--code CODE`          CSE:32/ENTC:37/IT:39/MECH:41/ELPO:43/firstYear:48 
 
   `--type TYPE`          R/B/RV/EV 
 
   `--start START`        start roll number 
 
   `--end END`            end roll number 
 
   `--semester SEMESTER`  1, 2, 3, ...   

   `-h, --help`            show the help message and exit (optional)  

The following example outputs the result of BE Electronics and Telecommunication Engineering, Summer 2025 session for the specified ranger of roll numbers:

   ```sh
   python3 result_cli.py --session 22 --course UG --code 37 --type R --start 23BG310200 --end 23BG310215 --semester 6
   ```
<!-- CONTRIBUTING -->
## Contributing

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".

<!-- LICENSE -->
## License

Distributed under the GNU GPLv3. See `LICENSE.txt` for more information.
