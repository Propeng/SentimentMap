# -*- coding: utf-8 -*-
    
import jpype
import jpype.imports
from jpype.types import *
from jpype import JPackage
from jpype import JClass

# Launch the JVM
if not jpype.isJVMStarted():
    jpype.startJVM( "-ea", "-Djava.class.path=E:\\Projects\\GitHub Repos\\SentimentMap\\FarasaSegmenterJar.jar")
import java.lang

#from java.lang import System
#print(System.getProperty("java.class.path"))
f1 = JClass('com.qcri.farasa.segmenter.Farasa')
farasa = f1()

def lemmatize(sentence):
    x = farasa.lemmatizeLine(sentence)
    print(x)
    lemmatized = " ".join(x)
    return lemmatized

def shutdown():
    jpype.shutdownJVM()

#text = "RT @AssiellMustafa: +1 والله ، أنا بشكركوا جدا أنا من غيركو نثينج ربنا يخليكوا ليا  https://t.co/m6AkXM0n6k"
#print(lemmatize(text))
