import steps.ScrapeDOC as ScrapeDOC
import steps.WriteMessages as WriteMessages
import steps.SendEmails as SendEmails

ScrapeDOC.Scrape()
WriteMessages.writeMessages()
SendEmails.sendEmails()