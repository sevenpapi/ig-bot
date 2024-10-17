# ig-bot
Instagram bot development library with out-of-the-box functions to automate messages in Instagram group chats/DM's. 

Disclaimer: automated spamming is against Instagram TOS, I will not be held responsible for accounts being terminated for malicious usage of this library. This library should be used to automatically send weather alerts to group chats and humorously respond to specific users, not for mass unsolicited messaging.

To use, simply construct a function that consumes a "message" object (contains sender, message content, etc.) and decorate it with the @message() decorator.

There is also support for sending messages to a particular channel at a pre-specified interval.

See implementation in `core` for implementation and argument details.
