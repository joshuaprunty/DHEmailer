import json

def writeMessages():
    
    with open('/Users/joshprunty/Desktop/DHEmailer/data/users.json', 'r') as usrs:
        userData = json.load(usrs)

    with open('/Users/joshprunty/Desktop/DHEmailer/data/meals.json','r') as meals:
        mealData = json.load(meals)

    messages = {}

    for user in userData:
        message = {}
        message['name'] = user['name']
        message['content'] = 'Hi ' + message['name'] + ',' + '\n\n' + "Here are today's meals at your preferred dining halls: \n\n"

        for hall in user['halls']:
            message['content'] += hall.title() + '\n'
            for meal in user['meals']:
                if meal in mealData[hall]:
                    message['content'] += meal.title() + '\n'
                    for line in mealData[hall][meal]:
                        message['content'] += line + '\n'
                else:
                    message['content'] += meal.title() + ' not offered at this hall.\n'
            message['content'] += '\n'
        
        message['content'] += '\n' + 'All for today. Check in tomorrow.' + '\n' + '-Python'
        messages[user["email"]] = message['content']

    with open('/Users/joshprunty/Desktop/DHEmailer/data/messages.json', 'w') as file:
        json.dump(messages, file)

    print('complete')