from config.config import Settings

class Core:

  def __init__(self, config: Settings):
    self.config= config
    self.service_name = self.config.service_name
    self.anthropic_key = self.config.anthropic_key
    self.app_name = self.config.app_name
   