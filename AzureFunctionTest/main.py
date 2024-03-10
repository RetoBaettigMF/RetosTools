from teams_push import send_teams_message
from rolx_connector import rolX
def main():
    try:
        rolx = rolX()
        users=rolx.get_users()
        print(users)
        send_teams_message("Test", "RolX Connecton Working!")
    except Exception as e:
        print(e)
        send_teams_message("Error", "Error in rolx_connector.py")
        
if __name__ == "__main__":
    main()