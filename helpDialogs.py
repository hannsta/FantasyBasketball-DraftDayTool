def IndGamesExp():
	title="Individual Games Graph"
	explainText='''<p style="font-size:12px">This graph displays every game a specific player has played, with individual games represented
	as single point "score" assigned based on the stats they accumulated that game.
These score are calculated using the same formula as the player ranking scores (see player ranking help),
based on a dataset that includes every player's games over the last 5 years.<br>
<br>
<b>What is the y-axis?</b>
<p style="font-size:12px">The y-axis is the score each game recieved, with the minimum of -10 and maximum of 25. Since 
these values are mostly arbitrary, the axis instead displays percentiles. 1% of the 150,000 
individual stat lines recieved a score greater than 11.5, 5% received a score greater than 7.6,
and so on. Since these are based on the sum of z-scores, the average score is 0. The median(50%) 
however is slihgtly lower at -0.67.<br>
<br>
<b>What is 0 and how can anything be below it?</b>
<p style="font-size:12px">Zero represents the score of a player's game where every single stat category is 0. If a player's only stat 
is a miss or turnover, the overall effect will be negative.<br>
<br>
<b>What is the line?</b>
<p style="font-size:12px">The line represents the trend of a player's performance throughout the 2015 season. It is based on 
a 2nd order polynomial fit and is not intended to be used for predictive purposes.
'''
	return explainText, title
	
def gameSliders():
	title="Ranking Adjustments"
	explainText='''
<p style="font-size:12px">The initial values displayed in the main table are the z-scores for each value calculated over the 
span of the entire 2015 season. These values are added together (with turnovers subtracted) to
provide a total score in the first "Tot" column. <br><br>

<b>Category Sliders</b><br>
Since most fantasy teams have at least one weakness it is not always beneficial to see the 
total from every category added together. If you consistently lose turnovers, the amount of
turnovers a player gets is irrelevant to their value to your team. By removing this value you
can get a better picture of what players fit your team specifically.<br>
<br>
These sliders apply a multiplier to each category between 1 and 0, then display the adjusted
total in the "Adj Tot" column. A slider at 0 will completely remove the category from the equation,
while a slider at 1 means that the category retain its true value.
<br><br>
<b>Timeline Slider</b><br>
This slider adjusts how many games are used in the average and deviation calculations. When the slder is completely
to the left, all 82 games are used to calculate averages for each player. When it is completely to the right,
the last 1 game is used. 
<br><br>This can be used to observe the effects of lineup changes, trades, and player improvement
that can dramitcally change a players output throughout the drsdon. For a comple trend analysis, double click on the
player's name.
better predict next year's results.'''
	return explainText, title

	
def teamGraph():
	title="Team Averages Graph"
	explainText='''This graph represents the average z-score of your selected team'same players
in each stat category.<Br><Br>

<b>Green Bars</b><br>
Green bars represent your team. 
<br><br>
<b>Red Bars</b><br>
Red bars represent the average of all players picked that are not on your team.
 '''
	return explainText, title
