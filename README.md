# Whatsapp-Automation-with-Selenium

This is a small project I built to help send WhatsApp messages automatically.
Instead of typing messages one by one, this script uses Python + Selenium to send a message (and image) to a list of phone numbers.

What It Can Do
1. Send the same message to many contacts
2. Add a personalized caption
3. Send an image
4. Save numbers that failed (with screenshots)
5. Allow you to change the contact list anytime
6. Filter messy contacts using a small Python + Regex script

How It Works
1. Run the script
2. Scan your WhatsApp QR code
3. The script loops through your contact list
4. For each number:
      sends the message
      sends the picture
      If it fails, it saves the number + screenshot

How To Use
1. Put your contacts inside a text file
2. Put your image inside the img folder
3. Edit the message inside the Python script
4. Run

Why I Built It
I needed to send multiple messages at once, and doing it manually was tedious and stressful.
This script saved me time and also made me understand how automation works in real life.
