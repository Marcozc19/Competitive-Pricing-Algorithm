# Competitive-Pricing-Algorithm
This project is a combination of concepts ranging Game Theory, Machine Learning, and Data Science.

Game theory was initially employed to predict how opponents might react to our pricing decisions. This approach combined cooperation, exploitation, and forecasting opponent behavior. To ensure our pricing remained within optimal bounds, we incorporated safeguards into our predictions.

To compete effectively against different opponents, we introduced A/B testing. This allowed us to fine-tune and test specific hyperparameters of our agent during matches, optimizing performance against particular rivals. Additionally, we developed internal simulations that enabled us to conduct round-robin tournaments or head-to-head matches multiple times, which helped highlight overall performance and aggregate statistics.

To determine the best prices, we needed a method to estimate optimal pricing based on customer covariates. We trained an XGBoost model on historical data to estimate demand. Using these demand estimations, we navigated a price grid to find the price that would yield the highest revenue. This information was then fed into our agent, which adjusted prices according to the current competitive landscape.

Ultimately, this combination of strategic approaches led us to secure first place in the competition against 20 teams.
