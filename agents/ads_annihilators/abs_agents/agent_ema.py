from agents.ads_annihilators.abs_agents.alpha_agent import AlphaAgent


class EMAAgent(AlphaAgent):
    def __init__(self, *args, initial_ema=1.0, ema_weight=0.8, **kwargs):
        super().__init__(*args, **kwargs)
        self.op_alpha_emas = [initial_ema for _ in range(self.n_items)]
        self.ema_weight = ema_weight
        self.pred_op_alphas = self.last_op_alphas

    # Predicts the opponent alpha and sets it
    def predict(self):
        self.pred_op_alphas = self.last_op_alphas

    def calculate_ema(self):
        self.op_alpha_emas = [self.ema_weight * self.op_alpha_emas[i] +
                              (1 - self.ema_weight) * self.pred_op_alphas[i] for i in range(self.n_items)]

    def update_decision(self):
        super().update_decision()
        self.predict()
        self.calculate_ema()
