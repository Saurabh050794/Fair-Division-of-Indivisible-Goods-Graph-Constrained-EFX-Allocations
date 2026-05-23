import random


# Utility: valuation function
def value(v, bundle):
    return sum(v[g] for g in bundle)

# EFX check

def EFX(X_i, X_j, v_i):
    v_i_Xi = value(v_i, X_i)
    v_i_Xj = value(v_i, X_j)

    if v_i_Xi >= v_i_Xj:
        return True

    if not X_j:
        return True

    for g in X_j:
        if v_i_Xi >= v_i_Xj - v_i[g]:
            return True

    return False


def strongly_envies(X_i, X_j, v_i):
    return not EFX(X_i, X_j, v_i)

def strong_envy_pair(X_i, X_j, v_i, v_j):
    return (not EFX(X_i, X_j, v_i)) or (not EFX(X_j, X_i, v_j))



# LocalEFX

def local_efx(x_i, x_j, vi, vj):
    M_prime = sorted(x_i + x_j, key=lambda g: vi[g], reverse=True)
    Y1, Y2 = [], []

    for g in M_prime:
        if sum(vi[x] for x in Y1) <= sum(vi[x] for x in Y2):
            Y1.append(g)
        else:
            Y2.append(g)

    if sum(vj[x] for x in Y1) >= sum(vj[x] for x in Y2):
        return Y2, Y1
    else:
        return Y1, Y2



# DFS traversal (tree)

def dfs_orders(graph, root):

    pre_order = []      # Store forward edges in DFS pre order
    post_order = []     # Store backward edges in DFS post oredr

    # Inner recursive DFS function
    def dfs(i, parent):
        # Traverse all neighbors of node i
        for j in graph[i]:
            # Skip parent to avoid going backward
            if j != parent:
                # Pre-order: before visiting child
                pre_order.append((i, j))

                # Recursive DFS on child j
                dfs(j, i)

                # Post-order: after returning from child
                post_order.append((j, i))

    # Start DFS from root
    dfs(root, None)

    # Return both orders
    return pre_order, post_order


# Check if any strong envy exists

def exists_strong_envy(graph, X, valuations):
    for i in graph:
        for j in graph[i]:
            if strongly_envies(X[i], X[j], valuations[i]):
                return True
    return False



# Print all agents' current bundles

def print_all_bundles(X, valuations, agents):
    for k in agents:
        bundle = set(X[k])
        val = value(valuations[k], X[k])
        bundle_str = str(bundle).replace("set()", "{ }")
        print(f"    Agent {k + 1}: {bundle_str}  (value= {val})")


# Main Algorithm

