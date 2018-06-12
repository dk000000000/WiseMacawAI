# Chit chat module

This module use [Seq2Seq Wrapper for Tensorflow](https://github.com/suriyadeepan/practical_seq2seq) by [Suriyadeepan Ramamoorthy](https://github.com/suriyadeepan)and pretrained model with Twitter Chat Log

To use it, first go to ./ckpt/twitter run pull and then go to datasets/twitter and run pull, then run python app.py will start a Flask server takes GET?msg= input and responde a json with {'text':"output"}

Dependency: CUDA 8, tensorflow, Flask
