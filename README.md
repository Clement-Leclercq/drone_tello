# drone_tello 
## Questions : 
### ❓ Question 1 ❓<a name="question_1"></a>
Après lecture de cet extrait, répondez aux questions suivantes :
Quelles sont les quatre commandes classiques d’un drone quadrirotor ?
A l’aide de schémas et de repères que vous aurez fixés, expliquez comment
peut-on contrôler la trajectoire d’un drone quadricoptère.

### Throttle : 
![Throttle](https://github.com/Clement-Leclercq/drone_tello/blob/main/image/Throttle.png?raw=true)

### Roll : 
![Roll](https://github.com/Clement-Leclercq/drone_tello/blob/main/image/Roll.png?raw=true)

### Pitch : 
![Pitch](https://github.com/Clement-Leclercq/drone_tello/blob/main/image/Pitch.png?raw=true)

### Yaw :
![Yaw](https://github.com/Clement-Leclercq/drone_tello/blob/main/image/Yaw.png?raw=true)

### ❓ Question 2 : ❓

Quels topics correspondent à la commande du drone ?
Quel est respectivement le type de chacun des messages associés ?

| Topics | Types |
|-----------------|-----------------|
| /control | [geometry_msgs/msg/Twist] |
| /emergency | [std_msgs/msg/Empty] |
| /flip | [std_msgs/msg/String] |
| /land | [std_msgs/msg/Empty] |
| /takeoff | [std_msgs/msg/Empty] |

### 📉 Affichage de l'altitude mesurée : 

## Control du drone : 

### Introduction : 
Lancement avec Ubuntu 22.04  
Lancez 3 terminaux  
Sourcez votre ros2 humble  
Placez vous dans le dossier contenant le src du repo  
Build le package en effectuant:
```bash
colcon build
``` 
Sourcez les 3 terminaux: 
```bash
source install/setup.bash 
```
S'assûrer de bien être connecté au drone tello  
Dans le premier terminal: 
```bash
ros2 run tello tello
```

Dans le second terminal: 
```bash
 ros2 launch control control.launch.py 
```
-> une fenêtre RQT s'ouvre, vous pouvez choisir le topic image_raw  
Dans le troisème terminal: Il servira à changer les différents mode du drone via un appel de service  
```bash
 ros2 service call /drone_mode control_interfaces/srv/DroneMode "{mode: 0}"
```
-> vous pouvez changer le mode: 0 pour manuel, 1 pour scout, 2 pour Spielberg, 3 pour le follower de QR Code    

Lien de la playlist contenant les diffréntes démos de chaque mode: https://youtube.com/playlist?list=PLEFSyLthRPaKTrvjCAHfriWCbrdumMW5O&si=6MFcDMHthYX1npoO

### Décollage, atterisage et arret d'urgence : 
- Le decollage s'effectue à partir du bouton start de la télécommande
- L'atterisage s'effectue en utilisant le bouton back de la télécommande
- L'arret d'urgence utilise le bouton centrale de la télécommande

La node utilisée est **control** ce qui permet à ces actions d'etre independantes des differents modes de fonctionnement.  
Démonstration vidéo: https://youtu.be/ub3ZzUuB7SU?si=P_U4y89SkidaQQTP
### Mode manuel :
Le mode manuel permet de controler le drone avec la télécommande de Xbox. Le joystick de gauche permet de controler le Throttle et le Yaw quant au joystick droit, il permet de controler le pitch et le roll.  
Démonstration vidéo: https://youtu.be/eWMS9wSRR9A?si=pkOpIXrpR6O5PI6b  

Les différents boutons ABXY nous permettent de faire faire un flip dans une des 4 directions au drone.  
Démonstration vidéo: https://youtu.be/OdZ0dC0NkbQ?si=fF7q7hx6sQZt00Q6

### Mode scout :
Le mode scout permet au drone de rester en vol stationnaire tout en tournant sur lui même.  
Démonstration vidéo: https://youtu.be/g0M1cWxgqsA?si=w5vGnI43z_uuT9KD
### Mode Spielberg : 
Démonstration vidéo: https://youtu.be/GxWoVTguUL8?si=xAq99_BImZdGE_Gy
### Mode QR code follower : 
Démonstration vidéo: https://youtu.be/ydxsrOaWPzc?si=SZfchz_pwp_9GMRA




    
