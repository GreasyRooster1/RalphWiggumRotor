import os

from DeepSeekCoderV2 import DeepSeekCoderV2

model = DeepSeekCoderV2()
model.init_model()

model.send_model_request("what is the purpose of ralph wiggums in the context of AI?")
