
create database bibhal CHARACTER SET utf8;

/*
 * nom admin et mot de passe à changer et reporter dans bibhal/settings.py
 */

grant all privileges on bibhal.* 
   to bibhalAdmin identified by 'mdpBibhal'
