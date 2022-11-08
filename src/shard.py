from crypto import hash_sha256_hex, deterministic_fisher_yates
from Levenshtein import distance
import math

class Shard():
    def __init__(self, shard_index, shard_range_start, shard_range_end, shard_state=None, top_block_chunk_hash=None):
        self.shard_index = shard_index
        self.shard_range_start = shard_range_start
        self.shard_range_end = shard_range_end
        self.shard_state = shard_state
        self.top_block_chunk_hash = top_block_chunk_hash

        
class Committee():
    def __init__(self, committee_index, members, epoch, assigned_shard=None, allocated_round_leader=None, round=0):
        self.index = committee_index
        self.members = members
        self.assigned_shard = assigned_shard
        self.allocated_round_leader = allocated_round_leader
        self.round = round
        self.epoch = epoch
        
    def elect_round_leader(self, last_blockchunk_hash):
        target_hash = hash_sha256_hex(last_blockchunk_hash + str(self.round)) 
        # Find the commitee member with a publickey closest to the target hash
        lowest_d = 999999999
        elected = None
        for member in self.members:
            d = distance(member, target_hash)
            if (d < lowest_d):
                lowest_d = d
                elected = member
        return elected

def form_committee_list(number_committees, participating_fullnode_count, active_fullnode_list, epoch_number, epoch_salt):
    # Forms the list of commitees, and assigns each an equal number of members (participating_fullnode_count/ number_commitees)
    if (len(active_fullnode_list) < participating_fullnode_count):
        return False

    if (number_committees % participating_fullnode_count != 0): # we cannot split participating_fullnode_count into number_commitees commitees
        return False
    
    # Fisher yates shuffle the active_fullnode_list
    shuffled_afn_list = deterministic_fisher_yates(active_fullnode_list, epoch_salt)[:participating_fullnode_count]
    members_per_committee = participating_fullnode_count / number_committees
    committees = [Committee(0, [], epoch_number)]
    for i in range(1, number_committees + 1):
        committees.append(Committee(i, shuffled_afn_list[(i-1)*members_per_committee:(i)*members_per_committee], epoch_number))
    zero_commitee_members = deterministic_fisher_yates(shuffled_afn_list, epoch_salt)[:members_per_committee]
    committees[0].members = zero_commitee_members
    # Now form the consensus/zero committee
    return committees

def calculate_shards(number_shards, publickey_length_bytes=64):
    number_publickeys = math.factorial(publickey_length_bytes)
    if (number_publickeys % number_shards != 0):
        return False # Number of shards does not fit into number publickeys without a remainder
    
    keys_per_shard = number_publickeys / number_shards
    shards = []
    
    for shard_index in range(number_shards):
        shards.append(Shard(shard_index, shard_index * keys_per_shard, (shard_index + 1) * keys_per_shard))
        
    return shards
    

    

    