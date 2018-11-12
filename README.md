# WiseMacaw
Table of Contents
=================
  * [Overview](#overview)
  * [Contribution](#requirements)
  * [Quickstart](#quickstart)
  * [Citation](#citation)

## Overview:<br />
This is an team repository for Amazon Alexa Competition 2016-2017.<br />
Draft Paper [link](http://dk000000000.github.io/wise_macaw/pdf/Two-Layered%20Dialogue%20Framework%20to%20Experiment%20with%20Games%20and%20Gamification.pdf)
<br />
<br />
Team name:<br />
Wise Macaw(Originally BAKAbot)<br />
<br />
Team Website: [http://dk000000000.github.io/wise_macaw/index.html](http://dk000000000.github.io/wise_macaw/index.html)<br />
<br />
Advisor name:<br />
Mei Si<br />
<br />
Current Team Members(Alphabetical order):<br />
Zev Battad<br />
~~Craig Carlson~~(Graduated)<br />
~~Rahul Divekar~~(IP conflict)<br />
Jiashun Gou<br />
Jieming Ji<br />
Jingfei Zhou<br />
Qingyun Wang<br />
<br />

## Contribution:<br />
Jieming:
Design and implement three different dialog managers, most of Entertainment, Social-chat and Information modules and deployment of chatbot's system infrastructure. Experimented with training seq2seq on twitter dataset and Gamification of frame based dialog system.

Qingyun:
Independently developed a Python Program to extract popular news and comments from reddit or twitter; designed a recommendation system to provide users with most suitable news with best comments.

Jiashun:
Design and implement of ghost Adventure and text adventure, message board, word game and data management(redis).

Zev:
Dialog management, AIML bot and Scrpt Writing

Jingfei:
Horoscope & riddle

## Quickstart
Version:1.2.2<br />

<br />
Folder Structure:<br />
./EC2 is main function and all modules<br />
<br />
Code Architecture:<br />
./EC2/app.py is the Flask server that receive request from lambda function that were implemented by Jieming(Choose Menu initislized WiseMacawMenu else WiseMacawGame)<br />
./EC2/WiseMacawGame.py is the main python file that invoke by the Flask server that handles everything(Gamify Version)<br />
./EC2/WiseMacawMenu.py is the main python file that invoke by the Flask server that handles everything(Menu Version)<br />

## Citation<br />

We appreciate your citation if you find our code is beneficial.
```
@article{ji2017two,
  title={A Two-Layer Dialogue Framework For Authoring Social Bots},
  author={Ji, Jieming and Wang, Qingyun and Battad, Zev and Gou, Jiashun and Zhou, Jingfei and Divekar, Rahul and Carlson, Craig and Si, Mei},
  journal={Alexa Prize Proceedings},
  year={2017}
}
```
