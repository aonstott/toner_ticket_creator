from DBAccess import DBAccess
from TicketManager import TicketManager
from TonerAnalyzer import TonerAnalyzer
import json


class Manager:
    def __init__(self):
        self.db_access = DBAccess("report", "xVftpqiQyDssntxra", "pmsyglpi.byu.edu", 3306, "glpi")
        self.db_access.connect()
        self.ticket_manager = TicketManager("YW9uc3RvdHQ6Ym9ia2VlcHN0aW1lNzc=", "B2HA6LJIwSSLkVaGK4wQKdYFZbh5JBCh623wspMz", "https://pmsyglpi.byu.edu/apirest.php")
        self.toner_analyzer = TonerAnalyzer()

    def get_session_token(self):
        return self.ticket_manager.get_session_token()
    
    def get_low_toners(self):
        cartridge_levels = self.toner_analyzer.get_toner_levels()
        return self.toner_analyzer.find_low_toners(cartridge_levels)
    
    def create_tickets(self, session_token, low_toners):
        for toner in low_toners:
            print(toner)
        for toner in low_toners:
            ticket_exists = False
            ticket_name = toner.get_color() + " Toner Low at: " + toner.location
            colors = []
            if toner.get_color() == "Black":
                colors.append("k toner")
                colors.append("toner k")
                colors.append("toner black")
                colors.append("black toner")
                colors.append("black")
            elif toner.get_color() == "Cyan":
                colors.append("n toner")
                colors.append("toner c")
                colors.append("toner cyan")
                colors.append("cyan toner")
                colors.append("cyan")
            elif toner.get_color() == "Magenta":
                colors.append("a toner")
                colors.append("toner m")
                colors.append("toner magenta")
                colors.append("magenta toner")
                colors.append("magenta")
            elif toner.get_color() == "Yellow":
                colors.append("w toner")
                colors.append("toner y")
                colors.append("toner yellow")
                colors.append("yellow toner")
                colors.append("yellow")

            for color in colors:
                if ticket_exists is False:
                    #print(color + " " + toner.location)
                    response = self.ticket_manager.search_tickets(session_token, color, toner.location)
                    if response["totalcount"] > 0:
                        print(response)
                        for ticket in response["data"]:
                            print(ticket['13'])
                            if int(ticket['13']) == int(toner.printer_id):
                                print("Ticket already exists for: " + ticket_name)
                                ticket_exists = True
                                break
            print(ticket_exists)
            if ticket_exists:
                print("skipping")
                continue

            if toner.get_level() <= 10 and toner.get_level() > 5:
                print(toner.get_color() + " Toner at " + toner.location + " is at " + str(toner.level) + "%")
                print("Ticket will be created when toner level reaches 5% or lower.")
                
            elif toner.get_level() <= 5:
                ticket_description = toner.get_color() + " at " + toner.location + " is at " + str(toner.level) + "% <p> </p> <p><em>This ticket was created automatically</em></p>"
                location_id = self.db_access.get_location_id(toner.location)
                #response = self.ticket_manager.create_ticket(session_token, ticket_name, ticket_description, location_id, toner.printer_id)
                #ticket_id = response["id"]
                #if response status is in 200s, ticket was created successfully

                #self.ticket_manager.link_ticket(session_token, ticket_id, toner.printer_id)
                #self.ticket_manager.link_to_group(session_token, ticket_id, 2)
                print("Ticket created for: " + ticket_name)
                #print(json.dumps(response, indent=4))
                print(ticket_description)

def run():
    manager = Manager()
    session_token = manager.get_session_token()
    low_toners = manager.get_low_toners()
    manager.create_tickets(session_token, low_toners)


if __name__ == "__main__":
    run()


        