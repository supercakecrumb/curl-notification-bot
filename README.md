# queue_bot
Bot made to provide the easy way to make a queue on passing labs. 

## Security configuration

Set a unique `ADMIN_PASSWORD` through the deployment secret manager to enable private-chat admin enrollment. Without it enrollment is disabled; existing admins remain valid. Admin commands and credential scripts require a private chat. Request/message bodies are not logged.
Notification callers must send the per-user password returned by `/getbashscript`; anonymous requests are rejected.
