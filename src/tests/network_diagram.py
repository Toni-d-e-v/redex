# This test generates a list of  fullnodes. It then forms the commitee list, and the shard list, assigns each commitee a shard and then renders a series of diagrams

number_of_fullnodes            = 30
number_of_shards               = 5
number_of_members_in_committee = number_of_fullnodes / number_of_shards

from ecdsa import SigningKey, VerifyingKey

network_fullnodes = []
for i in range(number_of_fullnodes):
    sk = SigningKey.generate() # uses NIST192p
    vk = sk.verifying_key
    network_fullnodes.append(vk.to_string("uncompressed").hex())
    