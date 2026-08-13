import pandas as pd
import numpy as np
from faker import Faker

fake = Faker()

print("PayGuard AI environment is working!")
print("Test customer:", fake.name())
print("Test amount:", np.random.uniform(10, 500))