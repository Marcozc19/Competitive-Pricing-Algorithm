# from statsmodels.stats.proportion import proportions_ztest, proportion_confint
import numpy as np
from scipy.stats import norm
from agents.ads_annihilators.abs_agents.base_agent import BaseAgent


def proportions_ztest(successes, nobs):
    proportions = successes / nobs
    pooled_prop = np.sum(successes) / np.sum(nobs)
    pooled_se = np.sqrt(pooled_prop * (1 - pooled_prop) * np.sum(1 / nobs))
    z_stat = (proportions[1] - proportions[0]) / pooled_se
    pval = 1 - norm.cdf(z_stat)
    return z_stat, pval


def proportion_confint(successes, nobs, alpha=0.05):
    proportions = successes / nobs
    z_score = norm.ppf(1 - alpha / 2)
    se = np.sqrt(proportions * (1 - proportions) / nobs)
    confint_lower = proportions - z_score * se
    confint_upper = proportions + z_score * se
    return (confint_lower[0], confint_lower[1]), (confint_upper[0], confint_upper[1])


class ABTestVariantAttrs:
    def __init__(self,
                 agent: BaseAgent,
                 attributes,
                 ab_length=1000,
                 switch_times=1,
                 ab_alpha=0.05):

        self.agent = agent
        self.ab_length = ab_length
        self.ab_alpha = ab_alpha
        self.round_number = 0
        self.switch_interval = ab_length // (switch_times * 2)

        # AB Test attribute
        self.test_attributes = attributes
        for attribute_name in attributes.keys():
            attributes[attribute_name] = getattr(agent, attribute_name)
        self.og_attributes = attributes
        self.og_profit = 0
        self.test_profit = 0

    def set_attributes(self, attributes):
        for attribute_name, attribute_val in attributes.items():
            setattr(self.agent, attribute_name, attribute_val)

    def check_significance(self):
        num_each = self.ab_length // 2
        nobs = np.array([num_each, num_each])
        success = np.array([self.og_profit, self.test_profit])
        z_stat, pval = proportions_ztest(success, nobs=nobs)
        (lower_con, lower_treat), (upper_con, upper_treat) = proportion_confint(success, nobs=nobs, alpha=0.05)
        if pval < self.ab_alpha and lower_treat > lower_con and upper_con > upper_treat:
            # Test group is not same and has higher interval for profits
            self.set_attributes(self.test_attributes)
        else:
            self.set_attributes(self.og_attributes)

    def action(self, obs):
        if self.round_number == self.ab_length:
            self.test_profit = self.agent.profit - self.og_profit
            self.check_significance()
        elif self.round_number % self.switch_interval*2 == 0:     # finished test segment
            self.test_profit = self.agent.profit - self.og_profit
            self.set_attributes(self.og_attributes)
        elif self.round_number % self.switch_interval == 0:     # finished og segment (control)
            self.og_profit = self.agent.profit - self.test_profit
            self.set_attributes(self.test_attributes)

        # Run agent based on stage
        self.round_number += 1
        return self.agent.action(obs)
