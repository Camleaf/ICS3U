Keep refining the randomness value in the pathfinding algorithm and also add collision between player and enemies

For second part since enemies will never run into the player, only the other way around, collision code only needs to go onto the player side


The non-alignment issue with the bot preventing me from implementing collision is because when the box is diagonal the image stretches, and since I can't use sprite since position is relative I can't put a rect around it