# Pong-AI
Hello and welcome to AI Pong!

*Before trying to run the file, make sure you have pygame downloaded*

Here's how the it works:

The program launches a window that begins single player pong.  
Single player pong is just like regular pong, except there is only one paddle. If the ball hits the left, top, or right walls, it simply bounces off. If the ball hits the bottom wall (or the ground) however, the game is lost. It is the paddle's job to keep this from happening

The paddle is an AI agent that is trying to learn how to play the game successfully. The game keep starting over if it is lost and the game count is updated. 

I have included a button that you may press at any time that lets you speed up the learning process by turning off the display of the game. The game is still being run in the background, while the agent continues to learn how to play better. The button may be pressed again at any point to toggle the display back on. When you do this, you will be shown the current game that is being played. 

Here's a run while it's still learning:
![](Pong-AI/demo1.gif)
