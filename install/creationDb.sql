
create database cristhal CHARACTER SET utf8;

/*
 * nom admin et mot de passe à changer et reporter dans bibhal/settings.py
 */

grant all privileges on cristhal.* 
   to cristhalAdmin identified by 'mdpCristhal'
