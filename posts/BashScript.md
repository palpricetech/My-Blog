## Bash Scripting ##

1.)   Shell script to create users along with shell and home directory

#!/bin/bash

## Check if the script is run as root ##

[ "$(id -u)" -ne 0 ] && echo "Run as root" && exit 1

## Create user with shell and home directory ##

create_user() { useradd -m -s "$2" -d "$3" "$1" && echo "User $1 created." }

Example: user creation

create_user "Raj" "/bin/bash" "/home/Raj"

2.)  Shell script to create users and assign password

#!/bin/bash

# Check if the script is run as root

[ "$(id -u)" -ne 0 ] && echo "Run as root" && exit 1

# Function to create user and set password

create_user() { useradd -m -s "$2" -d "$3" "$1" && echo "$1:$4" | chpasswd && echo "User $1 created with password." }

Example: user creation

create_user "Raj" "/bin/bash" "/home/Raj" "password123"

3.)  Create users in bulk using shell script

#!/bin/bash

# Check if the script is run as root

[ "$(id -u)" -ne 0 ] && echo "Run as root" && exit 1

# Check if the user list file exists

[ "$(id -u)" -ne 0 ] && echo "Run as root" && exit 1

# Create users from the file

[ ! -f "$1" ] && echo "User list file not found!" && exit 1

# Create the user and set the password

useradd -m -s "$shell" -d "$homedir" "$username" && echo "$username:$password" | chpasswd && echo "User $username created." done < "$1"

Note:
