This is a fork of ServerlessNabaztag with added hooks for recording and RFID, and some basic Python scripts for speech recognition.
The new scripts are located in "hooks" folder. The .py scripts must be constantly running.
ttshandler_GPT.py constantly looks for new .wav files added into folder (with record.php), converts the recording with ffmpeg, uses SpeechRecognition to convert into text, sends the text in URL to a plaintext GPT endpoint (text.pollinations.ai/ for example) with GET request, gets plaintext response and converts it into .mp3, sending it to converted folder, and plays on Nabaztag with /play .
Connect the Nabaztag to your local IP with ServerlessNabaztag running, run the .py script, and hold the button on the bunny to record, release to send.

The original description BELOW:

ServerlessNabaztag
==================

ServerlessNabaztag is a firmware allowing control of the Nabaztag/tag directly via the web, without an external server (a web server is needed only for downloading the firmware and the mp3s).

With this firmware, you can connect at http://\<YOURNABAZTAGIP\>/ and completely control your rabbit with a very simple web interface, as show in the following screenshot:

![](/imgs/screenshot.png "Screenshot")

All the commands can be called with a single HTTP requests from an external program/script, example:

```
$ curl http://nabaztag/wakeup
```

In examples/check_mail.py, there is a script that turns on the nose when you have unread email and changes the lights color according to the weather forecast.

Configure the rabbit
--------------------

* Unplug the rabbit, press the button on its head and hold it while you replug your rabbit. When all the lights are blue, you can release the button
* On your computer, connect to the wifi network created by your rabbit (the name should be Nabaztag\<XX\>)
* Go to the configuration page at the following address: http://192.168.0.1
* At the bottom of the page, in General Info, change "Violet Platform" to http://nabaztag.joe.dj/vl
* Click on Update settings and wait for rabbit to reboot.
* You can now connect to the IP of your rabbit, configure and control it. (note: if your rabbit IP is assigned with DHCP, you have to discover the IP address. Usually you can check the assigned IP from some page on your router)


Server install instruction
--------------------------

* Create a folder "vl" an a website
* Download the file vl/bc.jsp
* Copy the file "bc.jsp" to the web server into the "vl" folder (note: it's not a Java Server Page, it's a binary file)
* Download the mp3 files from https://github.com/andreax79/ServerlessNabaztag/tree/main/vl
* Copy the mp3 files in the "vl/config" directory on the web server. The resulting directroy structure is the following:

![](/imgs/files.jpg "Directory structure")

* Unplug the rabbit, press the button on its head and hold it while you replug your rabbit. When all the lights are blue, you can release the button
* On your computer, connect to the wifi network created by your rabbit (the name should be Nabaztag\<XX\>)
* Go to the configuration page at the following address: http://192.168.0.1
* At the bottom of the page, in General Info, change "Violet Platform" to the url of the vl directory (without http://, example: 192.168.0.1/vl)
* Click on Update settings and wait for rabbit to reboot.
* You can now connect to the IP of your rabbit, configure and control it. (note: if your rabbit IP is assigned with DHCP, you have to discover the IP address. Usually you can check the assigned IP from some page on your router)

Firmware features
-----------------

* Control the rabbit via HTTP API
* Configure via web interface
* Fetch the current time from a time server and play the corresponding sound every hour
* Fetch weather from [open-meteo](https://open-meteo.com)
* Autonomously wake up at go to sleep
* Respond to ICMP pings

Development
-----------

Please install the following dependencies:
```
$ sudo apt-get install gcc-multilib g++-multilib
```

Build the compiler and the simulator:
```
$ make compilter
```

Build the firmware
```
$ make firmware
```

Start local web server:
```
$ sudo iptables -t nat -I PREROUTING -p tcp --dport 80 -j REDIRECT --to-ports 8000
$ python3 -m http.server
```

### Links

* [Nabaztag Firmware with WPA2 support](https://github.com/RedoXyde/nabgcc/tree/wpa2)
* [Milligram, A minimalist CSS framework](https://milligram.io)
* [open-meteo, Free Weather Forecast API for non-commercial use ](https://github.com/open-meteo/open-meteo)
* [pynab](https://github.com/nabaztag2018/pynab)
