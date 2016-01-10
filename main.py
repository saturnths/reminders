#!/usr/bin/env python3

from user_interface import reminders
import logging
import os


def main():
    os.makedirs('logs', exist_ok=True)
    logging.basicConfig(filename='logs/application.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s %(module)s - %(funcName)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    logging.info('Program started')
    reminders.init()

if __name__ == '__main__':
    main()
