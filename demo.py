import numpy as np

# Membership functions
def trimf(x, abc):
    a, b, c = abc
    return np.maximum(np.minimum((x - a) / (b - a + 1e-6), (c - x) / (c - b + 1e-6)), 0)

# Input ranges
x_pm25 = np.arange(0, 201, 1)
x_pm10 = np.arange(0, 251, 1)
x_no2  = np.arange(0, 201, 1)
x_co   = np.arange(0, 11, 0.1)
x_aq   = np.arange(0, 101, 1)

# Memberships for inputs
pm25_low = trimf(x_pm25, [0, 0, 50])
pm25_mod = trimf(x_pm25, [30, 75, 120])
pm25_high = trimf(x_pm25, [100, 150, 200])

pm10_low = trimf(x_pm10, [0, 0, 60])
pm10_mod = trimf(x_pm10, [40, 100, 160])
pm10_high = trimf(x_pm10, [140, 200, 250])

no2_low = trimf(x_no2, [0, 0, 50])
no2_mod = trimf(x_no2, [30, 100, 150])
no2_high = trimf(x_no2, [120, 170, 200])

co_low = trimf(x_co, [0, 0, 2])
co_mod = trimf(x_co, [1, 3.5, 6])
co_high = trimf(x_co, [5, 8, 10])

aq_poor = trimf(x_aq, [0, 0, 40])
aq_mod = trimf(x_aq, [30, 50, 70])
aq_good = trimf(x_aq, [60, 100, 100])

# Helper functions
def fuzzify(val, x, mf):
    return np.interp(val, x, mf)

def defuzz(x, mf):
    return np.sum(x * mf) / np.sum(mf) if np.sum(mf) != 0 else 0

# Core fuzzy logic function
def compute_air_quality(pm25_val, pm10_val, no2_val, co_val):
    μ_pm25_low = fuzzify(pm25_val, x_pm25, pm25_low)
    μ_pm25_mod = fuzzify(pm25_val, x_pm25, pm25_mod)
    μ_pm25_high = fuzzify(pm25_val, x_pm25, pm25_high)

    μ_pm10_low = fuzzify(pm10_val, x_pm10, pm10_low)
    μ_pm10_mod = fuzzify(pm10_val, x_pm10, pm10_mod)
    μ_pm10_high = fuzzify(pm10_val, x_pm10, pm10_high)

    μ_no2_low = fuzzify(no2_val, x_no2, no2_low)
    μ_no2_mod = fuzzify(no2_val, x_no2, no2_mod)
    μ_no2_high = fuzzify(no2_val, x_no2, no2_high)

    μ_co_low = fuzzify(co_val, x_co, co_low)
    μ_co_mod = fuzzify(co_val, x_co, co_mod)
    μ_co_high = fuzzify(co_val, x_co, co_high)

    rule1_strength = np.fmax.reduce([μ_pm25_high, μ_pm10_high, μ_no2_high, μ_co_high])
    aq_rule1 = np.fmin(rule1_strength, aq_poor)

    rule2_strength = np.fmax.reduce([μ_pm25_mod, μ_pm10_mod, μ_no2_mod, μ_co_mod])
    aq_rule2 = np.fmin(rule2_strength, aq_mod)

    rule3_strength = np.fmin.reduce([μ_pm25_low, μ_pm10_low, μ_no2_low, μ_co_low])
    aq_rule3 = np.fmin(rule3_strength, aq_good)

    aggregated = np.fmax(np.fmax(aq_rule1, aq_rule2), aq_rule3)

    score = defuzz(x_aq, aggregated)

    if score <= 40:
        status = "Poor 😷"
    elif score <= 70:
        status = "Moderate 😐"
    else:
        status = "Good 😊"

    return score, status
