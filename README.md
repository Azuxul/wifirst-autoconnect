# wifirst-autoconnect
A python script to automatically connect your devices to the Wifirst network.
Tested in CROUS residences (Smartcampus).


## Dependency
- Python3
- beautifulsoup4

## Instalation

Install dependency
`pip install beautifulsoup4` 

Clone this repository
`git clone https://github.com/Azuxul/wifirst-autoconnect.git` 

## Usage
### Direct connexion (with saved connexion info)
Dump your connexion ingo
`python wifirst-autoconnect.py -u <username> -p <password> -d`
 
 Then paste it into the `credentials.py` file at `INTERNAL_LOGIN`

Now you can use this command to connect
`python wifirst-autoconnect.py -a`

### Connexion with saved credentials
Write your password and username into the `credentials.py` 

Now you can use this command to connect
`python wifirst-autoconnect.py -s`

### Connexion without saved credentials
You can connext using the command
`python wifirst-autoconnect.py -u <username> -p <password>`

## Known issues
Using a custom DNS server can cause issue to the connexion

## License
This project is licensed under the GNU General Public License v3.0
