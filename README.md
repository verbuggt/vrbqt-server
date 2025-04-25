hi.

### this is my old backend.

some stuff is still in very early stages of development.<br>
some other stuff is at least partly functional.

dropi and core are kind ok i guess

---
### dropi

dropi is a zero knowledge pastebin.
all data gets encrypted in the browser before its sent to the server. 

a new page link is generated which holds the encryption key. this encryption key can be used to decrypt the data.

anyone with this link can access the data.

the data is decrypted by the browser once the link is opened again.

[try it out](https://vrbqt.de/d/?tkn=qRxDhHIFNjHQNNKD#lFttdDhpRd0OeZEcgJ2h7sBgUzrUId9x)

not even the server admins can decrypt the data unless they have the link

---
### core

the core provides some basic functionality like
 - [x] users and groups
 - [x] authentication
 - [ ] access control / permissions
 - [x] database connection
 - [ ] logging
 - [ ] custom errors

---
### roses
is a very minimal backend to provide one of my frontends with data storage and access

---
### vlink
is an url shortener. this could be integrated with dropi, that would break the encryption tho bcs, the decryption key would then have to be stored on the server giving the admins access to the data in any shortened dropi link.

---
### bike
got my bike stolen and decided to make a online registry with serial numbers and stuff.
its not finished tho :\(

