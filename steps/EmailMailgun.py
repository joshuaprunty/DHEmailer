import requests

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox81637676177741b494dd9f91798bec30.mailgun.org/messages",
		auth=("api", "<PRIVATE_API_KEY>"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox81637676177741b494dd9f91798bec30.mailgun.org>",
			"to": "Joshua Prunty <joshprunty@gmail.com>",
			"subject": "Hello Joshua Prunty",
			"text": "Congratulations Joshua Prunty, you just sent an email with Mailgun! You are truly awesome!"})

# You can see a record of this email in your logs: https://app.mailgun.com/app/logs.