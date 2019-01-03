# Flask Forgot Password

In my project I had to have the user forgot my password. I didn't know how to do it. Then I tried something like this and got a positive result.

### In This Project
Sqlalchemy needs to know the e-mail address of the existing user in the database when he wants to change his password. When the user enters my password, he / she will receive an email request. After sending the e-mail address, the e-mail address he wrote is searched in his database and if he is paired he will receive a mail. The outgoing mail also welcomes a url to the form site.com/(HashCode). After saying that hash code mail address is sent, it is generated randomly and registered to the database. Then click on the link in the inbound mail and change the password after the hash code itself is ignoring.

### Installation
```
pip install -r /path/to/requirements.txt
```
