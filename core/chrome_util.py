JS_ADD_TEXT_TO_INPUT = """
    var elm = arguments[0], txt = arguments[1];
    elm.value += txt;
    elm.dispatchEvent(new Event('keydown', {bubbles: true}));
    elm.dispatchEvent(new Event('keypress', {bubbles: true}));
    elm.dispatchEvent(new Event('input', {bubbles: true}));
    elm.dispatchEvent(new Event('keyup', {bubbles: true}));"""

def chrome_send_text_to_elem(bot, text):
    bot.driver.execute_script(JS_ADD_TEXT_TO_INPUT, bot.msg_textarea, text)
