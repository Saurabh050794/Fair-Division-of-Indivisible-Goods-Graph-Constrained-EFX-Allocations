def local_efx(x_i, x_j, vi, vj):
    
    #  All goods in M' and sort by vi descending
    M_prime = sorted(x_i + x_j, key=lambda g: vi[g], reverse=True)
    Y1, Y2 = [], []

    # Greedy split — always add to the bundle with smaller vi-value
    for g in M_prime:
        if sum(vi[x] for x in Y1) <= sum(vi[x] for x in Y2):
            Y1.append(g)
        else:
            Y2.append(g)

    # Give the higher-vj bundle to agent j (i+1); agent i gets the other
    if sum(vj[x] for x in Y1) >= sum(vj[x] for x in Y2):
        return Y2, Y1   # Xi=Y2, X_{i+1}=Y1
    else:
        return Y1, Y2   # Xi=Y1, X_{i+1}=Y2



def EFX(X_i, X_j, v_i):
    v_i_Xi = sum(v_i[g] for g in X_i)
    v_i_Xj = sum(v_i[g] for g in X_j)

    # No envy at all → EFX trivially satisfied
    if v_i_Xi >= v_i_Xj:
        return True

    
    if not X_j:
        return True

    # Check if removing any single good from X_j eliminates envy
    for g in X_j:
        if v_i_Xi >= v_i_Xj - v_i[g]:
            return True
    return False  # Envy does not disappear after removing any single good


def strong_envy(X_i, X_j, v_i, v_j):
    return ( not EFX(X_i, X_j, v_i) or not EFX(X_j, X_i, v_j))


def sweeping_algorithm(v, goods):
    n = len(v)  # number of agents

    # Initial allocation
    X = [[] for _ in range(n)]
    X[0] = goods[:]  # initially, all goods to agent 1

    iteration = 0
    while True:
        iteration += 1
        print(f"\nIteration- {iteration}")
    

        # Use sorted bundles so comparison is order-independent
        X_prev = [sorted(bundle) for bundle in X]

        # Forward sweep
        print("\n--- Forward Sweep ---")
        for i in range(n - 1):
            X[i], X[i + 1] = local_efx(X[i], X[i + 1], v[i], v[i + 1])
            print(f"\n local_efx--(Agent {i+1}, Agent {i+2}):")
            for k in range(n):
                val = sum(v[k][g] for g in X[k])
                print(f"    Agent {k+1}: {str(set(X[k])).replace('set()', '{ }')}  (value= {val})")

        # Backward sweep
        print("\n--- Backward Sweep ---")
        for i in range(n - 2, -1, -1):
            X[i], X[i + 1] = local_efx(X[i], X[i + 1], v[i], v[i + 1])
            print(f"\n local_efx--(Agent {i+1}, Agent {i+2}):")
            for k in range(n):
                val = sum(v[k][g] for g in X[k])
                print(f"    Agent {k+1}: {str(set(X[k])).replace('set()', '{  }')}  (value= {val})")

        # Check whether any adjacent pair still has strong envy
        print("\n--- Envy Check ---")
        strong_envy_exists = False
        for i in range(n - 1):
            se = strong_envy(X[i], X[i + 1], v[i], v[i + 1])

            vi, vj = v[i], v[i + 1]
            val_i_own  = sum(vi[g] for g in X[i])
            val_i_sees = sum(vi[g] for g in X[i + 1])
            val_j_own  = sum(vj[g] for g in X[i + 1])
            val_j_sees = sum(vj[g] for g in X[i])

            # Least-valued good in opponent's bundle (worst-case removal for EFX)
            min_g_for_i = min(X[i + 1], key=lambda g: vi[g]) if X[i + 1] else None
            min_g_for_j = min(X[i],     key=lambda g: vj[g]) if X[i]     else None

            efx_i = EFX(X[i], X[i + 1], vi)
            efx_j = EFX(X[i + 1], X[i], vj)

            print(f"\n  Agents {i+1} & {i+2}: {'(STRONG ENVY)' if se else '(No strong envy)'}")

            # Agent i's perspective
            opp_minus_i = f",  opponent least-valued good ({min_g_for_i}): {vi[min_g_for_i]}" if min_g_for_i else ""
            print(f"    Agent {i+1} view  →  own: {val_i_own},  opponent: {val_i_sees}{opp_minus_i}")
            print(f"      EFX {' ' if efx_i else 'NOT'} satisfied for Agent {i+1}.")

            # Agent j's perspective
            opp_minus_j = f",  opponent least-valued good ({min_g_for_j}): {vj[min_g_for_j]}" if min_g_for_j else ""
            print(f"    Agent {i+2} view  →  own: {val_j_own},  opponent: {val_j_sees}{opp_minus_j}")
            print(f"      EFX {' ' if efx_j else 'NOT'} satisfied for Agent {i+2}.")

            if se:
                strong_envy_exists = True

        # Stopping conditions
        if X_prev == [sorted(b) for b in X] and strong_envy_exists:
            print("\nFailure: Strong envy remains.")
            return None

        if not strong_envy_exists:
            print("\nSuccess: Strong envy eliminated.")
            return X


# Example

  

import random

n = int(input('Number of agents (n): '))
m = int(input('Number of goods  (m): '))

goods_list = [f'g{i+1}' for i in range(m)]
agents_list =[f'Agent-{i+1}' for i in range(n)]
valuations = [
    {g: random.randint(1, 10) for g in goods_list}
    for _ in range(n)
]
print(f"\nGoods : {{{', '.join(goods_list)}}}")
print(f"\nAgents: {set(agents_list)}")
print('\nValuations:')
for i, v in enumerate(valuations):
    print(f'  Agent {i+1}:  {v}')
   
allocation = sweeping_algorithm(valuations, goods_list)

if allocation:
    print("\n"+"="*40)
    print("FINAL ALLOCATION ")
    print("="*40)
    for i, bundle in enumerate(allocation):
        print(f"\nAgent {i+1} gets: {str(set(bundle)).replace('set()', '{ }')}")
        print(f"  Value: {sum(valuations[i][g] for g in bundle)}")
    
    