def tree_efx_allocation(graph, root, items, valuations):
    agents = list(graph.keys())

    # Step 1: Initialization — root gets all goods
    X = {i: [] for i in agents}
    X[root] = list(items)

    iteration = 0

    #  Loop until no strong envy
    while exists_strong_envy(graph, X, valuations):
        iteration += 1
        print(f"\n{'=' * 50}")
        print(f"ITERATION {iteration}")
        print("=" * 50)

        X_init = {i: sorted(X[i]) for i in X}

        # ── Forward pass 
        print("\n--- Forward Pass (root → leaves) ---")
        for parent, child in pre_order:
            X[parent], X[child] = local_efx(X[parent], X[child],valuations[parent], valuations[child])
            print(f"\n  local_efx(Agent {parent + 1}, Agent {child + 1}):")
            print_all_bundles(X, valuations, agents)

        # ── Backward pass 
        print("\n--- Backward Pass (leaves → root) ---")
        for child, parent in post_order:
            X[child], X[parent] = local_efx(X[child], X[parent],valuations[child], valuations[parent])
            print(f"\n  local_efx(Agent {child + 1}, Agent {parent + 1}):")
            print_all_bundles(X, valuations, agents)

        # ── Envy Check ──
        print("\n--- Envy Check ---")
        strong_envy_exists = False

        for i in graph:
            for j in graph[i]:
                if j <= i:          # check each edge once
                    continue
                vi, vj = valuations[i], valuations[j]
                se = strong_envy_pair(X[i], X[j], vi, vj)

                val_i_own  = value(vi, X[i])
                val_i_sees = value(vi, X[j])
                val_j_own  = value(vj, X[j])
                val_j_sees = value(vj, X[i])

                min_g_for_i = min(X[j], key=lambda g: vi[g]) if X[j] else None
                min_g_for_j = min(X[i], key=lambda g: vj[g]) if X[i] else None

                efx_i = EFX(X[i], X[j], vi)
                efx_j = EFX(X[j], X[i], vj)

                label = "(STRONG ENVY)" if se else "(No strong envy)"
                print(f"\n  Agents {i + 1} & {j + 1}: {label}")

                opp_min_i = (
                    f",  opponent least-valued good ({min_g_for_i}): {vi[min_g_for_i]}"
                    if min_g_for_i else ""
                )
                print(f"    Agent {i + 1} view  →  own: {val_i_own},  opponent: {val_i_sees}{opp_min_i}")
                print(f"      EFX {'   ' if efx_i else 'NOT'} satisfied for Agent {i + 1}.")

                opp_min_j = (
                    f",  opponent least-valued good ({min_g_for_j}): {vj[min_g_for_j]}"
                    if min_g_for_j else ""
                )
                print(f"    Agent {j + 1} view  →  own: {val_j_own},  opponent: {val_j_sees}{opp_min_j}")
                print(f"      EFX {'   ' if efx_j else 'NOT'} satisfied for Agent {j + 1}.")

                if se:
                    strong_envy_exists = True

        # Stopping condition: no change but envy persists → failure
        if {i: sorted(X[i]) for i in X} == X_init and strong_envy_exists:
            print("\nFailure: Strong envy remains and allocation is stuck.")
            return "Failure"
        if not strong_envy_exists:
            print("\nSuccess: Strong envy eliminated.")
            return X
    


# ----Generate random tree

import random

def generate_random_tree(n):    # It creates a random tree by connecting each new node to one previous node
    graph = {}

    # Empty adjacency list
    for i in range(n):
        graph[i] = []

    # Connect each node to one previous node
    for i in range(1, n):
        parent = random.choice(range(i))   # random previous node
        graph[i].append(parent)
        graph[parent].append(i)
    return graph


# Main

n_agents = int(input("Number of agents (n): "))
m_items  = int(input("Number of goods (m): "))

agents = list(range(n_agents))   # creates a list of all agent

# Goods as set {}
goods = {f'g{i+1}' for i in range(m_items)}       # Create a set of goods named g1, g2, g3, ..., gm

# Valuations
valuations = {
    i: {g: random.randint(1, 10) for g in goods}   # Assign random value (1 to 10) for each good to agent i
    for i in agents
}

# Tree
graph = generate_random_tree(n_agents)
root = 0


# Print Input

print("=" * 50)
print("INPUT")
print("=" * 50)

print("\nTree (adjacency list):")
for node in graph:
    print(f"Agent {node+1}: { [n+1 for n in graph[node]] }")  

print("\nGoods:")
print(sorted({f'g{i+1}' for i in range(m_items)}, key=lambda g: int(g[1:])))

print("\nValuations:")
for i in valuations:
    sorted_val = {g: valuations[i][g] for g in sorted(valuations[i], key=lambda g: int(g[1:]))}
    print(f"Agent {i+1}: {sorted_val}")


# -----DFS order
pre_order, post_order = dfs_orders(graph, root)


pre_order_ = [(p + 1, c + 1) for (p, c) in pre_order]
post_order_ = [(c + 1, p + 1) for (c, p) in post_order]
print("\npre_order =", pre_order_)
print("\npost_order =", post_order_)


# ---------------------------
# Allocation Result
# ---------------------------
result = tree_efx_allocation(graph, root, goods, valuations)


if result:
    print("\n" + "=" * 50)
    print("FINAL ALLOCATION")
    print("=" * 50)
    for i in sorted(result.keys()):
        bundle = result[i]
        print(f"\nAgent {i+1} gets: {str(set(bundle)).replace('set()', '{ }')}")
        print(f"Value: {sum(valuations[i][g] for g in bundle)}")











        