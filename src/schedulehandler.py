import re
from authenticationerror import *
from datetime import datetime
from config import adminBotName

class ScheduleHandler():
            
    def addSchedule(self, bot, params, nick):
        
        if len(params) > 5:
            bot.send_message(nick, "Too many parameters!")
            return
        elif len (params) < 5:
            bot.send_message(nick, "Not enough parameters!")
            return

        currentDay = params[2].upper()

            
        # check syntax of time parameters
        timeFormat = re.compile(r'[0-2][0-9]\:[0-5][0-9]')
        if timeFormat.match(params[3]) is None:
            bot.send_message(nick, 'Incorrect start time format')
        if timeFormat.match(params[4]) is None:
            bot.send_message(nick, 'Incorrect end time format')
            
            
        try:
            with open(params[1].lower() + 'schedule.txt','r') as scheduleFile:
                # read a list of lines into data
                fileContents = scheduleFile.readlines()
                    
                # find correct line in file  
                for i in xrange(len(fileContents)):   
                    if currentDay in fileContents[i]:
                        fileContents[i] = currentDay + ' ' + params[3] + ' ' + params[4] + '\n'                            
                            
                # and write everything back
            with open(params[1].lower() + 'schedule.txt', 'w') as scheduleFile:
                scheduleFile.writelines( fileContents )
                    
        # file does not exist - create it
        except IOError:
            days = ['MONDAY\n', 'TUESDAY\n', 'WEDNESDAY\n', 'THURSDAY\n', 'FRIDAY\n', 'SATURDAY\n', 'SUNDAY']
            with open(params[1] + 'schedule.txt', 'w') as scheduleFile:
                scheduleFile.writelines(days)
            #rerun addSchedule    
            ScheduleHandler().addSchedule(bot, params, nick)
        
        
        
    def removeSchedule(self, bot, params, nick):
        currentDay = params[2].upper()
        try:
            with open(params[1].lower() + 'schedule.txt','r') as scheduleFile:
                # read a list of lines into data
                fileContents = scheduleFile.readlines()
                    
                # find correct line in file  
                for i in xrange(len(fileContents)):   
                    if currentDay in fileContents[i]:
                        fileContents[i] = currentDay + '\n'

                with open(params[1].lower() + 'schedule.txt', 'w') as scheduleFile:
                    scheduleFile.writelines( fileContents )
                    
        # file does not exist
        except IOError:
            return


    def changePayPeriod(self, bot, theDate, nick):
        # Make sure the date is in the correct format (mm/dd/yy)
        dateFormat = re.compile(r'\d+/\d+/\d+')
        dateMatch = dateFormat.match(theDate[0])
     
        if dateMatch is None:
            bot.send_message(nick, 'Date has incorrect format. Enter date in mm/dd/yy format')
            raise SyntaxError
            return 
        
        # make sure the date is a valid date
        try:
            dateFormat = datetime.strptime(theDate[0], '%m/%d/%y')
        
        except ValueError as err:
            bot.send_message(nick, nick + ", the date you entered is not valid")
            print err
            return
            
        # get the current date
        currentDate = datetime.now()
        
        # The pay period date cannot be less than the current date  
        if(dateFormat < currentDate):
            bot.send_message(nick, 'The new pay period cannot be less than today\'s date ' + currentDate.strftime("%A, %d %B %Y %I:%M%p"))
            raise ValueError
            return 
        
        # otherwise, the user is now cleared to change the pay period
        # rather than overwriting file each time, read the file and check the current pay period
        # if it is the same with the new pay period, inform the user and make no changes
        with open('payPeriod.txt', 'w') as payPeriod:
            payPeriod.writelines(dateFormat.strftime("%A, %d %B %Y %I:%M%p"))
        
        bot.send_message(nick, 'Pay period end date was successfully changed')
        return True