import os

class Config:
    SECRET_KEY = OS.ENVIRON.GET('SECRET_KEY') or 'you-will-never-guess'