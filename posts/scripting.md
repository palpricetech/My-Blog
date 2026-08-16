## Bash Scripting

### 1) Shell script to create users along with shell and home directory

```bash
#!/bin/bash

## Check if the script is run as root ##
[ "$(id -u)" -ne 0 ] && echo "Run as root" && exit 1

## Create user with shell and home directory ##
create_user () {
  useradd -m -s "$2" -d "$3" "$1" && echo "User $1 created."
}

# Example: user creation
create_user "Raj" "/bin/bash" "/home/Raj"
```

### 2) Shell script to create users and assign password

```bash
#!/bin/bash

# Check if the script is run as root
[ "$(id -u)" -ne 0 ] && echo "Run as root" && exit 1

# Function to create user and set password
create_user () {
  useradd -m -s "$2" -d "$3" "$1" \
    && echo "$1:$4" | chpasswd \
    && echo "User $1 created with password."
}
```

<!-- TODO: The rest of this post was truncated during migration.
     Open the original on Blogger, copy the remaining scripts here,
     and format them in Markdown code blocks:
     https://basicprince.blogspot.com/2024/11/scripting.html -->
