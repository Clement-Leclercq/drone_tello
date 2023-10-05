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
Build le package en effectuant: colcon build  
Sourcez les 3 terminaux: source install/setup.bash  
S'assûrer de bien être connecté au drone tello  
Dans le premier terminal: 
```bash
ros2 run tello tello
```
->   
Dans le second terminal:  
-> ros2 launch control control.launch.py  
-> une fenêtre RQT s'ouvre, vous pouvez choisir le topic image_raw  
Dans le troisème terminal: Il servira à changer les différents mode du drone via un appel de service  
-> ros2 service call /drone_mode control_interfaces/srv/DroneMode "{mode: 0}"  
-> vous pouvez changer le mode: 0 pour manuel, 1 pour scout, 2 pour Spielberg, 3 pour le follower de QR Code  

### Décollage, atterisage et arret d'urgence : 
- Le decollage s'effectue à partir du bouton start de la télécommande
- L'atterisage s'effectue en utilisant le bouton back de la télécommande
- L'arret d'urgence utilise le bouton centrale de la télécommande

La node utilisée est **control** ce qui permet à ces actions d'etre independantes des differents modes de fonctionnement.

### Mode manuel :
Le mode manuel permet de controler le drone avec la télécommande de Xbox. Le joystick de gauche permet de controler le Throttle et le Yaw quant au joystick droit, il permet de controler le pitch et le roll.

### Mode scout :

### Mode Spielberg : 

### Mode QR code follower : 




    
