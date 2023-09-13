# Install git
- Download the git tools by google "git" or from this [link](https://git-scm.com/download/win)
- Install the tool under your user name

# First time use
- For the first time of use, register your user name and email in the git system
- Replace "yourname" and your_email@example.com with your information
```
git config --global user.name "yourname"
git config --global yser.email your_email@example.com
```

- This only needs to be done once. 
- You can always edit the file ".gitconfig" in the folder of "C:/users/Yourname"

# Create a folder as a local repository

- Use the Windows FileExplore to create a folder under "Documents" 
- Run```git init``` to initialize the folder
- After doing some changes, use ```git add .``` to stage the changes
- Use ```git commit -m "commit message"``` to commit a change. The message shall be replaced with an actual message for you to remember what was changed

# Synchronize with Github.com repository

- Go to Github.com and create your free account using an email of yours (It is convinient to use the same email as you did in ```git config```)
- In the Dashboard, click New
- Put a Repository name. 
- If you want to share it with others, choose Public. Othewise, choose Private
- Use the default settings, which can be changed later
- Once you created the repository, in the 
- 
