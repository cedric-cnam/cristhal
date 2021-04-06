   /* Nom de base à reporter dans cristhal/local_settings.py */
    create database cristhal CHARACTER SET utf8;

    /*
    * Nom admin et mot de passe à changer et reporter dans cristhal/local_settings.py
    */

    grant all privileges on cristhal.* 
        to cristhalAdmin identified by 'mdpCristhal'
