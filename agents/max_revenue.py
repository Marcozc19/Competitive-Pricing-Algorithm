class Agent(object):
    def __init__(self, agent_number, params={}):
        self.this_agent_number = agent_number  # index for this agent
        self.n_items = params["n_items"]
        self.alpha = 1.0
        self.cust_value_0 = 1.0
        self.cust_value_1 = 1.0
        self.project_part = params['project_part'] #useful to be able to use same competition code for each project part
    
    def _process_last_sale(self, new_buyer_covariates, last_sale):
        did_customer_buy_from_me = last_sale[1] == self.this_agent_number
        covs = new_buyer_covariates
        if did_customer_buy_from_me:  # can increase prices
            self.alpha *= 1.1
        else:  # should decrease prices
            self.alpha *= 0.9
        (self.cust_value_0, self.cust_value_1), revenue = optimizer.get_revenue_maximizing_prices_and_revenue_from_cov(covs)
    
    # Given an observation which is #info for new buyer, information for last iteration, and current profit from each time
    # Covariates of the current buyer
    # Data from last iteration (which item customer purchased, who purchased from, prices for each agent for each item (2x2, where rows are agents and columns are items)))
    # Returns an action: a list of length n_items=2, indicating price this agent is posting for each item.

    def action(self, obs):
        new_buyer_covariates, last_sale, state = obs
        self._process_last_sale(new_buyer_covariates, last_sale)

        if self.project_part == 1:
            return [new_buyer_covariates[0]*self.alpha]
        
        else:
            return [self.cust_value_0, self.cust_value_1]
