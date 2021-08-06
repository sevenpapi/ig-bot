import config
import logs.console as console
from core.utils import commandify

def admin_on_deactivate(bot, recent_msg):
    console.log(console.QUIT, "Sending termination message '" + config.kill_message + "' to chat.")
    bot.send_message(config.kill_message)
    bot.quit()

def admin_on_run(bot, recent_msg):
    bot.running = True
    console.log(console.START, "Sending run message '" + config.startup_message + "' to chat.")
    bot.send_message(config.run_message)

def admin_on_quit(bot, recent_msg):
    bot.running = False
    console.log(console.QUIT, "Sending quit message '" + config.quit_message + "' to chat.")
    bot.send_message(config.quit_message)

# called if last sender is an administrator
def listen_admin(bot, recent_msg, notifications, interval_commands):
    if recent_msg.content == commandify(config.admin_commands['_deactivate']):
        admin_on_deactivate(bot, recent_msg)
    elif recent_msg.content == commandify(config.admin_commands['_run']) and not bot.running:
        admin_on_run(bot, recent_msg)
    elif recent_msg.content == commandify(config.admin_commands['_quit']) and bot.running:
        admin_on_quit(bot, recent_msg)
    else:
        for n in notifications:
            if n.toggle_command is not None and recent_msg.content == (tog_cmd_str := commandify(n.toggle_command)):
                n.enabled = not n.enabled
                s_res = "Toggled notification '" + n.func_run.__name__ + "'. Re-enable with '" + tog_cmd_str + "'. "
                console.log(console.WARNING, s_res + "Details: " + str(n))
                bot.send_message(s_res)
                return
        for i in interval_commands:
            if recent_msg.content == (tog_cmd_str := commandify(i.toggle_command)):
                i.enabled = not i.enabled
                s_res = "Toggled interval command '" + i.f_response.__name__ + "'. Re-enable with '" + tog_cmd_str + "'. "
                console.log(console.WARNING, s_res + "Details: " + str(i))
                bot.send_message(s_res)
                return
