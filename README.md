<p align="center">
  <img src="https://user-images.githubusercontent.com/90923369/213894576-2f14557d-88cc-4292-b624-2fb8d9e1eed8.png">
</p>

# AADShell
<div align="center">
AADShell is a Microsoft Graph application. This applications core function is to retrieve and analyze user object sign-in logs within a mulit-tenant Azure Active Directory environment, allowing faster analysis of user sign-in event history. 
</div>  

# Functions
Currently, the application allows the operator to perform the following actions
  
  * Retrieve and filter sign-in data for user objects.
  * Send IP's used for event creation to external API's for further processing. [Virus Total, Abuse IP Database, IP Geolocation]
  * Switch between registered tenants without closing the application.

# Control Flow
<p align="center">
  <img src="https://user-images.githubusercontent.com/90923369/213894719-fe2ad9ed-0e36-4cd5-9d8e-9ce73f98cfab.jpg">
</p>


# Development
AADShell was developed in both Windows and Debian Linux environments with python 3.9 and python 3.10 respectively.

# Setup
[Setup Instructions](https://github.com/wizardy0ga/_AADShell/blob/main/docs/setup_instructions.txt)

# Further Information
[Information File](https://github.com/wizardy0ga/_AADShell/blob/main/docs/Information.txt)

# Notes

> **Warning**
> Ensure care is taken with the application secrets, API Keys and the decryption key you will be using. The application secret can be used by an attacker
> to access data within the directory application that has generated the secret, under the context of the application and with the permissions that were
> assigned to application.

> **Note**
> The AAD Logo is property of Microsoft. I do not own that photo. This is not an official Microsoft application or repository. I am not assosciated with Microsoft.
