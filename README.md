# drone_tello 

## Questions :

❓ Question 1 ❓
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

❓ Question 2 : ❓

Quels topics correspondent à la commande du drone ?
Quel est respectivement le type de chacun des messages associés ?

| Topics | Types |
|-----------------|-----------------|
| /control | [geometry_msgs/msg/Twist] |
| /emergency | [std_msgs/msg/Empty] |
| /flip | [std_msgs/msg/String] |
| /land | [std_msgs/msg/Empty] |
| /takeoff | [std_msgs/msg/Empty] |


    
