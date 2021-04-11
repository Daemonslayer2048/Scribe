# Scribe
An Oxidized alternative

# Installation  
## Fedora 33  
Os packages:  
```
dnf install gcc libffi-devel
```

## Complete
### Web  
 * Working Example
 * View latest Config
 * View configs in Git repos
 * Disable Devices
### API  
 * Add/Remove Device
 * Add/Remove User
 * Add/Remove Group
 * Endpoint testing with GitLab CI (On going)
 * Git Repos
   * Local

## To-do
* Working Docker Image
* [Working Packer Image](https://learn.hashicorp.com/packer)
* Git Repos
  * Remote
* Emails
* Authentication
* Security (Something/Anything)
* Improve gathering repo directory, config file name, etc. Appending filenames manually is not the correct way to do it.
* API /repo/device/{alias} returns 204 if alias is not found, you need to return an error!
* Move to MariaDB
* Add devices in WebUI
* Add repos in WebUI
* Add models in WebUI
