import math
publickey_bytes = 64
publickey_combinations = math.factorial(publickey_bytes)
for num_shard in range(1, 500):
    if (publickey_combinations % num_shard == 0):
        print("{}, {}".format(num_shard, publickey_combinations/num_shard))
