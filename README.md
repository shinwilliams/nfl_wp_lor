Win probability added (WPA) is commonly used in American football analytics to quantify the value generated to a team by an individual play. However, taking arithmetic means of probabilities in incorrect and produces attenuation (shrinkage towards the center) because probabilities are bounded between 0 and 1. Plays which have pre/post win probabilities in the middle of the range are overweighted when arithmetically averaged compared to those near the boundary.

To see this, recall that the logistic regression which nflfastr's win probability calculations predicts log-odds as a linear combination of game state variables, then uses the logistic link function to convert to probabilities. Suppose we have a play which moves the ball from the offense's 25 yardline to the 30 yardline. Before the play, there is some vector describing all the game state variables g1, and a vector of the model's weights w. This produces some change in the game state, modifying it to g2 (this would include the change in down, distance, yardline, game clock, etc.). The win probability before the play was 1/(1+e^(-g1 w)), and after the play is 1/(1+e^(-g2 w)), so WPA = 1/(1+e^(-g2 w)) - 1/(1+e^(-g1 w)). But suppose we ran the exact same play, in the exact same game situation except that the score were different. Now, if we call the new pre-play game state g3, the game state following the play will be g3 + (g2 - g1), because the play modified every game state variable by the exact same amount as before. So the new pre and post-play win probabilities will be 1/(1+e^(-g3 w)) and 1/(1+(-(g3 + (g2 - g1)) w), and WPA = 1/(1+(-(g3 + (g2 - g1)) w) - 1/(1+e^(-g3 w)). Clearly, despite that the play produced the exact same change to the game state, the WPA will be different. For example, if g1 represents a tied game (so pre-play WP is close to 0.5) but g2 represents a blowout (so pre-play WP is close to 0 or 1), the slope of the link function is much steeper at g1 than it is at g3, so WPA will be much greater for the exact same play with the exact same results when it happens at g1 and not at g3. Hence, when we take the arithmetic mean of WPA, even though we do not explicitly weight plays differently, the outcomes of plays which occured when win probability was closer to 0.5 will be implicitly overweighted in the average due to the nonlinearity of the link function.

This statistical artifact occurs for any nonlinear or even nonparametric model, whether we are comparing the same model with itself or with another model, and whether those models compare cross-sectionally or temporally, so long as we are taking additive differences of their predictions. The only model which does not suffer this issue is an Linear Probability Model, whose predictions are not bounded between 0 and 1. This likely means that EPA models using multinomial logit probabilities times the vector of drive outcome point values have the same bias baked in, though the bias would be centered around the play-level mean of expected points instead of 0.5 (?).

An improved method is to take the average of log-odds ratios (or equivalently, the geomean of odds ratios). Continuing with our example, suppose we compare the pre and post-play log-odds of running the play at g1 vs. at g3. In the first situation, pre-play log-odds are g1 w, and post-play log-odds are g2 w, so the difference is (g2 - g1) w. In the second situation, pre-play log odds are g3 w, and post-play log-odds are g3 + (g2 - g1) w, which also gives a difference (g3 + (g2 - g1) - g3) w = (g2 - g1) w.

The immediate question this raises is whether the value of certain plays is systematically mismeasured by WPA due to selection bias in the game state in which they occur. Conventional football analytics wisdom says that passing is more effective than rushing, for instance. The code in this repo tests this hypothesis against 1999-2025 play-by-play data to show the average WPA and average log-odds differences of rushing and passing plays. These are the results:

Pass Average WPA: 0.00036209134912752744

Rush Average WPA: -0.0009047917288908253

Pass Average WPLOR: -0.013055507689992488

Rush Average WPLOR: 0.0031114618374578147

