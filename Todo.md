This is a todo list, or a rough roadmap.
✅ - once a task is completed, place a ticket mark emoji in between the brackets.

## Parsers 
- [ ] Normalize inner spaces in input parsing. so for example | Flikken    Rotterdam | would be | Flikken Rotterdam |
- [ ] Normalize input, and improve error handling.

## Models
- [ ] In DutchEnglishVocab table, add extra columns, like category, maybe pronunciation

## Bot Commands 
- [✅] Migrate bot commands from bot.py to bot_commands.py
- [ ] Add Intermediate Commands:  recent, practice, export, import
- [ ] Add Advanced Commands: stats, progress, most_used, wordstats, (practice log table), random, quiz
- [ ] Add visualization aspects and commands, like pichart and regression, bars
- [ ] Add shortcuts like /edit_comment, /edit_example
- [ ] Add pagination to get the command. It will help with proper returning when the word list gets too big
- [ ] Add confirmation for editing and deleting
- [ ] Add possibility to edit the Dutch word itself
- [ ] Add drop-down menu bar to see all the commands available when a user types /


## Handlers
- [ ] Add delete confirmation?

## CRUD
- [ ] Make or integrate CRUDs

## UX
- [ ] Add command buttons, which will activate commands without the need to write them out explicitly
- [ ] Let users choose which language "vaul" they would like to proceed with(so if learning multiple language simultaneously, the vocab would be mixed all in one "vault"

## Session
- [ ] Automatically close sessions

## Security 
- [ ] Validation of user input
- [ ] Add login and password details
 


## Chatbot
- [ ] Making a custom chatbot or connecting an existing one to my telegram bot to make sentences, corrections, synonyms

## NLP
- [ ] lemmatization (e.g all forms of the word lopen)
- [ ] spot and correct spelling issues 
- [ ] NER, 
- [ ] Auto tagging,
- [ ] Similarity Clustering
- [ ] Sentiment analysis



## Cloud Service
- [ ] Make the bot run 24/7 by connecting to cloud service, like AWS

## Backup
- [ ] Add /backup command or auto-export to file

## Scalability
- [✅] Upload on GitHub
- [ ] Share with fellows