|Year	|Passes	|Rushes	|Pass WPA	|Rush WPA	|Pass WPLOR	|Rush WPLOR	|WPA Diff	|LOR Diff|
|-----|-------|-------|---------|---------|-----------|-----------|---------|--------|
|	1999	|	18417	|	13603	|	-0.001905	|	-0.003574	|	-0.024777	|	-0.017506	|	0.001669	|	-0.007271	|
|	2000	|	17926	|	13813	|	-0.001606	|	-0.002118	|	-0.025049	|	-0.004317	|	0.000512	|	-0.020732	|
|	2001	|	18157	|	14080	|	-0.001179	|	-0.002369	|	-0.023391	|	-0.006891	|	0.00119	|	-0.0165	|
|	2002	|	19330	|	14408	|	-0.000589	|	-0.001159	|	-0.017528	|	0.000947	|	0.00057	|	-0.018475	|
|	2003	|	18295	|	14798	|	-0.00084	|	-0.001122	|	-0.02546	|	0.001795	|	0.000282	|	-0.027255	|
|	2004	|	18246	|	14646	|	-0.000267	|	-0.001391	|	-0.019307	|	0.002205	|	0.001124	|	-0.021512	|
|	2005	|	18299	|	14591	|	-0.000756	|	-0.001739	|	-0.023253	|	0.001759	|	0.000983	|	-0.025012	|
|	2006	|	18236	|	14669	|	-0.000429	|	-0.001123	|	-0.020614	|	0.002187	|	0.000694	|	-0.022801	|
|	2007	|	18798	|	14192	|	-0.000131	|	-0.001784	|	-0.014668	|	-0.002492	|	0.001653	|	-0.012176	|
|	2008	|	18265	|	14287	|	0.000599	|	-0.000781	|	-0.014284	|	0.005054	|	0.00138	|	-0.019338	|
|	2009	|	18816	|	14275	|	0.000709	|	-0.000929	|	-0.011066	|	0.000962	|	0.001638	|	-0.012028	|
|	2010	|	19099	|	14118	|	0.000213	|	-0.001524	|	-0.013299	|	0.001111	|	0.001737	|	-0.01441	|
|	2011	|	19382	|	14179	|	0.000512	|	-0.001096	|	-0.014419	|	0.00371	|	0.001608	|	-0.018129	|
|	2012	|	19686	|	14180	|	0.000655	|	-0.000757	|	-0.008587	|	0.003	|	0.001412	|	-0.011587	|
|	2013	|	20135	|	14077	|	0.000421	|	-0.00079	|	-0.011805	|	0.000695	|	0.001211	|	-0.0125	|
|	2014	|	19835	|	13834	|	0.001097	|	-0.000888	|	-0.00919	|	0.001308	|	0.001985	|	-0.010498	|
|	2015	|	20325	|	13616	|	0.000719	|	-0.00139	|	-0.007608	|	0.002144	|	0.002109	|	-0.009752	|
|	2016	|	20240	|	13461	|	0.001418	|	-0.000969	|	-0.005338	|	0.000526	|	0.002387	|	-0.005864	|
|	2017	|	19534	|	13891	|	0.000321	|	-0.001209	|	-0.012686	|	0.002727	|	0.00153	|	-0.015413	|
|	2018	|	19770	|	13447	|	0.001745	|	-0.000005	|	-0.002873	|	0.011185	|	0.00175	|	-0.014058	|
|	2019	|	19855	|	13587	|	0.001362	|	-0.00049	|	-0.008486	|	0.005874	|	0.001852	|	-0.01436	|
|	2020	|	20139	|	14030	|	0.001978	|	0.000767	|	-0.000411	|	0.013099	|	0.001211	|	-0.01351	|
|	2021	|	20955	|	14718	|	0.001713	|	0.000536	|	-0.004428	|	0.011828	|	0.001177	|	-0.016256	|
|	2022	|	20338	|	15009	|	0.000635	|	0.000764	|	-0.011529	|	0.013222	|	-0.000129	|	-0.024751	|
|	2023	|	20671	|	14840	|	0.000446	|	-0.000204	|	-0.013885	|	0.006702	|	0.00065	|	-0.020587	|
|	2024	|	19953	|	15012	|	0.001147	|	0.000723	|	-0.004917	|	0.013256	|	0.000424	|	-0.018173	|
|	2025	|	8446	|	6122	|	0.001521	|	0.0009	|	-0.007237	|	0.013788	|	0.000621	|	-0.021025	|


According to WPA, passing generates 0.05 % more win probability per play than rushing, but when we instead look at log-odds ratio differences, run plays give an average of 0.0162 more log-odds, which if evaluated from a 50% win probability baseline is about a 0.405% advantage in win probability. Of course, evaluated from a different baseline, the way this translates to win probabilities will be different, but even at a 95% baseline give a 0.07% increase to win probability. The point is not to compare this number with the WPA number, both because they are not inherently comparable but because WPA is a flawed measure, which log-odds measurement can improve upon without any changes to the underlying model. Instead, we should look specifically at what the log-odds interpretation says, independent of WPA, to determine the value of plays.

Obviously, this is far from a conclusive refutation of passing's superiority. A more in-depth analysis which used log-odds comparisons while also controlling for context would give a better picture than this one, for it is precisely the context-dependence which gives rise to the attenuation bias inherent to WPA. Chief among contextual factors is the selection bias that occurs due to coaches running the ball to bleed the clock. Counterfactual analysis would need to accurately assess the changes in odds ratios if offenses were to attempt to pass while also letting the clock run down. Likely there are many other situational factors that would need to be evaluated, and recommendations to change strategy to run/pass more should be tailored to those specific situations where the numbers indicate would be most effective, not simply a global mandate to run/pass more in the aggregate.

This is only a preliminary analysis. But it is suggestive that with such a small change, not only does the sign of the difference but the order of magnitude changes to such an extent that rushing suddenly looks much more effective than passing in terms of win/loss outcomes.
